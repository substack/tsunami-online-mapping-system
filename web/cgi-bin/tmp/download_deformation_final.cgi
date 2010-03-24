#!/bin/bash


#Mapping directory

html_map=/usr/local/apache2/htdocs/mapping
map_dir=/export/burn/nicolsky/mapping


echo Content-type: text/html
echo ""

tmpf=$(ls ${html_map}/../deformations/*.tmp)
for f in $tmpf; do
  fname=${f%.tmp}
  mv $f $fname
done


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
