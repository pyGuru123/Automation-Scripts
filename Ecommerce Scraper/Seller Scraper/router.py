import os
import pandas as pd
from loguru import logger
from fastapi import File, UploadFile, APIRouter, BackgroundTasks

from app.sellers_scraper.utils import main


router = APIRouter(prefix="/sellers_scraper", tags=["sellers_scraper"])


@router.post("/upload_file/")
async def test_excel_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)) -> str:
    if file.filename.endswith('.xlsx'):
        filename = file.filename.split('.')[0] + "-output.xlsx"
        try:
            background_tasks.add_task(main, file.file, filename)
            return filename
        except Exception as e:
            logger.error(f"error {e} in the sellers_scraper module")
            return f"Something went wrong : {e}"
    else:
        return f"file not in excel format: {file.filename}"
