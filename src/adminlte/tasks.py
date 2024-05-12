"""Create a test task"""
import logging
from celery import shared_task
from celery.signals import celeryd_init


logger = logging.getLogger(__name__)


@shared_task
def hello_world():
    logger.info("Hello, World!")


@celeryd_init.connect()
def test_hello_world(conf=None, **kwargs):
    """Prepare reports on project start."""
    hello_world.delay()
