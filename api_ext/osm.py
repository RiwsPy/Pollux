from . import call as base_call


def call(self, query: str, skel_qt: bool = False, **kwargs) -> dict:
    query = get_query(query, out_format="json", end="body", skel_qt=skel_qt)

    return base_call(self,
                     url="http://overpass-api.de/api/interpreter",
                     data=query)


def get_query(query: str, out_format: str = "json", end: str = "body", skel_qt: bool = False) -> bytes:
    ret = f'[out:{out_format}];\n'
    ret += query
    ret += f'\nout {end};'
    if skel_qt:
        ret += '>;out skel qt;'
    return ret.encode('utf-8')
