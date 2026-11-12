-- Mock e-commerce schema (P4). Matches docs/data_dictionary.md.
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    created_at  TIMESTAMP NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name       VARCHAR(150) NOT NULL,
    price      DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock      INTEGER NOT NULL CHECK (stock >= 0)
);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date  TIMESTAMP NOT NULL,
    status      VARCHAR(20) NOT NULL
        CHECK (status IN ('pending', 'paid', 'shipped', 'cancelled'))
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    unit_price    DECIMAL(10,2) NOT NULL
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES orders(order_id),
    amount     DECIMAL(10,2) NOT NULL,
    method     VARCHAR(20) NOT NULL
        CHECK (method IN ('card', 'bank transfer', 'wallet')),
    paid_at    TIMESTAMP  -- NULL until paid
);
