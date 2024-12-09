from config.config import (
    SSS_CSV_PATH,
    INSTITUTE_ID, 
    START_DATE, 
    END_DATE
)
import pandas as pd

student_df = pd.read_csv(SSS_CSV_PATH)
STUDENT_IDS = student_df.loc[:, 'studentId'].to_list()

def get_eng_query():

    eng_query = [
        {
            '$match': {
                'testDate': {
                    '$gte': START_DATE,
                    '$lt': END_DATE
                },
                'studentId': {
                    '$in': STUDENT_IDS
                }
            }
        },
        {
            '$project': {
                'studentId': 1,
                'subjectId': 1,
                'engagement': {
                    '$divide': ['$totalTimeTaken', 3600]
                }
            }
        }
    ]
    return eng_query


def get_prof_query():

    prof_query = [
        {
            '$match': {
                'instituteId': INSTITUTE_ID
            }
        },
        {
            '$project': {
                'subjects': {
                    '$arrayToObject': {
                        '$map': {
                            'input': '$subjects',
                            'as': 'subject',
                            'in': {
                                'k': '$$subject.name',
                                'v': '$$subject.proficiency'
                            }
                        }
                    }
                }
            }
        },
        {
            '$replaceRoot': {
                'newRoot': {
                    '$mergeObjects': [
                        '$$ROOT',
                        '$subjects'
                    ]
                }
            }
        },
        {
            '$addFields': {
                'studentId': {
                    '$toString': '$_id'
                }
            }
        },
        {
            '$project': {
                'subjects': 0,
                '_id':0
            }
        }
    ]
    return prof_query