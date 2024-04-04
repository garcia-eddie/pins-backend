
# APP ########################################################################

up:
	docker-compose -f docker-compose.yml up --build

down:
	docker-compose -f docker-compose.yml down --volumes --remove-orphans


# Testing ########################################################################

test-up:
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

test-down:
	docker-compose -f docker-compose.test.yml down --volumes --remove-orphans

# API ##############################################################################

build-api:
	docker build -f Dockerfile.api . -t pin-api-image

up-api:
	docker run -d --name pin-api -p 80:80 pin-api-image

down-api:
	docker rm -f pin-api
