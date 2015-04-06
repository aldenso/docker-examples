SINGLE HOST CONSUL & REGISTRATOR + NGINX LOADBALANCER
=====================================================

We are going to use consul and registrator in a single host, then we are going
to create one nginx container to work as loadbalancer for several apps

Download the consul image

		# docker pull progrium/consul:latest

Download the registrator image

		# docker pull progrium/registrator:latest
	
Create the consul container

		# docker run -p 8400:8400 -p 8500:8500 -p 8600:8600 -p 53:53/udp --name consul -h <hostname> progrium/consul:latest -server -bootstrap &

Check consul

		# curl localhost:8500/v1/catalog/nodes
		# docker logs consul

Create registrator container

		# docker run -d -v /var/run/docker.sock:/tmp/docker.sock --name registrator -h <hostname> progrium/registrator:latest -internal consul://$DOCKER_IP:8500
	where $DOCKER_IP=172.17.42.1

Check registrator

		# docker logs registrator
		must say something like this
		2015/04/06 04:22:06 registrator: Using consul registry backend at consul://172.17.42.1:8500
		2015/04/06 04:22:06 registrator v5 listening for Docker events...
		2015/04/06 04:22:06 registrator: ignored: ae0215f64b47 no published ports
		2015/04/06 04:22:06 registrator: added: 3728d4899918 centos:consul:8301
		2015/04/06 04:22:06 registrator: added: 3728d4899918 centos:consul:8302
		2015/04/06 04:22:07 registrator: added: 3728d4899918 centos:consul:8400
		2015/04/06 04:22:07 registrator: added: 3728d4899918 centos:consul:8500
		2015/04/06 04:22:07 registrator: added: 3728d4899918 centos:consul:8600
		2015/04/06 04:22:07 registrator: added: 3728d4899918 centos:consul:8300
		2015/04/06 04:22:07 registrator: added: 3728d4899918 centos:consul:8301:udp
		2015/04/06 04:22:07 registrator: added: 3728d4899918 centos:consul:8302:udp
		2015/04/06 04:22:07 registrator: added: 3728d4899918 centos:consul:53:udp

Start a few app previously created (https://github.com/aldenso/docker-examples/tree/master/flaskapp), but giving some envs for registrator to work with consul.
		# docker run -d --name flaskapp1 -p 8080 -e "SERVICE_NAME=flaskapp" -e "SERVICE_TAGS=master" aldenso/flaskapp
		# docker run -d --name flaskapp2 -p 8080 -e "SERVICE_NAME=flaskapp" -e "SERVICE_TAGS=master" aldenso/flaskapp
		# docker run -d --name flaskapp3 -p 8080 -e "SERVICE_NAME=flaskapp" -e "SERVICE_TAGS=backup" aldenso/flaskapp

Check registrator

		# docker logs registrator
		2015/04/06 04:32:40 registrator: added: 94738187a8c8 94738187a8c8:flaskapp1:8080
		2015/04/06 04:32:40 registrator: added: 6bf303d76755 6bf303d76755:flaskapp2:8080
		2015/04/06 04:32:51 registrator: added: 9989bfafb83f 9989bfafb83f:flaskapp3:8080
		# curl http://172.17.42.1:8500/v1/catalog/services
		{"consul":[],"flaskapp":["master","backup"]}
		# curl http://172.17.42.1:8500/v1/catalog/service/flaskapp | python -m json.tool
		[
    		{
        		"Address": "172.17.0.16",
        		"Node": "94738187a8c8",
        		"ServiceAddress": "",
        		"ServiceID": "94738187a8c8:flaskapp1:8080",
        		"ServiceName": "flaskapp",
        		"ServicePort": 8080,
        		"ServiceTags": [
            		"master"
        		]
    		},
    		{
        		"Address": "172.17.0.17",
        		"Node": "6bf303d76755",
        		"ServiceAddress": "",
        		"ServiceID": "6bf303d76755:flaskapp2:8080",
        		"ServiceName": "flaskapp",
        		"ServicePort": 8080,
        		"ServiceTags": [
            		"master"
        		]
    		},
    		{
        		"Address": "172.17.0.18",
        		"Node": "9989bfafb83f",
        		"ServiceAddress": "",
        		"ServiceID": "9989bfafb83f:flaskapp3:8080",
        		"ServiceName": "flaskapp",
        		"ServicePort": 8080,
        		"ServiceTags": [
            		"backup"
        		]
    		}
		]
		# dig @172.17.42.1 flaskapp.service.consul
		# dig @172.17.42.1 -t SRV flaskapp.service.consul

OK, now our apps are registered in consul

Before we start working in the nginx container, we are going to setup our system,
because we are going to use consul-template in nginx, to recognize the changes of
states in servers involved in load balancing

First we install and set golang in our host (my case is centOS) to compile the 
consul-template

		# yum install golang
		# mkdir ~/go
		# vim ~/.bash_profile
		GOPATH=~/go
		EXPORT GOPATH
		# . ~/.bash_profile

Download the consul template from source

		# cd /tmp
		# git clone https://github.com/hashicorp/consul-template.git
		# cd consul-template
		# make
		# cp bin/consul-template $PATH_TO_DOCKERFILE; cd $PATH_TO_DOCKERFILE

Now let's test the template against our nginx template (service.ctmpl)

		# ./consul-template -consul 172.17.42.1:8500 -template service.ctmpl:/tmp/consul.result -dry -once > /tmp/consul.result
		# cat /tmp/consul.result
		upstream flaskapp {
  			least_conn;
  				server 172.17.0.17:8080 max_fails=3 fail_timeout=60 weight=1;
  				server 172.17.0.16:8080 max_fails=3 fail_timeout=60 weight=1;
  				server 172.17.0.18:8080 max_fails=3 fail_timeout=60 weight=1;
  
		}

		server {
  			listen 8080 default_server;

  			charset utf-8;

  			location / {
   				proxy_pass http://flaskapp;
  			}
		}

We are ready to build the nginx image

		# docker build -t <name>/nginxlbflaskapp .

Start the nginx container

		# docker run -p 8080:8080 -d --name nginxlb1 -v $PATH_TO_DOCKERFILE/service.ctmpl:/templates/service.ctmpl <name>/nginxlbflaskapp

Verify the service is running in the container

		# docker logs nginxlb1

Check the load balancer is working

		# curl http://172.17.42.1:8080
		Hello from Docker container: 9989bfafb83f
		# curl http://172.17.42.1:8080
		Hello from Docker container: 6bf303d76755
		# curl http://172.17.42.1:8080
		Hello from Docker container: 94738187a8c8
		or
		# curl http://localhost:8080
		Hello from Docker container: 9989bfafb83f

It's alive... now you see three different apps containers responding
