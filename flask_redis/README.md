# Flask-redis

This is a python3 example for a basic voting poll, using flask and redis.

```sh
docker pull redis:4-alpine
```

Start a redis container (non-permanent storage).

```sh
docker run --name redis-server -p 6379:6379 -d redis:4-alpine
```

If you want permanent storage use the next command.

```sh
docker run --name redis-server -v /vols4docker/redis4:/data -p 6379:6379 \
-d redis:4-alpine redis-server --appendonly yes
```

Now build the docker image for the app and run a container.

```sh
docker build --rm -t <name>:voting-app .
```

```sh
export REDISHOST=$(docker inspect -f '{{ .NetworkSettings.IPAddress }}' redis-server)
```

```sh
docker run --name voting-app -e REDISHOST="$REDISHOST" -e REDISPORT="6379" \
-d -p 8080:8080 <name>:voting-app
```

Check the images.

```sh
docker images
```

```txt
REPOSITORY              TAG                  IMAGE ID            CREATED             SIZE
aldenso                 voting-app           43568cd90e6b        9 seconds ago       114MB
redis                   4-alpine             d3117424aaee        3 weeks ago         27.1MB
```

Check the containers.

```sh
docker ps
```

```txt
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                    NAMES
e0be2bf286c2        aldenso:voting-app   "python /src/run.py"     9 seconds ago       Up 2 seconds        0.0.0.0:8080->8080/tcp   voting-app
74dc26569dd9        redis:4-alpine       "docker-entrypoint.s…"   7 minutes ago       Up 6 minutes        0.0.0.0:6379->6379/tcp   redis-server
```

Now let's check the service.

Get candidates.

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates -X GET
```

```json
{
  "message": "No candidates!"
}
```

Create a new candidate.

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates -X POST -d '{"name": "aldenso"}' -H "Content-Type: application/json"
```

```json
{
  "message": "created."
}
```

Get votes for the new candidate (default 0)

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates/name/aldenso -X GET
```

```json
{
  "votes": 0
}
```

Try to create an existing candidate.

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates -X POST -d '{"name": "aldenso"}' -H "Content-Type: application/json"
```

```json
{
  "error": "candidate already exists."
}
```

Create another candidate (an IT one :D).

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates -X POST -d '{"name": "pennywise"}' -H "Content-Type: application/json"
```

```json
{
  "message": "created."
}
```

Get all candidates info.

```sh
 curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates -X GET
```

```json
{
  "candidates": {
    "aldenso": {
      "votes": 0
    },
    "pennywise": {
      "votes": 0
    }
  }
}
```

Add votes for a candidate.

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates/name/aldenso -X PUT -H "Content-Type: application/json"  # several times
```

Try to add votes to a non-existing candidate.

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates/name/pennywis -X PUT -H "Content-Type: application/json"
```

```json
{
  "error": "candidate does not exists."
}
```

Add votes to the other candidate ("You'll float too")

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates/name/pennywise -X PUT -H "Content-Type: application/json"  # a couple of times
```

Get all candidates info updated.

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates -X GET
```

```json
{
  "candidates": {
    "aldenso": {
      "votes": 3
    },
    "pennywise": {
      "votes": 2
    }
  }
}
```

Check with your browser the template (http://<YOURIPADDRESS>:8080/index).

```sh
curl http://<YOURIPADDRESS>:8080/index
```

```html
<!DOCTYPE html>
<html lang="utf-8">
<head>
</head>
<body>
<h3>Flask Voting App</h3>


<h5>Simple app to query a redis db.</h5>

<p>Candidate - Votes</p>

<p>aldenso - 3</p>

<p>pennywise - 2</p>

</body>%
```


Now you can delete the candidates, and check no candidates exists anymore.

```sh
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates/name/pennywise -X DELETE
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates/name/aldenso -X DELETE
curl http://<YOURIPADDRESS>:8080/voting/api/v1/candidates -X GET
```

```json
{
  "message": "No candidates!"
}
```

check the app logs.

```sh
docker logs voting-app
```

```text
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
192.168.56.101 - - [01/Mar/2018 02:13:23] "GET /voting/api/v1/candidates HTTP/1.1" 200 -
192.168.56.101 - - [01/Mar/2018 02:13:50] "POST /voting/api/v1/candidates HTTP/1.1" 201 -
192.168.56.101 - - [01/Mar/2018 02:14:22] "GET /voting/api/v1/candidates/name/aldenso HTTP/1.1" 200 -
192.168.56.101 - - [01/Mar/2018 02:14:42] "GET /voting/api/v1/candidates HTTP/1.1" 200 -
192.168.56.101 - - [01/Mar/2018 02:15:18] "POST /voting/api/v1/candidates HTTP/1.1" 400 -
192.168.56.101 - - [01/Mar/2018 02:17:32] "POST /voting/api/v1/candidates HTTP/1.1" 201 -
192.168.56.101 - - [01/Mar/2018 02:17:48] "GET /voting/api/v1/candidates HTTP/1.1" 200 -
192.168.56.101 - - [01/Mar/2018 02:18:34] "PUT /voting/api/v1/candidates/name/aldenso HTTP/1.1" 204 -
192.168.56.101 - - [01/Mar/2018 02:18:35] "PUT /voting/api/v1/candidates/name/aldenso HTTP/1.1" 204 -
192.168.56.101 - - [01/Mar/2018 02:18:36] "PUT /voting/api/v1/candidates/name/aldenso HTTP/1.1" 204 -
192.168.56.101 - - [01/Mar/2018 02:18:53] "PUT /voting/api/v1/candidates/name/pennywis HTTP/1.1" 404 -
192.168.56.101 - - [01/Mar/2018 02:19:37] "PUT /voting/api/v1/candidates/name/pennywise HTTP/1.1" 204 -
192.168.56.101 - - [01/Mar/2018 02:19:38] "PUT /voting/api/v1/candidates/name/pennywise HTTP/1.1" 204 -
192.168.56.101 - - [01/Mar/2018 02:20:06] "GET /voting/api/v1/candidates HTTP/1.1" 200 -
192.168.56.101 - - [01/Mar/2018 02:20:24] "GET /index HTTP/1.1" 200 -
192.168.56.101 - - [01/Mar/2018 02:21:12] "DELETE /voting/api/v1/candidates/name/pennywise HTTP/1.1" 204 -
192.168.56.101 - - [01/Mar/2018 02:21:17] "DELETE /voting/api/v1/candidates/name/aldenso HTTP/1.1" 204 -
192.168.56.101 - - [01/Mar/2018 02:21:35] "GET /voting/api/v1/candidates HTTP/1.1" 200 -
```

Stop the containers.

```sh
docker stop voting-app redis-server
```
