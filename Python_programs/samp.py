import pandas as pd

df=pd.DataFrame({"A":[True,False,True],"B":[2,3,4]})
print(type(df.query('A=="True"')))