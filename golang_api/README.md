# golang_api

Go language Rest API example, with a small docker image base (alpine).

For convenience we'll use the next example <https://github.com/aldenso/golang-examples/tree/master/gorilla>

It's very important to build the static binary like the following command.

```bash
CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-w' -o server .
```

```text
gorilla $ pwd
~/go/src/github.com/aldenso/golang-examples/gorilla

gorilla $ CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-w' -o server .

gorilla $ ls
handlers.go  main.go  README.md  router.go  server

gorilla $ ls -lrth
total 4.9M
-rw-r--r-- 1 aldenso aldenso 1.8K Sep 13 09:52 README.md
-rw-r--r-- 1 aldenso aldenso  530 Sep 13 09:52 router.go
-rw-r--r-- 1 aldenso aldenso  207 Sep 13 09:52 main.go
-rw-r--r-- 1 aldenso aldenso 2.3K Sep 13 09:52 handlers.go
-rwxr-xr-x 1 aldenso aldenso 4.9M Sep 17 21:54 server
```

The binary size is only 4.9MB, now move the binary to the path where you want the Dockerfile to be.

```text
gorilla $ mv server ~/github/docker-examples/golang_api
```

Pull the alpine image and see the size difference with other images in your docker host.

```text
golang_api $ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
centos              latest              328edcd84f1b        6 weeks ago         193MB

golang_api $ sudo docker pull alpine
Using default tag: latest
latest: Pulling from library/alpine
88286f41530e: Pull complete
Digest: sha256:f006ecbb824d87947d0b51ab8488634bf69fe4094959d935c0c103f4820a417d
Status: Downloaded newer image for alpine:latest

golang_api $ sudo docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
alpine              latest              76da55c8019d        4 days ago          3.97MB
centos              latest              328edcd84f1b        6 weeks ago         193MB
```

Create the Dockerfile.

```Dockerfile
golang_api $ cat Dockerfile
# Build binary with the following command
# CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-w' -o server .
FROM alpine
MAINTAINER aldenso@gmail.com
WORKDIR /app
COPY server /app/
ENTRYPOINT ["./server"]
```

Build the image.

```text
golang_api $ sudo docker build -t aldenso/golang_api .
Sending build context to Docker daemon  5.072MB
Step 1/5 : FROM alpine
 ---> 76da55c8019d
Step 2/5 : MAINTAINER aldenso@gmail.com
 ---> Running in 4c96c963d5e9
 ---> 6253a34293bf
Removing intermediate container 4c96c963d5e9
Step 3/5 : WORKDIR /app
 ---> f63ee2160132
Removing intermediate container a2f4370e047b
Step 4/5 : COPY server /app/
 ---> 5f4027033cc7
Step 5/5 : ENTRYPOINT ./server
 ---> Running in 7afe7c31b8a5
 ---> dd23a7caf5c6
Removing intermediate container 7afe7c31b8a5
Successfully built dd23a7caf5c6
Successfully tagged aldenso/golang_api:latest

golang_api $ sudo docker images
REPOSITORY           TAG                 IMAGE ID            CREATED              SIZE
aldenso/golang_api   latest              dd23a7caf5c6        About a minute ago   9.03MB
alpine               latest              76da55c8019d        4 days ago           3.97MB
centos               latest              328edcd84f1b        6 weeks ago          193MB
```

As you can see, the image size is only above 9MB, now run a container with the image and test it.

```text
golang_api $ sudo docker run --rm -p 8080:8080 aldenso/golang_api
golang_api $ curl http://localhost:8080
golang_api $ curl http://localhost:8080/api/user
null
golang_api $ curl http://localhost:8080/api/user -d '{"name": "aldenso"}' -X POST
golang_api $ curl http://localhost:8080/api/user -d '{"name": "Altair"}' -X POST
golang_api $ curl http://localhost:8080/api/user
[
    {
        "id": 0,
        "name": "aldenso",
        "created_at": "2017-09-18T02:22:58.886560709Z"
    },
    {
        "id": 1,
        "name": "Altair",
        "created_at": "2017-09-18T02:23:25.210770244Z"
    }
]

golang_api $ sudo docker ps
CONTAINER ID        IMAGE                COMMAND             CREATED             STATUS              PORTS                    NAMES
00f6e291d7a7        aldenso/golang_api   "./server"          4 minutes ago       Up 4 minutes        0.0.0.0:8080->8080/tcp   epic_engelbart

golang_api $ sudo docker logs epic_engelbart
172.17.0.1 - - [18/Sep/2017:02:22:02 +0000] "GET / HTTP/1.1" 404 0
172.17.0.1 - - [18/Sep/2017:02:22:14 +0000] "GET /api/user HTTP/1.1" 200 4
172.17.0.1 - - [18/Sep/2017:02:22:58 +0000] "POST /api/user HTTP/1.1" 201 0
172.17.0.1 - - [18/Sep/2017:02:23:25 +0000] "POST /api/user HTTP/1.1" 201 0
172.17.0.1 - - [18/Sep/2017:02:23:28 +0000] "GET /api/user HTTP/1.1" 200 225
172.17.0.1 - - [18/Sep/2017:02:24:53 +0000] "GET /api/user HTTP/1.1" 200 225
```

It works, now you can stop the container (CTRL + C).