#!pip install kaggle
import kaggle
#!kaggle datasets download ankitbansal06/retail-orders -f orders.csv

#import data and check for null values(part of data cleaning)
import pandas as pd
df = pd.read_csv('orders.csv')
df.head(20)
df['Ship Mode'].unique()

#ideally the column names have to be in lowercase and no spaces, "underscore"
df.rename(columns={'Order Id':'order_id', 'City':'city'})#individual change of names
df.columns = df.columns.str.lower()
df.columns =df.columns.str.replace(' ','_')
df.head(6)

#deriving the discount value from the percentage given
df['discount']=df['list_price']*df['discount_percent']*.01
df['sale_price']=df['list_price']-df['discount']
df['profit']=df['sale_price']-df['cost_price']
df.head(5)

#Drop unnecessary columns
df.dtypes
#change the datatype from obj to date
df['order_date']=pd.to_datetime(df['order_date'],format="%Y-%m-%d")
df.drop(columns=['list_price','cost_price','discount_percent'],inplace=True)
