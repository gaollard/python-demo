class DatabaseConnection:
    def __enter__(self):
        self.conn = connect_to_db()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return False  # 不吞掉异常

with DatabaseConnection() as conn:
    conn.execute("SELECT * FROM users")