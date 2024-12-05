# main.py

from data_access.database import DatabaseClient
from processing.process_data import load_student_details, process_exam_data
from config.config import CSV_FILE_PATH, GOOGLE_CRED_PATH, SHEET_NAME, ENGAGEMENT_TAB_NAME
from config.gs_auth import get_gs_obj
from output.update_data import update_eng_data
import pandas as pd

def main():
    # Initialize Database Client
    db_client = DatabaseClient()

    # Load Student Details
    df_students = load_student_details(CSV_FILE_PATH)

    # Fetch and Process JEE Data
    jee_data = db_client.get_eng_data(db_type='jee')
    if not jee_data:
        print('No data available in jee table')
        return
    jee_df = pd.DataFrame(jee_data)
    jee_df['studentId'] = jee_df['studentId'].astype(str)
    df_jee_output = process_exam_data(df_students, jee_df, exam_type='jee')

    # Fetch and Process NEET Data
    neet_data = db_client.get_eng_data(db_type='neet')
    if not neet_data:
        print('No data available in neet table')
        return
    neet_df = pd.DataFrame(neet_data)
    neet_df['studentId'] = neet_df['studentId'].astype(str)
    # Replace botany and zoology subject IDs with biology id (5)
    neet_df['subjectId'] = neet_df['subjectId'].replace({"4": "5", "146": "5"})
    df_neet_output = process_exam_data(df_students, neet_df, exam_type='neet')

    # Combine JEE and NEET Data
    df_output = pd.concat([df_jee_output, df_neet_output], ignore_index=True)
    df_output['stud_subj_id'] = df_output['Student ID'] + df_output['Subject']
    df_output.set_index('stud_subj_id', inplace=True)

    # Update the engagement data to google sheet
    gs_obj = get_gs_obj(GOOGLE_CRED_PATH, SHEET_NAME)   # Authenticate google sheet
    update_eng_data(df_output, gs_obj, pd, ENGAGEMENT_TAB_NAME)

if __name__ == '__main__':
    main()
