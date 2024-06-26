import pandas as pd
import unittest

################### 1
gods = "dataset/greek_gods.csv"
godesses = "dataset/greek_godesses.csv"

df1 = pd.read_csv(gods)
df2 = pd.read_csv(godesses)

df_merged = pd.merge(df1, df2, on=['Domain', 'Symbol', 'Age'], how='outer')
# print(df_merged.head(11))

# df1.rename(columns={'God':'God/Goddess'}, inplace=True)
# df2.rename(columns={'Goddess':'God/Goddess'}, inplace=True)

df3 = pd.concat([df1, df2], axis=0)     # joins multiple df along rows or columns , if you don't rename it'll be same as df_merged
# print(df3.head(10))

################ 2

df4_1 = df3[df3['Age']>8000].sort_values(by='Age', ascending=False)
df4_2 = df3.query('Age>8000').sort_values(by='Age', ascending=False) 
# print(df4_1)

class TestClass(unittest.TestCase):
    def test_shape_verify(self):        # the test method name must start with test for test to run
        self.assertEqual(df4_1.shape, df4_2.shape)


# if __name__ == '__main__':
#     unittest.main()

############### 3

df5 = pd.merge(df1, df2, on='Domain', how='outer')
df5 = df5.groupby('Domain').mean('Age').reset_index()
df5['Age'] = df5['Age_x'].combine_first(df5['Age_y'])   # fills column with 1st column if nan fills with second column
# print(df5[['Domain','Age']])       # since domain is index it'll come

########## 4

df6 = df3
df6=df6[df6['Age']==df6['Age'].max()]           # .max() returns maximum value from column/columns
print(df6['Age'].values[0], end=" is age of ")
if 'NaN' not in df6['God'].values:              # .values gives direct values
    print(df6['God'].values[0], " the God.")
else:
    print(df6['Goddess'].values[0], " the Goddess")
    
########## 5

df1['Age_group'] = df1['Age'].apply(lambda y : 'Young' if y<5000 else ('Middle-aged' if (y>=5000 and y<=8000) else 'Old')) # .apply() takes every element from series/ndarray and apply required functyion on all elemens one by one
df2['Age_group'] = df2['Age'].apply(lambda y : 'Young' if y<5000 else ('Middle-aged' if (y>=5000 and y<=8000) else 'Old')) 
print(df1, df2, sep='\n')

######### 6
god_mean = df1['Age'].mean()
goddess_mean = df2['Age'].mean()
if god_mean<goddess_mean:
    print(f"God group seems to be older by an average of {abs(god_mean-goddess_mean)}")
else:
    print(f"Goddess group seems to be older by an average of {abs(god_mean-goddess_mean)} years.")
    
########### 7
print("### 7 ###")
df_gods=df1.rename(columns={'God':'God/Goddess'})
df_godesses=df2.rename(columns={'Goddess':'God/Goddess'})

df_merged = pd.concat([df_gods, df_godesses])

for index, rows in df_merged.iterrows():
    if rows['Age'] > 8000:
        print(rows['God/Goddess'])
        
########## 8
print("### 8 ###")
index_oldest = 0
index, oldest = 0, df_merged['Age'].iloc[[5]].values[0]
while index<len(df_merged):
    if (current_age := df_merged['Age'].iloc[[index]].values[0]) > oldest:
        index_oldest, oldest = index, current_age
    index+=1
print(f"The oldest {'god' if index_oldest<5 else 'goddess'} is {df_merged['God/Goddess'].iloc[[index_oldest]].values[0]}")