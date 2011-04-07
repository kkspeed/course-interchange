from CourseSel import *

cs = CourseSel ()

username = raw_input ('username: ')
passwd = raw_input ('password: ')

cs.try_login (username, passwd)

table = cs.get_course_table ()

fi = open ('out1.html', 'wc')
print >> fi, table
