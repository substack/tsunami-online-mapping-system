#!/bin/bash

ip=$(tail -1 ../logs/access_log | sed 's/\./ /g' | awk '{printf "%d.%d.%d.%d", $1,$2,$3,$4}')
data=$(/opt/sfw/bin/curl http://netgeo.caida.org/perl/netgeo.cgi?target=$ip | /usr/sfw/bin/ggrep LAT: -A 1 | sed 's/<br>//g' | sed 's/[A-Z:]//g')

your_lat=$(echo $data | awk '{print $1}')
your_lon=$(echo $data | awk '{print $2}')

#<BR><BR>
#<font size=2>Your are located at $your_lat degrees of latitude and $your_lon degrees of longitude.</font>


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
done

#grid=PW24
#Latitude=100
#Longitude=100
#field=Z

#Extracting data from NetCDF files
tmp=tmp_$RANDOM$RANDOM$RANDOM$RANDOM
files=$(ls www_data/$grid/nc_$grid*.nc)
for file in $files; do
  www_data/read_xy $file $field $Latitude $Longitude scratch/$tmp.dat
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
set title "Depth = $depth,m"
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
<HEAD><TITLE>$field graphs</TITLE></HEAD>
<BODY>
<!--<IFRAME SRC="http://www.aeic.alaska.edu/2ndpagetop.html" TITLE="GI Page Top" width="100%" height="176" frameborder="0" border="0" scrolling="NO"></IFRAME>-->

<iframe src="http://www.gi.alaska.edu/newgipagetop.html" title="GI Page Top" width="100%" height="185" frameborder="0" scrolling="no"></iframe> 
EOM

if [[ $depth < 0 ]]; then
  echo '<Center><font color="darkred"><H2>Oops! The point you have selected is either on land, or close to it.<BR>'
  echo 'Please select points in the ocean only.</H2></font></Center>'
else
  echo '<font color="darkblue"><H2>Modeled 1964 Sea Level Height Plot:</H2></font>'
  echo '<'img src="/images/$tmp.png"'>'
fi 

cat << EOM
<p><a href="http://www.aeic.alaska.edu/"><img src="http://www.giseis.alaska.edu/emboss_AEIC.gif" alt="aeic logo" width=200 /></a><br /><br />We thank <a href="http://www.arsc.edu">Arctic Region Supercomputing Center</a> for their support in computing.</p>
</BODY>
</HTML>
EOM
