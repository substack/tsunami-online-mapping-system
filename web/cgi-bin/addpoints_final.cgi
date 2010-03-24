#!/bin/bash

echo Content-type: text/html
echo ""

#Parsing incomming parameters
line=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/&/ /g'); points=(${line})

listname=${points[1]}
filename=${points[0]}

mv ../htdocs/$filename ../htdocs/grids/list_points.$listname
cd ../htdocs/grids
./list2js.sh list_points.$listname

cat << EOM

  <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
  <html xmlns="http://www.w3.org/1999/xhtml">
  <head>
  </head>

  <body onload='window.close();'></body>
</html>

EOM
