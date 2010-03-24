#!/bin/bash 

server=burn.giseis.alaska.edu

map_dir=/export/burn/nicolsky/mapping
html_map=/usr/local/apache2/htdocs/mapping



ID=$1
rm -f points.tar.gz


step=$(grep Step ../restart.tmp | awk -F'=' '{print $2}')
dt=$(grep Computation ../restart.tmp | awk -F'=' '{print $2}')
dt=$(printf "%10f" ${dt})

ctime=$(echo "scale=0; ${dt}*${step}" | bc )
otime=$(cat ts.time)
otime=$(echo "scale=0; ${otime}" | bc )


if [ "$ctime" != "$otime" ]; then

   echo $ctime > ts.time

   tsfiles=$(ls ../*.ts)
   if [ "${tsfiles}" != "" ]; then
      echo 'Creating PNG files'
  
      for tsf in $tsfiles; do  
         name=${tsf##../Point_}
         name=${name%.ts}
         desc=$(awk -F'#' '{print $2}' ../list_points.tmp | awk '{if ($1=="'${name}'") for (i=2; i<=NF; i++) printf("%s ",$i)}' )

         gnuplot << EOC 
            set term postscript
            set output "Point_${name}_Z.ps"
            set ylabel "Sea level, m/sec"
            set xlabel "Time after the earthquake, min"

            set xtics 60
            set mxtics 4

            set grid xtics ytics mxtics mytics
            plot "<awk '{print \$1/60,\$2}' ${tsf}" using 1:2 every ::2 with lines title "${desc}"
EOC
         gnuplot << EOC 
            set term postscript
            set output "Point_${name}_V.ps"
            set ylabel "Velocity, m/sec"
            set xlabel "Time after the earthquake, min"

            set xtics 60
            set mxtics 4

            set grid xtics ytics mxtics mytics
            plot "<awk '{print \$1/60,(\$3<0.1) ? 0.0 : sqrt(\$4*\$4+\$5*\$5)/\$3}' ${tsf}" using 1:2 every ::2 with lines title "${desc}"
EOC
            convert -rotate 90 Point_${name}_V.ps Point_${name}_V.png
            convert -rotate 90 Point_${name}_Z.ps Point_${name}_Z.png
      done
   fi
   
   
   

   echo   'mkdir -p     '${html_map}'/'${ID}'/preview' > ${ID}_ts_tmp.sh
   echo   'chmod -R 777 '${html_map}'/'${ID}          >> ${ID}_ts_tmp.sh
   chmod 700 ${ID}_ts_tmp.sh
   scp ${ID}_ts_tmp.sh ${server}:${map_dir}
   ssh ${server} ${map_dir}'/'${ID}'_ts_tmp.sh'


   #Copying files to burn
   scp ts.time                ${server}:${html_map}/${ID}/preview
   scp *.png                   ${server}:${html_map}/${ID}/preview
   scp ../*.ts                 ${server}:${html_map}/${ID}/preview 
   scp ../list_points.tmp      ${server}:${html_map}/${ID}/preview 


   echo   'chmod 644 '${html_map}'/'${ID}'/preview/*' > ${ID}_ts_tmp.sh
   scp ${ID}_ts_tmp.sh ${server}:${map_dir}
   ssh ${server} ${map_dir}'/'${ID}'_ts_tmp.sh'

fi

rm -f ts_preview.busy

