# Task1

This project is a Python script that retrieves product data from a SQLite database, and creates an XML file for a Google Shopping feed.

# Requirements
Python 3
xml.etree.ElementTree
sqlite3
xml.dom.minidom
# How to use
Connect to a SQLite database and create a cursor.
Execute a SQL query to select product data from multiple tables.
Iterate through the results of the query, and retrieve additional data from the manufacturer and product_description tables using the product_id and manufacturer_id.
Create the XML tree using xml.etree.ElementTree, and add the relevant data to the tree.
Write the tree to an XML file named 'feed.xml' with UTF-8 encoding and xml declaration.
Use xml.dom.minidom to format the xml file.

# TODO
Also the additional image link section is commented out and the current implementation is not able to add additional image links.




