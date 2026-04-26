# CodeGrade step0
# Run this cell without changes

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

df_boston = pd.read_sql("""
SELECT e.firstName, e.lastName 
FROM employees e 
JOIN offices o USING(officeCode)
WHERE o.city = 'Boston'                  
                        """, conn)

df_boston

# CodeGrade step2
# Replace None with your code
df_zero_emp = pd.read_sql("""
SELECT o.city, o.country, o.addressLine1 
FROM offices o 
LEFT JOIN employees e USING(officeCode) 
WHERE e.officeCode IS NULL               
                        """, conn)

df_zero_emp

# CodeGrade step3
# Replace None with your code
df_employee = pd.read_sql("""
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees e 
LEFT JOIN offices o USING(officeCode)
ORDER BY firstName, lastName                  
                        """, conn)

df_employee

# CodeGrade step4
# Replace None with your code
df_contacts = pd.read_sql("""
SELECT c.contactfirstname, c.contactlastname, c.phone, salesrepemployeenumber
FROM customers c
LEFT JOIN orders o USING(customerNumber)
WHERE o.customerNumber IS NULL
ORDER BY c.contactlastname
                        """, conn)

df_contacts

# CodeGrade step5
# Replace None with your code
df_payment = pd.read_sql("""
SELECT c.contactfirstname, c.contactlastname, p.paymentdate, p.amount   
FROM customers c 
JOIN payments p USING(customerNumber)
ORDER BY CAST(p.amount AS DECIMAL(10,2)) DESC;
""", conn)

df_payment

# CodeGrade step6
# Replace None with your code

df_credit = pd.read_sql("""
SELECT e.firstName, e.lastName, e.employeenumber, COUNT(c.salesrepemployeenumber) AS number_of_customers
FROM employees e 
JOIN customers c ON e.employeenumber = c.salesrepemployeenumber
GROUP BY e.employeenumber
HAVING AVG(c.creditlimit) > 90000
ORDER BY number_of_customers DESC
                        """, conn)

df_credit

# CodeGrade step7
# Replace None with your code
df_product_sold = pd.read_sql("""
SELECT p.productname, COUNT(od.productcode) AS numorders, SUM(od.quantityordered) AS totalunits
FROM products p 
JOIN orderdetails od ON p.productcode = od.productcode
GROUP BY p.productname
ORDER BY totalunits DESC                    
""", conn)

df_product_sold

# CodeGrade step8
# Replace None with your code
df_total_customers = pd.read_sql("""
SELECT 
    p.productName, 
    p.productCode, 
    COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productName, p.productCode
ORDER BY numpurchasers DESC;
             
""", conn)

df_total_customers

# CodeGrade step9
# Replace None with your code
df_customers = pd.read_sql("""
SELECT COUNT(c.customernumber) AS n_customers, o.officecode, o.city
FROM customers c
JOIN employees e ON c.salesrepemployeenumber = e.employeenumber
JOIN offices o USING(officecode)   
GROUP BY o.officecode  
""", conn)

df_customers

# CodeGrade step10
# Replace None with your code
df_under_20 = pd.read_sql("""
WITH UnderperformingProducts AS (
    -- Subquery: Find products ordered by fewer than 20 customers
    SELECT od.productCode
    FROM orderdetails od
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY od.productCode
    HAVING COUNT(DISTINCT o.customerNumber) < 20
)
SELECT DISTINCT 
    e.employeeNumber, 
    e.firstName, 
    e.lastName, 
    off.city AS officeCity, 
    off.officeCode
FROM employees e
JOIN offices off ON e.officeCode = off.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
WHERE od.productCode IN (SELECT productCode FROM UnderperformingProducts);

""", conn)

df_under_20

# Run this cell without changes

conn.close()