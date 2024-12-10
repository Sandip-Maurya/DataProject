import gspread
from config.config import (
    GOOGLE_CRED_PATH,
    SHEET_NAME,
)

def get_gs_obj():
    sa = gspread.service_account(GOOGLE_CRED_PATH)
    gs_obj = sa.open(SHEET_NAME)
    return gs_obj
