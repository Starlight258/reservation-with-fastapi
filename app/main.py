from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR
from app.database import create_db_and_tables
from app.routers import admin, reservation

app = FastAPI()

# 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/css", StaticFiles(directory=str(STATIC_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(STATIC_DIR / "js")), name="js")
app.mount("/image", StaticFiles(directory=str(STATIC_DIR / "image")), name="image")

# 라우터 등록
app.include_router(admin.router)
app.include_router(reservation.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables() 