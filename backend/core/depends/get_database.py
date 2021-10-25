from starlette.requests import Request


def get_database(request: Request):
    return request.state.db
