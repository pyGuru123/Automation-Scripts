import os
import tempfile
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from src.config import get_constraints
from src.tests import main
from src.highlighter import highlight_logs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

app = FastAPI()

@app.post("/uploadfile/")
async def test_excel_file(file: UploadFile = File(...)):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        log_file_name = os.path.splitext(file.filename)[0] + ".txt"
        log_path = os.path.join(LOG_DIR, log_file_name)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            lines = file.file.readlines()
            temp_file.writelines(lines)
            temp_file.seek(0)

            filename = file.filename
            REQUIREMENTS = get_constraints(temp_file)
            
            res = main(temp_file, log_path, REQUIREMENTS)
            if res:
                highlight_logs(temp_file, temp_file.name, log_path)
                return FileResponse(temp_file.name, filename=filename, 
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        raise HTTPException(400, detail="Bad File Format, not a excel file")