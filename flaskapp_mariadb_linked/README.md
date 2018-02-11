# dockerfiles-python-flask-mariadb

Docker example app using Alpine python image, with python3 and flask, linked with previously created mariadb container [mariadb example](https://github.com/aldenso/docker-examples/tree/master/mariadb).

Get Docker version.

```sh
docker version
```

To build:

Copy the sources down and run the build.

```sh
docker build --rm -t <name>/flaskmariadb:flaskmariadb .
# docker build --rm -t aldenso/flaskmariadb:flaskmariadb .
```

To run a container (if port 8080 is open on your host):

```sh
docker run -d -p 8080:8080 --link mariadb:mariadb1 <name>/flaskmariadb:flaskmariadb
# docker run -d --name=flaskmariadb -p 8080:8080 --link mariadb:mariadb1 \
# aldenso/flaskmariadb:flaskmariadb
```

or to assign a random port that maps to port 8080 on the container:

```sh
docker run -d -p 8080 --link mariadb:mariadb1 <name>/flaskmariadb:flaskmariadb
# docker run -d --name=flaskmariadb -p 8080 --link mariadb1:mariadb1 \
# aldenso/flaskmariadb:flaskmariadb
```

To the port that the container is listening on:

```sh
docker ps
```

To test:

```sh
curl http://localhost:8080
curl "http://$(docker inspect -f '{{.NetworkSettings.IPAddress}}' <containername>):8080"
```

Output:

```txt
<!DOCTYPE html>
<html lang="utf-8">
<head>
</head>
<body>
<h3>Flask App</h3>


<h5>Simple app to query a Database in Docker.</h5>



<p>Name - Lastname - Birth - Death</p>

<p>Jhon - Doe - 1982-02-11 - 2050-02-12</p>


</body>%
```

To view the logs.

```sh
docker logs <containername>
```

To list containers.

```sh
docker ps <containername>
```

To stop a running container.

```sh
docker stop <containername>
```

To restart a running container.

```sh
docker restart <containername>
```

To inspect the container.

```sh
docker inspect <containername>
```

To inspect a specific resource from container (example: IP Address).

```sh
docker inspect -f '{{ .NetworkSettings.IPAddress }}' <containername>
```
