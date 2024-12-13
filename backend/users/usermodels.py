import pymysql # PyMySQLをインポート
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id, email, password_hash=None, role=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def connect_db():
        return pymysql.connect(
            host="shopol-database.crqyu4yoi82f.ap-northeast-1.rds.amazonaws.com",
            user="admin",
            password="Future0308",
            database="ShopOL",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor  # Set the cursor class to DictCursor
        )

    @staticmethod
    def get_db_connection():
        return User.connect_db()

    @staticmethod
    def get(email):
        try:
            # Establish connection and create cursor
            connection = User.get_db_connection()
            cursor = connection.cursor()

            # Execute the SQL query
            cursor.execute('SELECT id, email, password_hash, role FROM users WHERE email = %s', (email,))

            # Fetch one user record
            user = cursor.fetchone()

            # Debugging: Print the fetched user
            print("Fetched user:", user)

            # Close connection and cursor
            cursor.close()
            connection.close()

            if user:
                return User(user['id'], user['email'], user['password_hash'], user['role'])
            return None
        except Exception as e:
            print("Error occurred:", e)
            return None

    @staticmethod
    def create_user(email, password):
        connection = User.get_db_connection()
        cursor = connection.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password_hash) VALUES (%s, %s)', (email, password_hash))
        connection.commit()
        user_id = cursor.lastrowid
        connection.close()
        return user_id

    @staticmethod
    def update_user(user_id, email=None, password=None):
        connection = User.get_db_connection()
        cursor = connection.cursor()
        if email:
            cursor.execute('UPDATE users SET email = %s WHERE id = %s', (email, user_id))
        if password:
            password_hash = generate_password_hash(password)
            cursor.execute('UPDATE users SET password_hash = %s WHERE id = %s', (password_hash, user_id))
        connection.commit()
        connection.close()

    @staticmethod
    def delete_user(user_id):
        connection = User.get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        connection.commit()
        connection.close()

    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)
