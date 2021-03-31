from __future__ import absolute_import, unicode_literals

from celery import shared_task, Celery
from celery.schedules import crontab
from datetime import datetime
from .models import Ticket

@shared_task
def auto_close_ticket():
    tickets = Ticket.objects.all()

    datediff = datetime.now()
    # fivedays =
    #
    # for ticket in tickets:
    #     if ticket.status == 'OH' and ticket.last_updated <=




