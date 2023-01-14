# import sqlite3
# from xml.etree.ElementTree import Element, SubElement, tostring
# from xml.dom import minidom
#
# conn = sqlite3.connect('data.sqlite')
# cursor = conn.cursor()
#
# query = '''
# SELECT product.product_id, product.model, product_description.name, product_description.description, product.manufacturer_id, product.price, product_image.image
# FROM product
# JOIN product_description ON product.product_id = product_description.product_id
# JOIN product_image ON product.product_id = product_image.product_id
# WHERE product.status = '1'
# '''
#
# cursor.execute(query)
#
# results = cursor.fetchall()
#
# feed = Element('feed')
#
# for row in results:
#     print()
#     product = SubElement(feed, 'product')
#     id = SubElement(product, 'id')
#     id.text = str(row[0])
#     title = SubElement(product, 'title')
#     title.text = row[1]
#     description = SubElement(product, 'description')
#     description.text = row[2]
#     link = SubElement(product, 'link')
#     link.text = 'https://butopea.com/p/' + str(row[0])
#     image_link = SubElement(product, 'image_link')
#     image_link.text = 'https://butopea.com/image/catalog/' + row[6]
#     additional_image_link = SubElement(product, 'additional_image_link')
#     additional_image_link.text = 'https://butopea.com/image/catalog/' + row[6]
#     availability = SubElement(product, 'availability')
#     availability.text = 'in stock'
#     price = SubElement(product, 'price')
#     price.text = str(row[5]) + ' HUF'
#     brand = SubElement(product, 'brand')
#     brand.text = row[4]
#     condition = SubElement(product, 'condition')
#     condition.text = 'new'
#
# xml_str = tostring(feed, encoding='unicode', method='xml')
# xml_str = minidom.parseString(xml_str).toprettyxml()
#
# with open('feed.xml', 'w') as f:
#     f.write(xml_str)
#
# conn.close()


import xml.etree.ElementTree as ET
import sqlite3
import xml.dom.minidom

conn = sqlite3.connect('data.sqlite')
cursor = conn.cursor()

cursor.execute('''SELECT product.product_id, product.model, product.image, product.manufacturer_id, product.price, product.status, product.ean, product.quantity, manufacturer.name, product_description.name, product_description.description
                  FROM product
                  JOIN manufacturer ON product.manufacturer_id = manufacturer.manufacturer_id
                  JOIN product_description ON product.product_id = product_description.product_id
                  JOIN product_image ON product.product_id = product_image.product_id
                  WHERE product.status = '1'
                  ''')

products = cursor.fetchall()

root = ET.Element('rss', {'xmlns:g': 'http://base.google.com/ns/1.0', 'version': '2.0'})
channel = ET.SubElement(root, 'channel')
ET.SubElement(channel, 'title').text = 'Example - Butopea Store'
ET.SubElement(channel, 'link').text = 'https://butopea.com'
ET.SubElement(channel, 'description').text = 'This is Task1'

for product in products:
    product_id, model, image, manufacturer_id, price, status, ean, quantity, manufacturer, name, description = product
    item = ET.SubElement(channel, 'item')
    ET.SubElement(item, 'g:id').text = product_id
    ET.SubElement(item, 'g:title').text = name
    ET.SubElement(item, 'g:description').text = description
    ET.SubElement(item, 'g:link').text = f'https://butopea.com/p/{product_id}'
    ET.SubElement(item, 'g:image_link').text = f'https://butopea.com/image/catalog/{image}'
    ET.SubElement(item, 'g:condition').text = 'new'
    ET.SubElement(item, 'g:availability').text = 'in stock'
    ET.SubElement(item, 'g:price').text = f'{price} HUF'
    ET.SubElement(item, 'g:brand').text = manufacturer
    ET.SubElement(item, 'g:gtin').text = ean
    cursor.execute('''SELECT product_image.image, product_image.sort_order FROM product_image WHERE 
                        product_image.product_id = ?''', (product_id,))
    images = cursor.fetchall()
    for i in images:
        image_link, sort_order = i
        ET.SubElement(item, 'g:additional_image_link',
                     {'g:image_link': f'https://butopea.com/image/catalog/{image_link}', 'g:sort_order': sort_order})

tree = ET.ElementTree(root)
tree.write("feed.xml", encoding="UTF-8", xml_declaration=True)


dom = xml.dom.minidom.parse('feed.xml') # or xml.dom.minidom.parseString(xml_string)
pretty_xml_as_string = dom.toprettyxml()

with open('feed.xml', 'w') as f:
    f.write(pretty_xml_as_string)

conn.close()
