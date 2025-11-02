/*

You are given the details of employees of a new startup. Write an SQL query to retrieve number of Software Engineers , Data Professionals and Managers in the team to separate columns. Below are the rules to identify them using Job Title. 

 

1- Software Engineers  :  The title should starts with “Software”

2- Data Professionals :  The title should starts with “Data”

3- Managers : The title should contain "Manager"

 

Tables: Employees
+-------------+-------------+
| COLUMN_NAME | DATA_TYPE   |
+-------------+-------------+
| EmployeeID  | int         |
| Name        | varchar(20) |
| JoinDate    | date        |
| JobTitle    | varchar(20) |
+-------------+-------------+

software_engineers | data_professionals | managers 
--------------------+--------------------+----------
                  9 |                  3 |        3
(1 row)

*/

select 
sum(case when starts_with(jobTitle, 'Software') then 1 else 0 end) as software_engineers,
sum(case when starts_with(jobTitle, 'Data') then 1 else 0 end) as data_professionals,
sum(CASE when jobTitle ~ 'Manager' then 1 else 0 end) as managers
from employees; 