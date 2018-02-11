import os

basedir = os.path.abspath(os.path.dirname(__file__))

mydb_user = "testdb"
mydb_pwd = "myNewPass"
dbhostname = "mariadb1"
mydb = "testdb"
SQLALCHEMY_DATABASE_URI='mysql+pymysql://%s:%s@%s:3306/%s' % (mydb_user,
    mydb_pwd, dbhostname, mydb)
