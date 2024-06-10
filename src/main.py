from fastapi import FastAPI
from routes.route import router
import uvicorn
from dotenv import load_dotenv
from tortoise.contrib.fastapi import register_tortoise
import os

app = FastAPI()

app.include_router(router)

DATABASE_URL = os.getenv("DATABASE_URL")

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "192.168.0.81",
                "port": "5400",
                "user": "currency",
                "password": "12345",
                "database": "currency_db",
            }
        }
    },
    "apps": {
        "models": {
            "models": ["models.model"],  
            "default_connection": "default",
        }
    }
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    db_url=DATABASE_URL,
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)