/*
Flipkart an ecommerce company wants to find out its top most selling product by quantity in each category. In case of a tie when quantities sold are same for more than 1 product, then we need to give preference to the product with higher sales value.
Display category and product in output with category in ascending order. 

Table: orders
+-------------+-------------+
| COLUMN_NAME | DATA_TYPE   |
+-------------+-------------+
| category    | varchar(10) |
| order_id    | int         |
| product_id  | varchar(20) |
| quantity    | int         |
| unit_price  | int         |
+-------------+-------------+

-- Output

category  |  product_id   
-----------+---------------
 Footwear  | floaters-3421
 Furniture | Table-3421
*/

with cte as ( 
select  category, product_id, sum(unit_price * quantity) as tot_sales, sum(quantity) as quantity_sold from orders
group by category, product_id
  )

select t.category, t.product_id from(
select category, product_id, row_number() over(partition by category order by quantity_sold desc,tot_sales desc) as rnk
from cte ) t
where t.rnk = 1