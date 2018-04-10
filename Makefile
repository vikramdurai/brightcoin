# install:
	# docker build -t brightcoin .

# test_peer:
	# docker run -d -p 8080:8080 brightcoin
	# docker run -d -p 8081:8080 brightcoin

run:
	docker-compose up -d

stop:
	# docker stop `docker ps -aq`
	docker-compose down