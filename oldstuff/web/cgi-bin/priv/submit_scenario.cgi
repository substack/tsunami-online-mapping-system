#!/bin/bash

echo Content-type: text/html
echo ""

#Mapping directory
map_dir=/export/burn/wtest/mapping
html_map=/usr/local/apachedev/htdocs/mapping




#Parsing incomming parameters
line=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|/ /g' ); points=(${line})
ipoints=$((${#points[@]}-1))


for ((i=0;i<=$ipoints;i+=1)); do 
  str=${points[$i]}
  str=$(echo $str | sed 's/=/ /g')
  type=$(echo $str | awk '{print $1}')
  
  if [ "$type" == "CaseDir" ]; then
     tmp_dir=$(echo $str | sed 's/CaseDir //g');
  fi

  if [ "$type" == "Name" ]; then
     name=$(echo $str | sed 's/Name //g' );
  fi

  if [ "$type" == "Person" ]; then
     person=$(echo $str | sed 's/Person //g' | sed 's/%20/ /g');
  fi

  if [ "$type" == "CaseNumber" ]; then 
     number=$(echo $str | sed 's/CaseNumber //g');
  fi

  if [ "$type" == "CPU_time" ]; then
     cputime=$(echo $str | sed 's/CPU_time //g');
  fi

  if [ "$type" == "Deformation" ]; then
     deformation=$(echo $str | sed 's/Deformation //g');
  fi

  if [ "$type" == "Nodes" ]; then
     nodes=$(echo $str | sed 's/Nodes //g');
  fi

  if [ "$type" == "NodeType" ]; then
     node_type=$(echo $str | sed 's/NodeType //g');
  fi

  if [ "$type" == "QType" ]; then
     QType=$(echo $str | sed 's/QType //g');
  fi

done

str_number=$(printf "%06d" $number)
mv ${map_dir}/${tmp_dir} ${map_dir}/CASE_${str_number}

cp ${map_dir}/CASE_${str_number}/readme.html ${html_map}/CASE_${str_number}.html

echo 'Investigator = '$person          >  ${map_dir}/CASE_${str_number}/readme.txt
echo 'Name         = '$name            >> ${map_dir}/CASE_${str_number}/readme.txt
echo 'CPU          = '$cputime         >> ${map_dir}/CASE_${str_number}/readme.txt
echo 'Deformation  = '$deformation     >> ${map_dir}/CASE_${str_number}/readme.txt
echo 'Nodes        = '$nodes           >> ${map_dir}/CASE_${str_number}/readme.txt
echo 'NodeType     = '$node_type       >> ${map_dir}/CASE_${str_number}/readme.txt
echo 'QueueType    = '$QType           >> ${map_dir}/CASE_${str_number}/readme.txt

echo $name > ${map_dir}/CASE_${str_number}.pending

#Obtain Case Number
case_number=$(cat $map_dir/last_id)
case_number=$(($case_number+1))
echo $case_number > $map_dir/last_id


cat << EOM
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head></head>
  <body onload='setTimeout("window.close();",1500);'>
  <h3>  Your scenario has been submitted. </h3>
  </body>
</html>

EOM
