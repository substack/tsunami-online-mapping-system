#!/bin/bash

echo Content-type: text/html
echo ""

#Mapping directory

html_map=/usr/local/apachedev/htdocs/mapping
map_dir=/export/burn/wtest/mapping



#Parsing incomming parameters
ID=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|/ /g' ); 

cd ${map_dir}
touch ${ID}.removing


rm -rf ${map_dir}/${ID}
rm -rf ${html_map}/${ID}*

cat << EOM
<html>  
  <body onload='setTimeout("window.close();",1500);'>
     <h3>Removing scenario ${ID}</h3>
  </body>
</html>
EOM
