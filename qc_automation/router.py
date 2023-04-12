import os
import time
from loguru import logger
import tempfile
import pandas as pd
from fastapi import File, UploadFile, APIRouter, BackgroundTasks

from app.qc_automation.tests import main


def get_log_path() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    return log_dir


router = APIRouter(prefix="/qc_automation", tags=["qc_automation"])


@router.post("/upload_file/")
async def test_excel_file(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
) -> str:
    if file.filename.endswith(".xlsx"):
        LOG_DIR = get_log_path()
        log_file_name = (
            f"{os.path.splitext(file.filename)[0]}-{int(time.time() * 100)}.txt"
        )
        log_path = os.path.join(LOG_DIR, log_file_name)

        filename = file.filename.split(".")[0] + "-filtered.xlsx"
        try:
            background_tasks.add_task(main, file.file, log_path, filename)
            return filename
        except Exception as e:
            logger.error(f"error {e} in the qc_automation module")
            return f"Something went wrong : {e}"
    else:
        return f"file not in excel or csv format: {file.filename}"
