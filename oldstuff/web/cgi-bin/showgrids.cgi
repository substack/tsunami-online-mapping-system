#!/bin/bash

echo Content-type: text/html
echo ""


#Parsing available grids
list_grids=$(ls ../htdocs/grids/*.extent)
let i=0
for grid in $list_grids; do
  grid=${grid##../htdocs/grids/} 
  grid=${grid%.extent}
  grids[i]=$grid
  let i=i+1 
done
igrids=$((${#grids[@]}-1))

#Parsing available deformations
list_deformations=$(ls ../htdocs/deformations/*.png)
let i=0
for file in $list_deformations; do
  file=${file##../htdocs/deformations/} 
  file=${file%.png}
  deformations[i]=$file
  let i=i+1 
done
ideformations=$((${#deformations[@]}-1))


#Parsing available coast lines
list_clines=$(ls ../htdocs/grids/*.kml)
let i=0
for file in $list_clines; do
  file=${file##../htdocs/grids/} 
  file=${file%.kml}
  clines[i]=$file
  let i=i+1 
done
iclines=$((${#clines[@]}-1))


#Parsing available lists of points
list_scripts=$(ls ../htdocs/scripts/list_*.js)
let i=0
for file in $list_scripts; do
  file=${file##../htdocs/scripts/list_}
  file=${file%.js} 
  scripts[i]=$file
  let i=i+1 
done
iscripts=$((${#scripts[@]}-1))



cat << EOM

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>

    <Style>
    BODY, P,TD{ font-family: Arial,Verdana,Helvetica, sans-serif; font-size: 10pt }
    A{font-family: Arial,Verdana,Helvetica, sans-serif;}
    B {	font-family : Arial, Helvetica, sans-serif;	font-size : 12px;	font-weight : bold;}
    .error_strings{ font-family:Verdana; font-size:10px; color:#660000;}
    </Style>

    <title>Google Maps JavaScript API Example</title>
    <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAG07sBB-qC9yaNXELGJpf5BRrbJnNmETF966luGlbSTr_RfkmQBR_r9lzzhGueAMWoH_XbKNIdXA-uw" type="text/javascript"></script>
    <script type="text/javascript">document.write('<script type="text/javascript" src="/scripts/extlargemapcontrol'+(document.location.search.indexOf('packed')>-1?'_packed':'')+'.js"><'+'/script>');</script>

    <script src="http://burn.giseis.alaska.edu/scripts/fault.js" type="text/javascript"></script>
    <script src="http://burn.giseis.alaska.edu/scripts/sprintf.js" type="text/javascript"></script>
    <script src="http://burn.giseis.alaska.edu/scripts/wz_jsgraphics.js" type="text/javascript"></script>
    <script src="http://burn.giseis.alaska.edu/scripts/gen_validatorv31.js" type="text/javascript"></script>

EOM
for ((i=0;i<=${iscripts};i+=1)); do 
    file=${scripts[$i]}
    echo '    <script src="http://burn.giseis.alaska.edu:8090/scripts/list_'$file'.js" type="text/javascript"></script>'
done
cat << EOM

    <script type="text/javascript">

    
   
    //<![CDATA[
     
       var frmvalidator;

       var counter=0;
       var tmp_ngrids, focus_grid;
       var map;
       var jg;

       var pi = 3.141592653589793; 


       var fault_list =  new Array();
       var fault_counter=0;

       var newdefwindow;


 
       var markers = new Array();

       var sort_type=1;
       var sort_previous=1;
       var sort_direction=1; 

       var lastFocus=-1;

       var old_deformation="";
       var old_coastline="";
       var coastline_kml;

       var priority_map = new Array();
       var priority_vis = new Array();

       var display_np   = 0;
       var display_p    = 0;
       var display_pp   = 10;

EOM

echo ' '
echo '       //Available deformations '
echo ' '
for ((i=0;i<=${ideformations};i+=1)); do 
    file=${deformations[$i]}
    echo '       var deformation_'${file}';'
done

echo '  '
echo '       //Available grids '
echo ' '
echo '       var grids = '${igrids}';'
echo '       var grid_name = new Array();'
for ((i=0;i<=${igrids};i+=1)); do 
    grid=${grids[$i]}
    echo '       grid_name['$i'] = new Array();'
    echo '       grid_name['$i'][0] = "'${grid}'";'

    tmpstr=$(sed 's/ /,/g' ../htdocs/grids/${grid}.mm)
    echo '       grid_name['$i'][1] = new Array('${tmpstr}');'
    echo '       grid_name['$i'][2] = 0;'
done


cat << EOM

       function unload() {
             if(newdefwindow != null) 
             newdefwindow.window.close();
       }

       function load() {

          var R = 6371; // km
          if (GBrowserIsCompatible()) {

             

             map = new GMap2(document.getElementById("map_canvas"));

             //map.setMapType(G_SATELLITE_MAP);
             map.addControl(new GMapTypeControl());
             map.setCenter(new GLatLng(59, -152.1419), 5);
             var extLargeMapControl = new ExtLargeMapControl();
             map.addControl(extLargeMapControl);
	     map.disableDoubleClickZoom();

             jg = new jsGraphics(document.getElementById("map_canvas"));
             
EOM

  echo '             //Define deformation overlays'
for ((i=0;i<=$ideformations;i+=1)); do 
  file=${deformations[$i]} 
  list=$(cat ../htdocs/deformations/$file.extent); bar=(${list}); 
  echo '             var boundaries_'$file'  = new GLatLngBounds(new GLatLng('${bar[2]},${bar[0]}'), new GLatLng('${bar[3]},${bar[1]}'));'
  echo '             deformation_'$file' = new GGroundOverlay("http://burn.giseis.alaska.edu/'deformations/$file.png'", boundaries_'$file');'
  echo ' '
done

cat << EOM

             for(var i=0; i<=grids;i++){
//                str="http://burn.giseis.alaska.edu/grids/"+grid_name[i][0]+".kml"
                grid_name[i][5]=""; //new GGeoXml(str);
             }

             for(var i=0; i<7; i++){
                priority_map[i] = new GGeoXml("http://burn.giseis.alaska.edu/kml/priority_list_"+(i+1)+".kml");
                priority_vis[i] = -1;
             }

             GEvent.addListener(map, "dblclick", function(e,crd) { 
                tmp_ngrids=0;
                if (crd.x < 0)
                   checkNumberGrids(360+crd.x, crd.y);
                else
                   checkNumberGrids(crd.x, crd.y);

                
                
                   if(confirm("Would you like to add a new deformation model?")){
                      openDEFWindow();

                      var M=createEQMarker(crd);
                      fault_list[fault_counter-1].M=M;
                      map.addOverlay(fault_list[fault_counter-1].M);

                      var l=newdefwindow.window.updateMarkerTable();
                      newdefwindow.window.updagePages(l);

                      return;
                   }
                


                if (tmp_ngrids>1) 
                   alert("The selected point lies within more than one grid."); 
                else if (tmp_ngrids==1){
		    if (confirm("Would you like to add a new watch point to " + grid_name[focus_grid][0] + " grid?")){
                        var marker = createMarker(crd, counter,grid_name[focus_grid][0]);
                        map.addOverlay(marker); 
                        markers[counter]=marker;
                        counter++;
			var l=updateMarkerTable();
			updagePages(l);
                    }
                }
                updateMarkerTable();
             });

             GEvent.addListener(map, "move", function() { 
                  redrawBBs();
             });
          }

          var selObj = document.getElementById('deformations');
          selObj.options[0].selected=true;

          var selObj = document.getElementById('select_markers');
          selObj.options[0].selected=true;
       }

function openDEFWindow(){
   if(newdefwindow == null)
       newdefwindow=window.open('/cgi-bin/new_deformation.cgi','','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no,width=900,height=500');
   else{
       if(newdefwindow.window.closed)
           newdefwindow=window.open('/cgi-bin/new_deformation.cgi','','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no,width=900,height=500');
  }
}

function createEQMarker(point) {
	  var cIcon = new GIcon(G_DEFAULT_ICON);
          cIcon.image = "http://www.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png";
          
          var number = fault_counter;

          var marker = new GMarker(point, {draggable:true, icon:cIcon});
          marker.initial = point;
          marker.point   = point;
          marker.number  = number;
          marker.flag_clicked=0;
          
          var strlon=Dec2Deg(point.x,'W','E',1);
          var strlat=Dec2Deg(point.y,'S','N',1);

          addFault(number, strlon, strlat, '---', '---', '---', '---', '---', '---', '---');
         
          fault_list[number].lon0=point.x;
          fault_list[number].lat0=point.y;


          GEvent.addListener(marker, "drag", function(latlng) {
             fault_list[number].lon0=latlng.x;
             fault_list[number].lat0=latlng.y;

             fault_list[number].lon=Dec2Deg(latlng.x,'W','E',1);
             fault_list[number].lat=Dec2Deg(latlng.y,'S','N',1);
  
             var l=newdefwindow.window.updateMarkerTable();
             newdefwindow.window.updagePages(l);

             if(fault_list[number].length != '---' && isNaN(fault_list[number].length) == false &&
                fault_list[number].strike != '---' && isNaN(fault_list[number].strike) == false)
                updateStrike(number,fault_list[number].strike);
             
             if(fault_list[number].width !='---' && isNaN(fault_list[number].width) == false)
                updateWidth(number,fault_list[number].width);

          });
          GEvent.addListener(marker, "click", function(latlng) {
             if(marker.flag_clicked==0){
                marker.FaultMarker = createFaultMarker(number,latlng);
                map.addOverlay(marker.FaultMarker);
                marker.flag_clicked=1;
             }
          });
          return marker;
       }



function createFaultMarker(number,point) {
	  var cIcon = new GIcon(G_DEFAULT_ICON);
          cIcon.image = "http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png";

          var R = 6371; // km
          
          var marker = new GMarker(point, {draggable:true, icon:cIcon});
          
          marker.initial = point;
          marker.point   = point;
          marker.number  = number;
          marker.flag_clicked=0;
          
          var points = [];
          points.push(point);
          marker.polygonFault = new GPolyline(points);
          map.addOverlay(marker.polygonFault);

               
          GEvent.addListener(marker, "drag", function(latlng) {
             fault_list[number].lon1=latlng.x;
             fault_list[number].lat1=latlng.y;

             map.removeOverlay(marker.polygonFault);
             var points = [];
             points.push(new GPoint(fault_list[number].lon0,fault_list[number].lat0));
             points.push(new GPoint(fault_list[number].lon1,fault_list[number].lat1));
             marker.polygonFault = new GPolyline(points, "#F88017");
             map.addOverlay(marker.polygonFault);


             var lon0=fault_list[number].lon0;   if(lon0<0) lon0+=360;
             var lon1=latlng.x;                  if(lon1<0) lon1+=360;
             var lat0=fault_list[number].lat0;
             var lat1=latlng.y;


             //Computing the LENGHT
             var dLat = (lat1-lat0)/180*pi;
             var dLon = (lon1-lon0)/180*pi; 
             var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                     Math.cos(lat0/180*pi) * Math.cos(lat1/180*pi) * 
                     Math.sin(dLon/2) * Math.sin(dLon/2); 
             var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 

             fault_list[number].length = sprintf('%5.1f',R * c);

             //Compute the STRIKE
             var y = Math.sin(dLon) * Math.cos(lat1/180*pi);
             var x = Math.cos(lat0/180*pi)*Math.sin(lat1/180*pi) -
                     Math.sin(lat0/180*pi)*Math.cos(lat1/180*pi)*Math.cos(dLon);
             var brng = Math.atan2(y, x)/pi*180;  if(brng<0) brng+=360;
             fault_list[number].strike = brng;

             if(fault_list[number].width !='---' && isNaN(fault_list[number].width) == false)
                updateWidth(number,fault_list[number].width);


             var l=newdefwindow.window.updateMarkerTable();
             newdefwindow.window.updagePages(l);
          });
          GEvent.addListener(marker, "click", function(latlng) {
             if(marker.flag_clicked==0){
                marker.WidthMarker = createWidthMarker(number,latlng);
                map.addOverlay(marker.WidthMarker);
                marker.flag_clicked=1;
             }
          });

          return marker;
       }

function updateLat(n,value){

     var lonval=Deg2Dec(value); 
     if(lonval=='Oops')
         lonval=value;


             fault_list[n].lat0=lonval;

             fault_list[n].lat=Dec2Deg(lonval,'S','N',1);


             fault_list[n].M.setLatLng(new GLatLng(fault_list[n].lat0,fault_list[n].lon0));

             if(fault_list[n].length != '---' && isNaN(fault_list[n].length) == false &&
                fault_list[n].strike != '---' && isNaN(fault_list[n].strike) == false)
                updateStrike(n,fault_list[n].strike);
             
             if(fault_list[n].width !='---' && isNaN(fault_list[n].width) == false)
                updateWidth(n,fault_list[n].width);
}

function updateLon(n,value){

     var lonval=Deg2Dec(value); 
     if(lonval=='Oops')
         lonval=value;


             fault_list[n].lon0=lonval;

             fault_list[n].lon=Dec2Deg(lonval,'W','E',1);


             fault_list[n].M.setLatLng(new GLatLng(fault_list[n].lat0,fault_list[n].lon0));

             if(fault_list[n].length != '---' && isNaN(fault_list[n].length) == false &&
                fault_list[n].strike != '---' && isNaN(fault_list[n].strike) == false)
                updateStrike(n,fault_list[n].strike);
             
             if(fault_list[n].width !='---' && isNaN(fault_list[n].width) == false)
                updateWidth(n,fault_list[n].width);
}

function updateStrike(n,value){
      var R = 6371; // km

      var lon1=fault_list[n].lon0/180*pi;
      var lat1=fault_list[n].lat0/180*pi;
      var d=fault_list[n].length;

      fault_list[n].strike = value;

      var lat2 = Math.asin( Math.sin(lat1)*Math.cos(d/R) + 
                            Math.cos(lat1)*Math.sin(d/R)*Math.cos(value/180*pi) );
      var lon2 = lon1 + Math.atan2(Math.sin(value/180*pi)*Math.sin(d/R)*Math.cos(lat1), 
                                   Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2));

      fault_list[n].lon1= lon2*180/pi;
      fault_list[n].lat1= lat2*180/pi;

      var marker = fault_list[n].M.FaultMarker;
      if(marker != null){ 
         marker.setLatLng(new GLatLng(fault_list[n].lat1,fault_list[n].lon1));
         map.removeOverlay(marker.polygonFault);
         var points = [];
         points.push(new GPoint(fault_list[n].lon0,fault_list[n].lat0));
         points.push(new GPoint(fault_list[n].lon1,fault_list[n].lat1));
         marker.polygonFault = new GPolyline(points, "#F88017");
         map.addOverlay(marker.polygonFault);
      }
      else{
         if(fault_list[n].length != '---' && isNaN(fault_list[n].length) == false &&
            fault_list[n].strike != '---' && isNaN(fault_list[n].strike) == false){
              fault_list[n].M.FaultMarker = createFaultMarker(n,new GLatLng(lat2,lon2));
              fault_list[n].M.flag_clicked=1;
              map.addOverlay(fault_list[n].M.FaultMarker);
              updateLength(n,fault_list[n].length);
         }
      }
      if(fault_list[n].width !='---' && isNaN(fault_list[n].width) == false)
         updateWidth(n,fault_list[n].width);
}

function updateLength(n,value){
      var R = 6371; // km

      var lon1=fault_list[n].lon0/180*pi;
      var lat1=fault_list[n].lat0/180*pi;
      var d=value;
      fault_list[n].length = value;

      strike=fault_list[n].strike;

      var lat2 = Math.asin( Math.sin(lat1)*Math.cos(d/R) + 
                            Math.cos(lat1)*Math.sin(d/R)*Math.cos(strike/180*pi) );
      var lon2 = lon1 + Math.atan2(Math.sin(strike/180*pi)*Math.sin(d/R)*Math.cos(lat1), 
                                   Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2));

      fault_list[n].lon1= lon2*180/pi;
      fault_list[n].lat1= lat2*180/pi;

      var marker = fault_list[n].M.FaultMarker;
      if(marker !=null){
         marker.setLatLng(new GLatLng(fault_list[n].lat1,fault_list[n].lon1));
         map.removeOverlay(marker.polygonFault);
         var points = [];
         points.push(new GPoint(fault_list[n].lon0,fault_list[n].lat0));
         points.push(new GPoint(fault_list[n].lon1,fault_list[n].lat1));
         marker.polygonFault = new GPolyline(points, "#F88017");
         map.addOverlay(marker.polygonFault); 
      }
      else{
         if(fault_list[n].length != '---' && isNaN(fault_list[n].length) == false &&
            fault_list[n].strike  != '---' && isNaN(fault_list[n].strike)  == false){
              fault_list[n].M.FaultMarker = createFaultMarker(n,new GLatLng(lat2,lon2));
              fault_list[n].M.flag_clicked=1;
              map.addOverlay(fault_list[n].M.FaultMarker);
              updateLength(n,fault_list[n].length);
         }
      }
      if(fault_list[n].width !='---' && isNaN(fault_list[n].width) == false)
         updateWidth(n,fault_list[n].width);
}




 function createWidthMarker(number, point) {
         
	  var cIcon = new GIcon(G_DEFAULT_ICON);
          cIcon.image = "http://www.google.com/intl/en_us/mapfiles/ms/micons/green-dot.png";

          var R = 6371; // km
          var marker = new GMarker(point, {draggable:true, icon:cIcon});
          marker.initial = point;
          marker.point   = point;
          marker.number  = number;

          var points = [];
          points.push(point);
          marker.polygonFault = new GPolyline(points);
          map.addOverlay(marker.polygonFault);
          

          GEvent.addListener(marker, "drag", function(latlng) {
             // marker.openInfoWindowHtml("Just drag a marker to a desired location ...");
             var brng = fault_list[number].strike;
             var brng90 = (brng-90)/180*pi;

             var lon1=latlng.x/180*pi;
             var lat1=latlng.y/180*pi;
             var lon2=fault_list[number].lon0/180*pi;
             var lat2=fault_list[number].lat0/180*pi;

             var dLat = lat2-lat1;
             var dLon = lon2-lon1; 
             var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                     Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon/2) * Math.sin(dLon/2); 
             var d0 = 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));

             
             var d = -getmin(d0,brng, brng90, lon1, lat1, lon2, lat2);
             //d = Math.max(Math.abs(d),0);
             //var b = brngmin(d, brng, brng90, lon1, lat1, lon2, lat2);

             updateWidth(number,Math.min(d,0));
             var l=newdefwindow.window.updateMarkerTable();
             newdefwindow.window.updagePages(l);
          });
          return marker;
       }

function updateWidth(n,value){
      var R = 6371; // km

      fault_list[n].width = sprintf('%5.1f',-Math.abs(value));
      var d = -Math.abs(value);

      var brng = fault_list[n].strike;
      var brng90 = (brng-90)/180*pi;
      

      var points = [];
      points.push(new GPoint(fault_list[n].lon0,fault_list[n].lat0));

      var lon1=fault_list[n].lon0/180*pi;
      var lat1=fault_list[n].lat0/180*pi;
      var lat2 = Math.asin( Math.sin(lat1)*Math.cos(d/R) + 
                            Math.cos(lat1)*Math.sin(d/R)*Math.cos(brng90) );
      var lon2 = lon1 + Math.atan2(Math.sin(brng90)*Math.sin(d/R)*Math.cos(lat1), 
                                          Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2));
      points.push(new GPoint(lon2/pi*180,lat2/pi*180));

      var lon1=fault_list[n].lon1/180*pi;
      var lat1=fault_list[n].lat1/180*pi;
      var lat2 = Math.asin( Math.sin(lat1)*Math.cos(d/R) + 
                            Math.cos(lat1)*Math.sin(d/R)*Math.cos(brng90) );
      var lon2 = lon1 + Math.atan2(Math.sin(brng90)*Math.sin(d/R)*Math.cos(lat1), 
                                   Math.cos(d/R)-Math.sin(lat1)*Math.sin(lat2));
      points.push(new GPoint(lon2/pi*180,lat2/pi*180));
      points.push(new GPoint(lon1/pi*180,lat1/pi*180));


      if(fault_list[n].M.FaultMarker != null){
         var marker = fault_list[n].M.FaultMarker.WidthMarker;
         if(marker == null){
            fault_list[n].M.FaultMarker.WidthMarker = createWidthMarker(n,new GLatLng(lat2/pi*180,lon2/pi*180));
            map.addOverlay(fault_list[n].M.FaultMarker.WidthMarker);
            fault_list[n].M.FaultMarker.flag_clicked=1;
            marker = fault_list[n].M.FaultMarker.WidthMarker;
         }
         map.removeOverlay(marker.polygonFault);

         marker.setLatLng(new GLatLng(lat2/pi*180,lon2/pi*180));
         marker.polygonFault = new GPolyline(points, "#F88017");
         map.addOverlay(marker.polygonFault);
      }
}


function computeFaultMw(j){
      var mu = 3.6e+11;
      var pi = 3.141592653589793;
      var M0 = mu * fault_list[j].slip * Math.abs(fault_list[j].width) * fault_list[j].length / Math.cos(fault_list[j].dip/180*pi) * 1e+6 * 1e+6;
      fault_list[j].M0 = M0;
      fault_list[j].Mw = Math.log(M0)/Math.log(10)/1.5 - 10.73;
      return 0;
}


function brngmin(d, brng, brng90, lon1, lat1, lon2, lat2){
    var R = 6371; // km
  //Get a tmp point
    var latX = Math.asin( Math.sin(lat1)*Math.cos(d/R) + 
                          Math.cos(lat1)*Math.sin(d/R)*Math.cos(brng90) );
    var lonX = lon1 + Math.atan2(Math.sin(brng90)*Math.sin(d/R)*Math.cos(lat1), 
                                 Math.cos(d/R)-Math.sin(lat1)*Math.sin(latX));

  //Get the bering to the tmp point
    var dLat = latX-lat2;
    var dLon = lonX-lon2; 
    var y = Math.sin(dLon)*Math.cos(latX);
    var x = Math.cos(lat2)*Math.sin(latX) -
            Math.sin(lat2)*Math.cos(latX)*Math.cos(dLon);
    var tbrng =  Math.atan2(y, x);

    tbrng=tbrng/pi*180;  if(tbrng<0) tbrng+=360;
    return  Math.abs(tbrng - brng);
}

function getmin(d0,brng, brng90, lon1, lat1, lon2, lat2){
  
  var xl=-200;
  var xr=190;
  var xtmp=(xl+xr)/2;
  var xc=(2*xl+xr)/3;

  var yl=brngmin(xl, brng, brng90, lon1, lat1, lon2, lat2);
  var yc=brngmin(xc, brng, brng90, lon1, lat1, lon2, lat2);
  var yr=brngmin(xr, brng, brng90, lon1, lat1, lon2, lat2);
  var ytmp;
  
  while (Math.abs(xr-xl)>1e-5){
    ytmp=brngmin(xtmp, brng, brng90, lon1, lat1, lon2, lat2);
    
    if(ytmp<yc){
      if(xtmp>xc){ xl=xc;   yl=yc;  xc=xtmp; yc=ytmp; xtmp=(xl+xtmp)/2;}
      else       { xr=xc;   yr=yc;  xc=xtmp; yc=ytmp; xtmp=(xr+xtmp)/2;}
    }
    else{
      if(xtmp>xc){ xr=xtmp; yr=ytmp; xtmp=xc; xc=(xtmp+xl)/2; 
         yc=brngmin(xc, brng, brng90, lon1, lat1, lon2, lat2);}
      else{          xl=xtmp; yl=ytmp; xtmp=xc; xc=(xtmp+xr)/2; 
         yc=brngmin(xc, brng, brng90, lon1, lat1, lon2, lat2);}
    }
  }
  return xtmp;
}












function set_sorting(type){
   if(type == 0){
      sort_type=type;
      var tbody = document.getElementById("DR"+sort_previous);
      tbody.src="";
      sort_previous=-1;
   }
   else{
      if(sort_type==type){
         sort_direction*=-1;
         var tbody = document.getElementById("DR"+type);
         if( sort_direction == -1)
            tbody.src="http://burn.giseis.alaska.edu/ico_sortDown.gif";
         else
            tbody.src="http://burn.giseis.alaska.edu/ico_sortUp.gif";
         sort_previous=sort_type;
      } 
      else{
         sort_type=type;
         sort_direction=1;
         var tbody = document.getElementById("DR"+type);
         tbody.src="http://burn.giseis.alaska.edu/ico_sortDown.gif";
         if( sort_previous > -1){ 
            var tbody = document.getElementById("DR"+sort_previous);
            tbody.src="";
         }
         sort_previous=sort_type;
      }
   } 
   updateMarkerTable();
}


function bubbleSortMetric(x, y){
   if (sort_direction == 1)
     if (x < y)
        return 1;
     else
        return 0;
   else
     if (x < y)
        return 0;
     else
        return 1;
}


function bubbleSort() {
   var indices = new Array();
   var field = new Array();

   var n=0;
   for (var i = 0; i < counter; i++){
      if (markers[i] != null){
         indices[n] = i;
         switch(sort_type){
            case 1:
               field[n]   = markers[i].grid; break;
            case 2:
               field[n]   = markers[i].name; break;
            case 3:
               field[n]   = markers[i].group; break;
         }
         n++;
      }
   }
   if (sort_type == 0)
      return indices;

   for (var i = 0; i < n;  i++) {
      for (var j = i; j < n; j++) {
         if (bubbleSortMetric(field[i],field[j])) {
            var tempValue = field[j];
            field[j] = field[i];
            field[i] = tempValue;
            var tempIndex = indices[j];
            indices[j] = indices[i];
            indices[i] = tempIndex;

         }
      }
   }
   return indices;
}





function Dec2Deg(dec,sn,sp,fancy){
   var suffix="";
   if(dec<0){
      suffix=sn;
      dec=-dec;
   }
   else
     suffix=sp;

   var deg=Math.floor(dec);       dec=dec-deg;
   var min=Math.floor(dec*60);    dec=dec-min/60;
   var sec=Math.round(dec*3600);
   if (fancy == 1) 
      return sprintf("%2.2d",deg)+"°"+sprintf("%2.2d",min)+"'"+sprintf("%2.2d",sec)+'" '+suffix;
   else
      return sprintf("%2.2d",deg)+"."+sprintf("%2.2d",min)+"."+sprintf("%2.2d",sec)+suffix;
}

function Deg2Dec(str){

   var factor=0;

   var temp = new Array();
   temp = str.split('°');
   var deg=parseFloat(sprintf('%5.2f',temp[0]));
   if(temp.length>1){
     temp = temp[1].split('\'');
     var min=parseFloat(sprintf('%5.2f',temp[0]));
  
     if(temp.length>1){
       temp = temp[1].split('"');
       var sec=parseFloat(sprintf('%5.2f',temp[0]));
     }
    
     var i=0;
     if(temp.length>1){
       while(temp[1].charAt(i)==' ')
         i++;
   
       if(temp[1].charAt(i)=='N' || temp[1].charAt(i)=='E')
         factor=1; 
       else
         if(temp[1].charAt(i)=='S' || temp[1].charAt(i)=='W')
           factor=-1;
     }  
   }

   var str='Oops';
   if(factor!=0)
     str=sprintf('%11.7f',factor*(deg+min/60+sec/3600));
   return str; 
}

function updateMarkerTable(){
	var mytable = document.getElementById("myTable");
	var mytbody = document.getElementById("myTbody");
	var myNewtbody = document.createElement("tbody");
	myNewtbody.id = "myTbody";
	var docFragment = document.createDocumentFragment();
	var trElem, tdElem, txtNode, link, cbx;

        var indices = bubbleSort();
        var ii=display_p*display_pp; 

        for (var i = ii; i < Math.min(indices.length,ii+display_pp); i++) {

              var j = indices[i];

	      trElem = document.createElement("tr");
             
              trElem.id = markers[j].value;
              if(markers[j].value == lastFocus)
                trElem.className = "tr0";
              else
                trElem.className = "tr1";
               
              //trElem.setAttribute("height", 30);

	      tdElem = document.createElement("td");
	      tdElem.className = "colr";
              tdElem.id = markers[j].value;
              tdElem.setAttribute("onmouseover", "focusMarker(this.id);lightTable(this.id);");

	      cbx = document.createElement("input");
	      cbx.setAttribute("type", "checkbox");  
              cbx.setAttribute("id", markers[j].value); 
              cbx.setAttribute("onclick", "markers[this.id].checked*=-1;"); 
              if(markers[j].checked == 1)
                  cbx.setAttribute("checked", true);  
              tdElem.appendChild(cbx); 
              trElem.appendChild(tdElem);



              tdElem = document.createElement("td");
              tdElem.className = "col0";
	      tdElem.id = markers[j].value;
              tdElem.setAttribute("onmouseover", "focusMarker(this.id);lightTable(this.id);");
              txtNode = document.createTextNode(markers[j].grid);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);


	      var str=Dec2Deg(markers[j].point.x,'W','E',1);
              tdElem = document.createElement("td");
              tdElem.className = "col1";
              tdElem.id = markers[j].value;
              tdElem.setAttribute("onmouseover", "focusMarker(this.id);lightTable(this.id);");
              txtNode = document.createTextNode(str); 
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              str=Dec2Deg(markers[j].point.y,'S','N',1);
              tdElem = document.createElement("td");
              tdElem.className = "col2";
	      tdElem.id = markers[j].value;
              tdElem.setAttribute("onmouseover", "focusMarker(this.id);lightTable(this.id);");
              txtNode = document.createTextNode(str); 
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);


              tdElem = document.createElement("td");
	      tdElem.className = "col3";
              tdElem.id = markers[j].value;
              tdElem.setAttribute("onmouseover", "focusMarker(this.id);lightTable(this.id);");
	      link = document.createElement("a");
	      link.setAttribute("name", markers[j].value);
	      link.setAttribute("title", markers[j].desc);
	      link.setAttribute("href", 'javascript:{changeMarkerName('+trElem.id+');var l=updateMarkerTable();}');  
              link.appendChild(document.createTextNode(markers[j].name));
              tdElem.appendChild(link); 
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "colg";
              tdElem.id = markers[j].value;
              tdElem.setAttribute("onmouseover", "focusMarker(this.id);lightTable(this.id);");
              txtNode = document.createTextNode(markers[j].group);//tableData[j].epsilon);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              if(markers[j].modify == -1)
                 str="Fixed";
              else
                 str="Free";

              tdElem = document.createElement("td");
	      tdElem.className = "col4";
              tdElem.id = markers[j].value;
              tdElem.setAttribute("onmouseover", "focusMarker(this.id);lightTable(this.id);");
	      link = document.createElement("a");
	      link.setAttribute("name", markers[j].value);
	      link.setAttribute("href", 'javascript:{changeMarkerFF('+trElem.id+');var l=updateMarkerTable();}');
              link.appendChild(document.createTextNode(str));
              tdElem.appendChild(link); 
              trElem.appendChild(tdElem);
   
              docFragment.appendChild(trElem);
	}

       

	myNewtbody.appendChild(docFragment);
	mytable.replaceChild(myNewtbody, mytbody);
        return indices.length;
}

function lightTable(id) {
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++) {
      if( tbody.childNodes[i].id  == id ) 
        tbody.childNodes[i].className= "tr0";
      else
        tbody.childNodes[i].className= "tr1";
   }
}

function SelectAll() {
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
        markers[tbody.childNodes[i].id].checked=1;
        tbody.childNodes[i].childNodes[0].childNodes[0].checked=true;
   }
}

function DeselectAll() {
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
        markers[tbody.childNodes[i].id].checked=-1;
        tbody.childNodes[i].childNodes[0].childNodes[0].checked=false;
   }
}

function Remove(){
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
      if(tbody.childNodes[i].childNodes[0].childNodes[0].checked == 1){
         var id=tbody.childNodes[i].childNodes[0].childNodes[0].id;
         map.removeOverlay(markers[id]);
         markers[id]=null;
         lastFocus=-1;
      }
   }
}

function Export(){
   var gstr="";
   for (var i = 0; i< counter; i++)
      if(markers[i] != null){
         var str= "";
         var id=markers[i].value;

         if(markers[i].name == "nameless"){
            focusMarker(id);
            changeMarkerName(id);
            updateMarkerTable();
         }
         str="|G=="+markers[i].grid+"&"+Dec2Deg(markers[i].point.x,'W','E',0)+"&"+Dec2Deg(markers[i].point.y,'S','N',0)+"&"+markers[i].name+"&"+markers[i].desc;
         gstr=gstr+str;
      }
   window.open('/cgi-bin/export_points.cgi?'+gstr,'','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no,width=900,height=500');
}


function FaultExport(){
   var gstr=newdefwindow.document.faults.eqname.value+"&";

   for (var i = 0; i< fault_counter; i++){
      var f=fault_list[i];
      if(f != null){
        if(isNaN(f.depth)  || f.depth == '---' ) {alert("Please complete all fields."); return}
        if(isNaN(f.slip)   || f.slip == '---' )  {alert("Please complete all fields."); return}
        if(isNaN(f.length) || f.length == '---' ){alert("Please complete all fields."); return}
        if(isNaN(f.width)  || f.width == '---' ) {alert("Please complete all fields."); return}
        if(isNaN(f.strike) || f.strike == '---' ){alert("Please complete all fields."); return}
        if(isNaN(f.dip)    || f.dip == '---' )   {alert("Please complete all fields."); return}
        if(isNaN(f.rake)   || f.rake == '---' )  {alert("Please complete all fields."); return}
     }
   } 

   for (var i = 0; i< fault_counter; i++){
      var f=fault_list[i];
      if(f != null){
         var wc = Math.abs(f.width) / Math.cos(f.dip/180*pi)
         var str=f.name+"|"+f.lon0+"|"+f.lat0+"|"+(1000*f.depth)+"|"+f.strike+"|"+f.dip+"|"+f.rake+"|"+f.slip+"|"+(1000*f.length)+"|"+(1000*wc)+"&";
         gstr=gstr+str;
      }
   }
   window.open('/cgi-bin/priv/export_deformation.cgi?'+gstr,'','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no,width=900,height=100');
}



       

       function createMarker(point, number,grid_str) {

	  var cIcon = new GIcon(G_DEFAULT_ICON);
          cIcon.image = "http://www.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png";


          var marker = new GMarker(point, {draggable:true, icon:cIcon});
          marker.value = number;
          marker.grid = grid_str;
          marker.point = point;
          marker.name = "nameless";
          marker.desc = "";
          marker.checked = -1;
          marker.group = "custom";
          marker.modify = 1;

          GEvent.addListener(marker, "click", function() {
             marker.openInfoWindowHtml(marker.desc);
             focusMarker(marker.value);
             updateMarkerTable();
             marker=updateNameMarker(marker);
             updateMarkerTable();
          });

          GEvent.addListener(marker, "dragstart", function() {
             //map.closeInfoWindow();
             focusMarker(marker.value);
             updateMarkerTable();
          });
                
          GEvent.addListener(marker, "dragend", function(latlng) {
             //marker.openInfoWindowHtml(marker.desc);
             marker.point=latlng;
             updateMarkerTable();
          });

          return marker;
       }




       function mergeMarkers(value){
          var str = "return merge_"+value+"();"
          var f = new Function(str); 
          var m2add=f();
          for (i in m2add) {
             var marker = createMarker(new GPoint(m2add[i].lon, m2add[i].lat), counter, m2add[i].grid);
             marker.name = m2add[i].name;
             marker.group = m2add[i].group;
             marker.desc = m2add[i].desc;
             marker.modify = -1;
             marker.disableDragging();
             map.addOverlay(marker); 
             markers[counter]=marker;
             counter++;
          }
          var l=updateMarkerTable();
          updagePages(l);
       }
       
       function updagePages(l){
          display_np=Math.floor(l/display_pp);
          if(l-display_np*display_pp>0)
             display_np++;
 
          var selObj = document.getElementById('select_page');
             var newOption = document.createElement("OPTION");
             newOption.text="Select Page";
             newOption.value=""; 
             selObj.options[0] = new Option(newOption.text,newOption.value); 

          for (var i=0;i<display_np;i++){
             var newOption = document.createElement("OPTION");
             newOption.text="Page "+(i+1);
             newOption.value=i; 
             selObj.options[i+1] = new Option(newOption.text,newOption.value);   
          }
          selObj.length = display_np+1;
          selObj.options[1].selected=true;
        }

       function listPages(c){
          display_p+=c;
          if(c<0)
             display_p=Math.max(0,display_p);
          else
             display_p=Math.min(display_np-1,display_p);
          var selObj = document.getElementById('select_page');

          selObj.options[display_p+1].selected=true;
          updateMarkerTable();
       }



       function focusMarker(value){
          if(lastFocus>-1)
             markers[lastFocus].setImage("http://www.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png");
          lastFocus=value;
          markers[lastFocus].setImage("http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png");
       }

       function updateNameMarker(marker){

          if(marker.modify == -1)
              return marker;
          var flag = 0;
          while (flag == 0){
             var retVal =  prompt("Please type a unique watch point name", marker.name); 
             flag = 1;
             for(var i=0; i < counter; i++){
                if(markers[i] != null){
                   if(markers[i].name == retVal && markers[i].value != marker.value){
                      alert("A point with this name already exists. \nPlease try again.");
                      flag=0;
                   }
                }
             }
          }
          if (retVal == "" || retVal == null){
             if(marker.name == "nameless")
                marker.name="nameless";
          }
          else 
                marker.name=retVal;
          var retVal =  prompt("Please type the watch point description", marker.desc); 
          if (retVal == "" || retVal == null)
             marker.desc = "";
          else
             marker.desc = retVal;

          return marker;
       }

       function changeMarkerName(id){

          for(var i=0; i < counter; i++){
             if(markers[i] != null)
                if(markers[i].value == id)
                   markers[i]=updateNameMarker(markers[i]);
             
          }
       }

       function changeMarkerFF(id){
          for(var i=0; i < counter; i++){
             if(markers[i] != null){
                if(markers[i].value == id){
                   markers[i].modify*=-1;
                   if(markers[i].modify == 1){
                      markers[i].enableDragging();
                      markers[i].group="custom";
                   }
                   else
                      markers[i].disableDragging();

                }     
             }
          }
       }




       function checkNumberGrids(lon, lat) {
           tmp_ngrids=0;
            
	   for (var i = 0; i <= grids; i++){
              coords=grid_name[i][1];
              if ( coords[0]<=lon && lon<=coords[1] && coords[2]<=lat && lat<=coords[3] && grid_name[i][2] == 1) {
                 tmp_ngrids++;
		 focus_grid=i;
              }
           }
	}



       function boxclick(box,str) {
          for (var i = 0; i <= grids; i++){
             if( grid_name[i][0] == str ){

                if (box.checked) {
 		   grid_name[i][2] = 1;

                   crds=grid_name[i][1];
                   grid_name[i][4] = new GPolygon([
                      new GLatLng( crds[2] , crds[0] ),
                      new GLatLng( crds[3] , crds[0] ),
                      new GLatLng( crds[3] , crds[1] ),
                      new GLatLng( crds[2] , crds[1] ),
                      new GLatLng( crds[2] , crds[0] )
                          ], "#f33f00", 1, 1, "#DD5500", 0.2);
                   map.addOverlay(grid_name[i][4]);
                   //map.addOverlay(grid_name[i][5]);
                } else {
                   map.removeOverlay(grid_name[i][4]);
                   //map.removeOverlay(grid_name[i][5]);
 		   grid_name[i][2] = 0;
                }
             }
          }
       }

       

       function showPriority(id){
          priority_vis[id]*=-1;
          if(priority_vis[id] == -1)
             map.removeOverlay(priority_map[id]);
          if(priority_vis[id] == 1)
             map.addOverlay(priority_map[id]);
       }



       function prepareScenario(){

          var friction = document.tsunami_parameters.friction.value;
          var level    = document.tsunami_parameters.level.value;

          var earth_gravity = document.tsunami_parameters.earth_gravity.value;
          var earth_radius  = document.tsunami_parameters.earth_radius.value;
          var earth_omega   = document.tsunami_parameters.earth_omega.value;

          var time_interval = document.tsunami_parameters.time_interval.value;
          var time_step     = document.tsunami_parameters.time_step.value;
          var time_output_step = document.tsunami_parameters.time_output_step.value;

          var options_bath = document.tsunami_parameters.prepost.selectedIndex;
          var options_def  = document.tsunami_parameters.deformations.selectedIndex;
          //alert(bath_pp);

          document.tsunami_parameters.reset();

          if(document.error_disp_handler.all_msgs.length == 0){
             document.tsunami_parameters.friction.value = friction;
             document.tsunami_parameters.level.value    = level;
             document.tsunami_parameters.earth_gravity.value = earth_gravity;
             document.tsunami_parameters.earth_radius.value = earth_radius;
             document.tsunami_parameters.earth_omega.value = earth_omega;
             document.tsunami_parameters.time_interval.value = time_interval;
             document.tsunami_parameters.time_step.value = time_step;
             document.tsunami_parameters.time_output_step.value = time_output_step;
             document.tsunami_parameters.prepost.options[options_bath].selected=true;
             document.tsunami_parameters.deformations.options[options_def].selected=true
          }
          else
             return;


          var tbody = document.getElementById("myTbody");
          var gstr="";
          var number=0;

          for(var i=0; i < counter; i++)
             if(markers[i] != null){
                var str= "";
                if(markers[i].name == "nameless"){
                   focusMarker(markers[i].value);
                   changeMarkerName(markers[i].value);
                   updateMarkerTable();
                }
                str="|Point="+markers[i].grid+"&"+Dec2Deg(markers[i].point.x,'W','E',0)+"&"+Dec2Deg(markers[i].point.y,'S','N',0)+"&"+markers[i].name+"&"+markers[i].desc;
                gstr=gstr+str;
                number++;
             }

          var selected_deformation=""; 
          if (old_deformation == "" ){
             alert("Error. No deformation model is selected.");
             return;  
          }
          else
             selected_deformation=old_deformation;



          var selected_grids="";
          for (var i = 0; i<grids; i++){
             if(grid_name[i][2] == 1){
                selected_grids = grid_name[i][0] +";"+selected_grids;
             }
          }
          if (selected_grids == "" ){
             alert("Error. No grids are selected.");
             return;
          }

          gstr = gstr + "|DEF="+selected_deformation + "|GRIDS="+selected_grids + "|Friction="+friction + "|Level="+level;

          gstr = gstr + "|TI="+time_interval + "|DT="+time_step + "|DS="+time_output_step;
          gstr = gstr + "|ER="+earth_radius + "|EG="+earth_gravity + "|EO="+earth_omega;
          gstr = gstr + "|PP="+options_bath;
          window.open('/cgi-bin/prepare_scenario.cgi?'+gstr,'','toolbar=no,location=no,directories=no,status=no,menubar=no,width=500,height=700');
}



          function trim(field){
                 field.value = (field.value).replace(/^\s*|\s*$/g,'');
          }



       function deformation_click(deformation) {
          //if(deformation=="custom"){
          //   window.open('/cgi-bin/priv/download_deformation.cgi','toolbar=no,location=no,directories=no,status=no,menubar=no,width=500,height=700');
          //   return;
          //}
           
          if(old_deformation != ""){
             var str="map.removeOverlay("+old_deformation+");";
             var f = new Function(str);
             f();
          }
          if(deformation != ""){
             var str="map.addOverlay("+deformation+");";
             var f = new Function(str);
             f();
             old_deformation=deformation; 
          }
	}

        function coastline_click(coastline) {
          if(old_coastline != "")
             map.removeOverlay(coastline_kml);
          if(coastline != ""){
             var str="http://burn.giseis.alaska.edu/grids/"+coastline+".kml";
             coastline_kml = new GGeoXml(str);
             map.addOverlay(coastline_kml);
             old_coastline=coastline; 
          }
	}




    //]]>
    </script>

<style type="text/css">
table {width:100%}
.tableWrapper {text-align:left}
.tr0 {background-color:#ffffcc}
.tr1 {background-color:#ccffcc}
.colr {width:5%}
.col0 {width:10%}
.col1 {width:20%}
.col2 {width:20%}
.col3 {width:15%}
.colg {width:15%}
.col4 {width:5%}
</style>


  </head>
  <body onload="load()" onunload="unload()">

    <div id="map_canvas" style="width:800px;height:500px"></div>
    <input type="button" value="Communities by priority level" onclick="top.newWin=window.open('http://burn.giseis.alaska.edu/kml_layers.html','win',' WIDTH=208,HEIGHT=230');" />
    <select onchange="coastline_click(this.value);">
             <option value="" > Coastal lines </option>
EOM
for ((i=0;i<=$iclines;i+=1)); do 
    file=${clines[$i]}
    echo '                        <option value="'$file'">Grid '$file'</option>'
done
cat << EOM
    </select>
    <input type="button" value="Create deformation" onclick="openDEFWindow();" />
    <br />
&nbsp

<div style="width:800px">
   <form name="tsunami_parameters">
      <table border="0" bgcolor="#cccccc">
         <tr>
            <td>
            <table border="0">
               <tr>
                  <td width="45%" align="right">Deformation model</td>
                  <td>
                     <select id='deformations' onchange="deformation_click(this.value);">
                        <option value="" > Available model </option>
EOM
for ((i=0;i<=$ideformations;i+=1)); do 
    file=${deformations[$i]}
    echo '                        <option value="deformation_'$file'">'$file'</option>'
done
cat << EOM
                                  <option value="custom">Upload a new deformation</option>
                     </select>
                  </td>
               </tr>
               <tr>    <td width="45%" align="right">Modeling time (h)</td> <td><input type="text" name="time_interval" value="1.0"/></td> </tr>
               <tr>    <td width="45%" align="right">Time step     (s)</td> <td><input type="text" name="time_step" value="1.0"/></td> </tr>
               <tr>    <td width="45%" align="right">Output step   (s)</td> <td><input type="text" name="time_output_step" value="300.0"/></td> </tr>
               

            </table>
            </td>
            <td width="50%">
               <table border="0">
                  <tr><td width="50%" align="right">Bottom friction</td>          <td><input type="text" name="friction" value="0.03"/></td> </tr>
                  <tr><td width="50%" align="right">Earth radius (m)</td>         <td><input type="text" name="earth_radius" value="6371.0e+3" readonly/></td> </tr>
                  <tr><td width="50%" align="right">Earth gravity (m/s^2)</td>    <td><input type="text" name="earth_gravity" value="9.8062" readonly/></td> </tr>
                  <tr><td width="50%" align="right">Earth rotation (1/s)</td>     <td><input type="text" name="earth_omega" value="0.72920e-4" readonly/></td> </tr>
               </table>
            </td>
         </tr> 

         <tr> 
            <td>
            <table border="0">
                  <tr><td width="45%" align="right">Sea level (m)</td><td><input type="text" name="level" value="0.0" onchange="this.value=sprintf('%3.1f',this.value);" size=3/>
                      <select id='prepost'>
                        <option value="1">Post-earthquake</option>
                        <option value="0">Pre-earthquake</option>
                     </select>
                  </td>  </tr>   
            </table>
            </td>
            <td width="50%" align="right">
               <input type="button" value="Prepare scenario" onclick="prepareScenario();" />
            </td>
         </tr>

      </table> 
      <div id='tsunami_parameters_errorloc' class='error_strings'></div> 
</form>
</div>


<script language="JavaScript" type="text/javascript">
//You should create the validator only after the definition of the HTML form
  frmvalidator  = new Validator_onreset("tsunami_parameters");
  frmvalidator.EnableOnPageErrorDisplaySingleBox();
  frmvalidator.EnableMsgsTogether();

  frmvalidator.addValidation("time_interval","req","Please enter the length of computational time in hours.");
  frmvalidator.addValidation("time_interval","maxlen=6");
  frmvalidator.addValidation("time_interval","decimal");

  frmvalidator.addValidation("time_step","req","Please enter the time step in the coarsest grid in seconds.");
  frmvalidator.addValidation("time_step","maxlen=6");
  frmvalidator.addValidation("time_step","decimal");

  frmvalidator.addValidation("time_output_step","req","Please enter the time step of saving results in seconds.");
  frmvalidator.addValidation("time_output_step","maxlen=6");
  frmvalidator.addValidation("time_output_step","decimal");


  frmvalidator.addValidation("friction","req","Please enter the bottom friction coefficient.");
  frmvalidator.addValidation("friction","maxlen=6");
  frmvalidator.addValidation("friction","decimal");

  frmvalidator.addValidation("level","req","Please enter adjustment to bathymetry.");
  frmvalidator.addValidation("level","maxlen=6");
  frmvalidator.addValidation("level","regexp=^[0-9\+\-][.0-9]{1,7}$");
</script>


<div style="width:800px;height:20px">
</div>
<div style="width:800px;background-color:#eeeeee">
<FORM NAME="points">
<table cellspacing="0" cellpadding="0" border="0">
   <tr><td> 
      <table cellspacing="0" cellpadding="0" border="0">   
         <tr>
            <td align="left">  
                               <select id="select_markers" onchange='mergeMarkers(this.options[this.selectedIndex].value)'>
                                   <option selected>Import markers</option>
EOM
for ((i=0;i<=${iscripts};i+=1)); do 
    file=${scripts[$i]}
    echo '    <option value="'$file'">' $file '</option>'
done
cat << EOM
                               </select>
                               <input type="button" value="Export" onclick="Export();" />
            </td> 
            <td align="right">
                               <input type="button" value="Previous Page" onclick="listPages(-1)" />
                               <select id="select_page" onchange='display_p=this.value;updateMarkerTable();'>
                               </select>
                               <input type="button" value="Next Page" onclick="listPages(1);" />
            </td>
         </tr>
      </table> 
   </td></tr>
   <tr><td>
      <div style="width:800px;height:3px;background-color:#9999ee">
      </div>
   </td></tr>
   <tr><td> 
      <div class="tableWrapper" style="width:800px;background-color:#99eeee">
      <table id="myTable" style="background-color:#eeeeee">
         <thead>
            <tr>
               <th></th><th><a href="javascript:set_sorting(1)">Grid <img id="DR1" border="0" src="http://burn.giseis.alaska.edu/ico_sortDown.gif" /> </a></th>
               <th>Longitude</th><th>Latitude</th>
               <th><a href="javascript:set_sorting(2)">Name  <img id="DR2" border="0" src=""/> </a></th>
               <th><a href="javascript:set_sorting(3)">Group <img id="DR3" border="0" src=""/> </a></th>
               <th>Fixed <br />/ Free</th>
            </tr>
         </thead>
         <tbody id="myTbody">
         </tbody>
      </table>
      </div>
   </td></tr> 
   <tr><td>
      <div style="width:800px;height:3px;background-color:#9999ee">
      </div>
   </td></tr>
   <tr><td> 
      <table cellspacing="0" cellpadding="0" border="0">   
         <tr>   
            <td align="left">  
                               <input type="button" value="Select All" onclick="SelectAll();" /> 
                               <input type="button" value="Deselect All" onclick="DeselectAll();" />  
                               <input type="button" value="Remove" onclick="Remove();var l=updateMarkerTable();updagePages(l);" /></td>  
                              
            </td>  
            <td align="right"><a href="javascript:set_sorting(0)">Do not sort</a></td>
         </tr>
      </table> 
   </td></tr>
</table>
</div>
  </body>
</html>
EOM
