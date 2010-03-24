#!/bin/bash

echo Content-type: text/html
echo ""

#Mapping directory

html_map=/usr/local/apache2/htdocs/mapping
map_dir=/export/burn/nicolsky/mapping



#Parsing incomming parameters
list=($(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|/ /g' )); 

ID=${list[0]}
community=${list[1]}

cd ${map_dir}
echo ${community} > ${ID}.archiving
rm -f ${ID}.paused ${ID}.pausing
rm -f ${ID}.resumed ${ID}.resuming

mv ${ID} ARCHIVE_${community}
mkdir ARCHIVE_${community}/${ID}/post_processing/
chmod 777 ARCHIVE_${community}/${ID}/post_processing/

mv ${html_map}/${ID}/preview ARCHIVE_${community}/${ID}


cat << EOM
<html>  
  <body onload='setTimeout("window.close();",1500);'>
     <h3>Archiving scenario ${ID} to ${community}</h3>
  </body>
</html>
EOM
