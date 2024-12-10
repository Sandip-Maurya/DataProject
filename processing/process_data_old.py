# processing/process_data.py

import pandas as pd
from config.config import SUBJECT_MAP, JEE_SUBJECT_IDS, NEET_OP_IDS

def load_student_details(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df

def process_eng_data(df_students, df_exam, exam_type='jee'):
    """
    Processes exam data and aggregates time spent by students per subject.

    :param df_students: DataFrame containing student details
    :param df_exam: DataFrame containing exam data
    :param exam_type: Type of exam ('jee' or 'neet')
    :return: DataFrame with aggregated data
    """
    if exam_type.lower() == 'jee':
        subject_ids = JEE_SUBJECT_IDS
    elif exam_type.lower() == 'neet':
        subject_ids = NEET_OP_IDS
    else:
        raise ValueError("exam_type must be either 'jee' or 'neet'")

    df_output = pd.DataFrame(columns=[
        'Student ID', 'Class', 'Exam', 'First Name', 'Last Name',
        'Subject', 'Engagement (in Minutes)', 'Engagement (in Hours)'
    ])
    op_idx = 0

    exam_ids = df_students[df_students['examName'].str.contains(exam_type.upper())]['studentId'].astype(str).tolist()

    for s_id in exam_ids:
        student = df_students[df_students['studentId'].astype(str) == s_id].iloc[0]
        firstName = student['firstName']
        lastName = student['lastName']
        studentClassName = student['studentClassName']
        examName = student['examName']
        studentId = student['studentId']

        for subjectId in subject_ids:
            df_exam_temp = df_exam[
                (df_exam['studentId'] == studentId) &
                (df_exam['subjectId'] == subjectId)
            ]
            if df_exam_temp.empty:
                timeSpentInMinutes = 0
            else:
                timeSpentInMinutes = df_exam_temp['timeSpentInMinutes'].sum()

            subject = SUBJECT_MAP.get(subjectId, 'Unknown')
            df_output.loc[op_idx] = [
                s_id, studentClassName, examName, firstName, lastName,
                subject, round(timeSpentInMinutes, 2), round(timeSpentInMinutes / 60, 2)
            ]
            op_idx += 1

    return df_output

def process_prof_data(df_exam, exam_type='jee'):
    df_output = pd.melt(df_exam, id_vars=['studentId'], var_name='Subject', value_name='Proficiency')
    return df_output