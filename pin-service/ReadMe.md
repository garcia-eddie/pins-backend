# Setup Instructions
Create an .env file with the variables below: \
PGADMIN_EMAIL=test@test.com \
PGADMIN_PASSWORD=pgpass \
DB_HOST=pin-db \
DB_NAME=pin_db \
DB_USER=devuser \
DB_PASS=devpass \
DB_PORT=5432

# Running The Application
Navigate to the project's root folder and run the command ***make up***. This will run the docker-compose file and set things up.

The api should be accessible through ***localhost:5050***.