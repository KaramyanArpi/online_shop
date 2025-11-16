from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)


class UserService:
    def __init__(self, db):
        self.db = db

    def register(self, username, age):
        if not username or not age:
            raise InvalidInputError()

        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        candidate = cursor.fetchone()

        if candidate:
            raise AlreadyExistsError("username", username)

        cursor.execute(
            "INSERT INTO users (username, age) VALUES (?, ?)",
            (username, age)
        )

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        self.db.commit()
        self.db.close()

        return dict(user)

    def update_username(self, user_id, new_username):
        if not user_id or not new_username:
            raise InvalidInputError("user_id", "new_username")

        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        candidate = cursor.fetchone()

        if not candidate:
            raise NotFoundError("User", "id", user_id)

        cursor.execute(
            "UPDATE users SET username = ? WHERE id = ?",
            (new_username, user_id)
        )

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        updated_user = cursor.fetchone()

        self.db.commit()
        self.db.close()

        return dict(updated_user)
