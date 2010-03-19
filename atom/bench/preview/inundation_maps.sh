#!/bin/bash --login

. /usr/share/modules/init/bash
module load matlab
. /u1/uaf/nicolsky/.profile


name=$1
ID=$2
step=$3
echo 'Creating GeoTiff images for '$name' grid'
   
cp ../../grids/$name.image .
cp ../../grids/$name.frame .
cp ../../grids/$name.line .
if [ -f $name.image ]; then
   flag=0
   while [ "${flag}" -eq "0" ]; do
      #Check Matlab licenses
      str=$(lmstat -f Matlab | grep "Users of Matlab: " | sed 's/[a-zA-Z:;()]//g')
      issued=$(echo $str | awk '{print $1}')
      used=$(echo   $str | awk '{print $2}')
      if [ "${issued}" -eq "${used}" ]; then
         echo Error : No Matlab licenses are currently available 
      else
         matlab -nosplash -nodisplay -r "name='$name'; step='$step'; ID='$ID'; inundation_maps();exit;"
         flag=1 
      fi
      sleep 5
   done
fi
