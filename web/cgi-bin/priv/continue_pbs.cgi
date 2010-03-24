#!/bin/bash

echo Content-type: text/html
echo ""

#Mapping directory

html_map=/usr/local/apachedev/htdocs/mapping
map_dir=/export/burn/wtest/mapping



#Parsing incomming parameters
ID=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|/ /g' ); 

cd ${map_dir}
touch ${ID}.resuming

rm -f ${ID}.paused
rm -f ${ID}.pausing
rm -f ${ID}.resumed

cat << EOM
<html>  
  <body onload='setTimeout("window.close();",1500);'>
     <h3>Continue scenario ${ID}</h3>
  </body>
</html>
EOM
