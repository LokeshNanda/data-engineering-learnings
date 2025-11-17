/*
You are given a history of credit card transaction data for the people of India across cities. Write an SQL to find percentage contribution of spends by females in each city.  Round the percentage to 2 decimal places. Display city, total spend , female spend and female contribution in ascending order of city.

Table: credit_card_transactions
+------------------+-------------+
| COLUMN_NAME      | DATA_TYPE   |
+------------------+-------------+
| amount           | int         |
| card_type        | varchar(10) |
| city             | varchar(10) |
| gender           | varchar(1)  |
| transaction_date | date        |
| transaction_id   | int         |
+------------------+-------------+

city    | total_spend | female_spend | female_contribution 
-----------+-------------+--------------+---------------------
 Bengaluru |        3450 |          300 |                8.70
 Delhi     |        1630 |         1430 |               87.73
 Mumbai    |        4150 |         4150 |              100.00
(3 rows)

*/

-- with cte as (
-- select city, sum(amount) as total_spend from credit_card_transactions
-- group by city
-- ),
-- cte2 as (
-- select city, sum(amount) as female_spend from credit_card_transactions
-- where gender = 'F'
-- group by city
-- )

-- select t.city, t.total_spend, f.female_spend, ROUND((female_spend * 1.0)/t.total_spend * 100,2) as female_contribution
-- from cte t
-- inner join cte2 f
-- on t.city = f.city
-- order by t.city asc


--

select city, SUM(CASE when gender = 'F' then amount else 0 end) as female_spend,
ROUND(SUM(CASE when gender = 'F' then amount else 0 end)*1.0/sum(amount)*100,2) as female_contribution
from credit_card_transactions
group by city
order by city asc
