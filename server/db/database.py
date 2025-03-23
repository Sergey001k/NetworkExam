import os
from tortoise.contrib.fastapi import register_tortoise

DATABASE_URL = os.getenv("DATABASE_URL")


def init_db(app):
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["db.db_models"]},
        generate_schemas=True,
        add_exception_handlers=True
    )