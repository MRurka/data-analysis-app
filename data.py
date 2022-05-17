import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def get_data(collection, field, user_uid):
    
    # Get Data from Firebase
    db = firestore.client()
    life_areas = db.collection(collection).where(field, '==', user_uid).stream()

    # Create dataframe
    df = pd.DataFrame()

    # Fill the dataframe
    for entry in life_areas:
        new_entry = entry.to_dict()
        new_row = pd.DataFrame.from_records(new_entry, index=[0])
        df = pd.concat([df, new_row], axis=0)
    
    # Replace string with numbers
    df = df.replace({
        'Bad'  : 1,
        'Meh'  : 2,
        'Okay' : 3,
        'Good' : 4,
        'Great': 5
    })

    # Format date
    df['creation_date'] = pd.to_datetime(df['creation_date'], format='%A, %B %d, %Y at %I:%M %p')

    # Reset the dataframes Index
    df = df.reset_index(drop=True)

    return df


def create_areas_df(dataframe):

    # Create dataframe
    df_areas = []

    # Fill dataframe with area columns
    for i in dataframe.loc[:,'area_score_career' : 'area_score_social']:
        df_areas.append(i)

    return df_areas
