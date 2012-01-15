#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys

if len(sys.argv) != 2:
	print >> sys.stderr, 'Usage: %s <db>' % sys.argv[0]
	sys.exit(1)

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()

cursor.execute('''
	CREATE TABLE ingredients (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name VARCHAR(50),
		quantity INTEGER,
		price INTEGER
	);
''')
cursor.execute('''
	CREATE TABLE recipe_ingredient (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		recipe VARCHAR(50),
		ingredient VARCHAR(50),
		quantity INTEGER
	);
''')

cursor.execute('''
	INSERT INTO ingredients (name, quantity, price)
	VALUES ('Beurre', 250, 150)
''')

cursor.execute('''
	INSERT INTO ingredients (name, quantity, price)
	VALUES ('Farine', 1000, 50)
''')

cursor.execute('''
	INSERT INTO ingredients (name, quantity, price)
	VALUES ('Levure', 250, 50)
''')

cursor.execute('''
	INSERT INTO ingredients (name, quantity, price)
	VALUES ('Sel', 150, 25)
''')

cursor.execute('''
	INSERT INTO ingredients (name, quantity, price)
	VALUES ('Sucre', 500, 50)
''')

cursor.execute('''
	INSERT INTO recipe_ingredient (recipe, ingredient, quantity)
	VALUES ('Pains aux chocolat', 'Beurre', 25)
''')

cursor.execute('''
	INSERT INTO recipe_ingredient (recipe, ingredient, quantity)
	VALUES ('Pains aux chocolat', 'Farine', 75)
''')

cursor.execute('''
	INSERT INTO recipe_ingredient (recipe, ingredient, quantity)
	VALUES ('Macarons', 'Beurre', 75)
''')

connection.commit()

cursor.close()
