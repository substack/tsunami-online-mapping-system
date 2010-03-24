#!/bin/bash

p=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//'); 


p=${p%%..*}

echo Content-type: text/html
echo ""



files=($(ls -l ../htdocs/file_doed/$p | sed '1d' | awk '{print $9}'))
flags=($(ls -l ../htdocs/file_doed/$p | sed '1d' | awk '{print $1}'))

cat << EOM
<HTML>
<HEAD><TITLE>File Download</TITLE></HEAD>
<BODY>
<font  face="monospace">
EOM

echo '<H1>Current Directory' $p '</H1>'
echo '<H2>'
if [ $p != '' ]; then
  echo '<<'a href="download.cgi?${p%/*}"'>..<a>><br>'
fi

for (( j = 0 ; j < 2 ; j++ ));do
for (( i = 0 ; i < ${#files[@]} ; i++ ));do
  flag=${flags[$i]}
  d=${flag:0:1}
  if [ $d == 'd' ]; then
    if [ $j -eq 0 ]; then
      echo '<<'a href="download.cgi?$p/${files[$i]}"'><font color=darkgreen>'${files[$i]}'</font><a>><br>'
    fi
  else
    if [ $j -eq 1 ]; then
      echo '&nbsp<'a href="/file_doed/$p/${files[$i]}"'>'${files[$i]} '<a><br>'
    fi
  fi
done
done
echo '</H2>'
cat << EOM
</font>
<br><br>
   <form action="/cgi-bin/upload.pl" method="post" enctype="multipart/form-data">
     <p>File to Upload: <input type="file" name="file_name" /></p>
     <input type="hidden" value="../htdocs/file_doed$p" name="directory" />
     <input type="hidden" value="$p" name="path" />
     <p><input type="submit" name="Submit" value="Submit Form" /></p>
   </form>
 
   Return to the <a href='/index.html'> home page</a>. <BR>
</BODY>
</HTML>
EOM
