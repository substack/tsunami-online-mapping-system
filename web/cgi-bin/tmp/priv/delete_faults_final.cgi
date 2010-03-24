#!/bin/bash


echo Content-type: text/html
echo ""


#Mapping directory

html_map=/usr/local/apache2/htdocs/mapping
map_dir=/export/burn/nicolsky/mapping




#Parsing incomming parameters
line=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|/ /g'); points=(${line})
ipoints=$((${#points[@]}-1))


for ((i=0;i<=$ipoints;i+=1)); do 
  str=${points[$i]}
  rm -f ${html_map}/../deformations/${str}.param
  rm -f ${html_map}/../scripts/param_${str}.js
done





cat << EOM
<HTML>
<HEAD>
 <script language="javascript">
   <!--
   setTimeout("self.close();",2000)
   //-->
   </script> 
</HEAD>
<BODY>
EOM

for ((i=0;i<=$ipoints;i+=1)); do 
  str=${points[$i]}
  echo '<h3> You have deleted "'$str'" subfaults.<br /></h3>'
done


cat << EOM
</BODY>
</HTML>
EOM
