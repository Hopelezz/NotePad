from database import Database


class Note:
    def __init__(self, id, title, content, created_at, updated_at, user_id):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.user_id = user_id

    @staticmethod
    def create(title, content, user_id):
        db = Database()
        db.cursor.execute(
            """
        INSERT INTO notes (title, content, user_id) VALUES (?, ?, ?)
        """,
            (title, content, user_id),
        )
        db.conn.commit()
        note_id = db.cursor.lastrowid
        db.close()
        return Note.get(note_id)

    @staticmethod
    def get(note_id):
        db = Database()
        db.cursor.execute(
            "SELECT id, title, content, created_at, updated_at, user_id FROM notes WHERE id = ?",
            (note_id,),
        )
        row = db.cursor.fetchone()
        db.close()
        if row:
            return Note(*row)
        return None

    @staticmethod
    def get_all(user_id):
        db = Database()
        db.cursor.execute(
            "SELECT id, title, content, created_at, updated_at, user_id FROM notes WHERE user_id = ? ORDER BY updated_at DESC",
            (user_id,),
        )
        rows = db.cursor.fetchall()
        db.close()
        return [Note(*row) for row in rows]

    def update(self):
        db = Database()
        db.cursor.execute(
            """
        UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
            (self.title, self.content, self.id),
        )
        db.conn.commit()
        db.close()

    def delete(self):
        db = Database()
        db.cursor.execute("DELETE FROM notes WHERE id = ?", (self.id,))
        db.conn.commit()
        db.close()
