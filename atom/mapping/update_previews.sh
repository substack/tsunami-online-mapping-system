list=$(ls CASE_00035*.pbs)

for file in ${list}; do
  ID=${file%.pbs}
  echo '=================================================='
  echo $ID
  echo '=================================================='
  cp ../bench/preview/preview.sh        ${ID}/preview/
  cp ../bench/preview/inundation_maps.* ${ID}/preview/
  cd ${ID}/preview/
  ./preview.sh ${ID}
  cd ../..
done
