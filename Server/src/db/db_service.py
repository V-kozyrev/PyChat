import datetime


class DataBaseServices:
    """
    db requests
    """

    def __init__(self, connection) -> None:
        self.connection = connection

    def register_user(self, login: str, password: str, name: str):  # user registration in db
        with self.connection.cursor() as cursor:
            cursor.execute("""INSERT INTO users (user_login, user_password, user_name, online) 
                            VALUES (%s, %s, %s, %s)""", (login, password, name, True))
            self.connection.commit()
        return self.get_user_id_by_login(login)

    def is_credential_valid(self, login: str, user_password: str):  # checking user data, login and password
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT id FROM users WHERE user_login = %s AND user_password = %s""",
                           (login, user_password))
            if cursor.fetchall() is not None:
                return True
            return False

    def change_offline_all_user(self):  # change offline users
        with self.connection.cursor() as cursor:
            cursor.execute("""UPDATE users SET online = %s WHERE online != %s""", (False, False))
            self.connection.commit()

    def change_online_user_id(self, user_id: int):  # change online user by id
        with self.connection.cursor() as cursor:
            cursor.execute("""UPDATE users SET online = %s WHERE ID = %s""", (True, user_id))
            self.connection.commit()

    def change_offline_user_id(self, user_id: int):  # change offline user by id
        with self.connection.cursor() as cursor:
            cursor.execute("""UPDATE users SET online = %s WHERE ID = %s""", (False, user_id))
            self.connection.commit()

    def get_user_name(self, user_id: int):  # get user name by id
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT user_name FROM users WHERE id = %s""", (user_id,))
            return cursor.fetchone()[0]

    def get_user_id_by_login(self, login: str):  # get user name by login
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT id FROM users WHERE user_login = %s""", (login,))
            return cursor.fetchone()[0]

    def get_user_id_by_name(self, name: str):  # get user id by name
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT id FROM users WHERE user_name = %s""", (name,))
            return cursor.fetchone()[0]

    def is_login_exists(self, login: str):  # check for the existence of a login
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT user_login FROM users WHERE user_login = %s""", (login,))
            if cursor.fetchall() is not None:
                return True
            return False

    def is_nickname_exists(self, name: str):  # check user nickname
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT user_name FROM users WHERE user_name = %s""", (name,))
            if cursor.fetchone() is not None:
                return True
            return False

    def chek_user_online(self, name: str):  # check the user online on the server
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT online FROM users WHERE user_name = %s""", (name,))
            if cursor.fetchone() is not None:
                return True
            return False

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
            cursor.execute("""SELECT users.user_name, message_history.message 
                                FROM users 
                                INNER JOIN message_history
                                    ON message_history.sender_id = users.id 
                                        AND recipient_id = 0
                                ORDER BY time DESC
                                LIMIT %s""", (limit,))
            return cursor.fetchall()

    def get_private_message_history(self, sender_id: int, recipient_id: int, limit: int):  # get private message history
        with self.connection.cursor() as cursor:
            cursor.execute(f"""SELECT users.user_name, message_history.message, message_history.time
                                FROM users 
                                INNER JOIN message_history
                                    ON message_history.sender_id = users.id 
                                        AND sender_id = %s
                                        AND recipient_id = %s
                                UNION
                                SELECT users.user_name, message_history.message, message_history.time
                                FROM users 
                                INNER JOIN message_history
                                    ON message_history.sender_id = users.id 
                                        AND sender_id = %s
                                        AND recipient_id = %s
                                ORDER BY time DESC
                                LIMIT %s""", (sender_id, recipient_id, recipient_id, sender_id, limit))
            return cursor.fetchall()
