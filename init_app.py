from os import environ as env
from dotenv import find_dotenv, load_dotenv

from app import app


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=env.get("API_PORT", 5000), debug=env.get("DEBUG", False)
    )
