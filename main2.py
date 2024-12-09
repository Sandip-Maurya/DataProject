from data_access.get_data import (
    get_jee_eng_data,
    get_neet_eng_data,
    get_jee_prof_data,
    get_neet_prof_data
)
from processing.process_data2 import (
    process_jee_eng_df,
    process_neet_eng_df 
)
from config.output_format import output_df
import pandas as pd 

jee_eng_data = get_jee_eng_data()
jee_eng_df = pd.DataFrame(jee_eng_data)
# print(jee_eng_df[:3])
output_df = process_jee_eng_df(jee_eng_df, output_df)


neet_eng_data = get_neet_eng_data()
neet_eng_df = pd.DataFrame(neet_eng_data)
output_df = process_neet_eng_df(neet_eng_df, output_df)
# print(output_df[:20])
# print(output_df[80:])

jee_prof_data = get_jee_prof_data()
jee_prof_df = pd.DataFrame(jee_prof_data)

neet_prof_data = get_neet_prof_data()
neet_prof_df = pd.DataFrame(neet_prof_data)
