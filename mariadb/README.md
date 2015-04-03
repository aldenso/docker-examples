dockerfiles-mariadb
===================

Mariadb for Centos7

Setup

Check your Docker version

	# docker version

Perform the build

	# docker build --rm -t <name>/mariadb:centos7 .
	# docker build --rm -t aldenso/mariadb:centos7 .

Check the image out.

	# docker images

Launching MariaDB

Quick start (not recommended for production use):

	# docker run --name=mariadb -d -p 3306:3306 <yourname>/mariadb

Recommended start

To use a separate data volume for /var/lib/mysql (recommended, to allow image update without losing database contents):

Create a data volume container: (it doesn't matter what image you use here, we'll never run this container again; it's just here to reference the data volume)

	# docker run --name=mariadb-data -v /var/lib/mysql <name>/mariadb true
	# docker run --name=mariadb-data -v /var/lib/mysql aldenso/mariadb:centos7 true

Initialise it using a temporary one-time mariadb container:

	# docker run -rm --volumes-from=mariadb-data <name>/mariadb /config_mariadb.sh
	# docker run -rm --volumes-from=mariadb-data aldenso/mariadb:centos7 /config_mariadb.sh

And now create the new persistent mariadb container:

	# docker run --name=mariadb -d -p 3306:3306 --volumes-from=mariadb-data <name>/mariadb
	# docker run --name=mariadb1 -d -p 45000:3306 --volumes-from=mariadb-data aldenso/mariadb:centos7

Using your MariaDB container

Keep in mind the initial password set for mariadb is: mysqlPassword. Change it now:

	# mysqladmin --protocol=tcp -u testdb -pmysqlPassword password myNewPass
	# mysqladmin --protocol=tcp --port=45000 -u testdb -pmysqlPassword password myNewPass

Connecting to mariadb:

	# mysql --protocol=tcp -utestdb -pmyNewPass
	# mysql --protocol=tcp --port=45000 -utestdb -pmyNewPass

Create a sample table and test database:

use testdb

CREATE TABLE testmariadb (id int NOT NULL AUTO_INCREMENT, name VARCHAR(10), lastname VARCHAR(10), birth DATE, death DATE, PRIMARY KEY(id));

insert into testmariadb (name, lastname, birth, death) values ('Jhon', 'Doe', '1982-02-11', '2050-02-12');

show tables;

describe testmariadb;

select * from testmariadb;
