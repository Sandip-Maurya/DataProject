from config.config import SUBJECT_MAP

def process_jee_eng_df(jee_eng_df):
    jee_eng_df['subject'] = jee_eng_df['subjectId'].map(SUBJECT_MAP)
    jee_eng_df['student_subject_id'] = jee_eng_df['studentId'] + jee_eng_df['subject']
    jee_eng_df.drop(columns = ['_id', 'subjectId', 'studentId', 'subject'], inplace=True)
    jee_eng_dict = jee_eng_df.set_index('student_subject_id')['engagement'].to_dict()
    return jee_eng_dict

def process_neet_eng_df(neet_eng_df):
    neet_eng_df.replace({'subjectId': {'4': '5', '146': '5'}}, inplace=True)
    neet_eng_df['subject'] = neet_eng_df['subjectId'].map(SUBJECT_MAP)
    neet_eng_df['student_subject_id'] = neet_eng_df['studentId'] + neet_eng_df['subject']
    neet_eng_df.drop(columns = ['_id', 'subjectId', 'studentId', 'subject'], inplace=True)
    neet_eng_df = neet_eng_df.groupby(by='student_subject_id').sum()
    neet_eng_dict = neet_eng_df['engagement'].to_dict()
    return neet_eng_dict

def process_jee_prof_df(jee_prof_df):
    jee_prof_df = jee_prof_df.melt(id_vars=['studentId'], var_name='subject', value_name='proficiency')
    jee_prof_df['student_subject_id'] = jee_prof_df['studentId'] + jee_prof_df['subject']
    jee_prof_df.drop(columns = ['studentId', 'subject'], inplace=True)
    jee_prof_dict = jee_prof_df.set_index('student_subject_id')['proficiency'].to_dict()
    return jee_prof_dict

def process_neet_prof_df(neet_prof_df):
    neet_prof_df['Biology'] = (neet_prof_df['Botany'] + neet_prof_df['Zoology'])/2
    neet_prof_df.drop(columns = ['Botany', 'Zoology'], inplace=True)
    neet_prof_df = neet_prof_df.melt(id_vars=['studentId'], var_name='subject', value_name='proficiency')

    neet_prof_df['student_subject_id'] = neet_prof_df['studentId'] + neet_prof_df['subject']
    neet_prof_df.drop(columns = ['studentId', 'subject'], inplace=True)
    neet_prof_dict = neet_prof_df.set_index('student_subject_id')['proficiency'].to_dict()
    return neet_prof_dict
