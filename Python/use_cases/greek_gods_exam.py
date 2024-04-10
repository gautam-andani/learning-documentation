import pandas as pd
import unittest

################### 1
gods = "dataset/greek_gods.csv"
godesses = "dataset/greek_godesses.csv"

df1 = pd.read_csv(gods)
df2 = pd.read_csv(godesses)

df_merged = pd.merge(df1, df2, on=['Domain', 'Symbol', 'Age'], how='outer')
# print(df_merged.head(11))

df1.rename(columns={'God':'God/Goddess'}, inplace=True)
df2.rename(columns={'Goddess':'God/Goddess'}, inplace=True)

df3 = pd.concat([df1, df2], axis=0)     # joins multiple df along rows or columns , if you don't rename it'll be same as df_merged
# print(df3.head(10))

################ 2

df4_1 = df3[df3['Age']>8000].sort_values(by='Age', ascending=False)
df4_2 = df3.query('Age>8000').sort_values(by='Age', ascending=False) 
print(df4_1)

class TestClass(unittest.TestCase):
    def test_shape_verify(self):        # the test method name must start with test for test to run
        self.assertEqual(df4_1.shape, df4_2.shape)


if __name__ == '__main__':
    unittest.main()

############### 3

