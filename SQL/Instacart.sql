
DROP TABLE orders;

CREATE TABLE departments(
	department_id INT PRIMARY KEY,
	department TEXT NOT NULL 
);

CREATE TABLE aisles(
	aisle_id INT PRIMARY KEY,
	aisle TEXT NOT NULL
);

CREATE TABLE products(
	product_id INT PRIMARY KEY,
	product_name TEXT NOT NULL,
	aisle_id INT NOT NULL,
	department_id INT NOT NULL
); 

CREATE TABLE orders(
	order_id INT PRIMARY KEY,
	user_id INT NOT NULL,
	eval_set VARCHAR(10) NOT NULL,
	order_number INT NOT NULL,
	order_dow SMALLINT NOT NULL ,
	order_hour_of_day SMALLINT NOT NULL ,
	days_since_prior_order NUMERIC(4,1)
);

CREATE TABLE order_products_prior(
	order_id INT NOT NULL,
	product_id INT NOT NULL,
	add_to_cart_order INT NOT NULL,
	reordered INT NOT NULL 	
);

SELECT COUNT(*) FROM departments;
SELECT COUNT(*) FROM aisles;
SELECT COUNT(*) FROM products;
TRUNCATE TABLE orders;
SELECT COUNT(*) from order_products_prior;


-- Validations

-- Primary Key Validations

SELECT department_id, COUNT(*)
FROM departments
GROUP BY department_id
HAVING COUNT(*)>1;

SELECT aisle_id,COUNT(*)
FROM aisles
GROUP BY aisle_id
HAVING COUNT(*)>1;

SELECT product_id,COUNT(*)
FROM products
GROUP BY product_id
HAVING COUNT(*)>1

SELECT order_id, COUNT(*)
FROM orders
GROUP BY order_id
HAVING COUNT(*)>1

--NULL Checks

SELECT COUNT(*) AS null_product_names
FROM products
WHERE product_name IS NULL

SELECT COUNT(*) AS null_departments
FROM departments
WHERE department IS NULL

SELECT COUNT(*) AS null_aisle
FROM aisles
WHERE aisle IS NULL

SELECT COUNT(*) AS null_users
FROM orders
WHERE user_id IS NULL

SELECT COUNT(*) AS null_days
FROM orders
WHERE order_dow IS NULL

--Domain Validation

SELECT 
MIN(order_hour_of_day),
MAX(order_hour_of_day)
FROM orders

SELECT 
MIN(order_dow),
MAX(order_dow)
FROM orders

SELECT DISTINCT reordered 
FROM order_products_prior
ORDER BY reordered; -- doesn't affect much

--Referential Validation(Without Foreign Keys)

SELECT COUNT(*) 
FROM products p
LEFT JOIN departments d
ON p.department_id = d.department_id
WHERE d.department_id IS NULL

SELECT COUNT(*)
FROM products p
LEFT JOIN aisles a
ON p.aisle_id = a.aisle_id
WHERE a.aisle_id IS NULL

SELECT COUNT(*)
FROM order_products_prior opp
LEFT JOIN products p
ON opp.product_id = p.product_id
WHERE p.product_id IS NULL

SELECT COUNT(*)
FROM order_products_prior opp
LEFT JOIN orders o
ON opp.order_id = o.order_id
WHERE o.order_id IS NULL

-- Adding Foreign Keys

ALTER TABLE products 
ADD CONSTRAINT fk_products_departments
FOREIGN KEY(department_id)
REFERENCES departments(department_id)

ALTER TABLE products
ADD CONSTRAINT fk_products_aisles
FOREIGN KEY(aisle_id)
REFERENCES aisles(aisle_id)

ALTER TABLE order_products_prior
ADD CONSTRAINT fk_opp_orders
FOREIGN KEY(order_id)
REFERENCES orders(order_id)

ALTER TABLE order_products_prior
ADD CONSTRAINT fk_opp_products
FOREIGN KEY(product_id)
REFERENCES products(product_id)

-- Creating Indexes

--PRODUCTS

CREATE INDEX idx_products_departments
ON products(department_id);

CREATE INDEX idx_products_aisles
ON products(aisle_id);

--ORDERS

CREATE INDEX idx_orders_user
ON orders(user_id);

--ORDER PRODUCTS

CREATE INDEX idx_opp_orders
ON order_products_prior(order_id);

CREATE INDEX idx_opp_products
ON order_products_prior(product_id);

-- To see all the indexes in the database

SELECT
    schemaname,
    tablename,
    indexname
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename;

-- 1. Understanding Overall size of the business

--Total Customers

SELECT COUNT(DISTINCT user_id)
FROM orders

-- Total Orders

SELECT COUNT(order_id)
FROM orders

-- Total Products

SELECT COUNT(product_id)
FROM products

-- Total Departments

SELECT COUNT(department_id)
FROM departments

-- Total Aisles

SELECT COUNT(aisle_id)
FROM Aisles

-- 2. Customer Ordering Time Analysis

-- Investigation 1: Which hour receives the highest number of orders

SELECT order_hour_of_day, COUNT(order_id) AS ordcount
FROM orders
GROUP BY order_hour_of_day
ORDER BY ordcount DESC

-- Investigation 2: Which day of the week receives highest number of orders

SELECT order_dow, COUNT(order_id) AS ordcount
FROM orders
GROUP BY order_dow
ORDER BY ordcount DESC

-- Investigation 3: Which Day-Hour combination receives the highest number of orders

SELECT 
	order_dow,
	order_hour_of_day,
	COUNT(*) AS ordcount
FROM orders
GROUP BY
	order_dow,
	order_hour_of_day
ORDER BY
	ordcount DESC

-- INvestigation 4: Which hour of the day has the lowest order.

SELECT 
	order_hour_of_day,
	COUNT(*) AS ordcount
FROM orders
GROUP BY order_hour_of_day
ORDER BY ordcount ASC

-- Investigation 5: Which part of the receives highest number of orders

WITH order_time AS
(
    SELECT
        order_id,
        CASE
            WHEN order_hour_of_day BETWEEN 0 AND 4 THEN 'Late Night'
            WHEN order_hour_of_day BETWEEN 5 AND 8 THEN 'Early Morning'
            WHEN order_hour_of_day BETWEEN 9 AND 11 THEN 'Morning'
            WHEN order_hour_of_day BETWEEN 12 AND 16 THEN 'Afternoon'
            WHEN order_hour_of_day BETWEEN 17 AND 20 THEN 'Evening'
            ELSE 'Night'
        END AS time_slot
    FROM orders
),

time_slot_orders AS(
	SELECT 
		time_slot,
		COUNT(*) AS total_orders
		FROM order_time
		GROUP BY time_slot
)

SELECT 
	time_slot,
	total_orders,
	ROUND(total_orders * 100/SUM(total_orders) OVER(),2) AS percentage_of_orders
FROM time_slot_orders
ORDER BY total_orders DESC


-- Investigation 6: Do customers place more orders on weekend or weekdays?

WITH day_type AS (
    SELECT
        CASE
            WHEN order_dow IN (0, 6) THEN 'Weekend'
            ELSE 'Weekday'
        END AS day_category
    FROM orders
),
day_category_orders AS (
    SELECT
        day_category,
        COUNT(*) AS total_orders
    FROM day_type
    GROUP BY day_category
)

SELECT
    day_category,
    total_orders,
    ROUND(
        total_orders * 100.0 /
        SUM(total_orders) OVER (),
        2
    ) AS percentage_of_orders
FROM day_category_orders
ORDER BY 
	total_orders DESC;

-- 3. Product Performance Analysis.

-- Investigation 1. Which products are ordered most?

SELECT 	
	p.product_id,
	p.product_name,
	COUNT(*) AS ordcount
FROM order_products_prior opp
INNER JOIN products p
	ON opp.product_id = p.product_id
GROUP BY
	p.product_id,
	p.product_name
ORDER BY
	ordcount DESC

-- Investigation 2. Which department receives most order

SELECT 
	d.department_id,
	d.department,
	COUNT(*) AS ordcount
FROM order_products_prior opp
INNER JOIN products p
	ON opp.product_id = p.product_id
INNER JOIN departments d
	on p.department_id = d.department_id
GROUP BY
	d.department_id,
	d.department
ORDER BY
	ordcount DESC

-- Investigation 3: Which aisles are most popular

SELECT 
	a.aisle_id,
	a.aisle,
	COUNT(*) AS ordcount
FROM order_products_prior opp
INNER JOIN products p
	ON opp.product_id = p. product_id
INNER JOIN aisles a
	ON p.aisle_id = a.aisle_id
GROUP BY 
	a.aisle_id,
	a.aisle
ORDER BY
	ordcount DESC

--Investigation 4: What percentage of orders does each dept contribute?

WITH department_orders AS(
	SELECT
		d.department_id,
		d.department,
		COUNT(*) AS total_orders
	FROM order_products_prior opp
	INNER JOIN products p
		ON opp.product_id = p.product_id
	INNER JOIN departments d
		ON p.department_id = d.department_id
	GROUP BY
		d.department_id,
		d.department
	ORDER BY
		total_orders DESC
)

SELECT
	department,
	total_orders,
	ROUND(total_orders * 100.0 / SUM(total_orders) OVER(),2) AS percentage_of_orders
FROM department_orders
ORDER BY
	percentage_of_orders DESC

-- Investigation 5. Which product have the highest reorder rate?

WITH reorder AS(
	SELECT 
		p.product_name,
		p.product_id,
		COUNT(*) AS total_purchases,
		SUM(reordered) AS repeat_purchases
	FROM order_products_prior opp
	INNER JOIN products P
		ON opp.product_id = p.product_id
	GROUP BY
		p.product_name,
		p.product_id
		HAVING COUNT(*) >= 100
)

SELECT 
	product_id,
	product_name,
	ROUND(repeat_purchases * 100.0 / total_purchases ,2) AS reorder_rate
	FROM reorder
	ORDER BY 
		reorder_rate DESC

-- Investigation 6: Is demand concentrated in few products?

WITH product_orders AS(
	SELECT
		p.product_id,
		p.product_name,
		COUNT(*) AS total_purchases
	FROM order_products_prior opp
	INNER JOIN products p
		ON opp.product_id = p.product_id
	GROUP BY
		p.product_id,
		p.product_name
),
pareto AS(
	SELECT 
		product_id,
		product_name,
		total_purchases,
		SUM(total_purchases) OVER(ORDER BY total_purchases DESC) AS running_total
	FROM product_orders
),
pareto_percentage AS(
SELECT 
	product_name,
	total_purchases,
	running_total,
	ROUND(running_total * 100.0/SUM(total_purchases) OVER(),2) AS cummulative_percentage
FROM pareto
)
SELECT 
	 
	COUNT(*) AS products_for_80_percent
FROM pareto_percentage
WHERE cummulative_percentage <= 80

-- Business Case 4: Customer loyalty and reodering

-- Investigation 1: Which customer places the highest number of orders

SELECT 
	user_id,
	COUNT(*) AS total_orders
FROM orders 
GROUP BY
	user_id
HAVING COUNT(*) >100
ORDER BY
	total_orders DESC

-- Investigation 2: Which customers exhibit the highest product reorder behaviour

WITH t1 AS(
	SELECT 
		od.user_id,
		COUNT(*) AS total_purchases,
		SUM(reordered) AS repeat_purchases
	FROM order_products_prior opp
	INNER JOIN orders od
		ON opp.order_id = od.order_id
	GROUP BY
		od.user_id
)

SELECT
	user_id,
	total_purchases,
	repeat_purchases,
	ROUND(repeat_purchases * 100.0 / total_purchases,2) AS reorder_rate
FROM t1
ORDER BY
	reorder_rate DESC


-- Investigation 3: On average, how many days do customer wait before placing the next order.

SELECT
	user_id,
	ROUND(AVG(days_since_prior_order) ,2) AS avg_wait_days
FROM orders
GROUP BY
	user_id
HAVING AVG(days_since_prior_order) > 7
ORDER BY 
	avg_wait_days


-- Investigation 4: Categorizing customers into segments based on how frequently they place orders


WITH avg_orders AS(
	SELECT 
		user_id,
		ROUND(AVG(days_since_prior_order),2) AS avg_wait_days
	FROM orders
	GROUP BY 
		user_id
)

SELECT 
	user_id,
	avg_wait_days,
	CASE
		WHEN avg_wait_days <= 7 THEN 'VIP'
		WHEN avg_wait_days <= 14 THEN 'Active'
		WHEN avg_wait_days <=30 THEN 'Occasional'
		ELSE 'Risk'
	END AS Customer_segment
FROM avg_orders
ORDER BY
	avg_wait_days


-- Same Investigation using NTILE() function


WITH avg_orders AS(
	SELECT 
		user_id,
		ROUND(AVG(days_since_prior_order),2) AS avg_wait_days
	FROM orders
	GROUP BY
		user_id
),

customer_segments AS(
	SELECT 
		user_id,
		avg_wait_days,
		NTILE(4) OVER(ORDER BY avg_wait_days) AS quartile
	FROM avg_orders
)

SELECT 
	user_id,
	avg_wait_days,
	CASE
		WHEN quartile = 1 THEN 'Frequent Shopper'
		WHEN quartile IN (2,3) THEN 'Regular Shopper'
		ELSE 'Infrequent Shopper'
	END AS customer_segment
FROM customer_segments
ORDER BY
	avg_wait_days

-- With percentage for the respective customer segements
	
	
WITH avg_orders AS (
    SELECT
        user_id,
        ROUND(AVG(days_since_prior_order),2) AS avg_wait_days
FROM orders
    GROUP BY user_id
),

customer_segments AS (
    SELECT
        user_id,
        CASE
            WHEN avg_wait_days < 7 THEN 'Frequent Shopper'
            WHEN avg_wait_days <= 14 THEN 'Regular Shopper'
            ELSE 'Infrequent Shopper'
        END AS customer_segment
    FROM avg_orders
)

SELECT
    customer_segment,
    COUNT(*) AS total_customers,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), -- to calculate the total whole customer count and using it to calculate percentage
        2
    ) AS percentage
FROM customer_segments
GROUP BY customer_segment
ORDER BY total_customers DESC;


-- Business Case 5: Department and Aisle performance


-- Investigation 1: Which department receives highest number of purchases

WITH department_orders AS (
    SELECT
        d.department_id,
        d.department,
        COUNT(*) AS total_purchases
    FROM order_products_prior opp
    INNER JOIN products p
        ON opp.product_id = p.product_id
    INNER JOIN departments d
        ON p.department_id = d.department_id
    GROUP BY
        d.department_id,
        d.department
)

SELECT
    department_id,
    department,
    total_purchases,
    ROUND(
        total_purchases * 100.0 /
        SUM(total_purchases) OVER (),
        2
    ) AS contribution_percentage
FROM department_orders
ORDER BY
    contribution_percentage DESC;


-- Investigation 2: Which department has highest reordered products

SELECT
    d.department_id,
    d.department,
    COUNT(*) AS total_purchases,
    SUM(opp.reordered) AS reordered_purchases
FROM order_products_prior opp
INNER JOIN products p
    ON opp.product_id = p.product_id
INNER JOIN departments d
    ON p.department_id = d.department_id
GROUP BY
    d.department_id,
    d.department
ORDER BY
    reordered_purchases DESC;

-- Investigation 3: Which aisles receive the highest no.of purchases?

SELECT 
	a.aisle_id,
	a.aisle,
	COUNT(*) AS total_purchases
FROM order_products_prior opp
INNER JOIN products p
	ON opp.product_id = p.product_id
INNER JOIN aisles a
	ON p.aisle_id = a.aisle_id
GROUP BY
	a.aisle_id,
	a.aisle
ORDER BY
	total_purchases DESC

-- Investigation 4: What percentage of total purchases does each aisle contribute.

-- Same code as above. but we have to put the previous one into a temp table and do the percentage calculation in the outer query

WITH aisle_order AS(
	SELECT 
		a.aisle_id,
		a.aisle,
		COUNT(*) AS total_purchases
	FROM order_products_prior opp
	INNER JOIN products p
		ON opp.product_id = p.product_id
	INNER JOIN aisles a
		ON p.aisle_id = a.aisle_id
	GROUP BY
		a.aisle_id,
		a.aisle
)
SELECT
	aisle_id,
	aisle,
	ROUND(total_purchases * 100.0 / SUM(total_purchases) OVER(),2) AS percentage_contribution
FROM aisle_order
ORDER BY
	percentage_contribution DESC

-- Investigation 5: Aisles with highest reordered purchases.

SELECT
    a.aisle_id,
    a.aisle,
    COUNT(*) AS total_purchases,
    SUM(opp.reordered) AS reordered_purchases
FROM order_products_prior opp
INNER JOIN products p
    ON opp.product_id = p.product_id
INNER JOIN aisles a
    ON p.aisle_id = a.aisle_id
GROUP BY
    a.aisle_id,
    a.aisle
ORDER BY
    reordered_purchases DESC;

-- Business Case 5: Basket analysis

-- Investigation 1: On avaerage how many products does a customer purchase in a single order

WITH basket_size AS(
	SELECT 
		order_id,
		COUNT(*) AS products_in_order
	FROM order_products_prior
	GROUP BY
		order_id
)

SELECT
    ROUND(AVG(products_in_order), 2) AS avg_basket_size
FROM basket_size;


-- Investigation 2: Identifying orders with most products(large Basket)

WITH basket_size AS(
	SELECT 
		order_id,
		COUNT(*) AS products_in_order
	FROM order_products_prior
	GROUP BY
		order_id
)

SELECT
	order_id,
	products_in_order,
    RANK() OVER(ORDER BY products_in_order DESC) AS rank_of_basket
FROM basket_size
ORDER BY
	rank_of_basket,
	order_id


