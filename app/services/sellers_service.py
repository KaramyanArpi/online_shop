from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)


class SellerService:
    def __init__(self, db):
        self.db = db

    def register(self, name, rating):
        if not name or not rating:
            raise InvalidInputError("name", "rating")

        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM sellers WHERE name = ?", (name, ))
        candidate = cursor.fetchone()

        if candidate:
            raise AlreadyExistsError("name", name)

        cursor.execute(
            "INSERT INTO sellers (name, rating) VALUES (?, ?)",
            (name, rating)
        )

        cursor.execute("SELECT * FROM sellers WHERE name = ?", (name, ))
        seller = cursor.fetchone()

        self.db.commit()

        return dict(seller)

    def update_name(self, seller_id, new_name):

        if not seller_id or not new_name:
            raise InvalidInputError("seller_id", "new_name")

        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM sellers WHERE id = ?", (seller_id, ))
        candidate = cursor.fetchone()

        if not candidate:
            raise NotFoundError("Seller", "id", seller_id)

        cursor.execute(
            "UPDATE sellers SET name = ? WHERE id = ?",
            (new_name, seller_id)
        )

        cursor.execute("SELECT * FROM sellers WHERE id = ?", (seller_id, ))
        updated_seller = cursor.fetchone()

        self.db.commit()

        return dict(updated_seller)






