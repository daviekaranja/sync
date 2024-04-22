import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from sqlalchemy.sql import text

from syncify.app.db.session import SessionLocal
# from syncify.app.scripts.system_logger import logger
logger = logging.getLogger(__name__)


max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN)
)
def init() -> None:
    try:
        db = SessionLocal()
        # Try and create session to check if the DB is awake
        db.execute(text('SELECT 1'))
        logger.info("Database started Successfully")
    except Exception as e:
        logger.error(e)
        logger.critical(f"oops database error{e}")
        raise e


def main() -> None:
    logger.info('Checking Database')
    init()
    logger.info("Service initialized successfully")


if __name__ == "__main__":
    main()