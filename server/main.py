import uvicorn
from fastapi import FastAPI
from routes.adminRouter import router as admin_router
from db.database import init_db
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(admin_router, prefix="/admin")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

load_dotenv("./.env")
init_db(app)

#For production
# if __name__ == "__main__":
#     load_dotenv("./.env")
#     init_db(app)
#     uvicorn.run("main:app")