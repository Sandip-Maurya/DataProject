import gspread
from datetime import datetime, timedelta


def update_eng_data(df_output, gs_obj, pd, ENGAGEMENT_TAB_NAME):    
    
    eng_ws = gs_obj.worksheet(ENGAGEMENT_TAB_NAME)

    gs_student_ids = eng_ws.col_values(1)
    gs_subjects = eng_ws.col_values(6)
    header_data = eng_ws.row_values(1)
    stud_subj_ids = [ student_id + subject for student_id, subject in zip(gs_student_ids, gs_subjects) ][1:]
    last_day = (datetime.today() - timedelta(days=1)).strftime('%d-%b-%y')
    eng_values = [[last_day]]

    for stud_subj_id in stud_subj_ids:
        eng_val = df_output.loc[stud_subj_id, 'Engagement (in Hours)']
        eng_val_list = [float(eng_val)]
        eng_values.append(eng_val_list)
      
    num_columns = len(eng_ws.row_values(1))  # Get no. of columns
    num_rows = len(eng_ws.col_values(1)) # Get no. of rows
    new_column_range = gspread.utils.rowcol_to_a1(1, num_columns + 1)  # First cell of the new column
    column_range = f"{new_column_range.split(':')[0]}:{new_column_range.split(':')[0][:-1]}{num_rows}"  # Create  column range (like G1:G121) as string
    
    eng_ws.update(eng_values, column_range)
    print(f'Engagement data updated for {last_day} on google sheet at {column_range}.')
