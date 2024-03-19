
# Pin Service ----------

up:
	docker-compose up --build

down:
	docker-compose down --volumes --remove-orphans

# API ----------------------------------

build-api:
	docker build -f Dockerfile.api . -t pin-api-image

up-api:
	docker run -d --name pin-api -p 80:80 pin-api-image

down-api:
	docker rm -f pin-api
