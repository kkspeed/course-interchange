# -*- encoding: utf-8 -*-


############################################################
# This code is largely inspired by GE.py written by
# LAOHYX
############################################################

from Curl import *
import re

class CourseSel:
	curl = Curl ()
	cookies = {}

	def get_token (self):
		content, status, session = self.curl.get_content ('http://electsys0.sjtu.edu.cn/edu/')
		pattern = re.compile (r'id="__EVENTVALIDATION" value="(.*?)" />')
		match = pattern.search (content)
		if match:
			evalid = match.group (1)

		pattern = re.compile (r'id="__VIEWSTATE" value="(.*?)" />')
		match = pattern.search (content)
		if match:
			vstate = match.group (1)

		session = session[0].split ('\t')[-2 : ]

		self.cookies[session[0]] = session[1]
		return evalid, vstate

	def try_login (self, username, passwd):
		evalid, vstate = self.get_token ()
		post_data = {
			'__VIEWSTATE': vstate,
			'__EVENTVALIDATION': evalid,
			'txtUserName': username,
			'txtPwd': passwd,
			'rbtnLst': '1',
			'Button1': '登录'
		}

		content, status, session = self.curl.post_data (
				'http://electsys0.sjtu.edu.cn/edu/index.aspx', 
				30, self.cookies, post_data)

		return status == 200

	def get_course_table (self):
		content, status, session = self.curl.get_content (
			'http://electsys0.sjtu.edu.cn/edu/student/elect/electResultOuter.aspx',
			30,
			self.cookies
			)


		pattern = re.compile ('<TABLE class="alltab" id="Table1" cellSpacing="0" cellPadding="0" width="100%" border="0">([\s\S]*?)</TABLE>')

		match = pattern.search (content)

		if (not match):
			return None

		return match.group (1)

