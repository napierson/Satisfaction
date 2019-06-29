# A shell script for entering new rows or altering existing rows
# in my Satisfactory database. I just fill in an empty list
# with new tuple(s) and bam.

import sqlite3

conn = sqlite3.connect("satisfaction.db")
c = conn.cursor()

#('p_name', 'm_name', out_rate)
new_products = []
if new_products:
	c.execute("PRAGMA foreign_keys = ON")
	c.executemany("INSERT INTO products VALUES (?, ?, ?)", new_products)

#('out_name', 'in_name', in_rate)
new_requirements = []
if new_requirements:
	c.execute("PRAGMA foreign_keys = ON")
	c.executemany("INSERT INTO requires VALUES (?, ?, ?)", new_requirements)

#('m_name', power_used)
new_buildings = []
if new_buildings:
	c.executemany("INSERT INTO power VALUES (?, ?)", new_buildings)

for row in c.execute("SELECT * FROM products"):
	print(row)
print()

for row in c.execute("SELECT * FROM requires"):
	print(row)
print()

for row in c.execute("SELECT * FROM power"):
	print(row)
print()

#c.execute("UPDATE [table] SET col_name = value WHERE col_name = value")

conn.commit()
conn.close()