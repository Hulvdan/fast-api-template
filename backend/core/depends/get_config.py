from starlette.requests import Request


def get_config(request: Request):
    return request.state.config
