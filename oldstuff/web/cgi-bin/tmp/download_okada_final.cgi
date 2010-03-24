#!/bin/bash


#Mapping directory

html_map=/usr/local/apache2/htdocs/mapping
map_dir=/export/burn/nicolsky/mapping


echo Content-type: text/html
echo ""

cd ${html_map}/../deformations
./list2js.sh


cat << EOM
<HTML>
<HEAD>
   <script language="javascript">
   <!--
   setTimeout("self.close();",1)
   //-->
   </script> 
</HEAD>
<BODY>
</BODY>
</HTML>
EOM
