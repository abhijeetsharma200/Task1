import sqlite3
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()

query = '''
SELECT product.product_id, product.model, product_description.name, product_description.description, product.manufacturer_id, product.price, product_image.image
FROM product
JOIN product_description ON product.product_id = product_description.product_id
JOIN product_image ON product.product_id = product_image.product_id
WHERE product.status = '1'
'''

cursor.execute(query)

results = cursor.fetchall()

feed = Element('feed')

for row in results:
    product = SubElement(feed, 'product')
    id = SubElement(product, 'id')
    id.text = str(row[0])
    title = SubElement(product, 'title')
    title.text = row[1]
    description = SubElement(product, 'description')
    description.text = row[2]
    link = SubElement(product, 'link')
    link.text = 'https://butopea.com/p/' + str(row[0])
    image_link = SubElement(product, 'image_link')
    image_link.text = 'https://butopea.com/image/catalog/' + row[6]
    additional_image_link = SubElement(product, 'additional_image_link')
    additional_image_link.text = 'https://butopea.com/image/catalog/' + row[6]
    availability = SubElement(product, 'availability')
    availability.text = 'in stock'
    price = SubElement(product, 'price')
    price.text = str(row[5]) + ' HUF'
    brand = SubElement(product, 'brand')
    brand.text = row[4]
    condition = SubElement(product, 'condition')
    condition.text = 'new'

xml_str = tostring(feed, encoding='unicode', method='xml')
xml_str = minidom.parseString(xml_str).toprettyxml()

with open('feed.xml', 'w') as f:
    f.write(xml_str)

conn.close()
