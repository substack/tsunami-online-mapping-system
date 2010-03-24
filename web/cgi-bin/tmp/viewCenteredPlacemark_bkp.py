#!/usr/bin/python

import cgi
import sys
import bisect


url = cgi.FieldStorage()
bbox = url['BBOX'].value
bbox = bbox.split(',')
west = float(bbox[0])
south = float(bbox[1])
east = float(bbox[2])
north = float(bbox[3])

#north=90
#south=0
#east=0
#west=360


res_lat=25
res_lon=25

file_lon = 'www_data/PA02_lon_dec.txt'
file_lat = 'www_data/PA02_lat_dec.txt'
grid_lon = map( float, open( file_lon ).readlines() )
grid_lat = map( float, open( file_lat ).readlines() )

min_grid_lon=min(grid_lon)
max_grid_lon=max(grid_lon)

min_grid_lat=min(grid_lat)
max_grid_lat=max(grid_lat)

dlon=(east-west)/res_lon
dlat=(north-south)/res_lat



header = ( 
   '<?xml version="1.0" encoding="UTF-8"?>\n'
   '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
   '<Folder>\n'
   '<name>Untitled Folder</name>\n'
   '<Style id="DD_style">\n'
	 '<LineStyle>\n'
	 '<color>ffaaaaaa</color>\n'
	 '<width>1</width>\n'
	 '</LineStyle>\n'
	 '<PolyStyle>\n'
	 '<color>19ff0000</color>\n'
	 '</PolyStyle>\n'
	 '</Style>\n'
	 '<open>1</open>\n')
	 
poly='''<Placemark>
    <description>
    Longitude %(lonc).2f, <BR> </BR> 
    Latitude %(latc).2f <BR> </BR>
    
    <![CDATA[
    <p align="center"><a href="http://burn.giseis.alaska.edu/cgi-bin/viewer.cgi?grid=PA02&lat=%(ii_lat).d&lon=%(ii_lon).d&field=Z">Sea level</p>
    <p align="center"><a href="http://www.aeic.alaska.edu/"><img src="http://www.giseis.alaska.edu/emboss_AEIC.gif" alt="aeic logo" width=150 /></p>
    ]]></description>
		<styleUrl>#DD_style</styleUrl>
		<Polygon>
			<tessellate>1</tessellate>
			<outerBoundaryIs>
				<LinearRing>
					<coordinates>%(lon_east).6f,%(lat_north).6f,0 %(lon_east).6f,%(lat_south).6f,0 %(lon_west).6f,%(lat_south).6f,0 %(lon_west).6f,%(lat_north).6f,0 %(lon_east).6f,%(lat_north).6f,0  </coordinates>
				</LinearRing>
			</outerBoundaryIs>
		</Polygon>
	</Placemark>'''
	
footer = (
   '</Folder>\n'
   '</kml>')

print 'Content-Type: application/vnd.google-earth.kml+xml\n'
print header
#print body
for ilat in range( 0, res_lat):
    for ilon in range( 0, res_lon ):
        lonc=east-(ilon+0.5)*dlon
        latc=north-(ilat+0.5)*dlat
        
        aux_latc=latc
        if lonc<0:
            aux_lonc=360+lonc
        else:
            aux_lonc=lonc

        ii_lon=bisect.bisect( grid_lon, aux_lonc )
        ii_lat=bisect.bisect( grid_lat, aux_latc )
        
        lon_west=lonc-dlon/2
        lon_east=lonc+dlon/2
        

        if (min_grid_lon<aux_lonc<max_grid_lon) and (min_grid_lat<aux_latc<max_grid_lat):
            print poly % { 'gname': 'PA02', 
                       'lon_east': lon_east, 'lon_west': lon_west, 
                       'lat_south': latc-dlat/2, 'lat_north': latc+dlat/2, 
                       'lonc': aux_lonc, 'latc': aux_latc,
                       'ii_lat': ii_lat, 'ii_lon': ii_lon }
        
print footer
