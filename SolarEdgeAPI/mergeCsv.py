import pandas as pd


#files = ['./2055689/2055689-daily.csv','./1816420/1816420-daily.csv']


# df = pd.merge(['./2055689/2055689-daily.csv', './1816420/1816420-daily.csv'],
#               on='date', how='outer', left_index=False, right_index=False)

# df = pd.merge(pd.read_csv('./2055689/2055689-daily.csv'), pd.read_csv('./1816420/1816420-daily.csv'),
#               on='date', how='outer', left_index=False, right_index=False,)

df = pd.concat([pd.read_csv(csv_name) for csv_name in ['./2055689/2055689-daily.csv', './1816420/1816420-daily.csv']], axis = 1)

df = pd.concat([pd.read_csv(csv_name) for csv_name in ['./2055689/2055689-daily.csv', './1816420/1816420-daily.csv']])


print(df.columns)

for column in df.columns:
    if 'Unnamed' in column:
        df.drop(column, axis=1, inplace=True)

print(df.columns)
df.fillna(0)
df.to_csv('testing.csv', index=False)
