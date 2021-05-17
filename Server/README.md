# Server

# Database preparation:

Chat server requires tables in the database to store messages and users. To create necessary tables for the server - apply the create_tables.sql script in any PostgreSQL client to your database.

To configure credential for the server, set  the specific environment variables:
* dbhost: host of your PostgreSQL instance,
* dbport: port of your PostgreSQL instance,
* database_name: name of your database, that you used in the previous step
* dbpassword: password for dbuser
* dbuser: user for with read/write acces for created tables to the specific database

or change the defaults in the file "Server/constants.py" to what you want

# Running:

go to repository root folder\
python3 Server\src\main.py
