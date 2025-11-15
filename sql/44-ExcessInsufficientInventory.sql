/*
Suppose you are a data analyst working for Flipkart. Your task is to identify excess and insufficient inventory at various Flipkart warehouses in terms of no of units and cost.  Excess inventory is when inventory levels are greater than inventory targets else its insufficient inventory.

Write an SQL to derive excess/insufficient Inventory volume and value in cost for each location as well as at overall company level, display the results in ascending order of location id.

 

Table: inventory
+------------------+-----------+
| COLUMN_NAME      | DATA_TYPE |
+------------------+-----------+
| inventory_level  | int       |
| inventory_target | int       |
| location_id      | int       |
| product_id       | int       |
+------------------+-----------+
Table: products
+-------------+--------------+
| COLUMN_NAME | DATA_TYPE    |
+-------------+--------------+
| product_id  | int          |
| unit_cost   | decimal(5,2) |
+-------------+--------------+

Output:
location_id | excess_insufficient_qty | excess_insufficient_value 
-------------+-------------------------+---------------------------
 1           |                      25 |                   1347.50
 2           |                     -25 |                  -1420.00
 3           |                      20 |                   1180.00
 4           |                     -12 |                   -600.00
 Overall     |                       8 |                    507.50
(5 rows)
*/


with cte as (select location_id, sum(inventory_level-inventory_target) as excess_insufficient_qty,
sum((inventory_level-inventory_target)* p.unit_cost) as excess_insufficient_value from inventory i
inner join products p
on i.product_id = p.product_id
group by location_id
order by location_id asc
)

select cast(location_id AS TEXT),excess_insufficient_qty,excess_insufficient_value from cte
union all
select 'overall', sum(excess_insufficient_qty), sum(excess_insufficient_value)
from cte