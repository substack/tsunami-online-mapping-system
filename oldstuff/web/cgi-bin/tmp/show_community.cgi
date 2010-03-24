#!/bin/bash


farch=/usr/local/apache2/htdocs/mapping/archive

echo Content-type: text/html
echo ""

cat << EOM

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
   "http://www.w3.org/TR/html4/frameset.dtd">
<HTML>
<HEAD>

<TITLE>Alaska Tsunami Inundation Mapping Project</TITLE>
<link rel="stylesheet" type="text/css" href="http://burn.giseis.alaska.edu/MenuStyle.css">
<link rel="stylesheet" type="text/css" href="http://burn.giseis.alaska.edu/MenuStyle_add.css">
 
<script type="text/javascript">
    //<![CDATA[

       function load() {

        // code for IE
	if(!document.body.currentStyle) return;
	var subs = document.getElementsByName('submenu');
	for(var i=0; i<subs.length; i++) {
		var li = subs[i].parentNode;
		if(li && li.lastChild.style) {
			li.onmouseover = function() {
				this.lastChild.style.visibility = 'visible';
			}
			li.onmouseout = function() {
				this.lastChild.style.visibility = 'hidden';
			}
		}
	     }

       }
    //]]>
    </script>

</HEAD>
<body onload="load()" >


EOM

echo '<div id=menu><ul id=menuList>'

places=($(awk -F';' '{print $1}' $farch))
ids=($(awk -F';' '{print $2}' $farch))
names=($(awk -F';' '{print $3}' $farch))
nplaces=$(wc $farch | awk '{print $1}')

p=${places[0]};
echo '<li><a href="#" name="submenu" class="submenu">'$p'</a><ul>'
for ((i=1;i<${nplaces};i++)); do
  if [ "${places[$i]}" != "$p" ]; then
     echo '</ul></li>'
     p=${places[$i]}
     echo '<li><a href="#" name="submenu" class="submenu">'$p'</a><ul>'
     echo '<li><a href="#">'${ids[$i]}'</a></li>'
  else
     echo '<li><a href="#">'${ids[$i]}'</a></li>'
  fi
done
echo '</ul></li>'
echo '</ul>'
echo '</div>'

cat << EOM



</BODY>
</HTML>

EOM
