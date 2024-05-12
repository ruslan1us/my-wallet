from celery import Celery, shared_task
from celery.schedules import crontab

from fastapi import Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.services.send_mail import send_email_async, send_email_background
from src.database import get_async_session

from src.api.services.statistics_services import Services

celery = Celery('tasks', broker='redis://localhost:6379')

celery.conf.beat_schedule = {
    'mail_report': {
        'task': 'src.api.tasks.tasks.send_all_users_report',
        'schedule': crontab(day_of_month='11', month_of_year='*'),
    },
}

celery.conf.timezone = 'UTC'


@shared_task
async def send_all_users_report(session: AsyncSession = Depends(get_async_session),
                                services: Services = Depends(Services)):

    users = await services.get_all_users(session=session)

    for user in users:
        expense = await services.get_the_biggest_expense(session=session, user=user)

        if expense == None:
            continue

        expense_dict_money_spinner = await expense[0][0].__dict__
        expense_dict_expense = await expense[1][0].__dict__

        await send_email_async({
            'subject': 'Month Report',
            'email_to': 'rusikkoliada@gmail.com',
            'body': {'money_spinner': f'{expense_dict_money_spinner.get('name')}',
                     'amount': f'{expense_dict_expense.get('amount')}',
                     'date': f'{expense_dict_expense.get('expensed_at')}',
                     'name': f'{user.username}'}
        })
