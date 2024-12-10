# config/config.py

import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI')
JEE_DB = 'qandi_analytics_jee'
NEET_DB = 'qandi_analytics_neet'
STUDENT_TIME_TAKEN_COLLECTION = 'averageStudentTimeTaken'
STUDENT_ANALYTICS_COLLECTION = 'studentAnalytics'
ENGAGEMENT_COLLECTION = 'averageStudentTimeTaken'
PROFICIENCY_COLLECTION = 'studentAnalytics'
INSTITUTE_ID = '65fa893f337a920f7e7f731f'

# Date Range Configuration
# START_DATE = datetime(2024, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
# END_DATE = datetime(2024, 11, 30, 0, 0, 0, tzinfo=timezone.utc)
utc_today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
last_day = utc_today - timedelta(days=1)
START_DATE = last_day
END_DATE = utc_today
TOTAL_SECONDS_IN_MINUTES = 60

# Subject Mapping
SUBJECT_MAP = {
    '1': 'Mathematics',
    '2': 'Physics',
    '3': 'Chemistry',
    '4': 'Botany',
    '146': 'Zoology',
    '5': 'Biology'
}

# Subject IDs
JEE_SUBJECT_IDS = ['2', '3', '1']
NEET_SUBJECT_IDS = ['2', '3', '4', '146']
NEET_OP_IDS = ['2', '3', '5']

# Shiva Students Paths
SSS_CSV_PATH = '/root/Projects/OfficeProj/DataProject/input/SSS_users.csv'
OUTPUT_FORMAT_PATH  = '/root/Projects/OfficeProj/DataProject/input/output_template.csv'

# Google Sheet Configuration
GOOGLE_CRED_PATH = '/root/Projects/OfficeProj/DataProject/input/qandi_cred.json'
SHEET_NAME = 'SSS - Proficiency & Engagement Data Day Wise'
ENGAGEMENT_TAB_NAME = 'Engagement'
PROFICIENCY_TAB_NAME = 'Proficiency'