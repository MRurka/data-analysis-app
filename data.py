import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# from authentication import auth

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)


def get_data(collection, field, user_uid):
    
    # GET DATA
    db = firestore.client()
    life_areas = db.collection(collection).where(field, '==', user_uid).stream()

    # CREATE DATAFRAME<
    df = pd.DataFrame()

    # FILL DATAFRAME
    for entry in life_areas:
        new_entry = entry.to_dict()
        new_row = pd.DataFrame.from_records(new_entry, index=[0])
        df = pd.concat([df, new_row], axis=0)
    
    df = df.replace({
        'Bad'  : 1,
        'Meh'  : 2,
        'Okay' : 3,
        'Good' : 4,
        'Great': 5
    })

    df['creation_date'] = pd.to_datetime(df['creation_date'], format='%A, %B %d, %Y at %I:%M %p')

    return df


def df_convert_to_datetime(dataframe, column_name):
    dataframe[column_name] = pd.to_datetime(df['Date'], format='%A, %B %d, %Y at %I:%M %p')
    return dataframe


def convert_moods_to_numbers(dataframe):
    dataframe = dataframe.replace({
    'Bad'  : 1,
    'Meh'  : 2,
    'Okay' : 3,
    'Good' : 4,
    'Great': 5
    })
    return dataframe


# Dataframe for Areas
# df_areas = []
# for i in df.loc[:,'H - Health Phys' : 'H - Life Overall']:
#     df_areas.append(i)

# print(df)


