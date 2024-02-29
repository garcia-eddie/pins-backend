# Notes:
Below are the things I have learned or practiced while working on this project.
## Docker
[Docker](https://www.docker.com/resources/what-container/) is useful for creating contained environments in which an application can exist. These contained environments, called containers, contain the application and any dependencies needed for it to run. For our restaurant location service, we use two containers: an api container **restaurant-location-api** and a database container **restaurant-location-db**.

Instead of having to build and run each part of the restaurant location service separately, we can use [docker-compose](https://docs.docker.com/compose/) to build and run both the api and the database at once. For this, we use the command **docker compose up --build** and our containers will start up. 

Our containers communicate with each other via the [user-defined bridge network](https://docs.docker.com/network/#user-defined-networks) **restaurant-location-net**. Bridge networks allow containers to identify each other by name, meaning that between containers on the **restaurant-location-net**, containers wanting to connect to **restaurant-location-db** will specify the host to be **retaurant-location-db** as opposed to localhost. 

If we want to access our containers from outside **restaurant-location-net**, we need to map the ports the containers use internally to ports that can be accessed externally. For example, our **restaurant-location-api** uses port 80 internally, and we map that to port 80 externally. This lets us locally access the api at port 80 through **localhost:80/**.

Our **restaurant-location-api** requires that **restaurant-location-db** has finished setting up. Currently, we use SqlAlchemy to setup the tables, which means that **restaurant-location-db** needs to be up and running before SqlAlchemy can do its thing in the **restaurant-location-api** container. To check that **restaurant-location-db** is up, we make use of a [healthcheck](https://docs.docker.com/compose/compose-file/05-services/#healthcheck) in our docker-compose file. The healthcheck runs the [pg_isready](https://www.postgresql.org/docs/current/app-pg-isready.html) command to check the status of the database within the container. Meanwhile, **restaurant-location-api** specifies this dependency via [depends_on](https://docs.docker.com/compose/compose-file/05-services/#depends_on), with the condition that **restaurant-location-db** is healthy.


## PostgreSQL
Postgres is a relational database that uses primary-secondary replication and supports several partitioning strategies. The main goal of this project is to simulate several workload scenarios and fine-tune Postgres to fufill the workload needs.

What motivated me to use Postgres specifically was the [PostGIS](https://postgis.net) extension, which adds support for geospatial data types called [Geometries](http://postgis.net/workshops/postgis-intro/geometries.html). PostGIS has a geometry type called [ST_Point](https://postgis.net/docs/ST_Point.html), which can store coordinate values in the form (long, lat). 

When creating points in PostGIS, it is important to specify that the points are following the [WGS 84 Spatial Reference System](https://gisgeography.com/wgs84-world-geodetic-system/). We do this by specifying the Spatial Reference Identifier (SRID) parameter to 4326, the ID for WGS 84, when creating a point using PostGIS' ST_Point.


## FastAPI
Coming Soon.
