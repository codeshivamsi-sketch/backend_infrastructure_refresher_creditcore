from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import AsyncSessionLocal
from models import LedgerEntry, EntryType
from pydantic import BaseModel
import uuid

router = APIRouter()

class PostingRequest(BaseModel):
    loan_id: uuid.UUID
    amount: float
    description: str

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
    

@router.post("/postings")
async def create_posting(request: PostingRequest, db: AsyncSession = Depends(get_db)):
    debit = LedgerEntry(
        loan_id=request.loan_id,
        entry_type=EntryType.DEBIT,
        amount=request.amount,
        description=request.description
    )
    credit=LedgerEntry(
        loan_id=request.loan_id,
        entry_type=EntryType.CREDIT,
        amount=request.amount,
        description=request.description
    )
    db.add(debit)
    db.add(credit)
    await db.commit()
    return {"debit": debit.id, "credit_id": credit.id, "amount": request.amount}

@router.get("/postings/{loan_id}")
async def get_postings(loan_id: uuid.UUID, db: AsyncSession=Depends(get_db)):
    result = await db.execute(
        select(LedgerEntry).where(LedgerEntry.loan_id == loan_id)
    )
    entries = result.scalars().all()
    if not entries:
        raise HTTPException(status_code=404, detail="No postings for this loan")
    return entries
