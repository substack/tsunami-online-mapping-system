#!/bin/bash

echo Content-type: text/html
echo ""


echo "high" > /export/burn/nicolsky/mapping/ccron

cat << EOM
<html>
<body>
High frequency cron!
</body>
</html>
EOM
