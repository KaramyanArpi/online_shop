from app import start_app
from app.db import init_db

if __name__ == "__main__":
    init_db()
    app = start_app()

    app.run(debug=True, port="8000")
