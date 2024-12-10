# Import all modules and scripts

from data_access.get_data import (
    get_jee_eng_data,
    get_neet_eng_data,
    get_jee_prof_data,
    get_neet_prof_data
)
from processing.process_data import (
    process_jee_eng_df,
    process_neet_eng_df,
    process_jee_prof_df,
    process_neet_prof_df
)
from config.config import (
    OUTPUT_FORMAT_PATH,
    SHEET_NAME,
    ENGAGEMENT_TAB_NAME,
    PROFICIENCY_TAB_NAME
)
from output.update_data import (
    update_eng_data,
    update_prof_data
)
from config.gs_auth import get_gs_obj
import pandas as pd 
print('Imports done')

# Load output format csv as pandas dataframe
output_df = pd.read_csv(OUTPUT_FORMAT_PATH)


# Get JEE Eng Data and Process it
jee_eng_data = get_jee_eng_data()
jee_eng_df = pd.DataFrame(jee_eng_data)
jee_eng_dict = process_jee_eng_df(jee_eng_df)

# Get NEET Eng Data and Process it
neet_eng_data = get_neet_eng_data()
neet_eng_df = pd.DataFrame(neet_eng_data)
neet_eng_dict = process_neet_eng_df(neet_eng_df)

# Update Engagement Data in output_df
eng_dict = jee_eng_dict | neet_eng_dict
output_df['engagement'] = output_df['student_subject_id'].map(eng_dict)
output_df['engagement'] = output_df['engagement'].fillna(0.0)
output_df['engagement'] = output_df['engagement'].round(2)
print('Engagement data fetched and processed')

# Get JEE Prof Data and Process it
jee_prof_data = get_jee_prof_data()
jee_prof_df = pd.DataFrame(jee_prof_data)
jee_prof_dict = process_jee_prof_df(jee_prof_df)

# Get NEET Prof Data and Process it
neet_prof_data = get_neet_prof_data()
neet_prof_df = pd.DataFrame(neet_prof_data)
neet_prof_dict = process_neet_prof_df(neet_prof_df)

# Update Proficiency Data in output_df
prof_dict = jee_prof_dict | neet_prof_dict
output_df['proficiency'] = output_df['student_subject_id'].map(prof_dict)
output_df['proficiency'] = output_df['proficiency'].fillna(0.0)
output_df['proficiency'] = output_df['proficiency'].round(2)
print('Proficiency data fetched and processed')

# Export the data to google sheet
output_df.set_index('student_subject_id', inplace=True)
gs_obj = get_gs_obj()
update_eng_data(output_df, gs_obj)
update_prof_data(output_df, gs_obj)
