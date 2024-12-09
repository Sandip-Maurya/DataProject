from pymongo import MongoClient
from data_access.get_query import get_eng_query, get_prof_query
from config.config import (
    MONGODB_URI,
    JEE_DB,
    NEET_DB,
    ENGAGEMENT_COLLECTION,
    PROFICIENCY_COLLECTION
)

# Access DataBase and Collection
client = MongoClient(MONGODB_URI)
jee_db = client[JEE_DB]
neet_db = client[NEET_DB]


# Make Query
eng_query = get_eng_query()
prof_query = get_prof_query()


# Get Enagagement Data
def get_jee_eng_data():
    cursor = jee_db[ENGAGEMENT_COLLECTION].aggregate(eng_query)
    jee_eng_data = list(cursor)
    return jee_eng_data

def get_neet_eng_data():
    cursor = neet_db[ENGAGEMENT_COLLECTION].aggregate(eng_query)
    neet_eng_data = list(cursor)
    return neet_eng_data

# Get Proficiency Data
def get_jee_prof_data():
    cursor = jee_db[PROFICIENCY_COLLECTION].aggregate(prof_query)
    jee_prof_data = list(cursor)
    return jee_prof_data

def get_neet_prof_data():
    cursor = neet_db[PROFICIENCY_COLLECTION].aggregate(prof_query)
    neet_prof_data = list(cursor)
    return neet_prof_data
