#!/bin/bash

#del_xyzs=$(ssh burn.giseis.alaska.edu "ls /usr/local/apache2/htdocs/deformations/*.deleting" 2>/dev/null)
#for file in ${del_xyzs}; do
#   fname=${file##/usr/local/apache2/htdocs/deformations/}
#   fname=${fname%.deleting}
#   rm -f deformations/${fname}.*
#   ssh burn.giseis.alaska.edu "rm -f "$file
#done

new_xyzs=$(ssh burn.giseis.alaska.edu "ls /usr/local/apache2/htdocs/file_doed/Dmitry/custom/*.xyz" 2>/dev/null)
for file in ${new_xyzs}; do
   scp burn.giseis.alaska.edu:$file deformations
   ssh burn.giseis.alaska.edu "rm -f "$file
   fname=${file##/usr/local/apache2/htdocs/file_doed/Dmitry/custom/}
   fname=${fname%.xyz}
   cd deformations
   ./xyz2ps.sh $fname
   cd ..
done


new_params=$(ssh burn.giseis.alaska.edu "ls /usr/local/apache2/htdocs/deformations/*.param.new" 2>/dev/null)
for file in ${new_params}; do
   scp burn.giseis.alaska.edu:$file deformations/okada
   ssh burn.giseis.alaska.edu "rm -f "$file
   fname=${file##/usr/local/apache2/htdocs/deformations/}
   fname=${fname%.param.new}
   cd deformations/okada
   mv ${fname}.param.new ${fname}.param
   ./compute_okada.sh ${fname}
   cd ..
   ./xyz2ps.sh $fname
   cd ..
done
