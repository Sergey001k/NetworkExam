import os
from fastapi import FastAPI
from routes.adminRouter import router as admin_router
from db.database import init_db
from dotenv import load_dotenv


app = FastAPI()
app.include_router(admin_router, prefix="/admin")

load_dotenv("./.env")
init_db(app)