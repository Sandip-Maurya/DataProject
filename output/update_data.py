import gspread
from datetime import datetime, timedelta
from config.config import (
    ENGAGEMENT_TAB_NAME,
    PROFICIENCY_TAB_NAME
)

last_day = (datetime.today() - timedelta(days=1)).strftime('%d-%b-%y')


def update_eng_data(output_df, gs_obj):    
    try:
        eng_ws = gs_obj.worksheet(ENGAGEMENT_TAB_NAME)

        gs_student_ids = eng_ws.col_values(1)
        gs_subjects = eng_ws.col_values(6)
        header_data = eng_ws.row_values(1)
        student_subject_ids = [ student_id + subject for student_id, subject in zip(gs_student_ids, gs_subjects) ][1:]
        eng_values = [[last_day]]

        for student_subject_id in student_subject_ids:
            eng_val = output_df.loc[student_subject_id, 'engagement']
            eng_val_list = [float(eng_val)]
            eng_values.append(eng_val_list)
        
        num_columns = len(header_data)  # Get no. of columns
        num_rows = len(gs_student_ids) # Get no. of rows
        new_column_range = gspread.utils.rowcol_to_a1(1, num_columns + 1)  # First cell of the new column
        column_range = f"{new_column_range.split(':')[0]}:{new_column_range.split(':')[0][:-1]}{num_rows}"  # Create  column range (like G1:G121) as string
        
        eng_ws.update(eng_values, column_range)
        print(f'Engagement data updated for {last_day} on google sheet at {column_range}.')
        return True
    except Exception as e:
        print(f'Some error occurred in updating Engagement data. The error is: {e}')
        return False
    

def update_prof_data(output_df, gs_obj):    
    try:
        prof_ws = gs_obj.worksheet(PROFICIENCY_TAB_NAME)

        gs_student_ids = prof_ws.col_values(1)
        gs_subjects = prof_ws.col_values(6)
        header_data = prof_ws.row_values(1)
        student_subject_ids = [ student_id + subject for student_id, subject in zip(gs_student_ids, gs_subjects) ][1:]
        prof_values = [[last_day]]

        for student_subject_id in student_subject_ids:
            prof_val = output_df.loc[student_subject_id, 'proficiency']
            prof_val_list = [float(prof_val)]
            prof_values.append(prof_val_list)
        num_columns = len(header_data)  # Get no. of columns
        num_rows = len(gs_student_ids) # Get no. of rows
        new_column_range = gspread.utils.rowcol_to_a1(1, num_columns + 1)  # First cell of the new column
        column_range = f"{new_column_range.split(':')[0]}:{new_column_range.split(':')[0][:-1]}{num_rows}"  # Create  column range (like G1:G121) as string

        prof_ws.update(prof_values, column_range)
        print(f'Proficiency data updated for {last_day} on google sheet at {column_range}.')
        return True
    except Exception as e:
        print(f'Some error occurred in updating Proficiency data. The error is: {e}')
        return False
