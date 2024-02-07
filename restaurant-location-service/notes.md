# Notes:
Below are the things I have learned or practiced while working on this project.
## Docker
Essentially, docker is useful for creating contained environments in which an application can exist. These contained environments, called containers, contain the application and any dependencies needed for it to run. More info here:
https://www.docker.com/resources/what-container/



## PostgreSQL

I went with Postgres because it is the database I am most familiar with, and also because its a relational database and I think the data that I will store will fit nicely.

I did consider using a graph database, like Neo4j, to store restaurant details but I'm not very familiar with graph databases, and the data I'm storing do not have any inherent relationships with each other. Graph databases might be useful when I need to recommend restaurants between friends.


## PostGIS
PostGIS is a Postgres extension that adds geometry tools.

Since we want to represent our points as points on Earth, and not just arbitrary points that lack a reference object, we need to use SRID 4326 with PostGIS. In a nutshell, SRID 4326 tells PostGIS that our points should be treated as coordinate points on Earth.

PostGIS was chosen as it provides support for coordinates, with the option to support spatial indexes later should we need to partition the database to improve range query performance. More info here:
http://postgis.net/workshops/postgis-intro/indexing.html