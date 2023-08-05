"""Base classes and function for REST, WMS, and WMF services."""
import socket
from collections import defaultdict
from dataclasses import dataclass
from itertools import product, zip_longest
from typing import Any, Dict, List, Mapping, MutableMapping, NamedTuple, Optional, Tuple, Union
from unittest.mock import _patch, patch
from warnings import warn

import pyproj
from orjson import JSONDecodeError
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from shapely.geometry import Polygon
from urllib3 import Retry

from . import utils
from .exceptions import InvalidInputType, InvalidInputValue, MissingInputs, ServerError, ZeroMatched
from .utils import MatchCRS

DEF_CRS = "epsg:4326"


class RetrySession:
    """Configures the passed-in session to retry on failed requests.

    The fails can be due to connection errors, specific HTTP response
    codes and 30X redirections. The code is based on:
    https://github.com/bustawin/retry-requests

    Parameters
    ----------
    retries : int, optional
        The number of maximum retries before raising an exception, defaults to 5.
    backoff_factor : float, optional
        A factor used to compute the waiting time between retries, defaults to 0.5.
    status_to_retry : tuple, optional
        A tuple of status codes that trigger the reply behaviour, defaults to (500, 502, 504).
    prefixes : tuple, optional
        The prefixes to consider, defaults to ("http://", "https://")
    """

    def __init__(
        self,
        retries: int = 3,
        backoff_factor: float = 0.3,
        status_to_retry: Tuple[int, ...] = (500, 502, 504),
        prefixes: Tuple[str, ...] = ("https://",),
    ) -> None:
        self.session = Session()
        self.retries = retries

        r = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_to_retry,
            method_whitelist=False,
        )
        adapter = HTTPAdapter(max_retries=r)
        for prefix in prefixes:
            self.session.mount(prefix, adapter)
        self.session.hooks = {"response": [lambda r, *args, **kwargs: r.raise_for_status()]}

    def get(self, url: str, payload: Optional[Mapping[str, Any]] = None,) -> Response:
        """Retrieve data from a url by GET and return the Response."""
        try:
            return self.session.get(url, params=payload)
        except (ConnectionError, RequestException):
            raise ConnectionError(f"Connection failed after {self.retries} retries.")

    def post(self, url: str, payload: Optional[MutableMapping[str, Any]] = None,) -> Response:
        """Retrieve data from a url by POST and return the Response."""
        try:
            return self.session.post(url, data=payload)
        except (ConnectionError, RequestException):
            raise ConnectionError(f"Connection failed after {self.retries} retries.")

    @staticmethod
    def onlyipv4() -> _patch:
        """Disable IPv6 and only use IPv4."""
        orig_getaddrinfo = socket.getaddrinfo

        def getaddrinfo_ipv4(host, port, family=socket.AF_INET, ptype=0, proto=0, flags=0):
            return orig_getaddrinfo(
                host=host, port=port, family=family, type=ptype, proto=proto, flags=flags,
            )

        return patch("socket.getaddrinfo", side_effect=getaddrinfo_ipv4)


class ArcGISRESTful:
    """Access to an ArcGIS REST service.

    Parameters
    ----------
    base_url : str, optional
        The ArcGIS RESTful service url.
    outformat : str, optional
        One of the output formats offered by the selected layer. If not correct
        a list of available formats is shown, defaults to ``geojson``.
    spatial_relation : str, optional
        The spatial relationship to be applied on the input geometry
        while performing the query. If not correct a list of available options is shown.
        It defaults to ``esriSpatialRelIntersects``.
    outfields : str or list
        The output fields to be requested. Setting ``*`` as outfields requests
        all the available fields which is the default behaviour.
    crs : str, optional
        The spatial reference of the output data, defaults to EPSG:4326
    n_threads : int, optional
        Number of simultaneous download, default to 4.
    """

    def __init__(
        self,
        base_url: str,
        outformat: str = "geojson",
        outfields: Union[List[str], str] = "*",
        spatial_relation: str = "esriSpatialRelIntersects",
        crs: str = DEF_CRS,
        n_threads: int = 4,
    ) -> None:

        self.session = RetrySession()
        self.base_url = base_url
        self.test_url()

        self._outformat = outformat
        self._spatial_relation = spatial_relation
        self._outfields = outfields if isinstance(outfields, list) else [outfields]
        self._n_threads = n_threads
        self.nfeatures = 0
        self.crs = crs
        self.out_sr = pyproj.CRS(self.crs).to_epsg()

    @property
    def outformat(self) -> str:
        return self._outformat

    @outformat.setter
    def outformat(self, value: str) -> None:
        if self.base_url is not None and value.lower() not in self.query_formats:
            raise InvalidInputValue("outformat", self.query_formats)

        self._outformat = value

    @property
    def spatial_relation(self) -> str:
        return self._spatial_relation

    @spatial_relation.setter
    def spatial_relation(self, value: str) -> None:
        valid_spatialrels = [
            "esriSpatialRelIntersects",
            "esriSpatialRelContains",
            "esriSpatialRelCrosses",
            "esriSpatialRelEnvelopeIntersects",
            "esriSpatialRelIndexIntersects",
            "esriSpatialRelOverlaps",
            "esriSpatialRelTouches",
            "esriSpatialRelWithin",
            "esriSpatialRelRelation",
        ]
        if value not in valid_spatialrels:
            raise InvalidInputValue("spatial_rel", valid_spatialrels)
        self._spatial_relation = value

    @property
    def outfields(self) -> List[str]:
        return self._outfields

    @outfields.setter
    def outfields(self, value: Union[List[str], str]) -> None:
        if not isinstance(value, (list, str)):
            raise InvalidInputType("outfields", "str or list")

        self._outfields = value if isinstance(value, list) else [value]

    def test_url(self) -> None:
        """Test the generated url and get the required parameters from the service."""
        try:
            resp = self.session.get(self.base_url, {"f": "json"}).json()
            try:
                self.units = resp["units"].replace("esri", "").lower()
            except KeyError:
                self.units = None
            self.maxrec_ount = resp["maxRecordCount"]
            self.query_formats = resp["supportedQueryFormats"].replace(" ", "").lower().split(",")
            self.valid_fields = list(
                set(
                    utils.traverse_json(resp, ["fields", "name"])
                    + utils.traverse_json(resp, ["fields", "alias"])
                    + ["*"]
                )
            )
        except KeyError:
            raise ServerError(self.base_url)

        self._max_nrecords = self.maxrec_ount

    @property
    def n_threads(self) -> int:
        return self._n_threads

    @n_threads.setter
    def n_threads(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise InvalidInputType("n_threads", "positive int")
        self._n_threads = value

    @property
    def max_nrecords(self) -> int:
        return self._max_nrecords

    @max_nrecords.setter
    def max_nrecords(self, value: int) -> None:
        if value > self.maxrec_ount:
            raise ValueError(
                f"The server doesn't accept more than {self.maxrec_ount}" + " records per request."
            )
        if value > 0:
            self._max_nrecords = value
        else:
            raise InvalidInputType("max_nrecords", "positive int")

    @property
    def featureids(self) -> List[Tuple[str, ...]]:
        return self._featureids

    @featureids.setter
    def featureids(self, value: Union[List[int], int]) -> None:
        if not isinstance(value, (list, int)):
            raise InvalidInputType("featureids", "int or list")

        oids = [str(value)] if isinstance(value, int) else [str(v) for v in value]

        self.nfeatures = len(oids)
        if self.nfeatures == 0:
            raise ZeroMatched("No feature ID were found within the requested region.")

        oid_list = list(zip_longest(*[iter(oids)] * self.max_nrecords))
        oid_list[-1] = tuple(i for i in oid_list[-1] if i is not None)
        self._featureids = oid_list

    def __repr__(self) -> str:
        """Print the service configuration."""
        return (
            "Service configurations:\n"
            + f"URL: {self.base_url}\n"
            + f"Max Record Count: {self.maxrec_ount}\n"
            + f"Supported Query Formats: {self.query_formats}\n"
            + f"Units: {self.units}"
        )

    def get_featureids(
        self, geom: Union[Polygon, Tuple[float, float, float, float]], geo_crs: str = DEF_CRS
    ) -> None:
        """Get feature IDs withing a geometry or bounding box.

        Parameters
        ----------
        geom : Polygon or tuple
            A geometry or bounding box
        geo_crs : str
            The spatial reference of the input geometry, defaults to EPSG:4326
        """
        if isinstance(geom, tuple):
            geom = MatchCRS.bounds(geom, geo_crs, self.crs)  # type: ignore
            geom_query = utils.ESRIGeomQuery(geom, self.out_sr).bbox()
        else:
            geom = MatchCRS.geometry(geom, geo_crs, self.crs)
            geom_query = utils.ESRIGeomQuery(geom, self.out_sr).polygon()

        payload = {
            **geom_query,  # type: ignore
            "spatialRel": self.spatial_relation,
            "returnGeometry": "false",
            "returnIdsOnly": "true",
            "f": self.outformat,
        }
        resp = self.session.post(f"{self.base_url}/query", payload)

        try:
            self.featureids = resp.json()["objectIds"]
        except (KeyError, TypeError, IndexError, JSONDecodeError):
            raise ZeroMatched("No feature ID were found within the requested region.")

    def get_features(self) -> List[Dict[str, Any]]:
        """Get features based on the feature IDs."""
        if not all(f in self.valid_fields for f in self.outfields):
            raise InvalidInputValue("outfields", self.valid_fields)

        payload = {
            "returnGeometry": "true",
            "outSR": self.out_sr,
            "outfields": ",".join(self.outfields),
            "f": self.outformat,
        }

        def getter(ids: Tuple[str, ...]) -> Union[Response, Tuple[str, ...]]:
            payload.update({"objectIds": ",".join(ids)})
            resp = self.session.post(f"{self.base_url}/query", payload)
            r_json = resp.json()
            try:
                if "error" in r_json:
                    return ids

                return r_json
            except AssertionError:
                if self.outformat == "geojson":
                    raise ZeroMatched(
                        "There was a problem processing the request with geojson outformat. "
                        + "Your can set the outformat to json and retry."
                    )

                raise ZeroMatched("No matching data was found on the server.")

        feature_list = utils.threading(getter, self.featureids, max_workers=self.n_threads)

        # Split the list based on type which are tuple and dict
        feature_types = defaultdict(list)
        for f in feature_list:
            feature_types[type(f)].append(f)

        features = feature_types[dict]

        if len(feature_types[tuple]) > 0:
            failed = [tuple(x) for y in feature_types[tuple] for x in y]
            retry = utils.threading(getter, failed, max_workers=self.n_threads * 2)
            fixed = [resp for resp in retry if not isinstance(resp, tuple)]

            nfailed = len(failed) - len(fixed)
            if nfailed > 0:
                warn(
                    f"From {self.nfeatures} requetsed features, {nfailed} were not available on the server."
                )

            features += fixed

        if len(features) == 0:
            raise ZeroMatched("No valid feature was found.")

        return features


@dataclass
class WMSBase:
    """Base class for accessing a WMS service.

    Parameters
    ----------
    url : str
        The base url for the WMS service e.g., https://www.mrlc.gov/geoserver/mrlc_download/wms
    layers : str or list
        A layer or a list of layers from the service to be downloaded. You can pass an empty
        string to get a list of available layers.
    outformat : str
        The data format to request for data from the service. You can pass an empty
        string to get a list of available output formats.
    version : str, optional
        The WMS service version which should be either 1.1.1 or 1.3.0, defaults to 1.3.0.
    crs : str, optional
        The spatial reference system to be used for requesting the data, defaults to
        epsg:4326.
    """

    url: str
    layers: Union[str, List[str]]
    outformat: str
    version: str = "1.3.0"
    crs: str = DEF_CRS

    def __repr__(self) -> str:
        """Print the services properties."""
        layers = self.layers if isinstance(self.layers, list) else [self.layers]
        return (
            "Connected to the WMS service with the following properties:\n"
            + f"URL: {self.url}\n"
            + f"Version: {self.version}\n"
            + f"Layers: {', '.join(lyr for lyr in layers)}\n"
            + f"Output Format: {self.outformat}\n"
            + f"Output CRS: {self.crs}"
        )

    def validate_wms(self) -> None:
        """Validate input arguments with the WMS service."""
        wms = WebMapService(self.url, version=self.version)

        valid_layers = {wms[lyr].name: wms[lyr].title for lyr in list(wms.contents)}

        if not isinstance(self.layers, (str, list)):
            raise InvalidInputType("layers", "str or list")

        layers = [self.layers] if isinstance(self.layers, str) else self.layers

        if any(lyr not in valid_layers.keys() for lyr in layers):
            raise InvalidInputValue("layers", (f"{n} for {t}" for n, t in valid_layers.items()))

        valid_outformats = wms.getOperationByName("GetMap").formatOptions
        if self.outformat not in valid_outformats:
            raise InvalidInputValue("outformat", valid_outformats)

        valid_crss = {lyr: [s.lower() for s in wms[lyr].crsOptions] for lyr in layers}
        if any(self.crs not in valid_crss[lyr] for lyr in layers):
            _valid_crss = (f"{lyr}: {', '.join(cs)}\n" for lyr, cs in valid_crss.items())
            raise InvalidInputValue("CRS", _valid_crss)

    def get_validlayers(self) -> Dict[str, str]:
        """Get the layers supportted by the WMS service."""
        wms = WebMapService(self.url, version=self.version)

        return {wms[lyr].name: wms[lyr].title for lyr in list(wms.contents)}


class WMS(WMSBase):
    """Get data from a WMS service within a geometry or bounding box.

    Parameters
    ----------
    url : str
        The base url for the WMS service e.g., https://www.mrlc.gov/geoserver/mrlc_download/wms
    layers : str or list
        A layer or a list of layers from the service to be downloaded. You can pass an empty
        string to get a list of available layers.
    outformat : str
        The data format to request for data from the service. You can pass an empty
        string to get a list of available output formats.
    crs : str, optional
        The spatial reference system to be used for requesting the data, defaults to
        epsg:4326.
    version : str, optional
        The WMS service version which should be either 1.1.1 or 1.3.0, defaults to 1.3.0.
    validation : bool, optional
        Validate the input arguments from the WMS service, defaults to True. Set this
        to False if you are sure all the WMS settings such as layer and crs are correct
        to avoid sending extra requests.
    """

    def __init__(
        self,
        url: str,
        layers: Union[str, List[str]],
        outformat: str,
        version: str = "1.3.0",
        crs: str = DEF_CRS,
        validation: bool = True,
    ) -> None:
        super().__init__(url, layers, outformat, version, crs)

        self.session = RetrySession()
        self.layers = [self.layers] if isinstance(self.layers, str) else self.layers
        if validation:
            self.validate_wms()

    def getmap_bybox(
        self,
        bbox: Tuple[float, float, float, float],
        resolution: float,
        box_crs: str = DEF_CRS,
        always_xy: bool = False,
        max_px: int = 8000000,
    ) -> Dict[str, bytes]:
        """Get data from a WMS service within a geometry or bounding box.

        Parameters
        ----------
        box : tuple
            A bounding box for getting the data.
        resolution : float
            The output resolution in meters. The width and height of output are computed in pixel
            based on the geometry bounds and the given resolution.
        box_crs : str, optional
            The spatial reference system of the input bbox, defaults to
            epsg:4326.
        always_xy : bool, optional
            Whether to always use xy axis order, defaults to False. Some services change the axis
            order from xy to yx, following the latest WFS version specifications but some don't.
            If the returned value does not have any geometry, it indicates that most probably the
            axis order does not match. You can set this to True in that case.
        max_px : int, opitonal
            The maximum allowable number of pixels (width x height) for a WMS requests,
            defaults to 8 million based on some trial-and-error.

        Returns
        -------
        dict
            A dict where the keys are the layer name and values are the returned response
            from the WMS service as bytes. You can use ``utils.create_dataset`` function
            to convert the responses to ``xarray.Dataset``.
        """
        utils.check_bbox(bbox)
        _bbox = MatchCRS.bounds(bbox, box_crs, self.crs)
        bounds = utils.bbox_decompose(_bbox, resolution, self.crs, max_px)

        payload = {
            "version": self.version,
            "format": self.outformat,
            "request": "GetMap",
        }

        if self.version == "1.1.1":
            payload["srs"] = self.crs

        else:
            payload["crs"] = self.crs

        geographic_crs = pyproj.CRS.from_user_input(self.crs).is_geographic

        def _getmap(args):
            lyr, bnds = args
            _bbox, counter, _width, _height = bnds

            if self.version != "1.1.1" and geographic_crs and not always_xy:
                _bbox = (_bbox[1], _bbox[0], _bbox[3], _bbox[2])

            payload["bbox"] = f'{",".join(str(c) for c in _bbox)}'
            payload["width"] = _width
            payload["height"] = _height
            payload["layers"] = lyr
            resp = self.session.get(self.url, payload)
            return f"{lyr}_dd_{counter}", resp.content

        return dict(_getmap(i) for i in product(self.layers, bounds))


@dataclass
class WFSBase:
    """Base class for WFS service.

    Parameters
    ----------
    url : str
        The base url for the WFS service, for examples:
        https://hazards.fema.gov/nfhl/services/public/NFHL/MapServer/WFSServer
    layer : str
        The layer from the service to be downloaded, defaults to None which throws
        an error and includes all the available layers offered by the service.
    outformat : str
        The data format to request for data from the service, defaults to None which
         throws an error and includes all the available format offered by the service.
    version : str, optional
        The WFS service version which should be either 1.1.1, 1.3.0, or 2.0.0.
        Defaults to 2.0.0.
    crs: str, optional
        The spatial reference system to be used for requesting the data, defaults to
        epsg:4326.
    """

    url: str
    layer: Optional[str] = None
    outformat: Optional[str] = None
    version: str = "2.0.0"
    crs: str = DEF_CRS

    def __repr__(self) -> str:
        """Print the services properties."""
        return (
            "Connected to the WFS service with the following properties:\n"
            + f"URL: {self.url}\n"
            + f"Version: {self.version}\n"
            + f"Layer: {self.layer}\n"
            + f"Output Format: {self.outformat}\n"
            + f"Output CRS: {self.crs}"
        )

    def validate_wfs(self):
        """Validate input arguments with the WFS service."""
        wfs = WebFeatureService(self.url, version=self.version)

        valid_layers = list(wfs.contents)
        if self.layer is None:
            raise MissingInputs(
                "The layer argument is missing."
                + " The following layers are available:\n"
                + ", ".join(valid_layers)
            )

        if self.layer not in valid_layers:
            raise InvalidInputValue("layers", valid_layers)

        valid_outformats = wfs.getOperationByName("GetFeature").parameters["outputFormat"]["values"]
        valid_outformats = [v.lower() for v in valid_outformats]
        if self.outformat is None:
            raise MissingInputs(
                "The outformat argument is missing."
                + " The following output formats are available:\n"
                + ", ".join(valid_outformats)
            )

        if self.outformat not in valid_outformats:
            raise InvalidInputValue("outformat", valid_outformats)

        valid_crss = [f"{s.authority.lower()}:{s.code}" for s in wfs[self.layer].crsOptions]
        if self.crs.lower() not in valid_crss:
            raise InvalidInputValue("crs", valid_crss)

    def get_validnames(self) -> List[str]:
        """Get valid column names for a layer."""
        max_features = "count" if self.version == "2.0.0" else "maxFeatures"

        payload = {
            "service": "wfs",
            "version": self.version,
            "outputFormat": self.outformat,
            "request": "GetFeature",
            "typeName": self.layer,
            max_features: "1",
        }

        resp = RetrySession().get(self.url, payload)
        utils.check_response(resp)

        r_json = resp.json()
        valid_fields = list(
            set(
                utils.traverse_json(r_json, ["fields", "name"])
                + utils.traverse_json(r_json, ["fields", "alias"])
                + ["*"]
            )
        )

        if None in valid_fields:
            valid_fields = list(utils.traverse_json(r_json, ["features", "properties"])[0].keys())

        return valid_fields


class WFS(WFSBase):
    """Data from any WFS service within a geometry or by featureid.

    Parameters
    ----------
    url : str
        The base url for the WFS service, for examples:
        https://hazards.fema.gov/nfhl/services/public/NFHL/MapServer/WFSServer
    layer : str
        The layer from the service to be downloaded, defaults to None which throws
        an error and includes all the available layers offered by the service.
    outformat : str
        The data format to request for data from the service, defaults to None which
         throws an error and includes all the available format offered by the service.
    version : str, optional
        The WFS service version which should be either 1.1.1, 1.3.0, or 2.0.0.
        Defaults to 2.0.0.
    crs: str, optional
        The spatial reference system to be used for requesting the data, defaults to
        epsg:4326.
    validation : bool, optional
        Validate the input arguments from the WFS service, defaults to True. Set this
        to False if you are sure all the WFS settings such as layer and crs are correct
        to avoid sending extra requests.
    """

    def __init__(
        self,
        url: str,
        layer: Optional[str] = None,
        outformat: Optional[str] = None,
        version: str = "2.0.0",
        crs: str = DEF_CRS,
        validation: bool = True,
    ) -> None:
        super().__init__(url, layer, outformat, version, crs)

        self.session = RetrySession()
        if validation:
            self.validate_wfs()

    def getfeature_bybox(
        self,
        bbox: Tuple[float, float, float, float],
        box_crs: str = DEF_CRS,
        always_xy: bool = False,
    ) -> Response:
        """Get data from a WFS service within a bounding box.

        Parameters
        ----------
        bbox : tuple
            A bounding box for getting the data: [west, south, east, north]
        box_crs : str, optional
            The spatial reference system of the input bbox, defaults to
            epsg:4326.
        always_xy : bool, optional
            Whether to always use xy axis order, defaults to False. Some services change the axis
            order from xy to yx, following the latest WFS version specifications but some don't.
            If the returned value does not have any geometry, it indicates that most probably the
            axis order does not match. You can set this to True in that case.

        Returns
        -------
        requests.Response
            WFS query response within a bounding box.
        """
        utils.check_bbox(bbox)

        if (
            self.version != "1.1.1"
            and pyproj.CRS.from_user_input(box_crs).is_geographic
            and not always_xy
        ):
            bbox = (bbox[1], bbox[0], bbox[3], bbox[2])

        payload = {
            "service": "wfs",
            "version": self.version,
            "outputFormat": self.outformat,
            "request": "GetFeature",
            "typeName": self.layer,
            "bbox": f'{",".join(str(c) for c in bbox)},{box_crs}',
            "srsName": self.crs,
        }

        resp = self.session.get(self.url, payload)
        utils.check_response(resp)

        return resp

    def getfeature_byid(
        self, featurename: str, featureids: Union[List[str], str], filter_spec: str = "1.1",
    ) -> Response:
        """Get features based on feature IDs.

        Parameters
        ----------
        featurename : str
            The name of the column for searching for feature IDs
        featureids : str or list
            The feature ID(s)
        filter_spec : str
            The OGC filter spec, defaults to "1.1". Supported versions are
            1.1 and 2.0.

        Returns
        -------
        requests.Response
            WMS query response
        """
        valid_features = self.get_validnames()
        if featurename not in valid_features:
            raise InvalidInputValue("featurename", valid_features)

        featureids = featureids if isinstance(featureids, list) else [featureids]

        if len(featureids) == 0:
            raise InvalidInputType("featureids", "int or str or list")

        fspecs = ["2.0", "1.1"]
        if filter_spec not in fspecs:
            raise InvalidInputValue("filter_spec", fspecs)

        def filter_xml1(pname, pid):
            fstart = '<ogc:Filter xmlns:ogc="http://www.opengis.net/ogc"><ogc:Or>'
            fend = "</ogc:Or></ogc:Filter>"
            return (
                fstart
                + "".join(
                    [
                        f"<ogc:PropertyIsEqualTo><ogc:PropertyName>{pname}"
                        + f"</ogc:PropertyName><ogc:Literal>{p}"
                        + "</ogc:Literal></ogc:PropertyIsEqualTo>"
                        for p in pid
                    ]
                )
                + fend
            )

        def filter_xml2(pname, pid):
            fstart = '<fes:Filter xmlns:fes="http://www.opengis.net/fes/2.0"><fes:Or>'
            fend = "</fes:Or></fes:Filter>"
            return (
                fstart
                + "".join(
                    [
                        f"<fes:PropertyIsEqualTo><fes:ValueReference>{pname}"
                        + f"</fes:ValueReference><fes:Literal>{p}"
                        + "</fes:Literal></fes:PropertyIsEqualTo>"
                        for p in pid
                    ]
                )
                + fend
            )

        fxml = filter_xml1 if filter_spec == "1.1" else filter_xml2

        payload = {
            "service": "wfs",
            "version": self.version,
            "outputFormat": self.outformat,
            "request": "GetFeature",
            "typeName": self.layer,
            "srsName": self.crs,
            "filter": fxml(featurename, featureids),
        }

        resp = self.session.post(self.url, payload)
        utils.check_response(resp)

        return resp


class ServiceURL:
    """Base URLs of the supported services."""

    @property
    def restful(self):
        return RESTfulURLs()

    @property
    def wms(self):
        return WMSURLs()

    @property
    def wfs(self):
        return WFSURLs()

    @property
    def http(self):
        return HTTPURLs()


class RESTfulURLs(NamedTuple):
    """A list of RESTful services URLs."""

    nwis: str = "https://waterservices.usgs.gov/nwis"
    nldi: str = "https://labs.waterdata.usgs.gov/api/nldi/linked-data"
    daymet_point: str = "https://daymet.ornl.gov/single-pixel/api/data"
    daymet_grid: str = "https://thredds.daac.ornl.gov/thredds/ncss/ornldaac/1328"
    wbd: str = "https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer"
    fws: str = "https://www.fws.gov/wetlands/arcgis/rest/services"
    fema: str = "https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHL/MapServer"


class WMSURLs(NamedTuple):
    """A list of WMS services URLs."""

    mrlc: str = "https://www.mrlc.gov/geoserver/mrlc_download/wms"
    fema: str = "https://hazards.fema.gov/gis/nfhl/rest/services/public/NFHLWMS/MapServer/WMSServer"
    nm_3dep: str = "https://elevation.nationalmap.gov/arcgis/services/3DEPElevation/ImageServer/WMSServer"
    fws: str = "https://www.fws.gov/wetlands/arcgis/services/Wetlands_Raster/ImageServer/WMSServer"


class WFSURLs(NamedTuple):
    """A list of WFS services URLs."""

    waterdata: str = "https://labs.waterdata.usgs.gov/geoserver/wmadata/ows"
    fema: str = "https://hazards.fema.gov/gis/nfhl/services/public/NFHL/MapServer/WFSServer"


class HTTPURLs(NamedTuple):
    """A list of HTTP services URLs."""

    ssebopeta: str = "https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/uswem/web/conus/eta/modis_eta/daily/downloads"
