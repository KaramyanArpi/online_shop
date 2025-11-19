from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)
from app.db import get_db

class SellerService:
    @staticmethod
    def register(name, rating):
        if not name or not rating:
            raise InvalidInputError("name", "rating")

        db = get_db()
        cursor = db.cursor()

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

        db.commit()
        db.close()

        return dict(seller)

    @staticmethod
    def update_name(seller_id, new_name):

        if not seller_id or not new_name:
            raise InvalidInputError("seller_id", "new_name")

        db = get_db()
        cursor = db.cursor()

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

        db.commit()
        db.close()

        return dict(updated_seller)

    @staticmethod
    def delete_seller(seller_id):
        if not seller_id:
            raise InvalidInputError("name", "seller_id")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM sellers WHERE id = ?", (seller_id, ))
        candidate = cursor.fetchone()

        if not candidate:
            raise NotFoundError("Seller", "id", seller_id)

        cursor.execute("DELETE FROM sellers WHERE id = ?", (seller_id, ))
        deleted_seller = cursor.fetchone()

        db.commit()
        db.close()

        return dict(deleted_seller)

    @staticmethod
    def get_seller_by_id(seller_id):
        if not seller_id:
            raise InvalidInputError("seller_id", "enough for it.")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM sellers WHERE id = ?", (seller_id,))
        seller = cursor.fetchone()

        if not seller:
            raise NotFoundError("User", "id", seller_id)

        db.close()

        return dict(seller)

    @staticmethod
    def get_sellers(limit, page):
        try:
            limit = int(limit)
            page = int(page)
        except ValueError:
            raise InvalidInputError("_limit", "page")

        offset = (page - 1) * limit

        db = get_db()
        cursor = db.cursor()

        rows = cursor.execute(
            "SELECT * FROM sellers LIMIT ? OFFSET ?",
            (page, offset)
        ).fetchall()

        return [dict(row) for row in rows]


    @staticmethod
    def get_own_products(seller_id, limit, page):
        if not seller_id or not limit or not page:
            raise InvalidInputError("seller_id, limit", "page")
        
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT s.id AS seller_id, p.id AS id, p.title, p.price FROM
            sellers AS s JOIN seller_products AS sp 
            ON s.id = sp.seller_id
            JOIN products AS p
            ON p.id = sp.product_id
            WHERE s.id = ?
            LIMIT ?
            OFFSET ?
        """, (seller_id, limit, limit * (page - 1), ))

        return [dict(x) for x in cursor.fetchall()]
        
