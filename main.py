# import xml.etree.ElementTree as ET
# import sqlite3
# import xml.dom.minidom
#
# # Connect to SQLite database and create cursor
# conn = sqlite3.connect('data.sqlite')
# cursor = conn.cursor()
#
# # Execute SQL query to select product data from multiple tables
# cursor.execute('''SELECT product.product_id, product.model, product.image, product.manufacturer_id, product.price, product.status, product.ean, product.quantity, manufacturer.name, product_description.name, product_description.description
#                   FROM product
#                   JOIN manufacturer ON product.manufacturer_id = manufacturer.manufacturer_id
#                   JOIN product_description ON product.product_id = product_description.product_id
#                   JOIN product_image ON product.product_id = product_image.product_id
#                   WHERE product.status = '1'
#                   ''')
#
# # Fetch all products from the query
# products = cursor.fetchall()
#
# # Create root element and channel element for the XML tree
# root = ET.Element('rss', {'xmlns:g': 'http://base.google.com/ns/1.0', 'version': '2.0'})
# channel = ET.SubElement(root, 'channel')
#
# # Add title, link, and description elements to the channel element
# ET.SubElement(channel, 'title').text = 'Example - Butopea Store'
# ET.SubElement(channel, 'link').text = 'https://butopea.com'
# ET.SubElement(channel, 'description').text = 'This is Task1'
#
# # Iterate through products to add item elements to the channel
# for product in products:
#     product_id, model, image, manufacturer_id, price, status, ean, quantity, manufacturer, name, description = product
#     item = ET.SubElement(channel, 'item')
#     ET.SubElement(item, 'g:id').text = product_id
#     ET.SubElement(item, 'g:title').text = name
#     ET.SubElement(item, 'g:description').text = description
#     ET.SubElement(item, 'g:link').text = f'https://butopea.com/p/{product_id}'
#     ET.SubElement(item, 'g:image_link').text = f'https://butopea.com/image/catalog/{image}'
#     ET.SubElement(item, 'g:condition').text = 'new'
#     ET.SubElement(item, 'g:availability').text = 'in stock'
#     ET.SubElement(item, 'g:price').text = f'{price} HUF'
#     ET.SubElement(item, 'g:brand').text = manufacturer
#     ET.SubElement(item, 'g:gtin').text = ean
#     # Fetch additional images for the product and add them as additional_image_link elements
#     cursor.execute('''SELECT product_image.image, product_image.sort_order FROM product_image WHERE
#                         product_image.product_id = ?''', (product_id,))
#     images = cursor.fetchall()
#     for i in images:
#         image_link, sort_order = i
#         ET.SubElement(item, 'g:additional_image_link',
#                       {'g:image_link': f'https://butopea.com/image/catalog/{image_link}', 'g:sort_order': sort_order})
#
# # Create an ElementTree from the root element
# tree = ET.ElementTree(root)
# # Write the tree to a file named 'feed.xml' with UTF-8 encoding and xml declaration
# tree.write("feed.xml", encoding="UTF-8", xml_declaration=True)
#
# dom = xml.dom.minidom.parse('feed.xml')  # or xml.dom.minidom.parseString(xml_string)
# pretty_xml_as_string = dom.toprettyxml()
#
# with open('feed.xml', 'w') as f:
#     f.write(pretty_xml_as_string)
#
# conn.close()


import xml.etree.ElementTree as ET
import sqlite3
import xml.dom.minidom

# Connect to SQLite database and create cursor
conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()

# Execute SQL query to select product data from multiple tables
cursor.execute("SELECT product_id, manufacturer_id, price, image, quantity FROM product WHERE status = '1'")

product_id = [] #done
manufacturer_id = [] #done
price = [] #done
brand = []
title = []
description = []
image = []
quantity = []
products = cursor.fetchall()

for product in products:
    product_id.append(product[0])
    manufacturer_id.append(product[1])
    price.append(product[2])
    image.append(product[3])
    quantity.append(int(product[4]))
    cursor.execute("SELECT name FROM manufacturer where manufacturer_id=?", (product[1],))
    brand.append(cursor.fetchall())
    cursor.execute("SELECT name FROM product_description where product_id=?", (product[0],))
    title.append(cursor.fetchall())
    cursor.execute("SELECT description FROM product_description where product_id=?", (product[0],))
    description.append(cursor.fetchall())
    cursor.execute("SELECT image FROM product_image where  sort_order!='0' and product_id=?",
                   (product[0],))
    image.append(cursor.fetchall())

image = [image[i].split() + image[i + 1] for i in range(0, len(image), 2)]




# Create root element and channel element for the XML tree
root = ET.Element('rss', {'xmlns:g': 'http://base.google.com/ns/1.0', 'version': '2.0'})
channel = ET.SubElement(root, 'channel')

# Add title, link, and description elements to the channel element
ET.SubElement(channel, 'title').text = 'Example - Butopea Store'
ET.SubElement(channel, 'link').text = 'https://butopea.com'
ET.SubElement(channel, 'description').text = 'This is Task1'

counter = 0

for i in range(len(product_id)):
    item = ET.SubElement(channel, 'item')
    ET.SubElement(item, 'g:id').text = product_id[counter]
    ET.SubElement(item, 'g:title').text = title[counter][0][0]
    ET.SubElement(item, 'g:description').text = description[counter][0][0]
    ET.SubElement(item, 'g:link').text = f'https://butopea.com/p/{product_id[counter]}'
    ET.SubElement(item, 'g:image_link').text = f'https://butopea.com/{image[counter][0]}'
    x = 0
    # for index in image:
    #     for j in range(len(index)):
    #         if j==0 and i!=x:
    #             continue
    #         else:
    #             ET.SubElement(item, 'g:additional_image_link').text = f'https://butopea.com/{index[j][0]}'
    #     x+=1
    ET.SubElement(item, 'g:availability').text = 'in stock' if quantity[counter]>0 else 'out of stock'
    ET.SubElement(item, 'g:price').text = f'{price[counter]} HUF'
    ET.SubElement(item, 'g:brand').text = brand[counter][0][0]
    ET.SubElement(item, 'g:condition').text = 'new'

    counter+=1


# Create an ElementTree from the root element
tree = ET.ElementTree(root)
# Write the tree to a file named 'feed.xml' with UTF-8 encoding and xml declaration
tree.write("feed.xml", encoding="UTF-8", xml_declaration=True)

dom = xml.dom.minidom.parse('feed.xml')  # or xml.dom.minidom.parseString(xml_string)
pretty_xml_as_string = dom.toprettyxml()

with open('feed.xml', 'w') as f:
    f.write(pretty_xml_as_string)

conn.close()
