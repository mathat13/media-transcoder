import factory
from faker import Faker
from db import Job  # import your SQLAlchemy model

fake = Faker()

class JobFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Job
        sqlalchemy_session = None  # we will inject the test DB session
        sqlalchemy_session_persistence = "commit"

    path = factory.LazyFunction(lambda: fake.file_path(extension="mkv"))
    status = "pending"