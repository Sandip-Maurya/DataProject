# main.py

from data_access.database import DatabaseClient
from processing.process_data import load_student_details, process_eng_data, process_prof_data
from config.config import SSS_CSV_PATH, GOOGLE_CRED_PATH, SHEET_NAME, ENGAGEMENT_TAB_NAME
from config.gs_auth import get_gs_obj
from output.update_data import update_eng_data
import pandas as pd

def main():
    # Initialize Database Client
    db_client = DatabaseClient()

    # Load Student Details
    df_students = load_student_details(SSS_CSV_PATH)

    # Fetch and Process JEE Engagement Data
    jee_eng_data = db_client.get_eng_data(db_type='jee')
    if not jee_eng_data:
        print('No JEE Engagement Data Available')
        return
    jee_eng_df = pd.DataFrame(jee_eng_data)
    # jee_eng_df['studentId'] = jee_eng_df['studentId'].astype(str)
    jee_eng_output = process_eng_data(df_students, jee_eng_df, exam_type='jee')

    # Fetch and Process NEET Engagement Data
    neet_eng_data = db_client.get_eng_data(db_type='neet')
    if not neet_eng_data:
        print('No NEET Engagement Data Available')
        return
    neet_eng_df = pd.DataFrame(neet_eng_data)
    neet_eng_df['studentId'] = neet_eng_df['studentId'].astype(str)
    # Replace botany and zoology subject IDs with biology id (5)
    neet_eng_df['subjectId'] = neet_eng_df['subjectId'].replace({"4": "5", "146": "5"})
    neet_eng_output = process_eng_data(df_students, neet_eng_df, exam_type='neet')

    # Combine JEE and NEET Engagement Data
    df_output = pd.concat([jee_eng_output, neet_eng_output], ignore_index=True)
    df_output['stud_subj_id'] = df_output['Student ID'] + df_output['Subject']
    df_output.set_index('stud_subj_id', inplace=True)
    # Update the Engagement Data to Google Sheet
    gs_obj = get_gs_obj(GOOGLE_CRED_PATH, SHEET_NAME)   # Authenticate Google Sheet
    update_eng_data(df_output, gs_obj, pd, ENGAGEMENT_TAB_NAME) # Update Engagement Data in Google Sheet


    # Fetch JEE Proficiency Data
    jee_prof_data = db_client.get_prof_data(db_type='jee')
    if not jee_prof_data:
        print('No JEE Proficiency Data Available')
        return
    jee_prof_df = pd.DataFrame(jee_prof_data)
    # print(jee_prof_df[:4])
    # jee_prof_df['_id'] = jee_prof_df['_id'].astype(str)
    jee_prof_output = process_prof_data(jee_prof_df, exam_type='jee')
    # print(jee_prof_output[:30])

   # Fetch NEET Proficiency Data
    neet_prof_data = db_client.get_prof_data(db_type='neet')
    if not neet_prof_data:
        print('No NEET Proficiency Data Available')
        return
    neet_prof_df = pd.DataFrame(neet_prof_data)
    neet_prof_df['studentId'] = neet_prof_df['studentId'].astype(str)
    neet_prof_output = process_prof_data(neet_prof_df, exam_type='neet')


if __name__ == '__main__':
    main()
