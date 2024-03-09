from fastapi import FastAPI, Depends, status

from api.expense import schemas
from typing import Annotated, List, Dict, Any

app = FastAPI(
    title='Financial literacy(My Wallet)'
)

expenses = []


@app.post('/add_expense')
async def add_expense(expense: Annotated[schemas.ExpenseCreate, Depends()]) -> dict[str, list[Any] | Any]:
    expenses.append(expense)
    return {'status': status.HTTP_200_OK, 'data': expenses}


# @app.get('read_expenses')
# async def read_expenses(expense: Annotated[schemas.ExpenseRead, Depends()]):
#     expenses | expense
#     return {'status': 200, 'data': expenses}
