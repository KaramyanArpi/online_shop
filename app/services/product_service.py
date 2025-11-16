from app.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    InvalidInputError
)

class ProductService:
    def __init__(self, db):
        self.db = db

    def register(self, title, price):
        if not title or not price:
            raise InvalidInputError("title", "price")

        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM products WHERE title = ?", (title, ))
        candidate = cursor.fetchone()

        if candidate:
            raise AlreadyExistsError("title", title)

        cursor.execute(
            "INSERT INTO products (title, price) VALUES (?, ?)",
            (title, price)
        )

        cursor.execute("SELECT * FROM products WHERE title = ?", (title, ))
        product = cursor.fetchone()

        self.db.commit()
        self.db.close()

        return dict(product)

    def update_product_title(self, product_id, new_title):
        if not product_id or not new_title:
            raise InvalidInputError("product_id", "new_title")

        cursor = self.db.cursor()

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

        self.db.commit()
        self.db.close()

        return dict(updated_product)


