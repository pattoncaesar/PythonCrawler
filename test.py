import requests

site = "https://query1.finance.yahoo.com/v7/finance/download/2330.TW?period1=0&period2=1549258857&interval=1d&events=history&crumb=hP2rOschxO0"
response = requests.get(site)
print(response)
from io import StringIO
import pandas as pd
df = pd.read_csv(StringIO(response.text))
print(df)

# import pickle
# with open('stock.pkl','wb') as f:
#     pickle.dump(df,f)