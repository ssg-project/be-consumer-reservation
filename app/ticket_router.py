# ticket_router.py
from fastapi import APIRouter

ticket_router = APIRouter()

@ticket_router.get("/tickets")
async def get_tickets():
    return {"message": "Here is a list of tickets"}

@ticket_router.post("/tickets")
async def create_ticket(ticket: dict):
    return {"message": "Ticket created", "ticket": ticket}