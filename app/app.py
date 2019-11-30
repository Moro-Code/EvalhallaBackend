from src import create_app
import os 


FLASK_ENV = os.environ.get("FLASK_ENV")

if FLASK_ENV is None:
    FLASK_ENV="development"
    os.environ["FLASK_ENV"] = "development"


application = app = create_app(FLASK_ENV)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)