from fastapi import APIRouter, status
from database import Session, ENGINE
from schemas import CargoModel


cargo_router = APIRouter(prefix="/cargo", tags=["Cargo"])
session = Session(bind=ENGINE)


@cargo_router.get("/orders")
async def get_cargo():
    cargo = session.query(CargoModel).all()
    return cargo