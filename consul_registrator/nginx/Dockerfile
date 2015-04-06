FROM nginx:1.7

#Install Curl
RUN apt-get update -qq && apt-get -y install curl
RUN mkdir /src
RUN rm -f /etc/nginx/conf.d/*

#Default Variables
ENV CONSUL consul://172.17.42.1:8500
ENV CONSUL_URL 172.17.42.1:8500

ADD . /src

EXPOSE 8080

CMD ["bash", "/src/start.sh"]
