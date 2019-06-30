# However, since the data is so nicely structured, it seemed to make sense to move it
# to an SQLite database. This also means that I don't need to recreate the contents of
# the database every time I want to run a single query; I can persistently store the
# records on my hard drive.

PLURALS = {"miner": "miners", "smelter": "smelters", "constructor": "constructors",\
			"assembler": "assemblers", "foundry": "foundries", "manufacturer": "manufacturers"}

import sqlite3
conn = sqlite3.connect("satisfaction.db")
c = conn.cursor()

def run_machines(name, n):
	c.execute("SELECT m_name, out_rate FROM products WHERE p_name=?", (name,))
	m_name, out_rate = c.fetchone()

	c.execute("SELECT power_used FROM power WHERE m_name=?", (m_name,))
	power_used = n * c.fetchone()[0]

	if n != 1:
		m_name = PLURALS[m_name]
	print("Running %d %s %s produces %d u/min" % (n, name, m_name, n * out_rate))

	c.execute("SELECT * FROM requires WHERE out_name=?", (name,))
	ingredients = c.fetchall()
	if ingredients:
		print("This requires:")
		power_used += requirements(name, n)
		
	print("\nThis consumes %.2f MW of power\n" % power_used)

def requirements(name, n):
	power_used = 0

	c.execute("SELECT in_name, in_rate FROM requires WHERE out_name=?", (name,))
	ingredients = c.fetchall()
	for ing in ingredients:
		ing_name = ing[0]
		ing_required = n * ing[1]

		c.execute("SELECT m_name, out_rate FROM products WHERE p_name=?", (ing_name,))
		ing_mname, ing_rate = c.fetchone()
		ing_ct = ing_required / ing_rate

		c.execute("SELECT power_used FROM power WHERE m_name=?", (ing_mname,))
		ing_power = ing_ct * c.fetchone()[0]
		power_used += ing_power

		if ing_ct != 1:
			ing_mname = PLURALS[ing_mname]

		print("%.2f %s %s (%d u/min)" % (ing_ct, ing_name, ing_mname, ing_required))
		
		power_used += requirements(ing_name, ing_ct)
	return power_used

run_machines('Screw', 8)
run_machines('Screw 2', 8)
conn.close()