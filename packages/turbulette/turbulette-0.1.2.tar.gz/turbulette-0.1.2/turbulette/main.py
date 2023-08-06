from importlib import import_module

from ariadne.asgi import GraphQL
from gino import Gino

from turbulette import conf

from .apps import Registry
from .apps.config import get_project_settings_by_env


def get_gino_instance() -> Gino:
    if conf.db:
        return conf.db
    database = Gino()
    conf.db = database
    return database


def setup(project_settings: str = None) -> GraphQL:
    """Load Turbulette applications and return the GraphQL route
    """

    project_settings_module = (
        get_project_settings_by_env()
        if not project_settings
        else import_module(project_settings)
    )

    # The database connection has to be initialized before the LazySettings object to be setup
    # so we have to connect to the database before the registry to be setup
    get_gino_instance()

    registry = Registry(project_settings_module=project_settings_module)
    conf.registry = registry
    schema = registry.setup()
    # At this point, settings are now available through `settings` from `turbulette.conf` module
    settings = conf.settings

    # Now that the database connection is established, we can use `settings`
    graphql_route = GraphQL(
        schema,
        debug=settings.DEBUG,
        extensions=[
            import_module(
                "ariadne.contrib.tracing.apollotracing"
            ).ApolloTracingExtension
        ]
        if settings.APOLLO_TRACING
        else None,
    )
    return graphql_route
