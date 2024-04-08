import pandas as pd

gods = "dataset/greek_gods.csv"
godesses = "dataset/greek_godesses.csv"



df1 = pd.read_csv(gods)
df2 = pd.read_csv(godesses)

df_merged = pd.merge(df1, df2, on=['Domain', 'Symbol', 'Age'], how='outer')

print(df_merged.head(11))

df1.rename(columns={'God':'name'}, inplace=True)
df2.rename(columns={'Goddess':'name'}, inplace=True)
df3 = pd.concat([df1, df2], axis=0)

print(df3.head(10))