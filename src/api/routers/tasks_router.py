from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.send_mail import send_email_background
from src.api.tasks.tasks import get_all_users
from src.database import get_async_session

from src.api.services.statistics_services import Services

router = APIRouter(
    prefix='/report'
)


@router.get('/send_all_users_report')
async def send_all_users_report(background_tasks: BackgroundTasks,
                                session: AsyncSession = Depends(get_async_session),
                                services: Services = Depends(Services)):

    users = await get_all_users(session=session)

    for user in users:
        expense = await services.get_the_biggest_expense(session=session, user=user)

        if expense == None:
            continue

        expense_dict_money_spinner = expense[0][0].__dict__
        expense_dict_expense = expense[1][0].__dict__

        send_email_background(background_tasks, {
            'subject': 'Month Report',
            'email_to': f'{user.email}',
            'body': {'money_spinner': f'{expense_dict_money_spinner.get('name')}',
                     'amount': f'{expense_dict_expense.get('amount')}',
                     'date': f'{expense_dict_expense.get('expensed_at')}',
                     'name': f'{user.username}'}
        })

    return 'success'
