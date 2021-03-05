import sqlite3

DB_PATH = './notes.db'
conn = sqlite3.connect(DB_PATH)
print("Opened database successfully")
conn.execute(
    'CREATE TABLE if not exists items (title VARCHAR(255) NOT NULL, description TEXT)')
print("Table created successfully")
conn.close()


def add_to_notes(title, desc):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            'insert into items(title, description) values(?,?)', (title, desc))
        conn.commit()
        return {"title": title, "description": desc}
    except Exception as e:
        print('Error: ', e)
        return None


notes_list = {}


def get_all_notes():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from items')
        rows = c.fetchall()
        return {"count": len(rows), "items": rows}
    except Exception as e:
        print('Error: ', e)
        return None


def get_notes(title):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select description from items where title='%s'" % title)
        status = c.fetchone()[0]
        print(status)
        return status
    except Exception as e:
        print('Error: ', e)
        return None


def update_note(title, desc):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            'update items set description=? where title=?', (desc, title))
        conn.commit()
        return {title: desc}
    except Exception as e:
        print('Error: ', e)
        return None


def delete_item(title):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("delete from items where title=?", (title,))
        conn.commit()
        return {'title': title}
    except Exception as e:
        print('Error: ', e)
        return None
