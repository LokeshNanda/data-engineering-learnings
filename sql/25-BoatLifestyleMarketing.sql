/*
boAt Lifestyle is focusing on influencer marketing to build and scale their brand. They want to partner with power creators for their upcoming campaigns. The creators should satisfy below conditions to qualify:

 

1- They should have 100k+ followers on at least 2 social media platforms and
2- They should have at least 50k+ views on their latest YouTube video.
Write an SQL to get creator id and name satisfying above conditions.

 

Table: creators
+-------------+-------------+
| COLUMN_NAME | DATA_TYPE   |
+-------------+-------------+
| id          | int         |
| name        | varchar(10) |
| followers   | int         |
| platform    | varchar(10) |
+-------------+-------------+
Table: youtube_videos
+--------------+-----------+
| COLUMN_NAME  | DATA_TYPE |
+--------------+-----------+
| id           | int       |
| creator_id   | int       |
| publish_date | date      |
| views        | int       |
+--------------+-----------+

Output:

id  | name  
-----+-------
 102 | Dhruv
 104 | Neha
 105 | Amit
(3 rows)

*/

with cte1 as (
select a.creator_id from(
select creator_id, views, row_number() over(partition by creator_id order by publish_date desc) as rn
from youtube_videos) a
where a.rn=1 and a.views > 50000
),
cte2 as (
select id, name
from creators
where followers > 100000
group by id, name
having count(*) >= 2
)

select cte2.id, cte2.name from cte2
inner join cte1
on cte2.id = cte1.creator_id