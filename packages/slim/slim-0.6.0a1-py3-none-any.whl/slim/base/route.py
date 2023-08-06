import inspect
import logging
import re
from types import FunctionType
from typing import Iterable, Type, TYPE_CHECKING, Dict, List, Optional, Tuple
from posixpath import join as urljoin

import typing

from slim.base.types.doc import ResponseDataModel
from slim.base.types.route_meta_info import RouteViewInfo, RouteInterfaceInfo
# from slim.base.ws import WSRouter
from slim.exception import InvalidPostData, InvalidParams, InvalidRouteUrl
from .web import Response
from slim.utils.exceptions import HTTPException
from slim.utils.types import ASGIInstance, Scope
from slim.utils import get_class_full_name, camel_case_to_underscore_case, repath, sentinel

if TYPE_CHECKING:
    from .view import BaseView
    from .app import Application

logger = logging.getLogger(__name__)


# __all__ = ('Route',)


class Route:
    _views: List[RouteViewInfo]

    def __init__(self, app):
        self._funcs = []
        self._views = []
        self._funcs_meta = []
        self.statics = []

        self._app = app
        self.before_bind = []
        self.after_bind = []  # on_bind(app)

        self._url_mappings: Dict[str, Dict[str, RouteInterfaceInfo]] = {}
        self._url_mappings_regex: Dict[str, Dict[re.Pattern, RouteInterfaceInfo]] = {}
        self._statics_mappings_regex: Dict[str, Dict[re.Pattern, PathPrefix]] = {}

    def interface(self, method, url=None, *, summary=None, va_query=None, va_post=None, va_headers=None,
                  va_resp=ResponseDataModel, deprecated=False):
        """
        Register interface
        :param method:
        :param url:
        :param summary:
        :param va_query:
        :param va_post:
        :param va_headers:
        :param va_resp:
        :param deprecated:
        :return:
        """

        def wrapper(func: FunctionType):
            self._funcs.append(func)
            arg_spec = inspect.getfullargspec(func)

            names_exclude = set()
            names_include = set()
            names_varkw = arg_spec.varkw

            if len(arg_spec.args) >= 1:
                # skip the first argument, the view instance
                names_exclude.add(arg_spec.args[0])
                for i in arg_spec.args[1:]:
                    names_include.add(i)

            for i in arg_spec.kwonlyargs:
                names_include.add(i)

            func._route_info = RouteInterfaceInfo(
                [method],
                url or func.__name__,
                func,
                summary=summary,
                va_query=va_query,
                va_post=va_post,
                va_headers=va_headers,
                va_resp=va_resp,
                deprecated=deprecated,

                names_exclude=names_exclude,
                names_include=names_include,
                names_varkw=names_varkw
            )
            return func

        return wrapper

    def view(self, url, tag_name=None):
        """
        Register View Class
        :param url:
        :param tag_name:
        :return:
        """
        from .view import BaseView

        def wrapper(view_cls):
            assert inspect.isclass(view_cls), '%r is not a class' % view_cls.__name__
            if issubclass(view_cls, BaseView):
                view_url = url if url else camel_case_to_underscore_case(view_cls.__name__)
                route_info = RouteViewInfo(view_url, view_cls, tag_name)
                view_cls._route_info = route_info
                self._views.append(route_info)
            return view_cls

        return wrapper

    def _bind(self):
        from ._view.request_view import RequestView
        from ._view.abstract_sql_view import AbstractSQLView

        def add_to_url_mapping(_meta, _fullpath):
            for method in _meta.methods:
                if isinstance(_meta, PathPrefix):
                    self._statics_mappings_regex.setdefault(method, {})
                    try:
                        _re = repath.pattern(_fullpath)
                        self._statics_mappings_regex[method][re.compile(_re)] = _meta
                    except Exception as e:
                        raise InvalidRouteUrl(_fullpath, e)
                else:
                    if ':' not in _fullpath and '(' not in _fullpath:
                        self._url_mappings.setdefault(method, {})
                        self._url_mappings[method][_fullpath] = _meta
                    else:
                        self._url_mappings_regex.setdefault(method, {})
                        try:
                            _re = repath.pattern(_fullpath)
                            self._url_mappings_regex[method][re.compile(_re)] = _meta
                        except Exception as e:
                            raise InvalidRouteUrl(_fullpath, e)

        # bind views
        for view_info in self._views:
            view_cls = view_info.view_cls
            view_cls._on_bind(self)

            for k, v in inspect.getmembers(view_cls):
                if isinstance(v, FunctionType):
                    # bind interface to url mapping
                    if getattr(v, '_route_info', None):
                        meta: RouteInterfaceInfo = v._route_info
                        meta.view_cls = sentinel  # just a flag
                        meta.view_cls_set.add(view_cls)

                        meta = meta.clone()  # make clone because interface could be inherit.
                        meta.view_cls = view_cls
                        meta.handler_name = '%s.%s' % (get_class_full_name(view_cls), meta.handler.__name__)

                        fullpath = urljoin(self._app.mountpoint, view_info.url, meta.url)
                        meta.fullpath = fullpath
                        add_to_url_mapping(meta, fullpath)
                        self._funcs_meta.append(meta)

            if issubclass(view_cls, AbstractSQLView):
                self._app.tables[view_cls.table_name] = view_cls
            view_cls._ready()

        # bind functions
        for i in self._funcs:
            if not i._route_info.view_cls:
                meta: RouteInterfaceInfo = i._route_info
                meta.view_cls = RequestView
                meta.handler_name = meta.handler.__name__
                meta.is_free_func = True

                fullpath = urljoin(self._app.mountpoint, meta.url)
                meta.fullpath = fullpath
                add_to_url_mapping(meta, fullpath)
                self._funcs_meta.append(meta)

        for i in self.statics:
            fullpath = urljoin(self._app.mountpoint, i.path)
            i.fullpath = fullpath
            add_to_url_mapping(i, fullpath)

    def query_path(self, method, path) -> Tuple[Optional[RouteInterfaceInfo], Optional[Dict]]:
        """
        Get route info for specified method and path.
        :param method:
        :param path:
        :return:
        """
        path_mapping = self._url_mappings.get(method, None)
        if path_mapping:
            ret = path_mapping.get(path)
            if ret:
                if ret.handler.__name__ not in ret.view_cls._interface_disable:
                    return ret, {}

        path_mapping = self._url_mappings_regex.get(method, None)
        if path_mapping:
            for i, route_info in path_mapping.items():
                m = i.fullmatch(path)
                if m:
                    if route_info.handler.__name__ not in route_info.view_cls._interface_disable:
                        return route_info, m.groupdict()

        return None, None

    def query_statics_path(self, method, path) -> Tuple[Optional[typing.Any], Optional[Dict]]:
        path_mapping = self._statics_mappings_regex.get(method, None)
        if path_mapping:
            for i, route_info in path_mapping.items():
                m = i.fullmatch(path)
                if m:
                    return route_info, m.groupdict()

        return None, None

    def websocket(self, url, obj):
        """
        Register Websocket
        :param url:
        :param obj:
        :return:
        """

        def wrapper(cls):
            if issubclass(cls, WSRouter):
                self.websockets.append((url, obj()))
            return cls

        return wrapper

    def add_static(self, prefix, path):
        """
        :param prefix: URL prefix
        :param path: file directory
        :param kwargs:
        :return:
        """
        from slim.base.staticfiles import StaticFiles
        prefix = PathPrefix(prefix, app=StaticFiles(directory=path), methods=['GET'])
        self.statics.append(prefix)

    def get(self, url=None, *, summary=None, va_query=None, va_post=None, va_headers=None,
            va_resp=ResponseDataModel, deprecated=False):
        kwargs = locals()
        del kwargs['self']
        return self.interface('GET', **kwargs)

    def post(self, url=None, *, summary=None, va_query=None, va_post=None, va_headers=None,
             va_resp=ResponseDataModel, deprecated=False):
        kwargs = locals()
        del kwargs['self']
        return self.interface('POST', **kwargs)


class PathPrefix:
    def __init__(
            self, path: str, app, methods: typing.Sequence[str] = ()
    ) -> None:
        self.path = path
        self.app = app
        self.methods = methods
        regex = "^" + path
        regex = re.sub("{([a-zA-Z_][a-zA-Z0-9_]*)}", r"(?P<\1>[^/]*)", regex)
        self.path_regex = re.compile(regex)

    def __call__(self, scope: Scope) -> ASGIInstance:
        if self.methods and scope["method"] not in self.methods:
            if "app" in scope:
                raise HTTPException(status_code=405)
            return Response(body="Method Not Allowed", status=405)
        return self.app(scope)
