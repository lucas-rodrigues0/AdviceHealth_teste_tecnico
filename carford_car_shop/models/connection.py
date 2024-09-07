import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from sqlalchemy_utils import database_exists, create_database
from dotenv import find_dotenv, load_dotenv


from models import Base


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def create_sqlite_db_url(path):
    """Create db url for sqlite. Use in-memory for testing and local file for development
    If directory does not exists create one.
    """
    if path != ":memory:" and not os.path.exists(path):
        os.makedirs(path)

    if path == ":memory:":
        db_url = "sqlite:///%s" % path
    else:
        db_url = "sqlite:///%sdb.sqlite3" % database_path

    return db_url


# Set database by the enviroment
if os.environ.get("DEV"):
    print("Connected to SQLite local file")
    database_path = os.environ.get("DB_DEV_PATH")

    db_url = create_sqlite_db_url(database_path)
elif os.environ.get("TESTING"):
    print("Connected to SQLite in-memory")

    database_path = os.environ.get("DB_TEST_PATH")

    db_url = create_sqlite_db_url(database_path)
else:
    print("Connected to PostgreSQL")

    config = {
        "dbname": os.environ.get("PG_DATABASE"),
        "user": os.environ.get("PG_USER"),
        "password": os.environ.get("PG_PASSWORD"),
        "host": os.environ.get("PG_HOST"),
        "port": os.environ.get("PG_PORT"),
    }

    # for the engine the db url specification
    # dialect+driver://username:password@host:port/database
    db_url = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"

# Create the engine for the database
engine = create_engine(db_url, echo=False)

# Instanciate the sessionmaker for connection
Session = sessionmaker(bind=engine)

# Create database if does not exists
if not database_exists(engine.url):
    create_database(engine.url)

# To inspect database for the tables
inspector = inspect(engine)


def create_tables():
    Base.metadata.create_all(engine)
    return
