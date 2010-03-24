#!/bin/bash

echo Content-type: text/html
echo ""

#Parsing incomming parameters
line=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/%20//g' | sed 's/&/ /g'); points=(${line})
ipoints=$((${#points[@]}-1))

fname=../../htdocs/deformations/${points[0]}.param
rm -f $fname 
touch $fname
for ((i=1;i<=$ipoints;i+=1)); do 
  echo ${points[$i]} | sed 's/|/ /g' | awk '{printf("%10s",$1); for(i=2;i<=NF;i++) printf("   %7.3f",$i); printf("\n") }' >> $fname
done

awk '{for(i=2;i<=NF;i++) printf("   %7.3f",$i); printf("\n") }' $fname >> $fname.new

cd ../../htdocs/deformations/ 
./list2js.sh ${fname#../../htdocs/deformations/}

cat << EOM

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
  </head>
  <body onload='setTimeout("window.close();",5000);'>
  <h3>
  Deformation according to these <a href="http://burn.giseis.alaska.edu/deformations/${points[0]}.param" target="_blank">parameters</a> will be computed shortly.<br />
  Please wait....
  </h3>
  </body>
</html>

EOM
