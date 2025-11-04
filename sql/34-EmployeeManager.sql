/*
You are given the table of employee details. Write an SQL to find details of employee with salary more than their manager salary but they joined the company after the manager joined.

Display employee name, salary and joining date along with their manager's salary and joining date, sort the output in ascending order of employee name.

Please note that manager id in the employee table referring to emp id of the same table.

 

Table: employee_manager
+--------------+-------------+
| COLUMN_NAME  | DATA_TYPE   |
+--------------+-------------+
| emp_id       | int         |
| emp_name     | varchar(10) |
| joining_date | date        |
| salary       | int         |
| manager_id   | int         |
+--------------+-------------+

Output:
emp_name | salary | joining_date | manager_salary | manager_joining_date 
----------+--------+--------------+----------------+----------------------
 Mohit    |  15000 | 2022-05-01   |          12000 | 2021-03-01
 Vikas    |  10000 | 2023-06-01   |           5000 | 2022-02-01
(2 rows)

*/

select e.emp_name,e.salary,e.joining_date,m.salary as manager_salary,m.joining_date as manager_joining_date from employee_manager e
inner join employee_manager m
on e.manager_id = m.emp_id
where e.salary > m.salary and e.joining_date > m.joining_date
order by e.emp_name asc