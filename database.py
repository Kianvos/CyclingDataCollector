import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database:", self.database)
        except mysql.connector.Error as err:
            print("Error connecting to the database:", {err})

    def insert_data(self, table_name, columns, data):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(columns)
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, data)
                self.conn.commit()
            except mysql.connector.Error as err:
                print("Error inserting data:", err)

    def close(self):
        if self.conn:
            self.conn.close()
