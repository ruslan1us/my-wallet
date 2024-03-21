from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from fastapi.exceptions import HTTPException

from src.api.expense.models import MoneySpinnerTable
from src.api.expense.schemas import MoneySpinnerCreate
from src.database import get_async_session

router = APIRouter(
    prefix='/money_spinners',
    tags=['money_spinners']
)


@router.get('/{money_spinner_id}')
async def get_money_spinner_by_id(money_spinner_id: int,
                                  session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(MoneySpinnerTable).where(MoneySpinnerTable.id == money_spinner_id)
        query_result = await session.execute(query)
        result = query_result.scalar()

        if result is None:
            raise Exception

        return {
                'status': 'OK',
                'data': result,
                'details': None
        }
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
        {
            'status': 'NOT_FOUND',
            'data': None,
            'details': f'No money-spinner with id: {money_spinner_id}'
        })


@router.post('/', status_code=201)
async def add_money_spinner(money_spinner: MoneySpinnerCreate,
                            session: AsyncSession = Depends(get_async_session)):
    try:
        new_money_spinner = MoneySpinnerTable(**money_spinner.model_dump())

        session.add(new_money_spinner)
        await session.commit()
        await session.refresh(new_money_spinner)

        return {
            'status': 'success',
            'data': f'added {money_spinner}',
            'details': None
        }
    except:
        raise HTTPException(status_code=400, detail=
        {
            'status': 'Bad request',
            'data': None,
            'details': None
        })