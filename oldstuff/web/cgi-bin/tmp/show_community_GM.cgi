#!/bin/bash

map_dir=/export/burn/nicolsky/mapping
html_map=/usr/local/apache2/htdocs/mapping
farch=${html_map}/archive
server=http://burn.giseis.alaska.edu



line=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|/ /g' ); parameters=(${line})
iparameters=$((${#parameters[@]}-1))


for ((i=0;i<=$iparameters;i+=1)); do 
  str=${parameters[$i]}
  str=$(echo $str | sed 's/=/ /g')
  type=$(echo $str | awk '{print $1}')

  if [ "$type" == "ID" ]; then
     ID=$(echo $str | sed 's/ID //g');
  fi
done




echo Content-type: text/html
echo ""

grd=($(ls ${html_map}/${ID}/preview/*0000000.nc))
grds=$((${#grd[@]}-1))

gif=($(ls ${html_map}/${ID}/preview/*.gif))
gifs=$((${#gif[@]}-1))

tss=($(ls ${html_map}/${ID}/preview/*.ts))
itss=$((${#tss[@]}-1))

kml=($(ls ${html_map}/${ID}/preview/*.kml))
kmls=$((${#kml[@]}-1))


cat << EOM

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN"
   "http://www.w3.org/TR/html4/frameset.dtd">
<HTML>
<HEAD>

<TITLE>Alaska Tsunami Inundation Mapping Project: 
EOM
echo ${ID}
cat << EOM
</TITLE>
 
<script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAG07sBB-qC9yaNXELGJpf5BRrbJnNmETF966luGlbSTr_RfkmQBR_r9lzzhGueAMWoH_XbKNIdXA-uw" type="text/javascript"></script>
<script type="text/javascript">document.write('<script type="text/javascript" src="/scripts/extlargemapcontrol'+(document.location.search.indexOf('packed')>-1?'_packed':'')+'.js"><'+'/script>');</script>

    
<script type="text/javascript">
    //<![CDATA[

       var tmp_ngrids=0;
       var grid_focus=0;
       var grid_area=0;
EOM
echo '       var cid="'${ID}'";'
echo '       var map;'
echo '       var grids = '${grds}';'
echo '       var grid_name = new Array();'
echo ' '
cat<< EOM
       function load() {
EOM
if [ ! -f ${html_map}/${ID}/preview/finished.txt ]; then
echo '        setTimeout("window.location.reload();",30000);'
fi
cat<< EOM
        if (GBrowserIsCompatible()) {
             map = new GMap2(document.getElementById("map_canvas"));
             //map.setMapType(G_SATELLITE_MAP);
             map.addControl(new GMapTypeControl());
             map.setCenter(new GLatLng(59, -152.1419), 5);
	     map.disableDoubleClickZoom();
             var extLargeMapControl = new ExtLargeMapControl();
             map.addControl(extLargeMapControl);
EOM
for ((i=0;i<=$itss;i+=1)); do 
   latlon=($(head -1 ${tss[$i]} | awk '{print $1,$2}'))
   pname=${tss[$i]##${html_map}/${ID}/preview/Point_}
   pname=${pname%.ts}
   link=${server}/mapping/${ID}/preview/Point_${pname}
   name=$(awk -F'#' '{print $2}' ${html_map}/${ID}/preview/list_points.tmp | awk '{if ($1=="'${pname}'") for (i=2; i<=NF; i++) printf("%s ",$i)}' )
   echo "             var point = new GPoint("${latlon[0]}","${latlon[1]}");"
   echo "             var marker = createMarker(point,\""$name"\",\""$link"\");"
   echo "             map.addOverlay(marker); "
done



for ((i=0;i<=$kmls;i+=1)); do 
   pname=${kml[$i]##${html_map}/${ID}/preview/}
   echo '             var str="'${server}'/mapping/'${ID}'/preview/'$pname'";'
   echo '             var tmpkml=new GGeoXml(str);'
   echo "             map.addOverlay(tmpkml); "
done


for ((i=0;i<=${grds};i+=1)); do 
    name=${grd[$i]%0000000.nc}
    name=${name##${html_map}/${ID}/preview/nc_}
    echo '       grid_name['$i'] = new Array();'
    echo '       grid_name['$i'][0] = "'${name}'";'

    tmpstr=$(sed 's/ /,/g' ../htdocs/grids/${name}.mm)
    echo '       grid_name['$i'][1] = new Array('${tmpstr}');'
                 
done

cat << EOM
             show_grids(); 
        
             GEvent.addListener(map, "dblclick", function(e,crd) { 
                grid_focus=-1;
                grid_area=1e6;
  
                var lat=crd.y;
                var lon=crd.x;
                  
                if (crd.x < 0) lon+=360;
                checkNumberGrids(360+crd.x, crd.y);

                if (grid_focus>-1){
                   if(confirm("Grid "+grid_name[grid_focus][0]+".\nShow the time series at this point?")) 
                      showts(grid_name[grid_focus][0],lon,lat,map.getZoom());
                }
             });
        }
       }

       function  show_grids() {
           for (var i=0;i<=grids;i++){
                    var crds=grid_name[i][1];
                     grid_name[i][4] = new GPolygon([
                      new GLatLng( crds[2] , crds[0] ),
                      new GLatLng( crds[3] , crds[0] ),
                      new GLatLng( crds[3] , crds[1] ),
                      new GLatLng( crds[2] , crds[1] ),
                      new GLatLng( crds[2] , crds[0] )
                          ], "#f33f00", 1, 1, "#DD5500", 0.2);
                   map.addOverlay(grid_name[i][4]);
          }
       }

       function checkNumberGrids(lon, lat) {
	   for (var i = 0; i <= grids; i++){
              var coords=grid_name[i][1];
              var tmp_ga=(coords[1]-coords[0])*(coords[3]-coords[2]);
              if ( coords[0]<=lon && lon<=coords[1] && coords[2]<=lat && lat<=coords[3] && grid_area > tmp_ga) {
		 grid_focus=i;
                 grid_area=tmp_ga;
              }
           }
	}

       function createMarker(point,grid_str,link_str) {
	  var cIcon = new GIcon(G_DEFAULT_ICON);
          cIcon.image = "http://www.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png";
          var marker = new GMarker(point, {draggable:false, icon:cIcon});

          GEvent.addListener(marker, "click", function() {
             marker.openInfoWindowHtml(grid_str+"<br />"+"<a href='"+link_str+".ts' target='_blank'>ASCII data</a>"+
             " "+"<a href='"+link_str+"_Z.png' target='_blank'>Level</a>"+" "+"<a href='"+link_str+"_V.png' target='_blank'>Velocity</a>");
          });

          return marker;
       }


       function showgif(id){
          window.open(id,'','toolbar=yes,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no,width=900,height=600');
       }

       function showts(grid,lon,lat,zoom){
          window.open('http://burn.giseis.alaska.edu/cgi-bin/show_ats.cgi?zoom='+zoom+'&ID='+cid+'&lon='+lon+'&lat='+lat+'&field=Z&grid='+grid,'','toolbar=yes,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no,width=600,height=900');
       }
    //]]>
    </script>

</HEAD>
<body style="background-color:#F8F8F8" onload="load()" >

<div id="map_canvas" style="width:800px;height:500px"></div>

EOM
echo '<br />'
echo 
name=$(cat  ${map_dir}/${ID}/readme.txt | grep Name        | awk -F'=' '{print $2}')
tstime=$(cat ${html_map}/${ID}/preview/ts.time)
tstime=$(echo "${tstime}/60" | bc)
tstime=$(printf "%.2f" $tstime)
echo '<h2>Computational results, '${tstime}' minutes since the EQ:</h2>'
echo '<h3><a href="/cgi-bin/show_pbs.cgi?'${ID}'" target="_blank">'${ID}'</a>:'${name}'</h3>'
echo '<table BORDER=1 CELLPADDING=3 CELLSPACING=1  RULES=ROWS FRAME=HSIDES>'
echo '<thead><tr><th>Animation of sea level&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th><th align="left">NetCDFs to download</th></tr></thead>'
echo '<tbody>'
for ((i=0;i<=$gifs;i+=1)); do 
   pname=${gif[$i]##${html_map}/${ID}/preview/}
   grid=${pname##animate_}
   grid=${grid%.gif}
   lnk=${server}/mapping/${ID}/preview/$pname
   echo "<tr><td>Grid <a href='javascript:{showgif("\"$lnk\"");}'>"$grid"</a></td><td align='left'><a href='"$lnk"'>"$grid.tar.gz"</a></td><tr>"
done
echo '</tbody>'
echo '</table><br />'

if [ "${kmls}" != "-1" ]; then
   echo '<h3>Maximum recorded values in inundation grids:</h3>'
   echo '<table BORDER=1 CELLPADDING=3 CELLSPACING=1  RULES=ROWS FRAME=HSIDES>'
   echo '<tr><th></th>'
   for ((i=0;i<=${kmls};i+=1)); do 
      pname=${kml[$i]##${html_map}/${ID}/preview/}
      grid=${pname%.max_dz.kml}
      echo '<th>Grid '${grid}'</th>'
   done
   echo '</tr><tr><td>Maximum&nbsp&nbsp&nbsp</td>'
   for ((i=0;i<=${kmls};i+=1)); do 
      pname=${kml[$i]##${html_map}/${ID}/preview/}
      grid=${pname%.max_dz.kml}
      echo '<td><a href="'${server}/mapping/${ID}/preview/${grid}_${ID}.max_dz.xyz'">Water depth</a></td>'
   done
   echo '</tr><tr><td>Maximum&nbsp&nbsp&nbsp </td>'
   for ((i=0;i<=${kmls};i+=1)); do 
      pname=${kml[$i]##${html_map}/${ID}/preview/}
      grid=${pname%.max_dz.kml}
      echo '<td><a href="'${server}/mapping/${ID}/preview/${grid}_${ID}.max_fl.xyz'">Drag force</a></td>'
   done
   echo '</tr><tr><td>&nbsp&nbsp&nbsp</td>'
   for ((i=0;i<=${kmls};i+=1)); do 
      pname=${kml[$i]##${html_map}/${ID}/preview/}
      grid=${pname%.max_dz.kml}
      echo '<td><a href="'${server}/mapping/${ID}/preview/${grid}_${ID}.H.xyz'">Bathymetry</a></td>'
   done
   echo '</tr>'
   echo '</table><br />'
   for ((i=0;i<=${kmls};i+=1)); do 
      pname=${kml[$i]##${html_map}/${ID}/preview/}
      grid=${pname%.max_dz.kml}
      echo '<h3>Inundation area in '$grid':</h3>'
      echo '<a href="'${server}/mapping/${ID}/preview/MAP_${grid}_${ID}_01.eps'"><img src="'${server}/mapping/${ID}/preview/MAP_${grid}_${ID}.png'" /></a>'
   done
   echo '<ul>'
   echo '<li><b style="color:#FFCC00">Yellow line </b>-<b> Observed inundation after the 1964 tsunami,</b></li>'
   echo '<li><b style="color:#FF3300">Red line </b>-<b> Simulated inundation,</b></li>'
   echo '<li><b style="color:#3300CC">Blue line </b>-<b> Simulated coastline.</b></li>'
   echo '</ul>'
fi



if [ "${itss}" -ge "0" ]; then
   echo '<h3>Time series at watch points:</h3>'
   echo '<table BORDER=1 CELLPADDING=3 CELLSPACING=1  RULES=ROWS FRAME=HSIDES>'
   echo '<thead><tr><th align="left">Point</th><th align="left">Location</th><th align="left">Height&nbsp&nbsp&nbsp</th><th align="left">Velocity&nbsp&nbsp</th><th align="left">ASCII data</th></tr></thead>'
   echo '<tbody>'
   for ((i=0;i<=$itss;i+=1)); do 
      pname=${tss[$i]##${html_map}/${ID}/preview/Point_}
      pname=${pname%.ts}
      name=$(awk -F'#' '{print $2}' ${html_map}/${ID}/preview/list_points.tmp | awk '{if ($1=="'${pname}'") for (i=2; i<=NF; i++) printf("%s ",$i)}' )
      tslnk=${server}/mapping${tss[$i]##${html_map}}
      vglnk=${tslnk%.ts}_V.png
      zglnk=${tslnk%.ts}_Z.png
   echo '<tr><td>'${pname}'&nbsp&nbsp&nbsp</td>'
   echo '<td align="left">'${name}'&nbsp&nbsp&nbsp</td>'
   echo '<td align="left"><a href="'${zglnk}'" target="_blank">'PNG'</a>&nbsp</td>'
   echo '<td align="left"><a href="'${vglnk}'" target="_blank">'PNG'</a></td>'
   echo '<td align="left"><a href="'${tslnk}'" target="_blank">'${pname}.ts'</a></td></tr>'
   done
   echo '</tbody>'
   echo '</table>'
   echo '<br /><strong>Compressed data for <a href="'${server}/mapping/${ID}/preview/points.tar.gz'" target="_blank">all watch points</a></strong>'
fi

cat << EOM

<br /><hr />
<p><strong>Useful Matlab scripts:</strong></p>
Load a NetCDF file to Matlab <a href="${server}/mapping/${ID}/preview/netcdf.m">(download)</a><br />
Load an XYZ file to Matlab <a href="${server}/mapping/${ID}/preview/loadXYZ.m">(download)</a> <br />
</BODY>
</HTML>

EOM
