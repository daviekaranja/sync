from fastapi import APIRouter, Query
from fastapi.responses import FileResponse, PlainTextResponse
from syncify.app.scripts.system_logger import settings

router = APIRouter()


@router.get('/logs', status_code=200)
async def get_logs(lines: int = Query(default=50, description="Number of lines to fetch")):
    # Path to the log file
    log_file_path = settings.logs_file
    # Read the last N lines from the log file
    with open(log_file_path, "r") as file:
        lines_list = file.readlines()[-lines:]
    # Join the lines into a single string
    logs = "".join(lines_list)
    # Return the logs as a plain text response
    return PlainTextResponse(logs)
