import pandas as pd 
df=pd.read_csv("sample_energy.csv",parse_dates=['timestamp'])
print(df.head(3))
df['year']=df['timestamp'].dt.year
print(df.head(3))
df['hour']=df['timestamp'].dt.hour
df['day']=df['timestamp'].dt.day_name()
print(df.tail(5))
print(df.head(20))
df_groupbyhour=df.df.groupbyhour(['timestamp'].dt.hour) ['usage_kwh'].sum()
df_groupbyDayname=df.df_groupby(df['timestamp'].dt.name) ['usage_kwh'].max()
print(df_groupbyhour)
print(df_groupbyDayname)