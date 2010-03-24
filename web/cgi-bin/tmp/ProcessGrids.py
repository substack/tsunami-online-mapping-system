#!/usr/bin/python

import cgi
import sys
import bisect



header = ('''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<HTML>
<HEAD>
<TITLE>Alaska Tsunami Inundation Mapping Project</TITLE>

<STYLE>
A:LINK    {Text-Decoration: none}
A:VISITED {Text-Decoration: none}
A:HOVER   {Text-Decoration: underline; color: #AA00CC}
</STYLE>

</HEAD>


''')

	
footer = ('''
</table>
</HTML>
''')

print 'Content-type: text/html\n'
print header

#f=open('mapping/status.txt','r')
#for line in f:
#	line=line.strip()
#	poly='''<tr><td><font color="%(color).10s">%(id).10s</font></td><td><a href="/mapping/%(id).10s/readme.html"><font color="%(color).10s">%(desc).100s</font></a></td><td align="right"><font color="%(color).10s">%(status).10s</font></td></tr>'''
#	str_id, str_desc, str_status = line.split(',')
#	if str_status.strip() == "Pending":
#		str_color = 'red'
#	elif str_status.strip() == "Active":
#		str_color = 'blue'
#	elif str_status.strip() == "Completed":
#		str_color = 'green'
#	print poly % { 'id': str_id, 'desc': str_desc, 'status': str_status, 'color': str_color}
        
print footer
