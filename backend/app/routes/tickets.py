from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Ticket
from ..schemas import TicketInput, TicketOut, TicketPriority, TicketStatus

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


def _get_ticket_or_404(db: Session, ticket_id: int) -> Ticket:
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    return ticket


@router.get("", response_model=list[TicketOut])
def list_tickets(
    status: TicketStatus | None = Query(default=None),
    priority: TicketPriority | None = Query(default=None),
    db: Session = Depends(get_db),
):
    statement = select(Ticket).order_by(Ticket.id.desc())
    if status:
        statement = statement.where(Ticket.status == status)
    if priority:
        statement = statement.where(Ticket.priority == priority)
    return db.scalars(statement).all()


@router.post("", response_model=TicketOut, status_code=201)
def create_ticket(payload: TicketInput, db: Session = Depends(get_db)):
    ticket = Ticket(**payload.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return _get_ticket_or_404(db, ticket_id)


@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, payload: TicketInput, db: Session = Depends(get_db)):
    ticket = _get_ticket_or_404(db, ticket_id)
    for field, value in payload.model_dump().items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = _get_ticket_or_404(db, ticket_id)
    db.delete(ticket)
    db.commit()
    return Response(status_code=204)
