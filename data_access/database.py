# data_access/database.py

from pymongo import MongoClient
from config.config import MONGODB_URI, JEE_DB, NEET_DB, STUDENT_TIME_TAKEN_COLLECTION, START_DATE, END_DATE

class DatabaseClient:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.jee_db = self.client[JEE_DB]
        self.neet_db = self.client[NEET_DB]
        self.collection = STUDENT_TIME_TAKEN_COLLECTION

    def get_eng_data(self, db_type='jee'):
        """
        Retrieves aggregated data from the specified database.

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

        cursor = db[self.collection].aggregate(eng_query)
        return list(cursor)

    def get_all_student_ids(self):
        """
        Retrieves all student IDs from the CSV file.

        :return: List of student IDs
        """
        import pandas as pd
        from config.config import CSV_FILE_PATH

        df = pd.read_csv(CSV_FILE_PATH)
        return df['_id'].astype(str).tolist()
