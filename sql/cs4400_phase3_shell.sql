/*
CS4400: Introduction to Database Systems
Spring 2021
Phase III Template
Team 39
Kaiwen Luo (kluo37)
Maiqi Ding (mding41)
Wen Li (wli486)
Zexing Song (zsong91)

Directions:
Please follow all instructions from the Phase III assignment PDF.
This file must run without error for credit.
*/

-- ID: 2a
-- Author: asmith457
-- Name: register_customer
DROP PROCEDURE IF EXISTS register_customer;
DELIMITER //
CREATE PROCEDURE register_customer(
	   IN i_username VARCHAR(40),
       IN i_password VARCHAR(40),
	   IN i_fname VARCHAR(40),
       IN i_lname VARCHAR(40),
       IN i_street VARCHAR(40),
       IN i_city VARCHAR(40),
       IN i_state VARCHAR(2),
	   IN i_zipcode CHAR(5),
       IN i_ccnumber VARCHAR(40),
	   IN i_cvv CHAR(3),
       IN i_exp_date DATE
)
BEGIN

-- Type solution below
IF LENGTH(i_zipcode) =5 THEN
	INSERT INTO USERS VALUES (i_username, MD5(i_password), i_fname, i_lname, i_street, i_city,i_state, i_zipcode);
	INSERT INTO CUSTOMER VALUES (i_username, i_ccnumber, i_cvv, i_exp_date);
ELSE 
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Zip is less than 5 digits';
END IF;

-- End of solution
END //
DELIMITER ;


-- ID: 2b
-- Author: asmith457
-- Name: register_employee
DROP PROCEDURE IF EXISTS register_employee;
DELIMITER //
CREATE PROCEDURE register_employee(
	   IN i_username VARCHAR(40),
       IN i_password VARCHAR(40),
	   IN i_fname VARCHAR(40),
       IN i_lname VARCHAR(40),
       IN i_street VARCHAR(40),
       IN i_city VARCHAR(40),
       IN i_state VARCHAR(2),
       IN i_zipcode CHAR(5)
)
BEGIN

-- Type solution below
INSERT INTO USERS VALUES (i_username, MD5(i_password), i_fname, i_lname, i_street, i_city,i_state, i_zipcode);
INSERT INTO EMPLOYEE VALUES (i_username);
-- End of solution
END //
DELIMITER ;

-- ID: 4a
-- Author: asmith457
-- Name: admin_create_grocery_chain
DROP PROCEDURE IF EXISTS admin_create_grocery_chain;
DELIMITER //
CREATE PROCEDURE admin_create_grocery_chain(
        IN i_grocery_chain_name VARCHAR(40)
)
BEGIN

-- Type solution below
INSERT INTO CHAIN VALUES (i_grocery_chain_name);
-- End of solution
END //
DELIMITER ;

-- ID: 5a
-- Author: ahatcher8
-- Name: admin_create_new_store
DROP PROCEDURE IF EXISTS admin_create_new_store;
DELIMITER //
CREATE PROCEDURE admin_create_new_store(
    	IN i_store_name VARCHAR(40),
        IN i_chain_name VARCHAR(40),
    	IN i_street VARCHAR(40),
    	IN i_city VARCHAR(40),
    	IN i_state VARCHAR(2),
    	IN i_zipcode CHAR(5)
)
BEGIN
-- Type solution below
IF EXISTS(SELECT * FROM store WHERE chainname=i_store_name AND Zipcode = i_zipcode) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Zip is not unique';
ELSE
INSERT INTO STORE VALUES (i_store_name, i_chain_name, i_street, i_city, i_state, i_zipcode);
END IF;
-- End of solution
END //
DELIMITER ;


-- ID: 6a
-- Author: ahatcher8
-- Name: admin_create_drone
DROP PROCEDURE IF EXISTS admin_create_drone;
DELIMITER //
CREATE PROCEDURE admin_create_drone(
	   IN i_drone_id INT,
       IN i_zip CHAR(5),
       IN i_radius INT,
       IN i_drone_tech VARCHAR(40)
)
BEGIN
-- Type solution below
IF EXISTS(SELECT * FROM USERS WHERE Zipcode=i_zip AND Username = i_drone_tech) THEN
	INSERT INTO DRONE VALUES (i_drone_id, "Available", i_zip, i_radius, i_drone_tech);
ELSE
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Drone technician does not match zip code';	
END IF;
-- End of solution
END //
DELIMITER ;


-- ID: 7a
-- Author: ahatcher8
-- Name: admin_create_item
DROP PROCEDURE IF EXISTS admin_create_item;
DELIMITER //
CREATE PROCEDURE admin_create_item(
        IN i_item_name VARCHAR(40),
        IN i_item_type VARCHAR(40),
        IN i_organic VARCHAR(3),
        IN i_origin VARCHAR(40)
)
BEGIN
-- Type solution below
IF i_item_type NOT IN ("Dairy", "Bakery", "Meat", "Produce", "Personal Care", "Paper Goods", "Beverages", "Other") THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Type is not correct';
ELSEIF i_organic NOT IN ("Yes","No") THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Origin is not correct';
ELSE
INSERT INTO ITEM VALUES (i_item_name, i_item_type, i_origin, i_organic);
END IF;
-- End of solution
END //
DELIMITER ;

-- ID: 8a
-- Author: dvaidyanathan6
-- Name: admin_view_customers
DROP PROCEDURE IF EXISTS admin_view_customers;
DELIMITER //
CREATE PROCEDURE admin_view_customers(
	   IN i_first_name VARCHAR(40),
       IN i_last_name VARCHAR(40)
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS admin_view_customers_result;
IF i_first_name IS NULL AND i_last_name IS NULL THEN

	CREATE TABLE admin_view_customers_result AS
	SELECT 
		Username,
		CONCAT(FirstName, ' ', LastName) AS Name,
		CONCAT(Street, ', ', City, ', ', State, ' ', Zipcode) AS Address
	FROM
		CUSTOMER
			NATURAL JOIN
		USERS;
ELSEIF i_first_name IS NULL AND i_last_name IS NOT NULL THEN
	CREATE TABLE admin_view_customers_result AS
	SELECT 
		Username,
		CONCAT(FirstName, ' ', LastName) AS Name,
		CONCAT(Street, ', ', City, ', ', State, ' ', Zipcode) AS Address
	FROM
		CUSTOMER
			NATURAL JOIN
		USERS
	WHERE 
		LastName = i_last_name;
ELSEIF i_first_name IS NOT NULL AND i_last_name IS NULL THEN	
	CREATE TABLE admin_view_customers_result AS
	SELECT 
		Username,
		CONCAT(FirstName, ' ', LastName) AS Name,
		CONCAT(Street, ', ', City, ', ', State, ' ', Zipcode) AS Address
	FROM
		CUSTOMER
			NATURAL JOIN
		USERS
	WHERE 
		FirstName = i_first_name;
ELSE    
	CREATE TABLE admin_view_customers_result AS
	SELECT 
		Username,
		CONCAT(FirstName, ' ', LastName) AS Name,
		CONCAT(Street, ', ', City, ', ', State, ' ', Zipcode) AS Address
	FROM
		CUSTOMER
			NATURAL JOIN
		USERS
	WHERE
		FirstName = i_first_name
			AND LastName = i_last_name;
END IF;
-- End of solution
END //
DELIMITER ;

-- ID: 9a
-- Author: dvaidyanathan6
-- Name: manager_create_chain_item
DROP PROCEDURE IF EXISTS manager_create_chain_item;
DELIMITER //
CREATE PROCEDURE manager_create_chain_item(
        IN i_chain_name VARCHAR(40),
    	IN i_item_name VARCHAR(40),
    	IN i_quantity INT, 
    	IN i_order_limit INT,
    	IN i_PLU_number INT,
    	IN i_price DECIMAL(4, 2)
)
BEGIN
-- Type solution below
IF NOT EXISTS(SELECT PLUNumber FROM chain_item WHERE ChainItemName = i_item_name AND ChainName = i_chain_name) THEN
	INSERT INTO CHAIN_ITEM VALUES (i_item_name, i_chain_name, i_PLU_number, i_order_limit, i_quantity, i_price);
ELSE
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicated chain item pair.';
END IF;
-- End of solution
END //
DELIMITER ;

-- ID: 10a
-- Author: dvaidyanathan6
-- Name: manager_view_drone_technicians
DROP PROCEDURE IF EXISTS manager_view_drone_technicians;
DELIMITER //
CREATE PROCEDURE manager_view_drone_technicians(
	   IN i_chain_name VARCHAR(40),
       IN i_drone_tech VARCHAR(40),
       IN i_store_name VARCHAR(40)
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS manager_view_drone_technicians_result;
IF i_drone_tech IS NULL AND i_store_name IS NULL THEN
	CREATE TABLE manager_view_drone_technicians_result AS
	SELECT 
		Username, CONCAT(FirstName, ' ', LastName) AS Name, StoreName
	FROM
		DRONE_TECH D
			NATURAL JOIN
		USERS U
	WHERE
		ChainName = i_chain_name;
    
ELSEIF i_drone_tech IS NULL AND i_store_name IS NOT NULL THEN
	CREATE TABLE manager_view_drone_technicians_result AS
	SELECT 
		Username, CONCAT(FirstName, ' ', LastName) AS Name, StoreName
	FROM
		DRONE_TECH D
			NATURAL JOIN
		USERS U
	WHERE
		ChainName = i_chain_name
			AND StoreName = i_store_name;

ELSEIF i_drone_tech IS NOT NULL AND i_store_name IS NULL THEN   
	CREATE TABLE manager_view_drone_technicians_result AS
	SELECT 
		Username, CONCAT(FirstName, ' ', LastName) AS Name, StoreName
	FROM
		DRONE_TECH D
			NATURAL JOIN
		USERS U
	WHERE
		ChainName = i_chain_name
			AND D.Username = i_drone_tech;	
ELSE   
	CREATE TABLE manager_view_drone_technicians_result AS
	SELECT 
		Username, CONCAT(FirstName, ' ', LastName) AS Name, StoreName
	FROM
		DRONE_TECH D
			NATURAL JOIN
		USERS U
	WHERE
		ChainName = i_chain_name
			AND StoreName = i_store_name
			AND D.Username = i_drone_tech;
END IF;
-- End of solution
END //
DELIMITER ;

-- ID: 11a
-- Author: vtata6
-- Name: manager_view_drones
DROP PROCEDURE IF EXISTS manager_view_drones;
DELIMITER //
CREATE PROCEDURE manager_view_drones(
	   IN i_mgr_username VARCHAR(40), 
	   IN i_drone_id INT, drone_radius INT
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS manager_view_drones_result;
IF i_drone_id IS NULL AND drone_radius IS NULL THEN
	CREATE TABLE manager_view_drones_result AS
	SELECT 
		ID AS 'Drone ID',
		DroneTech AS Operator,
		Radius,
		Zip AS 'Zip Code',
		DroneStatus AS 'Status'
	FROM
		DRONE d
			JOIN
		DRONE_TECH t ON d.DroneTech = t.Username
			JOIN
		MANAGER m ON t.ChainName = m.ChainName
	WHERE
		m.Username = i_mgr_username;
    
ELSEIF i_drone_id IS NOT NULL AND drone_radius IS NULL THEN
	CREATE TABLE manager_view_drones_result AS
	SELECT 
		ID AS 'Drone ID',
		DroneTech AS Operator,
		Radius,
		Zip AS 'Zip Code',
		DroneStatus AS 'Status'
	FROM
		DRONE d
			JOIN
		DRONE_TECH t ON d.DroneTech = t.Username
			JOIN
		MANAGER m ON t.ChainName = m.ChainName
	WHERE
		m.Username = i_mgr_username
		AND d.ID = i_drone_id;

ELSEIF i_drone_id IS NULL AND drone_radius IS NOT NULL THEN
	CREATE TABLE manager_view_drones_result AS
	SELECT 
		ID AS 'Drone ID',
		DroneTech AS Operator,
		Radius,
		Zip AS 'Zip Code',
		DroneStatus AS 'Status'
	FROM
		DRONE d
			JOIN
		DRONE_TECH t ON d.DroneTech = t.Username
			JOIN
		MANAGER m ON t.ChainName = m.ChainName
	WHERE
		m.Username = i_mgr_username
		AND d.Radius >= drone_radius;
    
ELSE
	CREATE TABLE manager_view_drones_result AS
	SELECT 
		ID AS 'Drone ID',
		DroneTech AS Operator,
		Radius,
		Zip AS 'Zip Code',
		DroneStatus AS 'Status'
	FROM
		DRONE d
			JOIN
		DRONE_TECH t ON d.DroneTech = t.Username
			JOIN
		MANAGER m ON t.ChainName = m.ChainName
	WHERE
		m.Username = i_mgr_username
			AND d.ID = i_drone_id
			AND d.Radius >= drone_radius;
END IF;

/*DROP TABLE IF EXISTS manager_view_drones_result;
CREATE TABLE manager_view_drones_result AS
 	SELECT d.ID, d.DroneTech, d.Radius, d.Zip, d.DroneStatus
     FROM 
     (SELECT d1.*, dt.ChainName
     FROM drone as d1
     LEFT JOIN 
     drone_tech as dt
     ON d1.DroneTech = dt. Username) as d
     WHERE d.ChainName = (SELECT ChainName
     FROM manager as m
     WHERE m.Username = i_mgr_username)
     AND 
	 (i_drone_id IS NULL OR d.ID = i_drone_id)
     AND 
     (drone_radius IS NULL OR d.Radius >= drone_radius);*/
-- End of solution
END //
DELIMITER ;

-- ID: 12a
-- Author: vtata6
-- Name: manager_manage_stores
DROP PROCEDURE IF EXISTS manager_manage_stores;
DELIMITER //
CREATE PROCEDURE manager_manage_stores(
	   IN i_mgr_username VARCHAR(50), 
	   IN i_storeName VARCHAR(50), 
	   IN i_minTotal INT, 
	   IN i_maxTotal INT
)
BEGIN
-- Type solution below
IF i_minTotal IS NULL THEN 
	SET i_minTotal = -1;
END IF;
IF i_maxTotal IS NULL THEN 
	SET i_maxTotal = 2147483647;
END IF;

DROP TABLE IF EXISTS manager_manage_stores_result;
CREATE TABLE manager_manage_stores_result AS
SELECT t1.StoreName, t1.Address, t4.`# Orders`, t2.Employees+1 as Employees, t4.Total
    FROM
    (SELECT s.ChainName, s.StoreName, CONCAT(s.Street,' ', s.City,',', s.State,' ', s.Zipcode) as Address
    FROM store as s
    WHERE s.ChainName = (SELECT ChainName FROM manager WHERE Username = i_mgr_username)
    AND i_storeName IS NULL OR s.StoreName = i_storeName) as t1
    INNER JOIN
	(SELECT dt.ChainName, dt.StoreName, count(*) as Employees
    FROM drone_tech as dt
    WHERE dt.ChainName = (SELECT ChainName FROM manager WHERE Username = i_mgr_username)
    AND i_storeName IS NULL OR dt.StoreName = i_storeName
    GROUP BY dt.ChainName, dt.StoreName) as t2
    ON t1.ChainName = t2.ChainName AND t1.StoreName = t2.StoreName
    INNER JOIN
    (SELECT t3.ChainName, t3.StoreName, count(*) as '# Orders', sum(t5.Total) as Total
    FROM
	(SELECT o.ID, o.OrderStatus, o.DroneID, d.DroneTech, dt.ChainName, dt.StoreName
    FROM
    orders as o
    LEFT JOIN
	drone as d
    on o.DroneID = d.ID
    LEFT JOIN
    drone_tech as dt
    on d.DroneTech = dt.Username
    WHERE dt.ChainName = (SELECT ChainName FROM manager WHERE Username = i_mgr_username)
    AND i_storeName IS NULL OR dt.StoreName = i_storeName) as t3
    LEFT JOIN
    (SELECT c.OrderID, sum(c.Quantity * ci.price) as 'Total'
    FROM `contains` as c
    INNER JOIN 
    chain_item as ci
    ON c.PLUNumber = ci.PLUNumber AND c.ItemName = ci.ChainItemName AND c.ChainName = ci.ChainName
    WHERE c.ChainName = (SELECT ChainName FROM manager WHERE Username = i_mgr_username)
	AND ci.ChainName = (SELECT ChainName FROM manager WHERE Username = i_mgr_username)
    GROUP BY c.OrderID) as t5
    ON t3.ID = t5.OrderID
    GROUP BY t3.ChainName, t3.StoreName) as t4
    ON t1.ChainName = t4.ChainName AND t1.StoreName = t4.StoreName
    WHERE (i_minTotal IS NULL OR t4.Total >= i_minTotal)
    AND (i_maxTotal IS NULL OR t4.Total <= i_maxTotal);
-- End of solution
END //
DELIMITER ;

-- ID: 13a
-- Author: vtata6
-- Name: customer_change_credit_card_information
DROP PROCEDURE IF EXISTS customer_change_credit_card_information;
DELIMITER //
CREATE PROCEDURE customer_change_credit_card_information(
	   IN i_custUsername VARCHAR(40), 
	   IN i_new_cc_number VARCHAR(19), 
	   IN i_new_CVV INT, 
	   IN i_new_exp_date DATE
)
BEGIN
-- Type solution below
UPDATE CUSTOMER 
SET 
    CcNumber = i_new_cc_number,
    CVV = i_new_CVV,
    EXP_DATE = i_new_exp_date
WHERE
    Username = i_custUsername;
-- End of solution
END //
DELIMITER ;

-- ID: 14a
-- Author: ftsang3
-- Name: customer_view_order_history
DROP PROCEDURE IF EXISTS customer_view_order_history;
DELIMITER //
CREATE PROCEDURE customer_view_order_history(
	   IN i_username VARCHAR(40),
       IN i_orderid INT
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS customer_view_order_history_result;
CREATE TABLE customer_view_order_history_result AS
SELECT 
    IFNULL(SUM(n.Quantity * ci.Price), 0.00) AS 'Total Amount',
    SUM(n.Quantity) AS 'Total Items',
    o.OrderDate AS 'Date of Purchase',
    d.ID AS 'Drone ID',
    t.Username AS 'Store Associate',
    o.OrderStatus AS Status
FROM
    ORDERS o
        JOIN
    CUSTOMER c ON o.CustomerUsername = c.Username
        LEFT JOIN
    DRONE d ON o.DroneID = d.ID
        LEFT JOIN
    DRONE_TECH t ON d.DroneTech = t.Username
        JOIN
    CONTAINS n ON o.ID = n.OrderID
        JOIN
    CHAIN_ITEM ci ON ci.ChainItemName = n.ItemName
        AND ci.ChainName = n.ChainName
        AND ci.PLUNumber = n.PLUNumber
WHERE
    o.CustomerUsername = i_username
        AND o.id = i_orderid
GROUP BY
	o.id;

-- End of solution
END //
DELIMITER ;

-- ID: 15a
-- Author: ftsang3
-- Name: customer_view_store_items
DROP PROCEDURE IF EXISTS customer_view_store_items;
DELIMITER //
CREATE PROCEDURE customer_view_store_items(
	   IN i_username VARCHAR(40),
       IN i_chain_name VARCHAR(40),
       IN i_store_name VARCHAR(40),
       IN i_item_type VARCHAR(40)
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS customer_view_store_items_result;
IF (SELECT Zipcode FROM STORE s WHERE s.StoreName = i_store_name AND s.ChainName = i_chain_name)
	= (SELECT Zipcode FROM USERS WHERE Username = i_username) THEN
	IF i_item_type IS NULL OR i_item_type = "ALL" THEN
		CREATE TABLE customer_view_store_items_result AS
		SELECT 
			ci.ChainItemName AS Items, 
            Orderlimit AS Quantity 
		FROM 
			CHAIN_ITEM ci 
				JOIN 
            ITEM i ON ci.ChainItemName = i.ItemName 
		WHERE ci.ChainName = i_chain_name;
	ELSE
		CREATE TABLE customer_view_store_items_result AS
		SELECT 
			ci.ChainItemName AS Items, 
            Orderlimit AS Quantity 
		FROM 
			CHAIN_ITEM ci 
				JOIN 
			ITEM i ON ci.ChainItemName = i.ItemName 
		WHERE ci.ChainName = i_chain_name 
			AND i.ItemType = i_item_type;
	END IF;
ELSE
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Zip of customer and store does not match';
END IF;

-- End of solution
END //
DELIMITER ;

-- ID: 15b
-- Author: ftsang3
-- Name: customer_select_items
DROP PROCEDURE IF EXISTS customer_select_items;
DELIMITER //
CREATE PROCEDURE customer_select_items(
	    IN i_username VARCHAR(40),
    	IN i_chain_name VARCHAR(40),
    	IN i_store_name VARCHAR(40),
    	IN i_item_name VARCHAR(40),
    	IN i_quantity INT
)
BEGIN
-- Type solution below
DECLARE Oid INT;
DECLARE plu INT;

IF EXISTS (SELECT PLUNumber FROM CHAIN_ITEM WHERE ChainItemName=i_item_name AND ChainName = i_chain_name) THEN
	SELECT PLUNumber INTO plu FROM CHAIN_ITEM WHERE ChainItemName=i_item_name AND ChainName = i_chain_name;
ELSE
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Do not have this item';
END IF;

IF (SELECT Zipcode FROM USERS WHERE Username=i_username) <>
	(SELECT Zipcode FROM STORE WHERE StoreName=i_store_name AND ChainName=i_chain_name)
    OR (SELECT ((SELECT Zipcode FROM USERS WHERE Username=i_username) <>
	(SELECT Zipcode FROM STORE WHERE StoreName=i_store_name AND ChainName=i_chain_name))) is NULL
    OR 
    i_quantity > (SELECT Orderlimit FROM CHAIN_ITEM WHERE ChainItemName =i_item_name AND ChainName = i_chain_name)
    OR
    (SELECT EXP_DATE FROM CUSTOMER WHERE Username = i_username)< curdate() 
    THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Errors';
END IF;


IF NOT EXISTS(SELECT * FROM ORDERS WHERE CustomerUsername = i_username and OrderStatus = "Creating") THEN
	-- SELECT max(ID)+1 INTO Oid FROM ORDERS;
	INSERT INTO ORDERS (OrderStatus, OrderDate, CustomerUsername) VALUES ('Creating', curdate(), i_username);
    SELECT ID INTO Oid FROM ORDERS WHERE OrderStatus = "Creating" AND CustomerUsername = i_username;
    INSERT INTO CONTAINS VALUES (Oid, i_item_name, i_chain_name, plu, i_quantity);
ELSE
	SELECT ID INTO Oid FROM ORDERS WHERE OrderStatus = "Creating" AND CustomerUsername = i_username;
    
     IF i_chain_name != (SELECT distinct ChainName FROM CONTAINS WHERE OrderID = Oid) THEN
 		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'One store each time';
     ELSE
     	INSERT INTO CONTAINS VALUES (Oid, i_item_name, i_chain_name, plu, i_quantity);
     END IF;
END IF;



-- IF NOT EXISTS(SELECT * FROM ORDERS WHERE CustomerUsername = i_username and OrderStatus = "Creating") THEN
-- 	SELECT max(ID)+1 INTO Oid FROM ORDERS;
-- 	INSERT INTO ORDERS VALUES (Oid, "Creating", curdate(), i_username, NULL);
-- ELSE
-- 	SELECT ID INTO Oid FROM ORDERS WHERE OrderStatus = "Creating" AND CustomerUsername = i_username;
    
--      IF i_chain_name != (SELECT distinct ChainName FROM CONTAINS WHERE OrderID = Oid) THEN
--  		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'One store each time';
--      END IF;
-- END IF;

-- IF (SELECT Zipcode FROM USERS WHERE Username=i_username) =
-- 	(SELECT Zipcode FROM STORE WHERE StoreName=i_store_name AND ChainName=i_chain_name) 
--     AND 
--     i_quantity <= (SELECT Orderlimit FROM CHAIN_ITEM WHERE ChainItemName =i_item_name AND ChainName = i_chain_name) THEN 
--     
--     INSERT INTO CONTAINS VALUES (Oid, i_item_name, i_chain_name, plu, i_quantity);
-- ELSE
-- 	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Zip of customer and store does not match or quantity is overlimit';
-- END IF;

-- IF  (SELECT year(EXP_DATE) FROM customer WHERE Username = i_username) >= year(now())
-- 	AND (SELECT month(EXP_DATE) FROM customer WHERE Username = i_username) >= month(now()) AND
--     IF (SELECT ID FROM orders WHERE CustomerUsername = i_username AND OrderStatus = 'Creating') IS NULL THEN
-- 	INSERT orders (OrderStatus, OrderDate, CustomerUsername) VALUES ('Creating', curdate(), i_username);
-- END IF;

-- IF (SELECT Zipcode FROM USERS WHERE Username=i_username) =
-- 	(SELECT Zipcode FROM STORE WHERE StoreName=i_store_name AND ChainName=i_chain_name)
--     AND 
--     i_quantity <= (SELECT Orderlimit FROM CHAIN_ITEM WHERE ChainItemName =i_item_name AND ChainName = i_chain_name) THEN
--     INSERT `contains` (OrderID, ItemName, ChainName, PLUNumber, Quantity)
--     VALUES ((SELECT ID FROM orders WHERE OrderStatus = 'Creating' AND CustomerUsername = i_username), 
-- 		i_item_name, 
-- 		i_chain_name, 
-- 		(SELECT PLUNumber FROM chain_item WHERE ChainItemName = i_item_name AND ChainName = i_chain_name),
-- 		i_quantity);
-- END IF;
-- End of solution
END //
DELIMITER ;
         
-- ID: 16a
-- Author: jkomskis3
-- Name: customer_review_order
DROP PROCEDURE IF EXISTS customer_review_order;
DELIMITER //
CREATE PROCEDURE customer_review_order(
	   IN i_username VARCHAR(40)
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS customer_review_order_result;
CREATE TABLE customer_review_order_result AS
SELECT 
    c.ItemName AS Items,
    c.Quantity AS Quantity,
    ci.Orderlimit AS Orderlimit,
    ci.Price AS 'Unit Cost'
FROM
    CHAIN_ITEM ci
        JOIN
    CONTAINS c ON ci.ChainName = c.ChainName
        AND ci.ChainItemName = c.ItemName
        AND ci.PLUNumber = c.PLUNumber
        JOIN
    ORDERS o ON c.OrderID = o.ID
WHERE
    o.CustomerUsername = i_username
        AND o.OrderStatus = 'Creating';

-- End of solution
END //
DELIMITER ;


-- ID: 16b
-- Author: jkomskis3
-- Name: customer_update_order
DROP PROCEDURE IF EXISTS customer_update_order;
DELIMITER //
CREATE PROCEDURE customer_update_order(
	   IN i_username VARCHAR(40),
       IN i_item_name VARCHAR(40),
       IN i_quantity INT
)
BEGIN
-- Type solution below
/*DECLARE Oid INT;
SELECT ID INTO Oid FROM ORDERS WHERE OrderStatus = 'Creating' AND CustomerUsername = i_username;

UPDATE CONTAINS 
SET 
    Quantity = i_quantity
WHERE
    OrderID = Oid AND ItemName = i_item_name;
*/
	UPDATE `contains`
    SET Quantity = i_quantity
    WHERE OrderID = (SELECT ID FROM orders WHERE OrderStatus = 'Creating' AND CustomerUsername = i_username) 
    AND ItemName = i_item_name;
    
    DELETE FROM `contains` 
    WHERE Quantity = 0 
    AND OrderID = (SELECT ID FROM orders WHERE OrderStatus = 'Creating' AND CustomerUsername = i_username);
	
    INSERT INTO chain_item
	SELECT ci.ChainItemName, ci.ChainName, ci.PLUNumber, ci.Orderlimit, ci.Quantity, ci.Price
    FROM chain_item as ci
    WHERE ci.ChainItemName = i_item_name AND ci.ChainName = (SELECT distinct(ChainName) FROM contains WHERE OrderID = (SELECT ID FROM orders WHERE OrderStatus = 'Creating' AND CustomerUsername = i_username))
--     INNER JOIN
--    (SELECT ItemName, ChainName, Quantity FROM `contains` WHERE OrderID = (SELECT ID FROM orders WHERE OrderStatus = 'Creating' AND CustomerUsername = i_username)) as c
--    ON ci.ChainItemName = c.ItemName AND ci.ChainName = c.ChainName
    ON DUPLICATE KEY UPDATE `Quantity` = (ci.Quantity - i_quantity);
    
-- 	UPDATE orders
-- 	SET OrderStatus = 'Pending'
-- 	WHERE OrderStatus = 'Creating' AND CustomerUsername = i_username;

END //
DELIMITER ;


-- ID: 17a
-- Author: jkomskis3
-- Name: drone_technician_view_order_history
DROP PROCEDURE IF EXISTS drone_technician_view_order_history;
DELIMITER //
CREATE PROCEDURE drone_technician_view_order_history(
        IN i_username VARCHAR(40),
    	IN i_start_date DATE,
    	IN i_end_date DATE
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS drone_technician_view_order_history_result;

IF i_start_date IS NULL THEN
	SET i_start_date = (SELECT min(OrderDate) FROM ORDERS);
END IF;

IF i_end_date IS NULL THEN
	SET i_end_date = (SELECT max(OrderDate) FROM ORDERS);
END IF;

CREATE TABLE drone_technician_view_order_history_result AS
SELECT 
    o.ID AS ID,
    CONCAT(ut.FirstName, ' ', ut.LastName) AS Operator,
    o.OrderDate AS Date,
    o.DroneID AS 'Drone ID',
    o.OrderStatus AS Status,
    SUM(n.Quantity * ci.Price) AS Total
FROM
    ORDERS o
		JOIN
	USERS uc ON uc.Username = o.CustomerUsername
		JOIN
    CONTAINS n ON o.ID = n.OrderID
        JOIN
    CHAIN_ITEM ci ON ci.ChainItemName = n.ItemName
        AND ci.ChainName = n.ChainName
        AND ci.PLUNumber = n.PLUNumber
		LEFT JOIN
	DRONE d ON o.DroneID = d.ID
		LEFT JOIN
	USERS ut ON ut.Username = d.DroneTech
WHERE
	ci.ChainName = (SELECT ChainName FROM DRONE_TECH WHERE Username = i_username) AND
    uc.Zipcode = (SELECT ZipCode FROM USERS WHERE Username = i_username)
GROUP BY o.ID
HAVING Date <= i_end_date
    AND Date >= i_start_date;

-- End of solution
END //
DELIMITER ;

-- ID: 17b
-- Author: agoyal89
-- Name: dronetech_assign_order
DROP PROCEDURE IF EXISTS dronetech_assign_order;
DELIMITER //
CREATE PROCEDURE dronetech_assign_order(
	   IN i_username VARCHAR(40),
       IN i_droneid INT,
       IN i_status VARCHAR(20),
       IN i_orderid INT
)
BEGIN
-- Type solution below

UPDATE orders
SET
DroneID =i_droneid,
OrderStatus = i_status
WHERE ID = i_orderid;

IF i_status = 'Delivered' or i_status = 'Pending' THEN
	UPDATE drone
	SET
	DroneStatus = 'Available'
	WHERE ID = i_droneid;
ELSE
	UPDATE drone
	SET
	DroneStatus = 'Busy'
	WHERE ID = i_droneid;
END IF;
-- End of solution
END //
DELIMITER ;

-- ID: 18a
-- Author: agoyal89
-- Name: dronetech_order_details
DROP PROCEDURE IF EXISTS dronetech_order_details;
DELIMITER //
CREATE PROCEDURE dronetech_order_details(
	   IN i_username VARCHAR(40),
       IN i_orderid VARCHAR(40)
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS dronetech_order_details_result;

CREATE TABLE dronetech_order_details_result AS
SELECT 
	CONCAT(uc.FirstName, ' ', uc.LastName) AS "Customer Name",
    o.ID AS "ORDER ID",
    SUM(n.Quantity * ci.Price) AS 'Total Amount',
    SUM(n.Quantity) AS 'Total Items',
    o.OrderDate AS 'Date of Purchase',
    d.ID AS 'Drone ID',
    CONCAT(ut.FirstName, ' ', ut.LastName) AS 'Store Associate',
    o.OrderStatus AS Status, 
    CONCAT(uc.Street, ', ', uc.City, ', ', uc.State, ' ', uc.Zipcode) AS Address
FROM
    ORDERS o
        LEFT JOIN
    DRONE d ON o.DroneID = d.ID
        LEFT JOIN
    CONTAINS n ON o.ID = n.OrderID
        LEFT JOIN
    CHAIN_ITEM ci ON ci.ChainItemName = n.ItemName
        AND ci.ChainName = n.ChainName
        AND ci.PLUNumber = n.PLUNumber
        LEFT JOIN
	USERS uc ON o.CustomerUsername = uc.Username
		LEFT JOIN 
	USERS ut ON d.DroneTech = ut.Username
GROUP BY o.ID
HAVING o.ID = i_orderid;

-- End of solution
END //
DELIMITER ;


-- ID: 18b
-- Author: agoyal89
-- Name: dronetech_order_items
DROP PROCEDURE IF EXISTS dronetech_order_items;
DELIMITER //
CREATE PROCEDURE dronetech_order_items(
        IN i_username VARCHAR(40),
    	IN i_orderid INT
)
BEGIN
-- Type solution below
DROP TABLE IF EXISTS dronetech_order_items_result;

CREATE TABLE dronetech_order_items_result AS
SELECT 
    ItemName AS ITEM, Quantity AS Count
FROM
    CONTAINS
WHERE
    OrderID = i_orderid;
-- End of solution
END //
DELIMITER ;

-- ID: 19a
-- Author: agoyal89
-- Name: dronetech_assigned_drones
DROP PROCEDURE IF EXISTS dronetech_assigned_drones;
DELIMITER //
CREATE PROCEDURE dronetech_assigned_drones(
        IN i_username VARCHAR(40),
    	IN i_droneid INT,
    	IN i_status VARCHAR(20)
)
BEGIN
-- Type solution below
IF i_status = "ALL" THEN
	SELECT NULL INTO i_status;
END IF;

DROP TABLE IF EXISTS dronetech_assigned_drones_result;
IF i_droneid IS NOT NULL AND i_status IS NOT NULL THEN
	CREATE TABLE dronetech_assigned_drones_result AS
	SELECT 
		d.ID AS 'Drone ID', d.DroneStatus AS Status, Radius
	FROM
		DRONE d
			JOIN
		DRONE_TECH t ON d.DroneTech = t.Username
	WHERE
		t.Username = i_username
			AND d.ID = i_droneid
			AND d.DroneStatus = i_status;
ELSEIF i_droneid IS NOT NULL AND i_status IS NULL THEN
	CREATE TABLE dronetech_assigned_drones_result AS
	SELECT 
		d.ID AS 'Drone ID', d.DroneStatus AS Status, Radius
	FROM
		DRONE d
			JOIN
		DRONE_TECH t ON d.DroneTech = t.Username
	WHERE
		t.Username = i_username
			AND d.ID = i_droneid;
ELSEIF i_droneid IS NULL AND i_status IS NOT NULL THEN
	CREATE TABLE dronetech_assigned_drones_result AS
	SELECT 
		d.ID AS 'Drone ID', d.DroneStatus AS Status, Radius
	FROM
		DRONE d
			JOIN
		DRONE_TECH t ON d.DroneTech = t.Username
	WHERE
		t.Username = i_username
			AND d.DroneStatus = i_status;
ELSE 
	CREATE TABLE dronetech_assigned_drones_result AS
	SELECT 
		d.ID AS 'Drone ID', d.DroneStatus AS Status, Radius
	FROM
		DRONE d
			JOIN
		DRONE_TECH t ON d.DroneTech = t.Username
	WHERE
		t.Username = i_username;
END IF;
-- DROP TABLE IF EXISTS dronetech_assigned_drones_result;
-- CREATE TABLE dronetech_assigned_drones_result AS SELECT i_username,i_droneid,i_status;
-- End of solution
END //
DELIMITER ;
