# utils/output_format.py

from config.config import OUTPUT_FORMAT_PATH
import pandas as pd

output_df = pd.read_csv(OUTPUT_FORMAT_PATH)
output_df.set_index('student_subject_id', inplace=True)
