# Server

# Data Base:

before starting the server, create a database and execute the file "create_tables"\
command: psql -h host -U username -d myDataBase -a -f create_tables
then create and fill in the environment variables\
dbpassword, dbuser, dbhost, dbport, database_name\
or change the defaults in the file "Server\constants.py" to what you want

# Running:

go to repository root folder\
python3 Server\src\main.py
