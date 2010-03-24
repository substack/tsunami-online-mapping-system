#!/bin/bash --login

. /usr/share/modules/init/bash
module load matlab
. /u1/uaf/nicolsky/.profile

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
  
   flag=0
   while [ "${flag}" -eq "0" ]; do
      #Check Matlab licenses
      str=$(lmstat -f Matlab | grep "Users of Matlab: " | sed 's/[a-zA-Z:;()]//g')
      issued=$(echo $str | awk '{print $1}')
      used=$(echo   $str | awk '{print $2}')
      if [ "${issued}" -eq "${used}" ]; then
         echo Error : No Matlab licenses are currently available 
      else
         matlab -nosplash -nodisplay -r "gname='$name';step=$step; preview();exit;"
         mv ${name}.max_dz.xyz ${name}_${ID}.max_dz.xyz 
         mv ${name}.max_fl.xyz ${name}_${ID}.max_fl.xyz 
         mv ${name}.H.xyz      ${name}_${ID}.H.xyz 
         flag=1 
      fi
      sleep 5
   done
done


tsfiles=$(ls ../*.ts)
if [ "${tsfiles}" != "" ]; then
   echo 'Creating PNG files'
   flag=0
   while [ "${flag}" -eq "0" ]; do
      #Check Matlab licenses
      str=$(lmstat -f Matlab | grep "Users of Matlab: " | sed 's/[a-zA-Z:;()]//g')
      issued=$(echo $str | awk '{print $1}')
      used=$(echo   $str | awk '{print $2}')
      if [ "${issued}" -eq "${used}" ]; then
         echo Error : No Matlab licenses are currently available 
      else
         rm -f tmp.m
   
         itsf=1 
         rm -f tmp.m
         for tsf in $tsfiles; do  
           name=${tsf##../Point_} 
           desc=$(grep ${name%.ts} ../list_points.tmp | awk -F'#' '{print $2}' | awk  '{for (i=2; i<=NF; i++) print $i}')
           echo "Case{"${itsf}"}={'"${name%.ts}"','"${desc}"','-r'};" >> tmp.m
           let itsf=itsf+1      
         done  
         matlab -nosplash -nodisplay -r "tmp(); ts2gif();exit;"
         cd .. 
         tar -cf - Point_*.ts | gzip -c > preview/points.tar.gz
         cd preview 
         flag=1  
      fi
      sleep 5
   done
fi


echo   'mkdir -p     '${html_map}'/'${ID}'/preview' > ${ID}_tmp.sh
echo   'chmod -R 777 '${html_map}'/'${ID}          >> ${ID}_tmp.sh
chmod 700 ${ID}_tmp.sh
scp ${ID}_tmp.sh ${server}:${map_dir}
ssh ${server} ${map_dir}'/'${ID}'_tmp.sh'

scp *.xyz ${server}:${html_map}/${ID}/preview   2>/dev/null
scp *.kml ${server}:${html_map}/${ID}/preview   2>/dev/null

grids=$(ls ../gBath*.bin)
for grid in ${grids}; do
  grid=${grid%.bin}
  grid=${grid#../gBath_}
  #echo $grid
  cd ../post_processing
  #tar -cf - nc_$grid*.nc | gzip -c > ../preview/${grid}.tar.gz
  
  psfiles=$(ls nc_$grid*.ps)
  for psf in $psfiles; do
    if [ ! -f ${psf%.ps}.gif ]; then
       convert -geometry 1000x1000 -density 300 -trim ${psf} ${psf%.ps}.gif 
    fi
  done  
  convert   -delay 30   -loop 0   nc_$grid*.gif   ../preview/animate_$grid.gif
  
  cd ../preview
done



#Copying files to burn
scp *.gif  *.png            ${server}:${html_map}/${ID}/preview
scp points.tar.gz           ${server}:${html_map}/${ID}/preview
scp loadXYZ.m               ${server}:${html_map}/${ID}/preview
scp netcdf.m                ${server}:${html_map}/${ID}/preview

ncfiles=$(ls ../post_processing/nc_*.nc)
for f in ${ncfiles}; do
   f=${f%.nc}
   if [ ! -f ${f}.copied ]; then
      scp ${f}.nc ${server}:${html_map}/${ID}/preview 
      touch ${f}.copied
   fi
done
scp ../*.ts                 ${server}:${html_map}/${ID}/preview 
scp ../list_points.tmp      ${server}:${html_map}/${ID}/preview 


echo   'chmod 644 '${html_map}'/'${ID}'/preview/*' > ${ID}_tmp.sh
scp ${ID}_tmp.sh ${server}:${map_dir}
ssh ${server} ${map_dir}'/'${ID}'_tmp.sh'


