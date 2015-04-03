dockerfiles-centos7-python-flask-mariadb
========================================

CentOS 7 dockerfile for python app with flask linked with previously created mariadb container

Get Docker version

	# docker version

To build:

Copy the sources down and do the build-

	# docker build --rm -t <name>/flaskmariadb:centos7 .
	# docker build --rm -t aldenso/flaskmariadb:centos7 .

To run (if port 8080 is open on your host):

	# docker run -d -p 8080:8080 <name>/flaskmariadb:centos7
	# docker run -d --name=flaskmariadb -p 8080:8080 --link mariadb1:mariadb1 aldenso/flaskmariadb:centos7

or to assign a random port that maps to port 8080 on the container:

	# docker run -d -p 8080 <name>/flaskmariadb:centos7
	# docker run -d --name=flaskmariadb -p 8080 --link mariadb1:mariadb1 aldenso/flaskmariadb:centos7

To the port that the container is listening on:

	# docker ps

To test:

	# curl http://localhost:8080
	# curl http://$(docker inspect -f '{{.NetworkSettings.IPAddress}}' <containername>):8080

To view the logs

	# docker logs <containername>

To list containers

	# docker ps <containername>

To stop a running container

	# docker stop <containername>

To restart a running container

	# docker restart <containername>

To inspect the container

	# docker inspect <containername>

To inspect a specific resource from container (example: IP Address)

	# docker inspect -f '{{ .NetworkSettings.IPAddress }}' <containername>
