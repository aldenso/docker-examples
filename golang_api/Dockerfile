# Build binary with the following command
# CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-w' -o server .
FROM alpine
MAINTAINER aldenso@gmail.com
WORKDIR /app
COPY server /app/
ENTRYPOINT ["./server"]
