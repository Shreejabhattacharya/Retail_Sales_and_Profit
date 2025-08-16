#Python analysis here. Another sql analysis has also been done. But due to visualizations complication alternate python has been used.

import pymysql as sal
from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://root:M%40Durga%4012345@127.0.0.1:3306/testschema')
conn = engine.connect()
#load the data into the sql server using append option
#we will drop the table in the sql for writing the correct format. 
#Instead of "replace" we will use "Append"
df.to_sql('df_orders' , con=conn , index=False, if_exists ='append')
df.columns
!pip install pyodbc
import pyodbc


!pip install mysql.connector
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='M@Durga@12345',
    database='testschema'  
)
#find top 10 highest revenue genrating products

query = "SELECT * FROM df_orders;"  
df = pd.read_sql(query, conn)
conn.close()

print(df.head(10))

#import pandas as pd
df['order_date'] = pd.to_datetime(df['order_date'])
df['order_year'] = df['order_date'].dt.year
df['order_month'] = df['order_date'].dt.month
df['order_year_month'] = df['order_date'].dt.to_period('M').astype(str)

print(df.head(10))

import matplotlib.pyplot as plt
import seaborn as sns
#!pip install plotly.express
import plotly.express as px

top_products = (
    df.groupby('product_id')['sale_price']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

print(top_products)

plt.figure(figsize=(8,6))
sns.barplot(data=top_products, x='sale_price', y='product_id', palette='viridis')
plt.title('Top 10 Products by Sales')
plt.xlabel('Total Sales')
plt.ylabel('Product ID')
plt.show()

#find top 5 highest selling products in  each region
#select distinct regions from df_orders;

region_product_sales = (
    df.groupby(['region', 'product_id'])['sale_price']
    .sum()
    .reset_index()
)

# For top 5 per region
region_product_sales['rank'] = region_product_sales.groupby('region')['sale_price'].rank(ascending=False, method='first')

top5_per_region = region_product_sales[region_product_sales['rank'] <= 5]

print(top5_per_region)

plt.figure(figsize=(12,8))
sns.barplot(data=top5_per_region, x='sale_price', y='product_id', hue='region')
plt.title('Top 5 Products in Each Region')
plt.show()

#month over month growth comparisn for sales for year : jan 2022 and jan 2023
sales_by_month_year = (
    df.groupby(['order_year', 'order_month'])['sale_price']
    .sum()
    .reset_index()
)

sales_pivot = sales_by_month_year.pivot(index='order_month', columns='order_year', values='sale_price')
print(sales_pivot)

sales_pivot.plot(kind='line', figsize=(10,6), marker='o')
plt.title('Month-over-Month Sales Comparison (2022 vs 2023)')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.legend(title='Year')
plt.show()

#For each category which month had highest sale?
category_month_sales = (
    df.groupby(['category', 'order_year_month'])['sale_price']
    .sum()
    .reset_index()
)

idx = category_month_sales.groupby('category')['sale_price'].idxmax()
best_months = category_month_sales.loc[idx]

print(best_months)

plt.figure(figsize=(10,6))
sns.barplot(data=best_months, x='sale_price', y='category', hue='order_year_month')
plt.title('Best Sales Month for Each Category')
plt.show()

#which subcategory had the highest growth by profit in 2023 compared to 2022?
profit_by_subcategory_year = (
    df.groupby(['sub_category', 'order_year'])['profit']
    .sum()
    .reset_index()
)

profit_pivot = profit_by_subcategory_year.pivot(index='sub_category', columns='order_year', values='profit')
profit_pivot = profit_pivot.fillna(0)

profit_pivot['growth_pct'] = (profit_pivot[2023] - profit_pivot[2022]) / profit_pivot[2022].replace(0, 1) * 100

profit_pivot = profit_pivot.sort_values('growth_pct', ascending=False)
print(profit_pivot)


print(profit_pivot.head(1))


top_growth = profit_pivot.head(10).reset_index()

plt.figure(figsize=(10,6))
sns.barplot(data=top_growth, x='growth_pct', y='sub_category', palette='magma')
plt.title('Top 10 Subcategories by Profit Growth (2023 vs 2022)')
plt.xlabel('Profit Growth (%)')
plt.show()

