#!/bin/bash --login

server=burn.giseis.alaska.edu

map_dir=/export/burn/nicolsky/mapping
html_map=/usr/local/apache2/htdocs/mapping

ID=$1

echo   'mkdir -p     '${html_map}'/'${ID}'/preview' > ${ID}_gif_tmp.sh
echo   'chmod -R 777 '${html_map}'/'${ID}          >> ${ID}_gif_tmp.sh
chmod 700 ${ID}_gif_tmp.sh
scp ${ID}_gif_tmp.sh ${server}:${map_dir}
ssh ${server} ${map_dir}'/'${ID}'_gif_tmp.sh'

convert_flag=0
grids=$(ls ../gBath*.bin)
for grid in ${grids}; do
  grid=${grid%.bin}
  grid=${grid#../gBath_}
  cd ../post_processing
  
  psfiles=$(ls nc_$grid*.ps 2>/dev/null)
  for psf in $psfiles; do
    if [ ! -f ${psf%.ps}.gif ]; then
       convert -geometry 1000x1000 -trim ${psf} ${psf%.ps}.gif 
    fi
    convert_flag=1
  done
  if [ "${convert_flag}" == "1" ]; then
     convert   -delay 30   -loop 0   nc_$grid*.gif   ../preview/animate_$grid.gif
  fi
  
  cd ../preview
done



#Copying files to burn
scp *.gif                   ${server}:${html_map}/${ID}/preview

ncfiles=$(ls ../post_processing/nc_*.nc 2>/dev/null)
for f in ${ncfiles}; do
   f=${f%.nc}
   if [ ! -f ${f}.copied ]; then
      scp ${f}.nc ${server}:${html_map}/${ID}/preview 
      touch ${f}.copied
   fi
done
scp ../list_points.tmp      ${server}:${html_map}/${ID}/preview 


echo   'chmod 644 '${html_map}'/'${ID}'/preview/*' > ${ID}_gif_tmp.sh
scp ${ID}_gif_tmp.sh ${server}:${map_dir}
ssh ${server} ${map_dir}'/'${ID}'_gif_tmp.sh'

rm -f animation_preview.busy

