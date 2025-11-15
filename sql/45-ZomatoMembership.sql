/*
Zomato is planning to offer a premium membership to customers who have placed multiple orders in a single day.

Your task is to write a SQL to find those customers who have placed multiple orders in a single day at least once , total order value generate by those customers and order value generated only by those orders, display the results in ascending order of total order value.

 

Table: orders_zm (primary key : order_id)
+---------------+-------------+
| COLUMN_NAME   | DATA_TYPE   |
+---------------+-------------+
| customer_name | varchar(20) |
| order_date    | datetime    |
| order_id      | int         |
| order_value   | int         |
+---------------+-------------+

OUTPUT:
customer_name | total_order_value | order_value 
---------------+-------------------+-------------
 Mudit         |               780 |         550
 Rahul         |              1300 |        1150
(2 rows)
*/

with cte1 as (
select customer_name, sum(order_value) as order_value
FROM(
select customer_name, date(order_date) as order_day, sum(order_value) as order_value from orders_zm
group by customer_name, date(order_date)
having count(*) > 1
) t
group by customer_name
),
cte2 as (
select customer_name, sum(order_value) as total_order_value
from orders_zm
group by customer_name
)

select cte1.customer_name, cte2.total_order_value, cte1.order_value 
from cte1
inner join cte2
on cte1.customer_name = cte2.customer_name
order by cte2.total_order_value asc