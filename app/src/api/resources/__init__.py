from .v1 import routes_creator as v1_routes_creator


def register_routes(app):
    # pylint: disable=too-many-function-args
    v1_routes_creator(app, True)