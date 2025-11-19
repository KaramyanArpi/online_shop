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

    @staticmethod
    def delete_user(user_id):
        if not user_id:
            raise InvalidInputError("username", "user_id")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        candidate = cursor.fetchone()

        if not candidate:
            raise NotFoundError("User", "id", user_id)

        deleted_user = dict(candidate)

        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
        db.close()

        return deleted_user

    @staticmethod
    def get_user_by_id(user_id):
        if not user_id:
            raise InvalidInputError("user_id", "enough for it.")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        db.close()

        if not user:
            raise NotFoundError("User", "id", user_id)

        return dict(user)

    @staticmethod
    def get_users(limit, page):
        try:
            limit = int(limit)
            page = int(page)
        except ValueError:
            raise InvalidInputError("limit", "page")

        offset = (page - 1) * limit
        db = get_db()
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM users LIMIT ? OFFSET ?", (limit, offset)).fetchall()
        db.close()
        return [dict(r) for r in rows]





