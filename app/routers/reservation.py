from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models.reservation import Reservation, ReservationCreateDto

router = APIRouter()


@router.post("/reservations")
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


@router.get("/reservations")
def read_reservations(session: Session = Depends(get_session)):
    reservations = session.exec(select(Reservation)).all()
    return {"reservations": reservations}


@router.get("/reservations/{reservation_id}")
def read_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        return {"error": "Reservation not found"}
    return reservation


@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        return {"error": "Reservation not found"}
    
    session.delete(reservation)
    session.commit()
    
    return {"message": "Reservation deleted successfully"} 