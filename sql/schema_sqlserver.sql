/* RetailPulse modernized SQL Server schema
   Based on the original Customer Sales Database System project.
*/
CREATE TABLE dbo.SalesPerson (
    SalesPersonID INT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL
);
GO
CREATE TABLE dbo.Customer (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    State CHAR(2) NOT NULL,
    SalesPersonID INT NOT NULL,
    CONSTRAINT FK_Customer_SalesPerson FOREIGN KEY (SalesPersonID)
        REFERENCES dbo.SalesPerson(SalesPersonID)
);
GO
CREATE TABLE dbo.Product (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL UNIQUE,
    Category VARCHAR(80) NOT NULL,
    ListPrice DECIMAL(12,2) NOT NULL CHECK (ListPrice >= 0)
);
GO
CREATE TABLE dbo.OrderHeader (
    OrderNumber INT PRIMARY KEY,
    OrderDate DATE NOT NULL,
    CustomerID INT NOT NULL,
    OrderStatus VARCHAR(20) NOT NULL DEFAULT 'Completed',
    CONSTRAINT FK_OrderHeader_Customer FOREIGN KEY (CustomerID)
        REFERENCES dbo.Customer(CustomerID)
);
GO
CREATE TABLE dbo.OrderDetail (
    DetailID INT PRIMARY KEY,
    OrderNumber INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(12,2) NOT NULL CHECK (UnitPrice >= 0),
    CONSTRAINT FK_OrderDetail_OrderHeader FOREIGN KEY (OrderNumber)
        REFERENCES dbo.OrderHeader(OrderNumber),
    CONSTRAINT FK_OrderDetail_Product FOREIGN KEY (ProductID)
        REFERENCES dbo.Product(ProductID)
);
GO
CREATE OR ALTER FUNCTION dbo.ConvertUSDtoEuro (@PriceUSD DECIMAL(12,2), @Rate DECIMAL(10,4) = 0.85)
RETURNS DECIMAL(12,2)
AS
BEGIN
    RETURN ROUND(@PriceUSD * @Rate, 2);
END;
GO
CREATE OR ALTER PROCEDURE dbo.InsertSalesPerson
    @SalesPersonID INT,
    @FirstName VARCHAR(50),
    @LastName VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    IF EXISTS (SELECT 1 FROM dbo.SalesPerson WHERE SalesPersonID = @SalesPersonID)
        THROW 50001, 'SalesPersonID already exists.', 1;
    INSERT INTO dbo.SalesPerson (SalesPersonID, FirstName, LastName)
    VALUES (@SalesPersonID, @FirstName, @LastName);
END;
GO
CREATE OR ALTER VIEW dbo.vw_SalesFacts AS
SELECT
    oh.OrderNumber,
    oh.OrderDate,
    oh.OrderStatus,
    c.CustomerID,
    c.CustomerName,
    c.State,
    sp.SalesPersonID,
    CONCAT(sp.FirstName, ' ', sp.LastName) AS SalesPersonName,
    p.ProductID,
    p.ProductName,
    p.Category,
    od.Quantity,
    od.UnitPrice,
    CAST(od.Quantity * od.UnitPrice AS DECIMAL(14,2)) AS LineRevenue
FROM dbo.OrderDetail od
JOIN dbo.OrderHeader oh ON oh.OrderNumber = od.OrderNumber
JOIN dbo.Customer c ON c.CustomerID = oh.CustomerID
JOIN dbo.SalesPerson sp ON sp.SalesPersonID = c.SalesPersonID
JOIN dbo.Product p ON p.ProductID = od.ProductID;
GO
