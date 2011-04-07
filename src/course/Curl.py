# -*- encoding: utf-8 -*-
import pycurl
import urllib
import StringIO

pycurl.global_init (pycurl.GLOBAL_DEFAULT)

class Curl:
	GET = pycurl.HTTPGET
	POST = pycurl.POST

	MAX_TIME_OUT = 180

	def __init__ (self):
		self.curl = pycurl.Curl ()
		self.reader = StringIO.StringIO ()

		# Initialize common options
		self.curl.setopt (pycurl.HTTPHEADER, ['Accept:'])
		self.curl.setopt (pycurl.HEADER, 1)
		self.curl.setopt (pycurl.WRITEFUNCTION, self.reader.write)
		self.curl.setopt (pycurl.FOLLOWLOCATION, 1)
		self.curl.setopt (pycurl.COOKIEFILE, '')

	def __dict_to_cookie__ (self, cookies):
		for key, value in cookies.items ():
			cookie = str(key) + '=' + str(value) + ';'
		cookie = cookie[0 : len(cookie) - 1]

		return cookie

	def get_content (self, url, timeout = None, cookies = None, data = None):
		self.curl.setopt (pycurl.URL, url)

		self.curl.setopt (self.GET, 1)

		if (timeout):
			self.curl.setopt (pycurl.TIMEOUT, timeout)
		else:
			self.curl.setopt (pycurl.TIMEOUT, self.MAX_TIME_OUT)

		if (cookies):
			cookie = self.__dict_to_cookie__ (cookies)
			self.curl.setopt (pycurl.COOKIE, cookie)

		self.curl.perform ()

		http_status = int (self.curl.getinfo (pycurl.HTTP_CODE))
		session_cookie = self.curl.getinfo (pycurl.INFO_COOKIELIST)

		content = self.reader.getvalue ()

		return content ,http_status, session_cookie

	def post_data (self, url, timeout = None, cookies = None, data = None):
		post_fields = urllib.urlencode (data)

		self.curl.setopt (pycurl.URL, url)
		self.curl.setopt (pycurl.POST, 1)
		self.curl.setopt (pycurl.POSTFIELDS, post_fields)
		
		if (cookies):
			cookie = self.__dict_to_cookie__ (cookies)
			self.curl.setopt (pycurl.COOKIE, cookie)

		if (timeout):
			self.curl.setopt (pycurl.TIMEOUT, timeout)
		else:
			self.curl.setopt (pycurl.TIMEOUT, self.MAX_TIME_OUT)

		self.curl.perform ()

		http_status = self.curl.getinfo (pycurl.HTTP_CODE)
		content = self.reader.getvalue ()
		session_cookie = self.curl.getinfo (pycurl.INFO_COOKIELIST)

		return content, http_status, session_cookie
