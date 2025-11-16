from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)
from app.db import get_db


class UserService:

    @staticmethod
    def register(username, age):
        if not username or not age:
            raise InvalidInputError()

        db = get_db()
        cursor = db.cursor()

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

        db.commit()
        db.close()

        return dict(user)

    @staticmethod
    def update_username(user_id, new_username):
        if not user_id or not new_username:
            raise InvalidInputError("user_id", "new_username")

        db = get_db()
        cursor = db.cursor()

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

        db.commit()
        db.close()

        return dict(updated_user)
