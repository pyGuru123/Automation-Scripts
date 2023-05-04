import os
import pandas as pd
from loguru import logger
from fastapi import File, UploadFile, APIRouter, BackgroundTasks

from app.sheets_combiner.utils import main

router = APIRouter(prefix="/sheets_combiner", tags=["sheets_combiner"])

@router.post("/upload_file/")
async def test_excel_file(
    background_tasks: BackgroundTasks, file: UploadFile = File(...)
) -> str:
    if file.filename.endswith(".xlsx"):
        filename = file.filename.split(".")[0] + "-merged.xlsx"
        try:
            background_tasks.add_task(main, file.file, filename)
            return filename
        except Exception as e:
            logger.error(f"error {e} in the sheets_combiner module")
            return f"Something went wrong : {e}"
    else:
        return f"file not in excel format: {file.filename}"
