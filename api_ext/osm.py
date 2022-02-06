from . import call as base_call


def call(self, query: str, **kwargs) -> dict:
    query = get_query(query, out_format="json", end="body")

    return base_call(self,
                     url="http://overpass-api.de/api/interpreter",
                     query=query)


def get_query(query: str, out_format: str = "json", end: str = "body") -> bytes:
    ret = f'[out:"{out_format}"];\n'
    ret += query
    ret += f'\nout {end};'
    return ret.encode('utf-8')
