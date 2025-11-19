from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)
from app.db import get_db

class ProductService:

    @staticmethod
    def register(title, price, sellers):
        if not title or not price or not sellers:
            raise InvalidInputError("sellers, title", "price")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM products WHERE title = ?", (title, ))
        candidate = cursor.fetchone()

        if candidate:
            raise AlreadyExistsError("title", title)

        cursor.execute(
            "INSERT INTO products (title, price) VALUES (?, ?)",
            (title, price)
        )

        cursor.execute("SELECT * FROM products WHERE title = ?", (title, ))
        product = dict(cursor.fetchone())

        print(product)

        for seller_id in sellers:
            print(seller_id)
            cursor.execute(
                "INSERT INTO seller_products (product_id, seller_id) VALUES (?, ?)",
                (product["id"], seller_id)
            )

        db.commit()
        db.close()

        return {
            **product,
            "sellers": sellers
        }

    @staticmethod
    def update_product_title(product_id, new_title):
        if not product_id or not new_title:
            raise InvalidInputError("product_id", "new_title")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id, ))
        candidate = cursor.fetchone()

        if not candidate:
            raise NotFoundError("Product", "id", product_id)

        cursor.execute(
            "UPDATE products SET title = ? WHERE id = ?",
            (new_title, product_id)
        )

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id, ))
        updated_product = cursor.fetchone()

        db.commit()
        db.close()

        return dict(updated_product)

    @staticmethod
    def delete_sellers_product(seller_id, product_id):
        if not seller_id or not product_id:
            raise InvalidInputError("seller_id", "product_id")

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM seller_products WHERE seller_id = ? AND product_id = ?",
            (seller_id, product_id)
        )
        candidate = cursor.fetchone()

        if not candidate:
            raise NotFoundError("Seller's product", "pair", (seller_id, product_id))

        cursor.execute(
            "DELETE FROM seller_products WHERE seller_id = ? AND product_id = ?",
            (seller_id, product_id)
        )

        db.commit()
        db.close()

        return {
            "msg": f"Seller's product ({seller_id}, {product_id}) deleted successfully."
        }


# API - Application Programming Interface
# GET, PUT, POST, DELETE, PATCH, HEAD, OPTIONS
# REST / RESTful API 1. JSON, 2. HTTP 3. Stateless
# 200, 201, 400, 401, 403, 404, 500
# SOAP
    # @staticmethod
    # def get_sellers_products(seller_id, page, limit):
    #     if not all([seller_id, page, limit]):
    #         raise InvalidInputError("seller_id, page", "_limit")

    #     try:
    #         page = int(page)
    #         limit = int(limit)
    #     except ValueError:
    #         raise InvalidInputError("page", "limit")

    #     offset = (page - 1) * limit

    #     db = get_db()
    #     cursor = db.cursor()

    #     cursor.execute(
    #         "SELECT COUNT(*) FROM seller_products WHERE seller_id = ?",
    #         (seller_id, )
    #     )
    #     total = cursor.fetchone()[0]

    #     if total == 0:
    #         raise NotFoundError("Seller's product", "pair", (seller_id, ))


    #     rows = cursor.execute(
    #         """
    #         SELECT * FROM seller_products
    #         WHERE seller_id = ? 
    #         LIMIT ? OFFSET ?
    #         """,
    #         (seller_id, limit, offset)
    #     ).fetchall()

    #     db.close()

    #     return {
    #         "seller_id": seller_id,
    #         "page": page,
    #         "limit": limit,
    #         "total": total,
    #         "results": [dict(r) for r in rows]
    #     }

    @staticmethod
    def get_product_by_id(product_id):
        if not product_id:
            raise InvalidInputError("product_id", "enough for it.")

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()

        if not product:
            raise NotFoundError("Product", "id", product_id)
        product = dict(product)


        db.close()

        return product



