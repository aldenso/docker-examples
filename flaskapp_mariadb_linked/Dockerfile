FROM centos:centos7

RUN yum -y update; yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install python-pip; yum clean all
RUN yum -y install gcc; yum clean all
RUN yum -y install python-devel; yum clean all
RUN yum -y install mysql-devel; yum clean all

ADD . /src

RUN cd /src; pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "/src/run.py"]
