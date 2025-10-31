/*
Given two tables: income_tax_dates and users, write a query to identify users who either filed their income tax returns late or completely skipped filing for certain financial years.

A return is considered late if the return_file_date is after the file_due_date.
A return is considered missed if there is no entry for the user in the users table for a given financial year (i.e., the user did not file at all).
Your task is to generate a list of users along with the financial year for which they either filed late or missed filing, and also include a comment column specifying whether it is a 'late return' or 'missed'. The result should be sorted by financial year in ascending order.

 

Table: income_tax_dates
+-----------------+------------+
| COLUMN_NAME     | DATA_TYPE  |
+-----------------+------------+
| financial_year  | varchar(4) |
| file_start_date | date       |
| file_due_date   | date       |
+-----------------+------------+
Table: users_itr
+------------------+------------+
| COLUMN_NAME      | DATA_TYPE  |
+------------------+------------+
| user_id          | int        |
| financial_year   | varchar(4) |
| return_file_date | date       |
+------------------+------------+

OUTPUT:
+---------+----------------+-------------+
| user_id | financial_year | comment     |
+---------+----------------+-------------+
|       1 | FY21           | late return |
|       1 | FY22           | missed      |
|       2 | FY23           | late return |
+---------+----------------+-------------+
*/

with cte as (
select u.user_id, it.financial_year,it.file_due_date   from users_itr u
cross join income_tax_dates it
group by u.user_id, it.financial_year,it.file_due_date
)

select c.user_id, c.financial_year,
CASE WHEN c.file_due_date < u.return_file_date THEN 'late return' else 'missing' END as comment
from cte c
left join users_itr u
on c.user_id = u.user_id and c.financial_year = u.financial_year
where u.return_file_date > c.file_due_date or u.return_file_date is null
order by c.financial_year asc