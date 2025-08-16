select * from df_orders;
show databases;
use testschema;

drop table df_orders;

create table df_orders(
order_id int primary key,
order_date date,
ship_mode varchar(20),
segment varchar(20),
country varchar(20),
city varchar(20),
state varchar(20),
postal_code varchar(20),
region varchar(20),
category varchar(20),
sub_category varchar(20),
product_id varchar(50),
quantity int,
discount decimal(7,2),
sale_price decimal(7,2),
profit decimal(7,2)
);

#find top 10 highest revenue genrating products
select product_id,sum(sale_price) as sales
from df_orders
group by product_id
order by sales desc;

#find top 5 highest selling products in  each region

#select distinct regions from df_orders;
with cte as (
select region, product_id,sum(sale_price) as sales
from df_orders
group by region,product_id)
select * from(
select *
,row_number()over(partition by region order by sales desc) as rn
from cte) A
where rn<=5;
#order by region,sales desc

#month over month growth comparisn for sales for year : jan 2022 and jan 2023
SELECT 
  order_month,
  SUM(CASE WHEN order_year = 2022 THEN sales ELSE 0 END) AS sales_2022,
  SUM(CASE WHEN order_year = 2023 THEN sales ELSE 0 END) AS sales_2023
FROM (
  SELECT 
    YEAR(order_date) AS order_year,
    MONTH(order_date) AS order_month,
    SUM(sale_price) AS sales
  FROM df_orders
  GROUP BY YEAR(order_date), MONTH(order_date)
) AS cte
GROUP BY order_month
ORDER BY order_month;

#For each category which month had highest sale?
with cte as(
select category, format(order_date,'%Y%m') as order_year_month
, sum(sale_price) as sales
from df_orders
group by category, format(order_date,'%Y%m')
order by category, format(order_date,'%Y%m')
)
select * from
(
select *,
row_number() over(partition by category order by sales desc) as rn
from cte
) a
where rn=1;


#which subcategory had the highest growth by profit in 2023 compared to 2022?

with cte as(
select sub_category,year(order_date) as order_year,
sum(sale_price) as sales
from df_orders
group by sub_category,year(order_date)
	)
    , cte2 as(
select sub_category
, SUM(CASE WHEN order_year = 2022 THEN sales ELSE 0 END) AS sales_2022
, SUM(CASE WHEN order_year = 2023 THEN sales ELSE 0 END) AS sales_2023
FROM cte
group by sub_category
)
select * 
,(sales_2023 - sales_2022)*100/sales_2022
from cte2
order by (sales_2023 - sales_2022)*100/sales_2022 desc
limit 1;


#Alternative approach

WITH cte AS (
  SELECT 
    sub_category,
    YEAR(order_date) AS order_year,
    SUM(profit) AS total_profit
  FROM df_orders
  GROUP BY sub_category, YEAR(order_date)
)
SELECT 
  sub_category,
  SUM(CASE WHEN order_year = 2022 THEN total_profit ELSE 0 END) AS profit_2022,
  SUM(CASE WHEN order_year = 2023 THEN total_profit ELSE 0 END) AS profit_2023,
  (SUM(CASE WHEN order_year = 2023 THEN total_profit ELSE 0 END) -
   SUM(CASE WHEN order_year = 2022 THEN total_profit ELSE 0 END)) AS profit_growth
FROM cte
GROUP BY sub_category
ORDER BY profit_growth DESC
LIMIT 1;
  
  