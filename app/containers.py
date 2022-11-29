from dotenv import load_dotenv
load_dotenv()
import os
from dependency_injector import containers, providers

from .database import Database
from .repositories import UserRepository, SupportOptionRepository
from .services import UserService, SupportOptionService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    db = providers.Singleton(Database, db_url=os.getenv('DATABASE_CONNECTION_STRING'))

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session
    )

    support_option_repository = providers.Factory(
        SupportOptionRepository,
        session_factory=db.provided.session
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )

    support_option_service = providers.Factory(
        SupportOptionService,
        user_repository=user_repository,
        support_option_repository=support_option_repository
    )