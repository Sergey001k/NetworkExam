import os
import logging
from tortoise.contrib.fastapi import register_tortoise


def init_db(app):
    register_tortoise(
        app,
        db_url=os.getenv("DATABASE_URL"),
        modules={"models": ["db.db_models"]},
        generate_schemas=True,
        add_exception_handlers=False
    )
