import pandas as pd

from google_sheets import google_sheet_data

# Dataframe for All Data Columns
df = google_sheet_data

# Convert Date Strings to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%A, %B %d, %Y at %I:%M %p')

# Replace String Values w/ Numbers
df = df.replace({
    'Bad'  : 1,
    'Meh'  : 2,
    'Okay' : 3,
    'Good' : 4,
    'Great': 5
})

# Dataframe for Areas
df_areas = []
for i in df.loc[:,'H - Health Phys' : 'H - Life Overall']:
    df_areas.append(i)
