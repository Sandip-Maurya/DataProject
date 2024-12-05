import gspread

def get_gs_obj(GOOGLE_CRED_PATH, SHEET_NAME):
    sa = gspread.service_account(GOOGLE_CRED_PATH)
    gs_obj = sa.open(SHEET_NAME)
    return gs_obj
