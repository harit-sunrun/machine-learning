#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by Harit Himanshu on 2012-02-11.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.

Builds the spam dataset based on input files(currently fetches from Gmail)
"""

from BeautifulSoup import BeautifulSoup

import email
import imaplib
import logging
import sys
import os

class Gmail():
	def __init__(self, user, passwd):
		self.mail 	= imaplib.IMAP4_SSL('imap.gmail.com')
		self.user 	= user
		self.passwd = passwd
		self.__connect()
		
	def __connect(self):
		try:
			self.mail.login(self.user, self.passwd)
		except:
			logging.error('Failed to connect to Gmail - ' + repr(sys.exc_info()[1]))
	
	def get_emails_as_text(self, label=None):
		""" returns the list of emails as the text for 'Subject' and 'body' of the email"""
		try:	
			#self.mail.select('[Gmail]/Spam')
			logging.warn('setting label - ' + label)
			self.mail.select(label)
			result, data = self.mail.uid('search', None, "ALL")
			email_ids = data[0].split()
			emails_as_text = []
			for i in email_ids:
				result, mail_data = self.mail.uid('fetch', i, '(RFC822)')
				try:
					mail_data = email.message_from_string(mail_data[0][1])
					mail_as_text = self.__get_email_payload_as_text(mail_data)
					if not mail_as_text:
						logging.error('Failed to get email as text, could be other mail type than multipart or text')
						continue

					print mail_data.get('Subject') + " " + mail_as_text
				except UnicodeDecodeError:
					logging.error('error decoding email, ignoring')
					continue
			#return self.__get_text(mail_data.get('Subject') + " " + mail_data.get_payload())
		except:
			logging.error('issues while extracting emails - ' + repr(sys.exc_info()[1]))

	def __get_text(self, data):
		if not data:
			raise Exception('No data passed to extract text')
	
	def __get_email_payload_as_text(self, data):
		if not data:
			raise Exception, 'can not get email text from empty payload'

		return_text = ''
		if data.get_content_maintype == 'multipart':
			text = ['']
			for part in data.get_payload():
				if part.get_content_main_type == 'text':
					text.append(part.get_payload())
			return_text = ''.join(text)
		elif data.get_content_maintype() == 'text':
			return_text = data.get_payload()
		if return_text:
			soup = BeautifulSoup(return_text)
			return ''.join(soup.findAll(text=True))
		else:
			return return_text

class Features():
	def __init__(text, spam_word_file):
		self.text = text
		self.spam_file = spam_word_file
		self.words = get_spam_words(self)
	
	def get_percentage_of_matched_word_in_text(self):
		""" percentage of words in the e-mail that match WORD {SPAM Words} """
		pass
	
	def get_percentage_of_matched_word_in_text(self):
		""" percentage of words in the e-mail that match WORD {SPAM Words} """
		pass
	
	def get_length_of_longest_capital_letter_sequence(self):
		pass
	
	def get_total_number_of_capital_letters(self):
		pass
	
	def get_spam_words(self):
		pass
		
	def get_words():
		pass

class Utilities():
	def __init__(self):
		pass
	
	def get_text_from_html(text):
		if not text:
			return None
		soup = BeautifulSoup(text)
		result = soup.findAll(text=True)
		if not result:
			return None
		return ''.join(result)
	
def main():
	email = Gmail('harit.himanshu@gmail.com', '')
	email = email.get_emails_as_text('[Gmail]/Spam')
	#email = email.get_emails_as_text('in')
	

if __name__ == '__main__':
	main()

