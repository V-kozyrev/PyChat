import datetime


class DataBaseServices:

    def __init__(self, connection) -> None:
        self.connection = connection

    def register_user(self, login: str, password: str, name: str):  # user registration in db
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO users (user_login, user_password, user_name, online) 
                VALUES ('{login}', '{password}', '{name}', {True})""")
            self.connection.commit()

        return self.get_user_id_by_login(login)

    def is_credential_valid(self, login: str, user_password: str):  # checking user data, login and password
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT id FROM users WHERE user_login = '{login}' AND user_password = '{user_password}'""")
            if cursor.fetchall() is not None:
                return True
            return False

    # def change_online_user(self, login: str):  # change online user by login
    #    with self.connection.cursor() as cursor:
    #        cursor.execute(f"""UPDATE users SET online = {True} WHERE user_login = '{login}'""")
    #        self.connection.commit()

    # def change_offline_user(self, login: str):  # change offline user by login
    #    with self.connection.cursor() as cursor:
    #        cursor.execute(f"""UPDATE users SET online = {False} WHERE user_login = '{login}'""")
    #        self.connection.commit()

    def change_offline_all_user(self):  # change offline users
        with self.connection.cursor() as cursor:
            cursor.execute(f"""UPDATE users SET online = {False} WHERE online != {False}""")
            self.connection.commit()

    def change_online_user_id(self, user_id: int):  # change online user by id
        with self.connection.cursor() as cursor:
            cursor.execute(f"""UPDATE users SET online = {True} WHERE ID = '{user_id}'""")
            self.connection.commit()

    def change_offline_user_id(self, user_id: int):  # change offline user by id
        with self.connection.cursor() as cursor:
            cursor.execute(f"""UPDATE users SET online = {False} WHERE ID = '{user_id}'""")
            self.connection.commit()

    def get_user_name(self, user_id: int):  # get user name by id
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT user_name FROM users WHERE id = {user_id}""")
            return cursor.fetchone()[0]

    def get_user_id_by_login(self, login: str):  # get user name by login
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT id FROM users WHERE user_login = '{login}'""")
            return cursor.fetchone()[0]

    def get_user_id_by_name(self, name: str):  # get user id by name
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT id FROM users WHERE user_name = '{name}'""")
            return cursor.fetchone()[0]

    def is_login_exists(self, login: str):  # check for the existence of a login
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT user_login FROM users WHERE user_login = '{login}'""")
            if cursor.fetchall() is not None:
                return True
            return False

    def chek_user_online(self, name: str):  # check the user online on the server
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT online FROM users WHERE user_name = '{name}'""")
            if cursor.fetchone() is not None:
                return True
            return False

    def get_online_list(self):  # get all online users
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT user_name FROM users WHERE online = {True}""")
            return cursor.fetchall()

    def add_message_history(self, sender_id: int, recipient_id: int, message):  # add message history in db
        with self.connection.cursor() as cursor:
            insert_query = """INSERT INTO message_history (sender_id, recipient_id, message, time) 
                                VALUES (%s,%s,%s,%s)"""
            item_purchase_time = datetime.datetime.now()
            item_tuple = (sender_id, recipient_id, f'{message}', item_purchase_time)
            cursor.execute(insert_query, item_tuple)
            self.connection.commit()

    def get_message_history_server(self, limit: int):  # get server message history
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT users.user_name, message_history.message 
                                FROM users 
                                INNER JOIN(
                                    SELECT sender_id, message, time
                                    FROM message_history
                                    WHERE recipient_id = 0
                                ) as message_history ON message_history.sender_id = users.id
                                ORDER BY time DESC
                                LIMIT {limit}""")

            return cursor.fetchall()

    def get_private_message_history(self, sender_id: int, recipient_id: int, limit: int):  # get private message history
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT users.user_name, message_history.message, message_history.time
                                FROM users 
                                INNER JOIN(
                                    SELECT sender_id, message, time
                                    FROM message_history
                                    WHERE sender_id = {sender_id} AND recipient_id = {recipient_id}
                                ) AS message_history ON message_history.sender_id = users.id
                                UNION
                                SELECT users.user_name, message_history.message, message_history.time
                                FROM users 
                                INNER JOIN(
                                    SELECT sender_id, message, time
                                    FROM message_history
                                    WHERE sender_id = {recipient_id} AND recipient_id = {sender_id}
                                ) AS message_history ON message_history.sender_id = users.id
                                ORDER BY time DESC
                                LIMIT {limit}""")
            return cursor.fetchall()
