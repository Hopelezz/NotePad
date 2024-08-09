from database import Database

class Note:
    def __init__(self, id, title, content, created_at, updated_at):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(title, content):
        db = Database()
        db.cursor.execute('''
        INSERT INTO notes (title, content) VALUES (?, ?)
        ''', (title, content))
        db.conn.commit()
        note_id = db.cursor.lastrowid
        db.close()
        return Note.get(note_id)

    @staticmethod
    def get(note_id):
        db = Database()
        db.cursor.execute('SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?', (note_id,))
        row = db.cursor.fetchone()
        db.close()
        if row:
            return Note(*row)
        return None

    @staticmethod
    def get_all():
        db = Database()
        db.cursor.execute('SELECT id, title, content, created_at, updated_at FROM notes ORDER BY updated_at DESC')
        rows = db.cursor.fetchall()
        db.close()
        return [Note(*row) for row in rows]

    def update(self):
        db = Database()
        db.cursor.execute('''
        UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        ''', (self.title, self.content, self.id))
        db.conn.commit()
        db.close()

    def delete(self):
        db = Database()
        db.cursor.execute('DELETE FROM notes WHERE id = ?', (self.id,))
        db.conn.commit()
        db.close()