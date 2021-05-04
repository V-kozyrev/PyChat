import datetime


class DataBaseServices:

    def __init__(self, connection) -> None:
        self.connection = connection

    def register_user(self, login: str, password: str, name: str):  # user registration in db
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO users (user_login, user_password, user_name, online) VALUES ('{login}', '{password}', '{name}', {True})""")
            self.connection.commit()

    def chek_user(self, login: str, user_password: str):  # checking user data, login and password
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT id FROM users WHERE user_login = '{login}' AND user_password = '{user_password}'""")
            if cursor.fetchall():
                return True
            else:
                return False

    #def change_online_user(self, login: str):  # change online user by login
    #    with self.connection.cursor() as cursor:
    #        cursor.execute(f"""UPDATE users SET online = {True} WHERE user_login = '{login}'""")
    #        self.connection.commit()

    #def change_offline_user(self, login: str):  # change offline user by login
    #    with self.connection.cursor() as cursor:
    #        cursor.execute(f"""UPDATE users SET online = {False} WHERE user_login = '{login}'""")
    #        self.connection.commit()

    def change_offline_all_user(self):  # change offline users
        with self.connection.cursor() as cursor:
            cursor.execute(f"""UPDATE users SET online = {False} WHERE online != {False}""")
            self.connection.commit()

    def change_online_user_id(self, id: int):  # change online user by id
        with self.connection.cursor() as cursor:
            cursor.execute(f"""UPDATE users SET online = {True} WHERE ID = '{id}'""")
            self.connection.commit()

    def change_offline_user_id(self, id: int):  # change offline user by id
        with self.connection.cursor() as cursor:
            cursor.execute(f"""UPDATE users SET online = {False} WHERE ID = '{id}'""")
            self.connection.commit()

    def get_user_name(self, id: int):  # get user name by id
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT user_name FROM users WHERE id = {id}""")
            return cursor.fetchone()[0]

    def get_user_id_by_login(self, login: str):  # get user name by login
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT id FROM users WHERE user_login = '{login}'""")
            return cursor.fetchone()[0]

    def get_user_id_by_name(self, name: str):  # get user id by name
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT id FROM users WHERE user_name = '{name}'""")
            return cursor.fetchone()[0]

    def chek_user_login(self, login: str):  # check for the existence of a login
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT user_login FROM users WHERE user_login = '{login}'""")
            if cursor.fetchall():
                return True
            else:
                return False

    def chek_user_online(self, name: str):  # check the user online on the server
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT online FROM users WHERE user_name = '{name}'""")
            if cursor.fetchone()[0]:
                return True
            else:
                return False

    def get_online_list(self):  # get all online users
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT user_name FROM users WHERE online = {True}""")
            return cursor.fetchall()

    def add_message_history(self, id_sender: int, id_recipient: int, message):  # add message history in db
        with self.connection.cursor() as cursor:
            insert_query = """INSERT INTO message_history (id_sender, id_recipient, message, time) VALUES (%s,%s,%s,%s)"""
            item_purchase_time = datetime.datetime.now()
            item_tuple = (id_sender, id_recipient, f'{message}', item_purchase_time)
            cursor.execute(insert_query, item_tuple)
            self.connection.commit()

    def get_message_history_server(self, limit: int):  # get server message history
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT users.user_name, message_history.message 
                                FROM users 
                                INNER JOIN(
                                    SELECT id_sender, message, time
                                    FROM message_history
                                    WHERE id_recipient = 0
                                ) as message_history ON message_history.id_sender = users.id
                                ORDER BY time DESC
                                LIMIT {limit}""")

            return cursor.fetchall()

    def get_private_message_history(self, id_sender: int, id_recipient: int, limit: int):  # get private message history
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT users.user_name, message_history.message, message_history.time
                                FROM users 
                                INNER JOIN(
                                    SELECT id_sender, message, time
                                    FROM message_history
                                    WHERE id_sender = {id_sender} AND id_recipient = {id_recipient}
                                ) AS message_history ON message_history.id_sender = users.id
                                UNION
                                SELECT users.user_name, message_history.message, message_history.time
                                FROM users 
                                INNER JOIN(
                                    SELECT id_sender, message, time
                                    FROM message_history
                                    WHERE id_sender = {id_recipient} AND id_recipient = {id_sender}
                                ) AS message_history ON message_history.id_sender = users.id
                                ORDER BY time DESC
                                LIMIT {limit}""")
            return cursor.fetchall()