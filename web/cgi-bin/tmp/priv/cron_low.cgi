#!/bin/bash

echo Content-type: text/html
echo ""


echo "low" > /export/burn/nicolsky/mapping/ccron

cat << EOM
<html>
<body>
Slow frequency cron!
</body>
</html>
EOM
