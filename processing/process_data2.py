import pandas as pd
from config.config import SUBJECT_MAP, JEE_SUBJECT_IDS, NEET_OP_IDS


def process_jee_eng_df(jee_eng_df, output_df):
    jee_eng_df['subject'] = jee_eng_df['subjectId'].map(SUBJECT_MAP)
    jee_eng_df['student_subject_id'] = jee_eng_df['studentId'] + jee_eng_df['subject']
    jee_eng_df.drop(columns = ['_id', 'subjectId', 'studentId', 'subject'], inplace=True)
    engagement_dict = jee_eng_df.set_index('student_subject_id')['engagement'].to_dict()
    output_df.replace({'engagement': engagement_dict}, inplace=True)

    # print(output_df[:20])
    return output_df

def process_neet_eng_df(neet_eng_df, output_df):
    neet_eng_df.replace({'subjectId': {'4': '5', '146': '5'}}, inplace=True)
    neet_eng_df['subject'] = neet_eng_df['subjectId'].map(SUBJECT_MAP)
    neet_eng_df['student_subject_id'] = neet_eng_df['studentId'] + neet_eng_df['subject']
    neet_eng_df.drop(columns = ['_id', 'subjectId', 'studentId', 'subject'], inplace=True)
    neet_eng_df = neet_eng_df.groupby(by='student_subject_id').sum()
    engagement_dict = neet_eng_df['engagement'].to_dict()
    output_df.replace({'engagement': engagement_dict}, inplace=True)

    print(engagement_dict)
    # print(output_df[:20])
    return output_df

def process_jee_prof_df():
    return 

def process_neet_prof_df():
    return 
