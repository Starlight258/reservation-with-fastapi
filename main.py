from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, create_engine, Session, select

app = FastAPI()

# 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory="resources/static"), name="static")
# CSS, JS, Images 직접 접근을 위한 설정
app.mount("/css", StaticFiles(directory="resources/static/css"), name="css")
app.mount("/js", StaticFiles(directory="resources/static/js"), name="js")
app.mount("/image", StaticFiles(directory="resources/static/image"), name="image")

templates = Jinja2Templates(directory="resources/templates")

@app.get("/admin", response_class=HTMLResponse)
async def show_admin_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin/index.html",
        context={"request": request}
    )


class Reservation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    date: str = Field(index=True)
    time: str = Field(index=True)


class ReservationCreateDto(BaseModel):
    name: str
    date: str
    time: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/reservations")
def create_reservation(reservation_dto: ReservationCreateDto, session: Session = Depends(get_session)):
    reservation = Reservation(
        name=reservation_dto.name,
        date=reservation_dto.date,
        time=reservation_dto.time
    )

    session.add(reservation)
    session.commit()
    session.refresh(reservation)

    return reservation


@app.get("/reservations")
def read_reservations(session: Session = Depends(get_session)):
    reservations = session.exec(select(Reservation)).all()
    return {"reservations": reservations}


@app.get("/reservations/{reservation_id}")
def read_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        return {"error": "Reservation not found"}
    return reservation


@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        return {"error": "Reservation not found"}

    session.delete(reservation)
    session.commit()

    return {"message": "Reservation deleted successfully"}
