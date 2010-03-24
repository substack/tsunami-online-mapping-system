#!/bin/bash

echo Content-type: text/html
echo ""


cat << EOM
<HTML>
<HEAD><TITLE>Deformation Uploader</TITLE></HEAD>
<BODY>
    Only XYZ files are currently supported.   
    <form action="/cgi-bin/upload_deformation.pl" method="post" enctype="multipart/form-data">
     <p>File to Upload: <input type="file" name="file_name" /></p>
     <input type="hidden" value="../htdocs/deformations" name="directory" />
     <input type="hidden" value="" name="path" />
     <p><input type="submit" name="Submit" value="Upload" /></p>
    </form>
</BODY>
</HTML>
EOM
