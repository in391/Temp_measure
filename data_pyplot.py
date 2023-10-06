import plotly.express as px
import pandas as pd
from datetime import datetime
import pytz

df = pd.read_csv("./data/data_temp_humid_4.csv", header=None)
df = df.rename(columns={0:'Time', 1:'Temp', 2:'Humid'})
df['Time'] = [datetime.fromtimestamp(x, tz=pytz.timezone('Japan')) for x in df['Time']]
df.head()

fig = px.line(df, x = 'Time', y = ['Temp', 'Humid'], title='Temp,Humid/Time Graph')
fig.show()