#!/bin/bash

echo Content-type: text/html
echo ""

#Parsing incomming parameters
line=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|G==/ /g'); points=(${line})
ipoints=$((${#points[@]}-1))



tmp_file_ms=grids/scratch/list_points_$RANDOM.tmp
tmp_file_tmp=grids/scratch/list_points_$RANDOM.tmp
tmp_file_dg=grids/scratch/list_points_$RANDOM.tmp

for ((i=0;i<=$ipoints;i+=1)); do 
  str=${points[$i]}
  str=($(echo $str | sed 's/&/ /g' | sed 's/%20/@/g' ));
  l=${#str[3]} 
  bar="@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
  let ll=15-l
  printf "%s %s  %4s  +  #%s %${ll}s %s\n" ${str[2]} ${str[1]} ${str[0]:0:4} ${str[3]} ${bar:0:ll} ${str[4]} >> ../htdocs/${tmp_file_tmp}
  sed 's/@/ /g' ../htdocs/${tmp_file_tmp} > ../htdocs/${tmp_file_ms}
done


sed 's/\./ /g' ../htdocs/${tmp_file_ms} | awk '{
       if (substr($3,3,1) == "N")
          flag_lat=1;
       else
          flag_lat=-1;
       if (substr($6,3,1) == "E")
          flag_lon=1;
       else
          flag_lon=-1;

       lat=flag_lat*($1+$2/60.0+substr($3,1,2)/3600);
       lon=flag_lon*($4+$5/60.0+substr($6,1,2)/3600);

       grid=$8;
       name=substr($9,2,length($9)-1);

       desc=$10;
       for (i=11; i<=NF; i++)
         desc=sprintf("%s %s",desc,$i);

       printf "%f, %f, %15s, %s, %s\n", lon, lat, name, grid, desc;
  }' > ../htdocs/${tmp_file_dg}




cat << EOM

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
  </head>
  <body>
  <a href="http://burn.giseis.alaska.edu:8090/${tmp_file_ms}">Save</a> the list in degree, minutes, and seconds,<br />
  <a href="http://burn.giseis.alaska.edu:8090/${tmp_file_dg}">Save</a> the list in decimal degrees, <br /> 

  <a href="http://burn.giseis.alaska.edu:8090/cgi-bin/addpoints.cgi?${tmp_file_ms}">Add</a> the list for the future.

  </body>
</html>

EOM
