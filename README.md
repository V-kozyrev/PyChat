# PyChat
Chat application for exchanging messages between users.\
Using PostgreSQL database to store information about users and their messages.\
The chat has several commands that you can enter to get information and send a private message:\
/p [nickname] [message] - to send a private message\
/h [quantity] - to view recent messages\
/mph [nickname] [quantity] - to view recent private messages\
/o - to view the list of online users\
/c - to view the list of commands\
# Dependancy Installation:
pip install -r requirements.txt
# Running:
go to chat folder and run\
python3 Server\src\main.py\
python3 Client\src\main.py
