#! /usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer
import cgi
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

	recipes = {}
	cursor.execute('SELECT recipe, ingredient, quantity FROM recipe_ingredients ORDER BY id DESC')
	for ingredient in cursor:
		if ingredient[0] not in recipes:
			recipes[ingredient[0]] = (set(), [])
		key = ingredient[1].lower()
		recipe = recipes[ingredient[0]]
		if key not in recipe[0]:
			recipe[0].add(ingredient[1])
			if ingredient[2]:
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
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(jsdb())
		else:
			try:
				with open(os.path.dirname(os.path.abspath(sys.argv[0])) + self.path) as fileToServe:
					self.send_response(200)
					self.send_header('Content-Type', 'text/html')
					self.end_headers()
					if self.path == '/index.html':
						self.wfile.write(fileToServe.read().replace('var jsdb = {};', 'var jsdb = ' + jsdb() + ';'))
					else:
						self.wfile.write(fileToServe.read())
			except IOError:
				self.send_error(404, 'File Not Found: %s' % self.path)


	def do_POST(self):
		data = cgi.FieldStorage(
			fp=self.rfile,
			headers=self.headers,
			environ={
				'REQUEST_METHOD': 'POST',
				'CONTENT_TYPE': self.headers['Content-Type'],
			}
		)
		if self.path == '/addingredient':
			try:
				cursor.execute('''
					INSERT INTO ingredients (name, quantity, price)
					VALUES ('%s', %s, %s)
''' % (data['name'].value, data['quantity'].value, data['price'].value))
				connection.commit()
				self.send_response(200)
				self.end_headers()
			except:
				self.send_error(404, 'File Not Found: %s (unable to add ingredient)' % self.path)
				raise
		elif self.path == '/addrecipe':
			try:
				cursor.execute('''
					INSERT INTO recipe_ingredients (recipe, ingredient, quantity)
					VALUES ('%s', '%s', %s)
''' % (data['name'].value, '__FAKE__', 0))
				connection.commit()
				self.send_response(200)
				self.end_headers()
			except:
				self.send_error(404, 'File Not Found: %s (unable to add recipe)' % self.path)
				raise
		elif self.path == '/addrecipeingredient':
			try:
				cursor.execute('''
					INSERT INTO recipe_ingredients (recipe, ingredient, quantity)
					VALUES ('%s', '%s', %s)
''' % (data['recipe'].value, data['ingredient'].value, data['quantity'].value))
				connection.commit()
				self.send_response(200)
				self.end_headers()
			except:
				self.send_error(404, 'File Not Found: %s (unable to add ingredient to recipe)' % self.path)
				raise
		else:
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
