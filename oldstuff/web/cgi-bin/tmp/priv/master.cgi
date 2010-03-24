#!/bin/bash

echo Content-type: text/html
echo ""

cat << EOM
<html>
<body>
<a href="/cgi-bin/priv/download_deformation.cgi">Download</a> a deformation<br />
<a href="/cgi-bin/priv/delete_deformation.cgi">Delete</a> a deformation<br />
<a href="/cgi-bin/priv/delete_list.cgi">Delete</a> a list of marker points<br />
<a href="/cgi-bin/priv/delete_faults.cgi">Delete</a> a subfault<br />
<br />
<a href="/cgi-bin/priv/cron_low.cgi">Set</a> the low frequency<br />
<a href="/cgi-bin/priv/cron_high.cgi">Set</a> the high frequency<br />
</body>
</html>
EOM
