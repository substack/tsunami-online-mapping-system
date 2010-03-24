#!/bin/bash

echo Content-type: text/html
echo ""

#Mapping directory

html_map=/usr/local/apachedev/htdocs/mapping
map_dir=/export/burn/wtest/mapping



#Parsing incomming parameters
ID=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|/ /g' ); 

cd ${map_dir}
touch ${ID}.pausing

rm -f ${ID}.resuming
rm -f ${ID}.resumed
rm -f ${ID}.paused


cat << EOM
<html>  
  <body onload='setTimeout("window.close();",1500);'>
     <h3>Pausing scenario ${ID}</h3>
  </body>
</html>
EOM
