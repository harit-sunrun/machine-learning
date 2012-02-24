#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by Harit Himanshu on 2012-02-11.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.

Builds the spam dataset based on input files(currently fetches from Gmail)
"""

from BeautifulSoup import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords

import email
import getpass
import imaplib
import logging
import os
import re
import sys


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
		emails_as_text = []
		try:
			logging.warn('setting label - ' + label)
			self.mail.select(label)
			result, data = self.mail.uid('search', None, "ALL")
			email_ids = data[0].split()
			for i in email_ids:
				result, mail_data = self.mail.uid('fetch', i, '(RFC822)')
				try:
					mail_data = email.message_from_string(mail_data[0][1])
					mail_as_text = self.__get_email_payload_as_text(mail_data)
					if not mail_as_text:
						logging.error('Failed to get email as text, could be other mail type than multipart or text')
						continue
					emails_as_text.append(mail_as_text)
				except UnicodeDecodeError:
					logging.error('error decoding email, ignoring')
					continue
		except:
			logging.error('issues while extracting emails - ' + repr(sys.exc_info()[1]))
		return emails_as_text

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
	word_splitter = re.compile('\\W*')

	def __init__(self,text, spam_word_file):
		self.text = text
		self.spam_file = spam_word_file
		self.spam_words = self.__get_spam_words()
		self.spam_pattern = re.compile('|'.join(map(re.escape, self.spam_words)))
		
	def get_features(self):
		if not self.text:
			raise Exception, 'No text to extract features from'
		for each_email in self.text:
			try:
				each_email = self.__get_content_from_text(each_email)
				total_words = self.__get_words(each_email)
				feature = self.__get_percentage_of_matched_word_in_text(each_email, total_words)
				print
				print '---------------------'*10
			except:
				logging.error('issues while extracting features from emails - ' + repr(sys.exc_info()[1]))
				continue
	
	def __get_content_from_text(self, text):
		""" Removes stop words from email """
		if not text:
			raise Exception, 'Can not extract content from email'
		s_words = stopwords.words('english')
		content  = [w.lower() for w in Features.word_splitter.split(text) if w.lower() not in s_words]
		return ' '.join(content)
			
	def __get_percentage_of_matched_word_in_text(self, email, total_words): 
		""" percentage of words in the e-mail that match WORD {SPAM Words} """
		match = Counter(self.spam_pattern.findall(email))
		for spam_word in self.spam_words:
			wc = match.get(spam_word, 0)
			#print spam_word, wc, total_words, float((100* wc)/total_words)
			print float((100* wc)/total_words),
	
	def __get_percentage_of_matched_character_in_text(self):
		""" percentage of words in the e-mail that match WORD {SPAM Words} """
		pass
	
	def __get_length_of_longest_capital_letter_sequence(self):
		pass
	
	def __get_total_number_of_capital_letters(self):
		pass
	
	def __get_spam_words(self):
		if not (os.path.exists(self.spam_file)):
			raise Exception, 'Could not locate file containing the spam words'
		return open(self.spam_file, 'r').read().lower().split('\n')
		
	def __get_words(self, text):
		""" Returns the list of words after removing stop words"""
		words = [s.lower() for s in Features.word_splitter.split(text)]
		return len(words)

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
	user = raw_input('Enter you email-id(include @gmail.com) : ')
	password = getpass.getpass('Enter your Gmail password : ')
	email = Gmail(user, password)
	text_emails = email.get_emails_as_text('[Gmail]/Spam')
	features = Features(text_emails, 'spamwords')
	features.get_features()

if __name__ == '__main__':
	main()

