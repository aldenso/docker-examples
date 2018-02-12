# docker-python-flask

Docker example for python3 app with flask.

Get Docker version.

```sh
docker version
```

To build:

Copy the sources down and do the build.

```sh
docker build --rm -t <name>/flask:flask .
# docker build --rm -t aldenso/flask:flask .
```

To run (if port 8080 is open on your host):

```sh
docker run -d -p 8080:8080 <name>/flask:flask
# docker run -d -p 8080:8080 aldenso/flask:flask
```

or to assign a random port that maps to port 8080 on the container:

```sh
docker run -d -p 8080 <name>/flask:flask
# docker run -d -p 8080 aldenso/flask:flask
```

Check the container:

```sh
docker ps
```

To test:

```sh
curl http://localhost:8080
curl http://$(docker inspect -f '{{.NetworkSettings.IPAddress}}' <containername>):8080
# curl http://localhost:<HostPort>
```

To view the logs.

```sh
docker logs <containername>
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
