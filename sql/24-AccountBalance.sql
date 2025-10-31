/*
You are given a list of users and their opening account balance along with the transactions done by them. Write a SQL to calculate their account balance at the end of all the transactions. Please note that users can do transactions among themselves as well, display the output in ascending order of the final balance.

 


Table: users
+-----------------+-------------+
| COLUMN_NAME     | DATA_TYPE   |
+-----------------+-------------+
| user_id         | int         |
| username        | varchar(10) |
| opening_balance | int         |
+-----------------+-------------+

Table: transactions
+-------------+-----------+
| COLUMN_NAME | DATA_TYPE |
+-------------+-----------+
| id          | int       |
| from_userid | int       |
| to_userid   | int       |
| amount      | int       |
+-------------+-----------+

Output:

username | final_balance 
----------+---------------
 Ankit    |          2000
 Amit     |          2800
 Agam     |          7500
 Rahul    |         10200
(4 rows)

*/


with cte as (
select from_userid as user_id, -1*amount as trans from transactions
union all
select to_userid as user_id, amount as trans from transactions
union all
select user_id, opening_balance as trans from users
)

select u.username, sum(trans) as final_balance
from cte c
inner join users u
on c.user_id = u.user_id
group by u.username
order by final_balance
