#! /usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer
import json
import os.path
import sqlite3
import sys

if len(sys.argv) != 2:
	print >> sys.stderr, 'Usage: %s <db>' % sys.argv[0]
	sys.exit(1)

connection = sqlite3.connect(sys.argv[1])
cursor = connection.cursor()

def jsdb():
	ingredients = {}
	cursor.execute('SELECT name, quantity, price FROM ingredients ORDER BY id DESC')
	for ingredient in cursor:
		key = ingredient[0].lower()
		if key not in ingredients:
			ingredients[key] = ingredient

	ingredients = {}
	cursor.execute('SELECT name, quantity, price FROM ingredients ORDER BY id DESC')
	for ingredient in cursor:
		key = ingredient[0].lower()
		if key not in ingredients:
			ingredients[key] = ingredient

	recipes = {}
	cursor.execute('SELECT recipe, ingredient, quantity FROM recipe_ingredient ORDER BY id DESC')
	for ingredient in cursor:
		if ingredient[0] not in recipes:
			recipes[ingredient[0]] = (set(), [])
		key = ingredient[1].lower()
		recipe = recipes[ingredient[0]]
		if key not in recipe[0]:
			recipe[0].add(ingredient[1])
			recipe[1].append((ingredient[1].lower(), ingredient[2]))
	for name, recipe in recipes.items():
		recipes[name] = recipe[1]

	return 	json.dumps({
		'ingredients': ingredients,
		'recipes': recipes
	})

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == '/jsdb':
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			self.wfile.write(jsdb())
		else:
			try:
				with open(os.path.dirname(os.path.abspath(sys.argv[0])) + self.path) as fileToServe:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					if self.path == '/index.html':
						self.wfile.write(fileToServe.read().replace('var jsdb = {};', 'var jsdb = ' + jsdb() + ';'))
					else:
						self.wfile.write(fileToServe.read())
			except IOError:
				self.send_error(404, 'File Not Found: %s' % self.path)


	def do_POST(self):
		try:
			self.send_error(404, 'File Not Found: %s (no POST action defined)' % self.path)
		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)

if __name__ == '__main__':
	try:
		server = BaseHTTPServer.HTTPServer(('', 8080), HTTPHandler)
		print 'Démarrage du serveur de recettes'
		server.serve_forever()
	except KeyboardInterrupt:
		print 'Arrêt du serveur de recettes'
		server.socket.close()

cursor.close()
