
# Restaurant Location Service ----------

up:
	docker-compose up --build

down:
	docker-compose down --volumes --remove-orphans

# API ----------------------------------

build-api:
	docker build -f Dockerfile.api . -t restaurant-location-api-image

up-api:
	docker run -d --name restaurant-location-api -p 80:80 restaurant-location-api-image

down-api:
	docker rm -f restaurant-location-api
