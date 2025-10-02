import logging
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def notify_new_request(request_id):
    logger.info(f"New request notification: {request_id}")

@shared_task
def monitor_contract_status(request_id):
    logger.info(f"Monitoring contract for request: {request_id}")
