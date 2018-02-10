dockerfiles-mariadb
===================

Mariadb for Centos7

Setup

Check your Docker version

```sh
docker version
```

Perform the build

```sh
docker build --rm -t <name>/mariadb:centos7 .
# docker build --rm -t aldenso/mariadb:centos7 .
```

Check the image out.

```sh
docker images
```

Launching MariaDB

Quick start (not recommended for production use):

```sh
docker run --name=mariadb -d -p 3306:3306 <yourname>/mariadb:centos7
```

Recommended start

To use a separate data volume for /var/lib/mysql (recommended, to allow image update without losing database contents):

Create a data volume container: (it doesn't matter what image you use here, we'll never run this container again; it's just here to reference the data volume)

```sh
docker run --name=mariadb-data -v /var/lib/mysql <name>/mariadb:centos7 true
# docker run --name=mariadb-data -v /var/lib/mysql aldenso/mariadb:centos7 true
```

or if you already have an active /var/lib/mysql and don't want to mix it, create another dir and assign it.

```sh
mkdir -p /vols4docker/mariadb
docker run --name=mariadb-data -v /vols4docker/mariadb:/var/lib/mysql \
<name>/mariadb:centos7 true
```

Initialise it using a temporary one-time mariadb container:

```sh
docker run --rm --volumes-from=mariadb-data <name>/mariadb:centos7 /config_mariadb.sh
# docker run --rm --volumes-from=mariadb-data aldenso/mariadb:centos7 /config_mariadb.sh
```

And now create the new persistent mariadb container:

```sh
docker run --name=mariadb -d -p 3306:3306 --volumes-from=mariadb-data \
<name>/mariadb:centos7
# docker run --name=mariadb1 -d -p 45000:3306 --volumes-from=mariadb-data \ aldenso/mariadb:centos7
```

Using your MariaDB container

Keep in mind the initial password set for mariadb is: mysqlPassword. Change it now:

```sh
mysqladmin --protocol=tcp -u testdb -pmysqlPassword password myNewPass
# mysqladmin --protocol=tcp --port=45000 -u testdb -pmysqlPassword password myNewPass
```

Connecting to mariadb:

```sh
mysql --protocol=tcp -utestdb -pmyNewPass
# mysql --protocol=tcp --port=45000 -utestdb -pmyNewPass
```

Create a sample table and test database:

```sh
use testdb

CREATE TABLE testmariadb (id int NOT NULL AUTO_INCREMENT, name VARCHAR(10), lastname VARCHAR(10), birth DATE, death DATE, PRIMARY KEY(id));

insert into testmariadb (name, lastname, birth, death) values ('Jhon', 'Doe', '1982-02-11', '2050-02-12');

show tables;

describe testmariadb;

select * from testmariadb;
```

Example output when running your MariaDB container.

```sql
MariaDB [(none)]> use testdb
Database changed
MariaDB [testdb]> CREATE TABLE testmariadb (id int NOT NULL AUTO_INCREMENT, name VARCHAR(10), lastname VARCHAR(10), birth DATE, death DATE, PRIMARY KEY(id));
Query OK, 0 rows affected (0.33 sec)

MariaDB [testdb]> insert into testmariadb (name, lastname, birth, death) values ('Jhon', 'Doe', '1982-02-11', '2050-02-12');
Query OK, 1 row affected (0.11 sec)

MariaDB [testdb]> show tables;
+------------------+
| Tables_in_testdb |
+------------------+
| testmariadb      |
+------------------+
1 row in set (0.01 sec)

MariaDB [testdb]> describe testmariadb;
+----------+-------------+------+-----+---------+----------------+
| Field    | Type        | Null | Key | Default | Extra          |
+----------+-------------+------+-----+---------+----------------+
| id       | int(11)     | NO   | PRI | NULL    | auto_increment |
| name     | varchar(10) | YES  |     | NULL    |                |
| lastname | varchar(10) | YES  |     | NULL    |                |
| birth    | date        | YES  |     | NULL    |                |
| death    | date        | YES  |     | NULL    |                |
+----------+-------------+------+-----+---------+----------------+
5 rows in set (0.05 sec)

MariaDB [testdb]> select * from testmariadb;
+----+------+----------+------------+------------+
| id | name | lastname | birth      | death      |
+----+------+----------+------------+------------+
|  1 | Jhon | Doe      | 1982-02-11 | 2050-02-12 |
+----+------+----------+------------+------------+
1 row in set (0.01 sec)
```
