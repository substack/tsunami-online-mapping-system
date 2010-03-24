#!/bin/bash

echo Content-type: text/html
echo ""


#Mapping directory
map_dir=/export/burn/wtest/mapping
html_map=/usr/local/apachedev/htdocs/mapping


#Obtain Case Number
case_number=$(cat $map_dir/last_id)
case_number=$(($case_number+1))


#Obtain a list of all grids
all_grids=$(grep '<Grid' $map_dir/grid_tree.xml | sed 's/<Grid file="//g' | sed 's/">//g' | sed 's/ //g')


#rm -rf ${map_dir}/CASE_R*

random_str=$(printf "%06d" $RANDOM)

tmp_dir=CASE_R_$random_str

mkdir -p ${map_dir}/${tmp_dir}

tmp_tree_file=${map_dir}/${tmp_dir}/tree_tmp.xml
tmp_file=${map_dir}/${tmp_dir}/tmp.xml
cp ${map_dir}/grid_tree.xml ${tmp_tree_file}

touch $map_dir/${tmp_dir}/list_points.tmp


#Parsing incomming parameters
line=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|/ /g' ); points=(${line})
ipoints=$((${#points[@]}-1))


tablestr="<table cellspacing="2" cellpadding="2" border="1"><tr><th>Latitude</th><th>Longitude</th><th>Grid</th><th>Label</th></tr>";

for ((i=0;i<=$ipoints;i+=1)); do 
  str=${points[$i]}
  str=$(echo $str | sed 's/=/ /g')
  type=$(echo $str | awk '{print $1}')
  
  if [ "$type" == "Point" ]; then
     str=($(echo $str | sed 's/Point //g' | sed 's/&/ /g' | sed 's/%20/@/g' ));
     tablestr=$(echo $tablestr "<tr> <td> "${str[2]}" </td><td> "${str[1]}" </td><td> "${str[0]:0:4}" </td><td> "${str[3]} "</td></tr>")

     l=${#str[3]} 
     bar="@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
     let ll=15-l
     printf "%s %s  %4s  +  #%s %${ll}s %s\n" ${str[2]} ${str[1]} ${str[0]:0:4} ${str[3]} ${bar:0:ll} ${str[4]} | sed 's/@/ /g' >> $map_dir/${tmp_dir}/list_points.tmp
     //echo ${str[2]}" "${str[1]}"  "${str[0]:0:4}"  +  #"${str[3]}${bar:0:ll} >> $map_dir/${tmp_dir}/list_points.tmp
  fi

  if [ "$type" == "DEF" ]; then
     deformation=$(echo $str | sed 's/DEF //g');
     deformation=${deformation##deformation_}
  fi

  if [ "$type" == "Friction" ]; then
     friction=$(echo $str | sed 's/Friction //g');
  fi

  if [ "$type" == "Level" ]; then
     level=$(echo $str | sed 's/Level //g');
  fi

  if [ "$type" == "EG" ]; then
     earth_gravity=$(echo $str | sed 's/EG //g');
  fi
  if [ "$type" == "ER" ]; then
     earth_radius=$(echo $str | sed 's/ER //g');
  fi
  if [ "$type" == "EO" ]; then
     earth_omega=$(echo $str | sed 's/EO //g');
  fi

  if [ "$type" == "TI" ]; then
     time_interval=$(echo $str | sed 's/TI //g');
  fi
  if [ "$type" == "DT" ]; then
     time_step=$(echo $str | sed 's/DT //g');
  fi
  if [ "$type" == "DS" ]; then
     time_output_step=$(echo $str | sed 's/DS //g');
  fi
  if [ "$type" == "PP" ]; then
     bath_pp=$(echo $str | sed 's/PP //g');
  fi


  if [ "$type" == "GRIDS" ]; then
     grids=$(echo $str | sed 's/GRIDS //g' | sed 's/;/ /g'); list_grids=(${grids});
     igrids=$((${#list_grids[@]}-1))
     grids="";
     for ((j=0;j<=$igrids;j+=1)); do
        g=${list_grids[$j]}
        g=${g%c}
        grids=$(echo ${g},${grids})
        all_grids=$(echo $all_grids | sed 's/'${g}'//g')
     done 
     list_useless_grids=(${all_grids});  iuseless_grids=$((${#list_useless_grids[@]}-1))
     
     for ((j=0;j<=${iuseless_grids};j+=1)); do
        g=${list_useless_grids[$j]}
        grep -v $g ${tmp_tree_file} | sed '/^$/d' | sed 's/ //g' > ${tmp_file}
        mv ${tmp_file} ${tmp_tree_file}
     done
     grids=${grids%,}
  fi
done
tablestr=$(echo $tablestr "</table>")


if [ "${bath_pp}" -eq "1" ]; then
  bath_type="Pre-earthquake topography"
else
  bath_type="Post-earthquake topography"
fi

time_interval_seconds=$(echo "scale=0; ${time_interval}*3600/${time_output_step}" | bc)
time_interval_seconds=$(echo "scale=0; ${time_interval_seconds}*${time_output_step}" | bc)


echo "Step                  =  "0                               >  ${map_dir}/${tmp_dir}/restart.tmp
echo "Computation time step =  "${time_step}                    >> ${map_dir}/${tmp_dir}/restart.tmp
echo "Output time step      =  "${time_output_step}             >> ${map_dir}/${tmp_dir}/restart.tmp
echo "Termination time      =  "${time_interval_seconds}        >> ${map_dir}/${tmp_dir}/restart.tmp
echo "Earth radius          =  "${earth_radius}                 >> ${map_dir}/${tmp_dir}/restart.tmp
echo "Gravity               =  "${earth_gravity}                >> ${map_dir}/${tmp_dir}/restart.tmp
echo "Omega                 =  "${earth_omega}                  >> ${map_dir}/${tmp_dir}/restart.tmp


#Creating readme html file

cat << EOF > ${map_dir}/${tmp_dir}/readme.html

<HTML>
<TITLE>Tsunami simulation parameters</TITLE>
<BODY>
<table cellspacing="2" cellpadding="2" border="0">
<tr><td align="right">Deformation model</td><td><input type="text" value="${deformation}" readonly/></td></tr>
<tr><td align="right">Grids</td>            <td><input type="text" value="${grids}"       readonly/></td></tr>
<tr><td></td></tr>
<tr><td align="right">Modeling time (h)</td>    <td><input type="text" value="${time_interval}"    readonly/></td></tr>
<tr><td align="right">Time step (s)</td>    <td><input type="text" value="${time_step}"    readonly/></td></tr>
<tr><td align="right">Output time step (s)</td>    <td><input type="text" value="${time_output_step}"    readonly/></td></tr>
<tr><td></td></tr>
<tr><td align="right">Bottom Friction</td>  <td><input type="text" value="${friction}"    readonly/></td></tr>
<tr><td align="right">Earth radius (m)</td>  <td><input type="text" value="${earth_radius}"    readonly/></td></tr>
<tr><td align="right">Earth gravity (m/s^2)</td>  <td><input type="text" value="${earth_gravity}"    readonly/></td></tr>
<tr><td align="right">Earth rotation (1/s)</td>  <td><input type="text" value="${earth_omega}"    readonly/></td></tr>
<tr><td></td></tr>
<tr><td align="right">Bathymetry level (m)</td> <td><input type="text" value="${level}"       readonly/></td></tr>
<tr><td align="right">Bathymetry type</td> <td><input type="text" value="${bath_type}"       readonly/></td></tr>
</table>

<p class="legend"><strong>Selected points:</strong></p>
$tablestr
<br />
Created on $(date)
<br />
<hr />
</BODY>
</HTML>

EOF


#Creating tree_grid file
tmp_tree_str=($(cat ${tmp_tree_file})); itmp_tree_str=$((${#tmp_tree_str[@]}-1))
rm -f ${tmp_tree_file}
for ((j=0;j<=$itmp_tree_str;j+=1)); do
   tmp_tree_token=($(echo ${tmp_tree_str[$j]} | sed 's/=/ /g'))
   if [ "${tmp_tree_token[0]}" == "</Gridfile" ]; then
       echo "</Grid>" >> ${tmp_tree_file}
   else
       echo "<Grid file="${tmp_tree_token[1]} >> ${tmp_tree_file}
   fi
done
mv ${tmp_tree_file} ${map_dir}/${tmp_dir}/grid_tree.xml
tmp_tree_file=${map_dir}/${tmp_dir}/grid_tree.xml

#Creating a root file

grid_name=$(head -1 ${tmp_tree_file} | sed 's/ //g' | sed 's/"/ /g' | awk '{print $2}')
tmp_grid_file=${map_dir}/${tmp_dir}/grid_${grid_name}.xml

cat << EOF > ${tmp_grid_file}
<grid>
  <bathymetry  file="/wrkdir/nicolsky/mapping/grids/DEM/${grid_name}.xyz" units="m"></bathymetry>
  <deformation file="/wrkdir/nicolsky/mapping/deformations/${deformation}.xyz" units="m"></deformation>
  <id name="${grid_name}"></id>
  <ratio lon="-1" lat="-1"></ratio>
  <corner west="-1" south="-1"></corner>
  <visualize color="b"></visualize>
  <physics type="propagation" friction="${friction}" level="${level}" bathpp="${bath_pp}"></physics>
</grid>
EOF



cat << EOM

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
  <Style>
    BODY, P,TD{ font-family: Arial,Verdana,Helvetica, sans-serif; font-size: 10pt }
    A{font-family: Arial,Verdana,Helvetica, sans-serif;}
    B {	font-family : Arial, Helvetica, sans-serif;	font-size : 12px;	font-weight : bold;}
    .error_strings{ font-family:Verdana; font-size:10px; color:#660000;}
    </Style>
  <script language="JavaScript" src="http://burn.giseis.alaska.edu/scripts/gen_validatorv31.js" type="text/javascript"></script>


  <script language="JavaScript" >


EOM
echo 'var points="'$tablestr'";'
echo 'var deformation="'${deformation}'";'
echo 'var grids="'${grids}'";'
echo 'var case_number="'${case_number}'";'
echo 'var level="'${level}'";'
echo 'var friction="'${friction}'";'
echo 'var CaseDir="'${tmp_dir}'";'
cat << EOM

     var frmvalidator;

     function DoCustomValidation(){
        var ans = prompt('Are you sure to submit this scenario? \nPlease, type "yes" to confirm.');
        if(ans.toLowerCase() != 'yes')
           return;

        var d=document.getElementsByName("CaseName")[0];
        var name=d.value;
        d=document.getElementsByName("Investigator")[0];
        var person=d.value;
        d=document.getElementsByName("CPU_time")[0];
        var cputime=d.value;
        
        var si=document.myform.Queue_type.selectedIndex;
        var QType=document.myform.Queue_type.options[si].value;

        d=document.getElementsByName("nodes_number")[0];
        var nodes_number=d.value;

        var si=document.myform.node_type.selectedIndex;
        var node_type=document.myform.node_type.options[si].value;
        
        document.myform.reset();
        if(document.error_disp_handler.all_msgs.length == 0){
           var str = "|CaseDir="+CaseDir+"|Name="+name+"|Person="+person+"|CPU_time="+cputime+"|QType="+QType+"|CaseNumber="+case_number+"|Deformation="+deformation;
           str=str+"|Nodes="+nodes_number+"|NodeType="+node_type;
           var w=window.open('/cgi-bin/priv/submit_scenario.cgi?'+str,'','toolbar=no,location=no,directories=no,status=no,menubar=no,width=400,height=200');
           self.close();
        }
     }

     function load(){
        var d=document.getElementsByName("deformation")[0];
        d.value=deformation;
        var d=document.getElementsByName("grids")[0];
        d.value=grids;
     }
     function popup(){
         var w=window.open('','','toolbar=no,location=no,directories=no,status=no,menubar=no,width=400,height=700');
         w.document.write('<TITLE>Selected points</TITLE>');
         w.document.write('<BODY>');
         w.document.write('<p class="legend"><strong>Selected points:</strong></p>');
         w.document.write(points);
         w.document.write('</BODY>');
         w.document.write('</HTML>');
     }

  </script> 

  </head>
  <body onload="load();">
  

<form name="myform">
<table cellspacing="2" cellpadding="2" border="0">
<tr><td align="right" class="legend"><strong>Scenario</strong></td>
EOM
echo '<td><strong>'$case_number'</strong></td></tr>'
cat << EOM
<tr><td align="right">Description</td><td><input type="text" name="CaseName" value=""/></td></tr>
<tr><td align="right">Principal investigator</td><td><input type="text" name="Investigator" value="John Doe"/></td></tr>
<tr><td align="right">&nbsp</td><td>&nbsp</td></tr>
<tr><th align="right">Scenario information</th><td>&nbsp</td></tr>
<tr><td align="right">Deformation model</td><td><input type="text" name="deformation" readonly/></td></tr>
<tr><td align="right">Grids</td><td><input type="text" name="grids" readonly/></td></tr>
<tr><td align="right">Points</td><td><a href="javascript:popup()">List</a></td></tr>

<tr><td align="right">&nbsp</td><td>&nbsp</td></tr>
<tr><th align="right">Queue information</th><td>&nbsp</td></tr>
<tr><td align="right">CPU hours</td><td><input type="text" name="CPU_time" value="8"/></td></tr>
<tr><td align="right">Queue type</td><td>
                     <select id='Queue_type'>
                        <option value="standard">Standard</option>
                        <option value="debug">Debug</option>
                        <option value="background">Background</option>
                     </select>
</td></tr>
<tr><td align="right">CPU node type</td><td>
                     <select id='node_type'>
                        <option value="4">4way</option>
                        <option value="16">16way</option>
                     </select>
</td></tr>
<tr><td align="right">Number of nodes</td><td><input type="text" name="nodes_number" value="8"/></td></tr>

<tr><td align="right"></td><td><div id='myform_errorloc' class='error_strings'></div></td></tr>
<tr><td align="right"></td><td><input type="button" value="Submit the case" onclick='DoCustomValidation();' /></td></tr>
</table>
</form>



<script language="JavaScript" type="text/javascript">
//You should create the validator only after the definition of the HTML form
 frmvalidator  = new Validator_onreset("myform");
 frmvalidator.EnableOnPageErrorDisplaySingleBox();
 frmvalidator.EnableMsgsTogether();


  frmvalidator.addValidation("CaseName","req","Please enter a short description");
  frmvalidator.addValidation("CaseName","maxlen=20",	"Max length for description is 20 characters");
  frmvalidator.addValidation("CaseName","alphanumeric","Name can contain alphabetic or numeric chars only");

  frmvalidator.addValidation("Investigator","maxlen=20");
  frmvalidator.addValidation("Investigator","req");
  frmvalidator.addValidation("Investigator","alpha","Principal investigator can contain alphabetic chars only. ");

  frmvalidator.addValidation("CPU_time","req","Please enter the requested CPU time");
  frmvalidator.addValidation("CPU_time","numeric","CPU hours can contain numeric chars only");

  frmvalidator.addValidation("nodes_number","req","Please enter the requested number of nodes");
  frmvalidator.addValidation("nodes_number","numeric","Number of nodes can contain numeric chars only");

  //frmvalidator.addValidation("LastName","req","Please enter your Last Name");
  //frmvalidator.addValidation("LastName","maxlen=20","For LastName, Max length is 20");
  
  //frmvalidator.addValidation("Address","maxlen=50");
  //frmvalidator.addValidation("Country","dontselect=0");
</script>

EOM
echo '<b>Currently available nodes:</b><hr/>'
echo '<table cellspacing="2" cellpadding="2" border="0">'
echo '<tr><th align="left">Nodes</th><th align="left">Standard</th><th align="left">Debug</th></tr>'
cat ${html_map}/current_nodes
#
#awk '{
#print "<tr><td>",$1,$2 "</td><td>",$3,"</td><td>",$4,"</td><td>",$5,"</td></tr>"
#}' ${html_map}/current_nodes
echo '</table>'
cat << EOM

  </body>
</html>

EOM
