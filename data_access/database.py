# data_access/database.py

from pymongo import MongoClient
from config.config import (
    MONGODB_URI,
    JEE_DB,
    NEET_DB,
    STUDENT_TIME_TAKEN_COLLECTION,
    STUDENT_ANALYTICS_COLLECTION,
    INSTITUTE_ID,
    START_DATE,
    END_DATE,
    CSV_FILE_PATH
)
import pandas as pd

class DatabaseClient:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.jee_db = self.client[JEE_DB]
        self.neet_db = self.client[NEET_DB]
        self.eng_collection = STUDENT_TIME_TAKEN_COLLECTION
        self.prof_collection = STUDENT_ANALYTICS_COLLECTION

    def get_eng_data(self, db_type='jee'):
        """
        Retrieves aggregated engagement data from the specified database.

        :param db_type: Type of exam ('jee' or 'neet')
        :return: List of aggregated records
        """
        if db_type.lower() == 'jee':
            db = self.jee_db
        elif db_type.lower() == 'neet':
            db = self.neet_db
        else:
            raise ValueError("db_type must be either 'jee' or 'neet'")

        eng_query = [
            {
                '$match': {
                    'testDate': {
                        '$gte': START_DATE,
                        '$lt': END_DATE
                    },
                    'studentId': {
                        '$in': self.get_all_student_ids()
                    }
                }
            },
            {
                '$project': {
                    'studentId': 1,
                    'subjectId': 1,
                    'timeSpentInMinutes': {
                        '$divide': ['$totalTimeTaken', 60]
                    },
                    'timeSpentInHours': {
                        '$divide': ['$totalTimeTaken', 3600]
                    }
                }
            }
        ]

        cursor = db[self.eng_collection].aggregate(eng_query)
        return list(cursor)

    def get_prof_data(self, db_type='jee'):
        """
        Retrieves aggregated proficiency data from the specified database.

        :param db_type: Type of exam ('jee' or 'neet')
        :return: List of aggregated proficiency records
        """
        if db_type.lower() == 'jee':
            db = self.jee_db
        elif db_type.lower() == 'neet':
            db = self.neet_db
        else:
            raise ValueError("db_type must be either 'jee' or 'neet'")

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

        cursor = db[self.prof_collection].aggregate(prof_query)
        return list(cursor)

    def get_all_student_ids(self):
        """
        Retrieves all student IDs from the CSV file.

        :return: List of student IDs
        """
        df = pd.read_csv(CSV_FILE_PATH)
        return df['studentId'].astype(str).tolist()
