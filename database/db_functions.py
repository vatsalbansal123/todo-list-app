import sqlite3

conn = sqlite3.connect("database/users.db")
c = conn.cursor()


def create_table(table_name, c, conn):
    c.execute(
        f"""CREATE TABLE {table_name}(
        task text
    )"""
    )
    conn.commit()


def add_record(table_name, details, c, conn):
    try:
        c.execute(f"""INSERT INTO {table_name} VALUES ('{details}')""")
    except:
        create_table("todo_db", c, conn)
        c.execute(f"""INSERT INTO {table_name} VALUES ('{details}')""")
    conn.commit()


def fetch_records(table_name, c, conn):
    try:
        c.execute(f"SELECT * FROM {table_name}")
        records = c.fetchall()
    except:
        create_table("todo_db", c, conn)
        c.execute(f"SELECT * FROM {table_name}")
        records = c.fetchall()
    conn.commit()
    return records


def delete_record(table_name, task, c, conn):
    try:
        c.execute(f"DELETE FROM {table_name} WHERE task='{task}'")
    except:
        create_table("todo_db", c, conn)
        c.execute(f"DELETE FROM {table_name} WHERE task='{task}'")
    conn.commit()


def update_record(table_name, previous_task, updated_task, c, conn):
    try:
        c.execute(
            f"UPDATE {table_name} SET task='{updated_task}' WHERE task='{previous_task}'"
        )
    except:
        create_table("todo_db", c, conn)
        c.execute(
            f"UPDATE {table_name} SET task='{updated_task}' WHERE task='{previous_task}'"
        )
    conn.commit()
