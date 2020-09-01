from celery.signals import task_postrun
from celery.utils.log import get_task_logger
from api.database import db_session as db
from api.models import clusters
from api.extensions import celery

logger = get_task_logger(__name__)


@celery.task
def build_image(uuid=None, docker_image=None, docker_tag=None,
                image_format=None):
    status = 'complete'
    clusters.Cluster.query.filter_by(uuid=uuid).update(dict(status=status))
    db.commit()
    return (status)


@celery.task
def log(message):
    logger.debug(message)
    logger.info(message)
    logger.warning(message)
    logger.error(message)
    logger.critical(message)


@task_postrun.connect
def close_session(*args, **kwargs):
    # Flask SQLAlchemy will automatically create new sessions for you from
    # a scoped session factory, given that we are maintaining the same app
    # context, this ensures tasks have a fresh session (e.g. session errors
    # won't propagate across tasks)
    db.remove()
