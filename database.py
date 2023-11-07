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

    def select(self, table_name, fields, where_column=None, where_value=None, where_type="=", joins=None, order_by=None, group_by=None, fetch_type="fetch_all"):
        if self.conn:
            try:
                cursor = self.conn.cursor(dictionary=True)
                fields = ', '.join(fields)
                query = f"SELECT {fields} from {table_name}"

                if joins:
                    for join in joins:
                        query = self._join(query, join)

                if where_column and where_value:
                    query = query + \
                        f" where {where_column} {where_type} {where_value}"
                if group_by:
                    group_by = self._auto_string_formatter(group_by)
                    query = query + f" group by {group_by}"
                if order_by:
                    order_by = self._auto_string_formatter(order_by)
                    query = query + f" order by {order_by}"
                cursor.execute(query)
                if fetch_type == "fetch_all":
                    return cursor.fetchall()
                elif fetch_type == "fetch_one":
                    return cursor.fetchone()
            except mysql.connector.Error as err:
                print("Error selecting values", err)

    def _join(self, query, join):
        join_type = join["type"]
        join_table = join["join_table"]
        join_table_field = join["join_table_field"]
        table = join["table"]
        field = join["field"]
        return f"{query} {join_type} {join_table} ON {join_table}.{join_table_field} = {table}.{field}"

    def _auto_string_formatter(self, input):
        if isinstance(input, str):
            return input
        elif isinstance(input, list):
            return ', '.join(map(str, input))

    def insert_data(self, table_name, columns, data):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                # Prepared statement
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
