-- Database Table Creation DDL Statements
-- ----------------------------------------------

-- Create SalesPerson Table
CREATE TABLE SalesPerson (
    SalesPersonID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL
);

-- Create Customer Table
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    State CHAR(2) NOT NULL,
    SalesPersonID INT NOT NULL,
    FOREIGN KEY (SalesPersonID) REFERENCES SalesPerson(SalesPersonID)
);

-- Create OrderHeader Table
CREATE TABLE OrderHeader (
    OrderNumber INT PRIMARY KEY,
    OrderDate DATE NOT NULL,
    CustomerID INT NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- Create OrderDetail Table
CREATE TABLE OrderDetail (
    DetailID INT PRIMARY KEY,
    OrderNumber INT NOT NULL,
    ItemName VARCHAR(100) NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (OrderNumber) REFERENCES OrderHeader(OrderNumber)
);

-- Function to Convert USD to Euro
-- ----------------------------------------------

CREATE FUNCTION dbo.ConvertUSDtoEuro (@PriceUSD DECIMAL(10,2))
RETURNS DECIMAL(10,2)
AS
BEGIN
    -- Assuming a conversion rate of 1 USD = 0.85 Euro (this would be updated regularly)
    DECLARE @PriceEuro DECIMAL(10,2);
    SET @PriceEuro = @PriceUSD * 0.85;
    RETURN @PriceEuro;
END;
GO

-- Stored Procedure to Insert a New Sales Person
-- ----------------------------------------------

CREATE PROCEDURE dbo.InsertSalesPerson
    @SalesPersonID INT,
    @FirstName VARCHAR(50),
    @LastName VARCHAR(50)
AS
BEGIN
    -- Check if the SalesPersonID already exists
    IF NOT EXISTS (SELECT 1 FROM SalesPerson WHERE SalesPersonID = @SalesPersonID)
    BEGIN
        INSERT INTO SalesPerson (SalesPersonID, FirstName, LastName)
        VALUES (@SalesPersonID, @FirstName, @LastName);
        
        SELECT 'Sales person added successfully' AS Result;
    END
    ELSE
    BEGIN
        SELECT 'Error: Sales person ID already exists' AS Result;
    END
END;
GO

-- Database Views
-- ----------------------------------------------

-- View for Customers and their Sales Persons
CREATE VIEW vw_CustomerSalesPerson AS
SELECT 
    c.CustomerID,
    c.Name AS CustomerName,
    c.State,
    s.SalesPersonID,
    s.FirstName + ' ' + s.LastName AS SalesPersonName
FROM 
    Customer c
JOIN 
    SalesPerson s ON c.SalesPersonID = s.SalesPersonID;
GO

-- View for Most Expensive Item Purchased by Each Customer
CREATE VIEW vw_MostExpensiveItemByCustomer AS
SELECT 
    c.CustomerID,
    c.Name AS CustomerName,
    MAX(od.Price) AS MostExpensiveItemPrice,
    (SELECT TOP 1 ItemName 
     FROM OrderDetail od2 
     JOIN OrderHeader oh2 ON od2.OrderNumber = oh2.OrderNumber 
     WHERE oh2.CustomerID = c.CustomerID AND od2.Price = MAX(od.Price)) AS ItemName
FROM 
    Customer c
JOIN 
    OrderHeader oh ON c.CustomerID = oh.CustomerID
JOIN 
    OrderDetail od ON oh.OrderNumber = od.OrderNumber
GROUP BY 
    c.CustomerID, c.Name;
GO

-- View for Most Expensive Item Sold by Each Sales Person
CREATE VIEW vw_MostExpensiveItemBySalesPerson AS
SELECT 
    s.SalesPersonID,
    s.FirstName + ' ' + s.LastName AS SalesPersonName,
    MAX(od.Price) AS MostExpensiveItemPrice,
    (SELECT TOP 1 od2.ItemName 
     FROM OrderDetail od2 
     JOIN OrderHeader oh2 ON od2.OrderNumber = oh2.OrderNumber 
     JOIN Customer c2 ON oh2.CustomerID = c2.CustomerID 
     WHERE c2.SalesPersonID = s.SalesPersonID AND od2.Price = MAX(od.Price)) AS ItemName
FROM 
    SalesPerson s
JOIN 
    Customer c ON s.SalesPersonID = c.SalesPersonID
JOIN 
    OrderHeader oh ON c.CustomerID = oh.CustomerID
JOIN 
    OrderDetail od ON oh.OrderNumber = od.OrderNumber
GROUP BY 
    s.SalesPersonID, s.FirstName + ' ' + s.LastName;
GO

-- View for Total Purchase Amount by Item for Each Customer
CREATE VIEW vw_TotalPurchaseByItemAndCustomer AS
SELECT 
    c.CustomerID,
    c.Name AS CustomerName,
    od.ItemName,
    SUM(od.Quantity * od.Price) AS TotalAmount
FROM 
    Customer c
JOIN 
    OrderHeader oh ON c.CustomerID = oh.CustomerID
JOIN 
    OrderDetail od ON oh.OrderNumber = od.OrderNumber
GROUP BY 
    c.CustomerID, c.Name, od.ItemName;
GO

-- Sample Data Insertion for Tables
-- ----------------------------------------------

-- Insert data into SalesPerson
INSERT INTO SalesPerson (SalesPersonID, FirstName, LastName) VALUES
(1, 'John', 'Doe'),
(2, 'Jane', 'Smith'),
(3, 'Robert', 'Johnson'),
(4, 'Emily', 'Williams'),
(5, 'Michael', 'Brown'),
(6, 'Sarah', 'Jones'),
(7, 'David', 'Miller'),
(8, 'Lisa', 'Davis'),
(9, 'Thomas', 'Wilson'),
(10, 'Jessica', 'Taylor'),
(11, 'Daniel', 'Anderson'),
(12, 'Jennifer', 'Thomas'),
(13, 'Christopher', 'Jackson'),
(14, 'Amanda', 'White'),
(15, 'Matthew', 'Harris'),
(16, 'Elizabeth', 'Martin'),
(17, 'Andrew', 'Thompson'),
(18, 'Olivia', 'Garcia'),
(19, 'James', 'Martinez'),
(20, 'Sophia', 'Robinson'),
(21, 'Ryan', 'Clark'),
(22, 'Emma', 'Rodriguez'),
(23, 'Joshua', 'Lewis'),
(24, 'Abigail', 'Lee'),
(25, 'Brandon', 'Walker');

-- Insert data into Customer
INSERT INTO Customer (CustomerID, Name, State, SalesPersonID) VALUES
(101, 'Acme Corporation', 'CA', 1),
(102, 'Globex Inc.', 'NY', 2),
(103, 'Soylent Corp', 'IL', 3),
(104, 'Initech', 'TX', 4),
(105, 'Umbrella Corp', 'WA', 5),
(106, 'Stark Industries', 'CA', 6),
(107, 'Wayne Enterprises', 'NJ', 7),
(108, 'Cyberdyne Systems', 'CA', 8),
(109, 'Massive Dynamic', 'NY', 9),
(110, 'LexCorp', 'DE', 10),
(111, 'Oscorp Industries', 'NY', 11),
(112, 'Tyrell Corporation', 'CA', 12),
(113, 'Weyland-Yutani', 'OR', 13),
(114, 'Dharma Initiative', 'FL', 14),
(115, 'Omni Consumer Products', 'MI', 15),
(116, 'Aperture Science', 'OH', 16),
(117, 'Black Mesa Research', 'NM', 17),
(118, 'Abstergo Industries', 'VA', 18),
(119, 'Rekall Inc.', 'CA', 19),
(120, 'Monsters Inc.', 'CA', 20),
(121, 'Dunder Mifflin', 'PA', 21),
(122, 'Wonka Industries', 'VT', 22),
(123, 'Gringotts', 'NY', 23),
(124, 'Los Pollos Hermanos', 'NM', 24),
(125, 'Sterling Cooper', 'NY', 25);

-- Insert data into OrderHeader
INSERT INTO OrderHeader (OrderNumber, OrderDate, CustomerID) VALUES
(1001, '2025-01-15', 101),
(1002, '2025-01-18', 102),
(1003, '2025-01-20', 103),
(1004, '2025-01-22', 104),
(1005, '2025-01-25', 105),
(1006, '2025-01-28', 106),
(1007, '2025-02-01', 107),
(1008, '2025-02-05', 108),
(1009, '2025-02-08', 109),
(1010, '2025-02-10', 110),
(1011, '2025-02-15', 111),
(1012, '2025-02-18', 112),
(1013, '2025-02-20', 113),
(1014, '2025-02-25', 114),
(1015, '2025-03-01', 115),
(1016, '2025-03-05', 116),
(1017, '2025-03-10', 117),
(1018, '2025-03-15', 118),
(1019, '2025-03-20', 119),
(1020, '2025-03-25', 120),
(1021, '2025-04-01', 121),
(1022, '2025-04-05', 122),
(1023, '2025-04-10', 123),
(1024, '2025-04-15', 124),
(1025, '2025-04-20', 125);

-- Insert data into OrderDetail
INSERT INTO OrderDetail (DetailID, OrderNumber, ItemName, Quantity, Price) VALUES
(10001, 1001, 'Laptop', 2, 1200.00),
(10002, 1001, 'Mouse', 3, 25.50),
(10003, 1002, 'Desktop Computer', 1, 1500.00),
(10004, 1002, 'Keyboard', 2, 45.75),
(10005, 1003, 'Printer', 1, 350.00),
(10006, 1003, 'Ink Cartridge', 4, 65.25),
(10007, 1004, 'Monitor', 2, 275.50),
(10008, 1004, 'HDMI Cable', 3, 15.99),
(10009, 1005, 'Tablet', 1, 599.99),
(10010, 1005, 'Tablet Case', 1, 49.99),
(10011, 1006, 'Smartphone', 2, 899.99),
(10012, 1006, 'Screen Protector', 3, 12.50),
(10013, 1007, 'External Hard Drive', 1, 129.99),
(10014, 1007, 'USB Drive', 5, 19.99),
(10015, 1008, 'Webcam', 1, 79.99),
(10016, 1008, 'Microphone', 1, 149.99),
(10017, 1009, 'Gaming Console', 1, 499.99),
(10018, 1009, 'Game Controller', 2, 59.99),
(10019, 1010, 'Router', 1, 189.99),
(10020, 1010, 'Network Cable', .5, 9.99),
(10021, 1011, 'Wireless Headphones', 1, 249.99),
(10022, 1011, 'Charging Stand', 1, 45.50),
(10023, 1012, 'Smart Speaker', 2, 129.99),
(10024, 1012, 'Smart Plug', 4, 24.99),
(10025, 1013, 'Fitness Tracker', 1, 149.99),
(10026, 1013, 'Replacement Band', 2, 19.99),
(10027, 1014, 'Virtual Reality Headset', 1, 399.99),
(10028, 1014, 'VR Controller', 2, 89.99),
(10029, 1015, 'Drone', 1, 799.99),
(10030, 1015, 'Extra Battery', 2, 79.99),
(10031, 1016, 'Digital Camera', 1, 599.99),
(10032, 1016, 'Camera Lens', 1, 349.99),
(10033, 1017, 'Bluetooth Speaker', 2, 129.99),
(10034, 1017, 'Portable Charger', 1, 59.99),
(10035, 1018, 'Smart Watch', 1, 299.99),
(10036, 1018, 'Watch Band', 2, 29.99),
(10037, 1019, 'E-reader', 1, 149.99),
(10038, 1019, 'E-reader Cover', 1, 39.99),
(10039, 1020, 'Projector', 1, 699.99),
(10040, 1020, 'Projection Screen', 1, 129.99),
(10041, 1021, 'Office Chair', 3, 249.99),
(10042, 1021, 'Desk Lamp', 5, 45.99),
(10043, 1022, 'Computer Desk', 2, 329.99),
(10044, 1022, 'Cable Management Kit', 2, 24.99),
(10045, 1023, 'Docking Station', 1, 159.99),
(10046, 1023, 'Wireless Mouse', 2, 49.99),
(10047, 1024, 'Graphics Tablet', 1, 279.99),
(10048, 1024, 'Stylus Pen', 1, 89.99),
(10049, 1025, 'Mechanical Keyboard', 1, 149.99),
(10050, 1025, 'Wrist Rest', 1, 24.99);