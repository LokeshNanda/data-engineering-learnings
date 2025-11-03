-- correlated subquery

/*
You are given the data of employees along with their salary and department. Write an SQL to find list of employees who have salary greater than average employee salary of the company.  However, while calculating the company average salary to compare with an employee salary do not consider salaries of that employee's department, display the output in ascending order of employee ids.

Table: employee
+-------------+-------------+
| COLUMN_NAME | DATA_TYPE   |
+-------------+-------------+
| emp_id      | int         |
| salary      | int         |
| department  | varchar(15) |
+-------------+-------------+

OUTPUT:

emp_id | salary | department  
--------+--------+-------------
    102 |  50000 | Analytics
    103 |  45000 | Engineering
    104 |  48000 | Engineering
    105 |  51000 | Engineering
    106 |  46000 | Science
    110 |  55000 | Engineering
    112 |  47000 | Analytics
    113 |  43000 | Engineering
(8 rows)

*/

select e1.emp_id, e1.salary, e1.department 
from employee e1
where e1.salary > ( select avg(e2.salary) from employee e2
	   where e1.department != e2.department
)
order by e1.emp_id