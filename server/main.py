import uvicorn
from fastapi import FastAPI

from endpoints.admin import router as admin_router
from endpoints.student import router as student_router
from db.db_connection import init_db
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv("./.env")

app = FastAPI()
app.include_router(admin_router, prefix="/admin")
app.include_router(student_router, prefix="/student")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


@app.get("/health")
def check_health():
    return {"status": "healthy"}


init_db(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
