import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from dateutil import tz

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def remove_timezone(timestamp):
    date_without_timezone = timestamp
    # Convert to date
    date_without_timezone = pd.to_datetime(date_without_timezone)
    # Remove +01:00
    date_without_timezone = date_without_timezone.strftime('%Y-%m-%d %H:%M:%S')
    # -> '2019-02-21 15:31:37'
    return date_without_timezone


def convert_datetime_timezones(timestamp):
    # Auto-detect zones:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    # utc = datetime.utcnow()
    utc = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    # Tell the datetime object that it's in UTC time zone since 
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)
    # Convert time zone
    local_datetime = utc.astimezone(to_zone)
    local_datetime = local_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return local_datetime


def utc_to_local(timestamp):
    new_date = convert_datetime_timezones(remove_timezone(timestamp))
    return new_date


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
    for timestamp in df['creation_date']:
        # Generate proper date (new date)
        new_date = utc_to_local(timestamp)
        # Replace original date with new date
        df = df.replace(timestamp, new_date)

    # Sort by Date
    df = df.sort_values(by=['creation_date'])

    # Reset Index
    df = df.reset_index(drop=True)

    return df


def create_areas_df(dataframe):

    # Create dataframe
    df_areas = []

    # Fill dataframe with area columns
    for i in dataframe.loc[:,'area_score_career' : 'area_score_social']:
        df_areas.append(i)

    return df_areas


# # For testing purposes
# pd.set_option("display.max_columns", None)
# data = get_data('life_areas', 'created_by', 'Z6vMdScziWY3ciTdqgfoU29Bwpc2')
# print(data)
