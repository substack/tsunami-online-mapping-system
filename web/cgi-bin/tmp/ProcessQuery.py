#!/usr/bin/python

import cgi
import sys
import bisect


#url = cgi.FieldStorage()
#bbox = url['BBOX'].value
#bbox = bbox.split(',')
#west = float(bbox[0])
#south = float(bbox[1])
#east = float(bbox[2])
#north = float(bbox[3])

north=90
south=0
east=0
west=360



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



<table border="0" width="800">
<tr><td>Case ID</td><td>Description</td><td align="right">Status</td></tr>
<tr><td></td><td></td><td align="right"></td></tr>
''')

	
footer = ('''
</table>
</HTML>
''')

print 'Content-type: text/html\n'
print header


f=open('/export/burn/nicolsky/mapping/status.txt','r')
for line in f:
	line=line.strip()
	poly='''<tr><td><font color="%(color).10s">%(id).10s</font></td><td><a href="/mapping/%(id).10s/readme.html"><font color="%(color).10s">%(desc).100s</font></a></td><td align="right"><font color="%(color).10s">%(status).10s</font></td></tr>'''
	str_id, str_desc, str_status = line.split(',')
	if str_status.strip() == "Pending":
		str_color = 'red'
	elif str_status.strip() == "Computing":
		str_color = 'blue'
	elif str_status.strip() == "Post-processing":
		str_color = 'green'
	print poly % { 'id': str_id, 'desc': str_desc, 'status': str_status, 'color': str_color}
        
print footer
