#!/bin/bash

html_map=/usr/local/apache2/htdocs/mapping

echo Content-type: text/html
echo ""

#Parsing incomming parameters
metin=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/&/ /g'); bar=(${metin})
ifinal=$((${#bar[@]}-1))

for ((i=0;i<=$ifinal;i+=1)); do 
  str=${bar[$i]}
  tbar=($(echo $str | sed 's/=/ /'))
  name=${tbar[0]}
  if [ "$name" = "grid" ];  then
    grid=${tbar[1]}
  fi
  if [ "$name" = "lat" ];  then
    Latitude=${tbar[1]}
  fi
  if [ "$name" = "lon" ];  then
    Longitude=${tbar[1]}
  fi
  if [ "$name" = "field" ];  then
    field=${tbar[1]}
  fi
  if [ "$name" = "ID" ];  then
    ID=${tbar[1]}
  fi
  if [ "$name" = "zoom" ];  then
    zoom=${tbar[1]}
  fi
done


#Extracting data from NetCDF files
tmp=tmp_$RANDOM$RANDOM$RANDOM$RANDOM

//echo  $Longitude $Latitude scratch/$tmp.dat '<br />'

files=$(ls ${html_map}/${ID}/preview/nc_$grid*.nc)
for file in $files; do
  www_data/ll2data $file $field $Longitude $Latitude scratch/$tmp.dat 
done


depth=$(head -1 scratch/$tmp.dat | awk '{printf "%.2f", $3}')



if [ "$field" = "Z" ];  then
    label="Sea level, m"
fi
if [ "$field" = "H" ];  then
    label="Depth, m"
fi
if [ "$field" = "U" ];  then
    label="Longitudinal water flux, m/s"
fi
if [ "$field" = "V" ];  then
    label="Latitudinal water flux, m/s"
fi

#Plotting the extracted data
cat << EOF > scratch/$tmp.gnu
reset
set terminal png transparent medium
set title "Depth = ${depth}m"
set xlabel "Time since the earthquake, s"
set ylabel "$label"
plot 'scratch/$tmp.dat' using 1:2 notitle with lines
EOF
/opt/sfw/bin/gnuplot scratch/$tmp.gnu > ../htdocs/images/$tmp.png

#Clean up
rm -rf scratch/$tmp.dat
rm -rf scratch/$tmp.gnu


cat << EOM
<HTML>
<HEAD>
<TITLE>$field graphs</TITLE>
<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAG07sBB-qC9yaNXELGJpf5BRrbJnNmETF966luGlbSTr_RfkmQBR_r9lzzhGueAMWoH_XbKNIdXA-uw" type="text/javascript"></script>
<script type="text/javascript">document.write('<script type="text/javascript" src="/scripts/extlargemapcontrol'+(document.location.search.indexOf('packed')>-1?'_packed':'')+'.js"><'+'/script>');</script>


<script type="text/javascript">
    //<![CDATA[

       function load() {
        if (GBrowserIsCompatible()) {
             var map = new GMap2(document.getElementById("map_canvas"));
             //map.setMapType(G_SATELLITE_MAP);
             map.addControl(new GMapTypeControl());

	     map.disableDoubleClickZoom();
EOM
   echo "             map.setCenter(new GLatLng("$Latitude","$Longitude"), "$(($zoom-1))");"
   echo "             var point = new GPoint("$Longitude","$Latitude");"
cat << EOM
             var cIcon = new GIcon(G_DEFAULT_ICON);
             cIcon.image = "http://www.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png";
             var marker = new GMarker(point, {draggable:false, icon:cIcon});
             GEvent.addListener(marker, "click", function() {
EOM
echo "                marker.openInfoWindowHtml('<table><tr><td>Longitude</td><td>'+"$(printf "%2.2f" $Longitude)"+'</td></tr><tr><td>Latitude</td><td align=right>'+"$(printf "%2.2f" $Latitude)"+'</td></tr></table>');"
cat << EOM
             });
             map.addOverlay(marker);
        }
       }
    //]]>
    </script>


</HEAD>
<BODY onload="load()" >
EOM

if [[ $depth < 0 ]]; then
  echo '<Center><font color="darkred"><H2>Oops! The point you have selected is either on land, or close to it.<BR>'
  echo 'Please select points in the ocean only.</H2></font></Center>'
else
  echo '<img src="/images/'$tmp.png'">'
  echo '<br />Computed sea level dynamics at the location shown by a marker on the map below <br />'
fi 

cat << EOM
<br /><br />
<div id="map_canvas" style="width:600px;height:300px"></div>
<p><br />We thank <a href="www.arsc.edu">Arctic Region Supercomputing Center</a> for their support.</p>
</BODY>
</HTML>
EOM
