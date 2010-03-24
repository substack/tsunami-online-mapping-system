#!/bin/bash --login

octave=/u2/wes/PET_HOME/pkgs/octave-3.0.5/bin/octave

server=burn.giseis.alaska.edu

map_dir=/export/burn/nicolsky/mapping
html_map=/usr/local/apache2/htdocs/mapping

ID=$1
rm -f *.gz *.xyz

step=$(grep Step ../restart.tmp | awk -F'=' '{print $2}' | sed 's/ //g')
dt=$(grep Computation ../restart.tmp | awk -F'=' '{print $2}' | sed 's/ //g')


rgrids=$(ls *.preview 2>/dev/null)
for grid in ${rgrids}; do
   name=${grid%.preview}
   echo 'Creating XYZ and KML files for '$name' grid'
  
   ${octave} --no-line-editing --silent preview_octave.m $name $step
   mv ${name}.max_dz.xyz ${name}_${ID}.max_dz.xyz 
   mv ${name}.max_fl.xyz ${name}_${ID}.max_fl.xyz 
   mv ${name}.H.xyz      ${name}_${ID}.H.xyz 
done

for grid in ${rgrids}; do
   name=${grid%.preview}
   ./inundation_maps.sh ${name} ${ID} ${step}
   convert -trim MAP_${name}_${ID}_01.png MAP_${name}_${ID}.png
   rm -f MAP_${name}_${ID}_01.png
done


tsfiles=$(ls ../*.ts)
if [ "${tsfiles}" != "" ]; then
   cd .. 
   tar -cf - Point_*.ts | gzip -c > preview/points.tar.gz
   cd preview
fi

echo 'Done' > finished.txt


echo   'mkdir -p     '${html_map}'/'${ID}'/preview' > ${ID}_tmp.sh
echo   'chmod -R 777 '${html_map}'/'${ID}          >> ${ID}_tmp.sh
chmod 700 ${ID}_tmp.sh
scp ${ID}_tmp.sh ${server}:${map_dir}
ssh ${server} ${map_dir}'/'${ID}'_tmp.sh'

scp *.xyz ${server}:${html_map}/${ID}/preview   2>/dev/null
scp *.kml ${server}:${html_map}/${ID}/preview   2>/dev/null

scp MAP_*.png ${server}:${html_map}/${ID}/preview      2>/dev/null
scp MAP_*.eps ${server}:${html_map}/${ID}/preview      2>/dev/null

scp finished.txt ${server}:${html_map}/${ID}/preview   2>/dev/null


#Copying files to burn
scp points.tar.gz           ${server}:${html_map}/${ID}/preview
scp loadXYZ.m               ${server}:${html_map}/${ID}/preview
scp netcdf.m                ${server}:${html_map}/${ID}/preview


echo   'chmod 644 '${html_map}'/'${ID}'/preview/*' > ${ID}_tmp.sh
scp ${ID}_tmp.sh ${server}:${map_dir}
ssh ${server} ${map_dir}'/'${ID}'_tmp.sh'


