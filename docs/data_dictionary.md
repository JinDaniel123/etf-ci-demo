# Data dictionary (P4)

| Table | Field | Type | Key / constraint | Description |
| --- | --- | --- | --- | --- |
| customers | customer_id | INTEGER | PK | Unique identifier for each customer |
| customers | name | VARCHAR(100) | NOT NULL | Customer's full name |
| customers | email | VARCHAR(255) | UNIQUE, NOT NULL | Login and contact email |
| customers | created_at | TIMESTAMP | NOT NULL | When the account was created |
| products | product_id | INTEGER | PK | Unique identifier for each product |
| products | name | VARCHAR(150) | NOT NULL | Product name |
| products | price | DECIMAL(10,2) | NOT NULL, >= 0 | Current list price |
| products | stock | INTEGER | NOT NULL, >= 0 | Units available |
| orders | order_id | INTEGER | PK | Unique identifier for each order |
| orders | customer_id | INTEGER | FK to customers | Who placed the order |
| orders | order_date | TIMESTAMP | NOT NULL | When the order was placed |
| orders | status | VARCHAR(20) | NOT NULL | pending, paid, shipped or cancelled |
| order_items | order_item_id | INTEGER | PK | Unique identifier for each line |
| order_items | order_id | INTEGER | FK to orders | Order this line belongs to |
| order_items | product_id | INTEGER | FK to products | Product being bought |
| order_items | quantity | INTEGER | NOT NULL, > 0 | Number of units |
| order_items | unit_price | DECIMAL(10,2) | NOT NULL | Price at time of purchase |
| payments | payment_id | INTEGER | PK | Unique identifier for each payment |
| payments | order_id | INTEGER | FK to orders | Order being paid for |
| payments | amount | DECIMAL(10,2) | NOT NULL | Amount charged |
| payments | method | VARCHAR(20) | NOT NULL | card, bank transfer or wallet |
| payments | paid_at | TIMESTAMP | NULL until paid | When payment succeeded |
