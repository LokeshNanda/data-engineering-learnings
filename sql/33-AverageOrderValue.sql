/*
Write an SQL query to determine the transaction date with the lowest average order value (AOV) among all dates recorded in the transaction table. Display the transaction date, its corresponding AOV, and the difference between the AOV for that date and the highest AOV for any day in the dataset. Round the result to 2 decimal places.

 

Table: transactions_aov 
+--------------------+--------------+
| COLUMN_NAME        | DATA_TYPE    |
+--------------------+--------------+
| order_id           | int          |
| transaction_amount | decimal(5,2) |
| transaction_date   | date         |
| user_id            | int          |
+--------------------+--------------+

Output:
transaction_date |  aov  | diff_from_highest_aov 
------------------+-------+-----------------------
 2024-02-26       | 30.00 |                103.33
(1 row)

*/

with cte as (
select transaction_date, avg(transaction_amount) as aov from transactions_aov
group by transaction_date
),
cte1 as(
select *,row_number() OVER(order by aov) as rn, max(aov) OVER() as highest_aov
from cte
)

select transaction_date, ROUND(aov,2) as aov, ROUND(highest_aov-aov,2) as diff_from_highest_aov from cte1
where rn=1
