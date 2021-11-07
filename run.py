#  Copyright (c) Fahad Ahammed 2021-2021.
from src import app

if __name__ == "__main__":
    app.run(
        host=app.config.get("HOST"),
        port=app.config.get("PORT")
    )