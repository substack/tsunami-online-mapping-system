#!/bin/bash

echo Content-type: text/html
echo ""

#Mapping directory

html_map=/usr/local/apachedev/htdocs/mapping


#Parsing incomming parameters
ID=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|/ /g' ); 


list_pbs=$(ls ${html_map}/${ID}.pbs*)

cat ${html_map}/${ID}.html | sed '$d' | sed '$d' | sed '$d'

echo '<h3> Submitted jobs:</h3>'
echo '<table>'

for f in $list_pbs; do
  echo '<tr><td>'
  echo '<a href="/mapping/'${f##${html_map}/}'">'Job ${f##${html_map}/${ID}.pbs.} '</a>'
  echo '</td></tr>'
done

echo '</table>'

cat << EOM
  </BODY>
</HTML>
EOM
