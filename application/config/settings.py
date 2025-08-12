# config/settings.py
import os

EXCEL_FILE_PATH1 = os.getenv("EXCEL_FILE_PATH1", "scores/readiness.xlsx")
EXCEL_FILE_PATH2 = os.getenv("EXCEL_FILE_PATH2", "scores/pre_application.xlsx")
EXCEL_FILE_PATH3 = os.getenv("EXCEL_FILE_PATH3", "scores/pre_readiness.xlsx")


