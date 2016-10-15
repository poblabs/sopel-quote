"""
quote.py - A simple quotes module for sopel
Copyright 2015, Andy Chung, iamchung.com
Licensed under the Eiffel Forum License 2.
"""

from __future__ import unicode_literals
from sopel.module import rate
import sopel
import random
import codecs # TODO in python3, codecs.open isn't needed since the default open does encoding.
import sqlite3
import MySQLdb
import time

@sopel.module.commands('q', 'quote')
@rate(5)
def quote(bot, trigger):
	options = QuoteModuleOptions()
	options.channel = trigger.sender
	options.nick = trigger.nick
	options.hostmask = trigger.hostmask
	options.user = bot.config.quote.user
	options.password = bot.config.quote.password
	options.database = bot.config.quote.database
	options.host = bot.config.quote.host
	options.owner = bot.config.core.owner

	dataprovider = MySQLQuoteDataProvider(options)
	
	# parse and execute command
	output = dataprovider.get_random()
	
	bot.say(output)

@sopel.module.commands('addq', 'addquote')
@rate(5)
def addq(bot, trigger):
	options = QuoteModuleOptions()
	options.channel = trigger.sender
	options.nick = trigger.nick
	options.hostmask = trigger.hostmask
	options.user = bot.config.quote.user
	options.password = bot.config.quote.password
	options.database = bot.config.quote.database
	options.host = bot.config.quote.host
	options.owner = bot.config.core.owner
	
	dataprovider = MySQLQuoteDataProvider(options)

	# parse and execute command
	data = trigger.group(2)
	if data is None or data == '':
		output = '%s: did you forget the quote? Correct usage: !addq <quote here>. Use | to separate multiple lines.' % trigger.nick
	else:
		output = dataprovider.add(data)
		
	bot.say(output)
		
@sopel.module.commands('delq', 'delquote')
@rate(2)
def delq(bot, trigger):
	options = QuoteModuleOptions()
	options.channel = trigger.sender
	options.nick = trigger.nick
	options.hostmask = trigger.hostmask
	options.user = bot.config.quote.user
	options.password = bot.config.quote.password
	options.database = bot.config.quote.database
	options.host = bot.config.quote.host
	options.owner = bot.config.core.owner
	
	dataprovider = MySQLQuoteDataProvider(options)

	# parse and execute command
	data = trigger.group(2)
	if data is None or data == '':
		output = 'Error: Missing the quote ID. Usage: !delq <quote ID>'
	else:
		output = validate_number_input(data)
		output = dataprovider.remove(int(data)) if output == '' else output
		
	bot.say(output)
		
@sopel.module.commands('findq', 'findquote')
@rate(3)
def findq(bot, trigger):
	options = QuoteModuleOptions()
	options.channel = trigger.sender
	options.nick = trigger.nick
	options.hostmask = trigger.hostmask
	options.user = bot.config.quote.user
	options.password = bot.config.quote.password
	options.database = bot.config.quote.database
	options.host = bot.config.quote.host
	options.owner = bot.config.core.owner
	
	dataprovider = MySQLQuoteDataProvider(options)

	# parse and execute command
	data = trigger.group(2)
	if data is None or data == '':
		output = '%s: Error: Missing the quote ID. Usage: !findq <quote ID>' % options.nick
		bot.say(output)
	else:
		output = dataprovider.search(data)
		if output == False:
			msg = "%s: Error: No match for quote containing: %s" % (options.nick, data)
			bot.say(msg)
		else:
			quote_count = len(output)
			bot.say("%s: Found these %s random results" % (options.nick, quote_count) )
			for row in output:
				bot.say("[%s]: %s" % (row[0], row[3]) )
				time.sleep(1)
	
	
@sopel.module.commands('getq', 'getquote')
@rate(5)
def getq(bot, trigger):
	options = QuoteModuleOptions()
	options.channel = trigger.sender
	options.nick = trigger.nick
	options.hostmask = trigger.hostmask
	options.user = bot.config.quote.user
	options.password = bot.config.quote.password
	options.database = bot.config.quote.database
	options.host = bot.config.quote.host
	options.owner = bot.config.core.owner
	
	dataprovider = MySQLQuoteDataProvider(options)

	# parse and execute command
	data = trigger.group(2)
	if data is None or data == '':
		output = 'Error: Missing the quote ID. Usage: !getq <quote ID>'
	else:
		output = validate_number_input(data)
		output = dataprovider.get_by_id(int(data)) if output == '' else output
	
	bot.say(output)
	
@sopel.module.commands('lastq', 'lastquote')
@rate(5)
def lastq(bot, trigger):
	options = QuoteModuleOptions()
	options.channel = trigger.sender
	options.nick = trigger.nick
	options.hostmask = trigger.hostmask
	options.user = bot.config.quote.user
	options.password = bot.config.quote.password
	options.database = bot.config.quote.database
	options.host = bot.config.quote.host
	options.owner = bot.config.core.owner
	
	dataprovider = MySQLQuoteDataProvider(options)

	# parse and execute command
	output = dataprovider.get_last_quote()
	
	bot.say(output)
	
def is_valid_int(num):
	"""Check if input is valid integer"""
	try:
		int(num)
		return True
	except ValueError:
		return False

def validate_number_input(data):
	"""Checks if input is both valid int and non-negative"""
	# check if argument is valid int
	if not is_valid_int(data):
		msg = 'Error: Command argument must be valid integer: %s' % (data)
		return msg

	# check if input is negative
	valid_int = int(data)
	if valid_int < 0:
		msg = 'Error: Command argument must be non-negative: %d' % (valid_int)
		return msg

	return ''

class QuoteModuleOptions:
	def __init__(self):
		self.datasource = None
		self.filename = None
		self.onefile = False

class QuoteDataProvider(object):
	def __init__(self, options):
		self.options = options

	def get_random(self):
		raise NotImplementedError('Should have implemented this.')

	def search(self, data):
		raise NotImplementedError('Should have implemented this.')

	def add(self, line_to_add):
		raise NotImplementedError('Should have implemented this.')

	def remove(self, quote_id):
		raise NotImplementedError('Should have implemented this.')

	def get_by_id(self, quote_id):
		raise NotImplementedError('Should have implemented this.')

class MySQLQuoteDataProvider(QuoteDataProvider):
	def __init__(self, options):
		
		self.nick = options.nick
		self.hostmask = options.hostmask
		self.channel = options.channel
		self.ts = int(time.time())
		self.owner = options.owner


		self.db = MySQLdb.connect(host=options.host,
					user=options.user,
					passwd=options.password,
					db=options.database)

		# you must create a Cursor object. It will let
		# you execute all the queries you need
		self.dbcursor = self.db.cursor()

	def get_random(self):
		self.dbcursor.execute('''
			SELECT * FROM quotes ORDER BY RAND() LIMIT 1
		''')
		quote = self.dbcursor.fetchone()
		if quote is None:
			msg = 'Error: No quotes in the database.'
		else:
			msg = '[%d] %s' % (quote[0], quote[3])
		self.db.close()
		return msg

	def add(self, line_to_add):
		# Add quote to DB
		sql = "INSERT INTO quotes(nick, host, quote, channel, timestamp) VALUES('%s', '%s', '%s', '%s', '%d')" % (self.nick, self.hostmask, line_to_add, self.channel, self.ts)
		self.dbcursor.execute(sql)
		# Get quote ID
		get_id_sql = "SELECT id FROM quotes ORDER BY id DESC LIMIT 1;"
		self.dbcursor.execute(get_id_sql)
		quote_id = self.dbcursor.fetchone()[0]
		self.db.commit()
		self.db.close()

		msg = '%s: Quote #%s added' % (self.nick, quote_id)
		print '[quote]: %s' % msg
		return msg

	def remove(self, quote_id):
		# Only bot owner, or quote owner can delete quote
		sql = "SELECT nick FROM quotes WHERE id='%s'" % quote_id
		self.dbcursor.execute(sql)
		result = self.dbcursor.fetchone()
		if result:
			quote_owner = result[0]
		else:
			quote_owner = None
			
		if quote_owner is None:
			msg = "Quote #%s does not exist" % quote_id
		else:
			if (self.nick != self.owner) and (quote_owner != self.nick):
				#msg = "%s: Error: only quote owner, or bot owner, can delete quotes. This quote was created by %s" % (self.nick, quote_owner)
				msg = "%s: Error: only quote owner, or bot owner, can delete quotes" % self.nick
			else:
				sql = "DELETE FROM quotes WHERE id='%s'" % quote_id
				self.dbcursor.execute(sql)
				self.db.commit()
				self.db.close()
				msg = 'Deleted quote #%d' % (quote_id)
			
		print '[quote]: %s' % msg		
		return msg
		
	def search(self, data):
		sql = "SELECT * FROM quotes WHERE quote LIKE '%s' ORDER BY RAND() LIMIT 5" % ('%' + data + '%')
		rows_count = self.dbcursor.execute(sql)
		if rows_count > 0:
			return self.dbcursor.fetchall()
		else:
			self.db.close()
			return False		

	def get_by_id(self, quote_id):
		sql = "SELECT * FROM quotes WHERE id='%s'" % quote_id
		self.dbcursor.execute(sql)
		quote = self.dbcursor.fetchone()
		if quote is None:
			msg = 'Error: no quote in the database with id #%d.' % (quote_id)
		else:
			msg = '[%d] %s' % (quote[0], quote[3])
		self.db.close()
		return msg
		
	def get_last_quote(self):
		sql = "SELECT * FROM quotes ORDER BY id DESC LIMIT 1"
		self.dbcursor.execute(sql)
		quote = self.dbcursor.fetchone()
		if quote is None:
			msg = 'Error: no quotes exist in the database.'
		else:
			msg = '[%d] %s' % (quote[0], quote[3])
		self.db.close()
		return msg
