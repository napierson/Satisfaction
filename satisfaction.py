# My first approach for a Satisfactory supply chain calculator utility.
# Took an object-oriented approach, writing a Factor class with
# appropriate instance variables and methods.

PLURALS = {"miner": "miners", "smelter": "smelters", "constructor": "constructors",\
			"assembler": "assemblers", "foundry": "foundries"}

class Factor:
	def __init__(self, name, out_rate, machine_name):
		self.name = name
		self.ingredients = []
		self.out_rate = out_rate
		self.machine_name = machine_name

	def run_machines(self, n):
		if n == 1:
			m_name = self.machine_name
		else:
			m_name = PLURALS[self.machine_name]
		print("Running %d %s %s produces %d u/min" % (n, self.name, m_name, n * self.out_rate))
		if self.ingredients:
			print("This requires:")
			self.requirements(n)
		print()			

	def requirements(self, n):
		for ing in self.ingredients:
				ing_name = ing[0].name
				ing_rate = n * ing[1]
				ing_ct = ing_rate / ing[0].out_rate
				if ing_ct == 1:
					m_name = ing[0].machine_name
				else:
					m_name = PLURALS[ing[0].machine_name]
				print("%.2f %s %s (%d u/min)" % (ing_ct, ing_name, m_name, ing_rate))
				ing[0].requirements(ing_ct)

iron_ore = Factor("Iron Ore", 60, "miner")

iron_ingot = Factor("Iron Ingot", 30, "smelter")
iron_ingot.ingredients.append((iron_ore, 30))

iron_plate = Factor("Iron Plate", 15, "constructor")
iron_plate.ingredients.append((iron_ingot, 30))

iron_rod = Factor("Iron Rod", 15, "constructor")
iron_rod.ingredients.append((iron_ingot, 15))

screw = Factor("Screw", 90, "assembler")
screw.ingredients.append((iron_rod, 15))

reinforced_iron_plate = Factor("Reinforced Iron Plate", 5, "assembler")
reinforced_iron_plate.ingredients.append((iron_plate, 20))
reinforced_iron_plate.ingredients.append((screw, 120))

coal = Factor("Coal", 60, "miner")

steel_ingot = Factor("Steel Ingot", 30, "foundry")
steel_ingot.ingredients.append((coal, 45))
steel_ingot.ingredients.append((iron_ore, 45))

steel_ingot2 = Factor("Alternate Steel Ingot", 45, "foundry")
steel_ingot2.ingredients = [(iron_ingot, 22.5), (coal, 45)]

sulfur = Factor("Sulfur", 60, "miner")

compacted_coal = Factor("Compacted Coal", 30, "assembler")
compacted_coal.ingredients = [(coal, 30), (sulfur, 30)]

steel_ingot3 = Factor("Third Steel Ingot", 45, "foundry")
steel_ingot3.ingredients = [(iron_ore, 45), (compacted_coal, 22.5)]

reinforced_iron_plate.run_machines(3)