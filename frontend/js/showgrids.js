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


//Available deformations 

var deformation_AkutanSource;
var deformation_Andreanof061096;
var deformation_Cascadia;
var deformation_Cascadia_Mw9;
var deformation_HNO1993;
var deformation_Ichinose;
var deformation_Johnson;
var deformation_Johnson_Kodiak;
var deformation_Johnson_PWS;
var deformation_Kurils111506;
var deformation_Pamplona;
var deformation_RatIslands65;
var deformation_Suito;
var deformation_Suito_Updated_KI;
var deformation_Suito_Updated_PWS;
var deformation_Suito_kod_new;
var deformation_Suito_pws_new;
var deformation_Suito_updated;
var deformation_def_shennan;
var deformation_def_shennan_Johnson;
var deformation_def_shennan_SuitoOld;
var deformation_shumagin_deform_cut;
var deformation_test_4faults;
var deformation_test_dip3_dep1;
var deformation_test_dip8_dep1;
var deformation_test_dip8_dep10;
var deformation_testr;
var deformation_yakataga;

//Available grids 

var grids = 37;
var grid_name = new Array();
grid_name[0] = new Array();
grid_name[0][0] = "AK15";
grid_name[0][1] = new Array(194.1667901,194.2998765,54.1082222,54.1584444);
grid_name[0][2] = 0;
grid_name[1] = new Array();
grid_name[1][0] = "AO15";
grid_name[1][1] = new Array(139.4341975,139.4998765,42.0311852,42.0725185);
grid_name[1][2] = 0;
grid_name[2] = new Array();
grid_name[2][0] = "AU08";
grid_name[2][1] = new Array(190.5811111,194.9522222,52.6211111,54.3855556);
grid_name[2][2] = 0;
grid_name[3] = new Array();
grid_name[3][0] = "AU24";
grid_name[3][1] = new Array(188.0366667,202.9633333,52.0033333,57.4633333);
grid_name[3][2] = 0;
grid_name[4] = new Array();
grid_name[4][0] = "CH03e";
grid_name[4][1] = new Array(200.7403704,202.3996296,55.7892593,56.5507407);
grid_name[4][2] = 0;
grid_name[5] = new Array();
grid_name[5][0] = "CR15";
grid_name[5][1] = new Array(214.0867901,214.4998765,60.5097037,60.7302963);
grid_name[5][2] = 0;
grid_name[6] = new Array();
grid_name[6][0] = "JU24";
grid_name[6][1] = new Array(219.0033333,229.9633333,54.0033333,60.2300000);
grid_name[6][2] = 0;
grid_name[7] = new Array();
grid_name[7][0] = "KC01";
grid_name[7][1] = new Array(207.5519753,207.6902469,57.7675309,57.8406173);
grid_name[7][2] = 0;
grid_name[8] = new Array();
grid_name[8][0] = "KC03e";
grid_name[8][1] = new Array(197.2003704,198.1507407,54.4492593,55.3507407);
grid_name[8][2] = 0;
grid_name[9] = new Array();
grid_name[9][0] = "KC08e";
grid_name[9][1] = new Array(196.2011111,198.1988889,54.2477778,55.4988889);
grid_name[9][2] = 0;
grid_name[10] = new Array();
grid_name[10][0] = "KD03";
grid_name[10][1] = new Array(207.4003704,207.7329630,57.5870370,57.9262963);
grid_name[10][2] = 0;
grid_name[11] = new Array();
grid_name[11][0] = "KD08";
grid_name[11][1] = new Array(205.0011111,208.3322222,56.3344444,58.7988889);
grid_name[11][2] = 0;
grid_name[12] = new Array();
grid_name[12][0] = "MB05";
grid_name[12][1] = new Array(139.4138519,139.4263951,42.0945855,42.1034392);
grid_name[12][2] = 0;
grid_name[13] = new Array();
grid_name[13][0] = "MO01";
grid_name[13][1] = new Array(139.4112346,139.4332099,42.0779012,42.1458025);
grid_name[13][2] = 0;
grid_name[14] = new Array();
grid_name[14][0] = "MO05";
grid_name[14][1] = new Array(139.4121235,139.4296049,42.0916226,42.1078836);
grid_name[14][2] = 0;
grid_name[15] = new Array();
grid_name[15][0] = "NS01";
grid_name[15][1] = new Array(207.4675309,207.5487654,57.7082716,57.7783951);
grid_name[15][2] = 0;
grid_name[16] = new Array();
grid_name[16][0] = "OK03";
grid_name[16][1] = new Array(139.3892593,139.6640741,41.9959259,42.2707407);
grid_name[16][2] = 0;
grid_name[17] = new Array();
grid_name[17][0] = "OK08";
grid_name[17][1] = new Array(138.5011111,140.5522222,40.5211111,43.2988889);
grid_name[17][2] = 0;
grid_name[18] = new Array();
grid_name[18][0] = "OK24";
grid_name[18][1] = new Array(137.5366667,141.5300000,39.5366667,44.2633333);
grid_name[18][2] = 0;
grid_name[19] = new Array();
grid_name[19][0] = "PA02";
grid_name[19][1] = new Array(120.0166667,259.9833333,10.0166667,64.9833333);
grid_name[19][2] = 0;
grid_name[20] = new Array();
grid_name[20][0] = "PW03";
grid_name[20][1] = new Array(211.2492593,214.6662963,59.6670370,61.3329630);
grid_name[20][2] = 0;
grid_name[21] = new Array();
grid_name[21][0] = "PW08";
grid_name[21][1] = new Array(211.0544444,214.9588889,58.5011111,61.4988889);
grid_name[21][2] = 0;
grid_name[22] = new Array();
grid_name[22][0] = "PW24";
grid_name[22][1] = new Array(204.0033333,214.9966667,55.0033333,61.9966667);
grid_name[22][2] = 0;
grid_name[23] = new Array();
grid_name[23][0] = "SE03";
grid_name[23][1] = new Array(210.3759259,210.7618519,59.7114815,60.1262963);
grid_name[23][2] = 0;
grid_name[24] = new Array();
grid_name[24][0] = "SE08";
grid_name[24][1] = new Array(210.0011111,210.9988889,59.5011111,60.1655555);
grid_name[24][2] = 0;
grid_name[25] = new Array();
grid_name[25][0] = "SE15";
grid_name[25][1] = new Array(210.5423457,210.7206173,59.9504321,60.1559877);
grid_name[25][2] = 0;
grid_name[26] = new Array();
grid_name[26][0] = "SI03e";
grid_name[26][1] = new Array(224.3337037,224.8085185,56.8670370,57.2662963);
grid_name[26][2] = 0;
grid_name[27] = new Array();
grid_name[27][0] = "SI08e";
grid_name[27][1] = new Array(223.8344444,224.8322222,56.7477778,57.4988889);
grid_name[27][2] = 0;
grid_name[28] = new Array();
grid_name[28][0] = "SI15e";
grid_name[28][1] = new Array(224.4830864,224.7835802,57.0163704,57.1502963);
grid_name[28][2] = 0;
grid_name[29] = new Array();
grid_name[29][0] = "SP03e";
grid_name[29][1] = new Array(199.0003704,200.1996296,54.7003704,55.6996296);
grid_name[29][2] = 0;
grid_name[30] = new Array();
grid_name[30][0] = "SP08e";
grid_name[30][1] = new Array(198.5011111,202.4988889,54.6011111,56.5988889);
grid_name[30][2] = 0;
grid_name[31] = new Array();
grid_name[31][0] = "UN03";
grid_name[31][1] = new Array(193.2492593,194.8329630,53.6670370,54.3507407);
grid_name[31][2] = 0;
grid_name[32] = new Array();
grid_name[32][0] = "UN15e";
grid_name[32][1] = new Array(193.3393827,193.5732099,53.8260000,53.9421481);
grid_name[32][2] = 0;
grid_name[33] = new Array();
grid_name[33][0] = "VL15";
grid_name[33][1] = new Array(213.2786420,213.8502469,61.0652593,61.1495556);
grid_name[33][2] = 0;
grid_name[34] = new Array();
grid_name[34][0] = "WT15";
grid_name[34][1] = new Array(211.2586420,211.5050617,60.7585926,60.8421481);
grid_name[34][2] = 0;
grid_name[35] = new Array();
grid_name[35][0] = "YK03";
grid_name[35][1] = new Array(219.5825926,220.5840741,59.3337037,59.8507407);
grid_name[35][2] = 0;
grid_name[36] = new Array();
grid_name[36][0] = "YK08";
grid_name[36][1] = new Array(219.5011111,221.1655556,59.0011111,60.0855556);
grid_name[36][2] = 0;
grid_name[37] = new Array();
grid_name[37][0] = "YK15";
grid_name[37][1] = new Array(220.0979012,220.4035802,59.4385926,59.6525185);
grid_name[37][2] = 0;

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

     jg = ne     
     //Define deformation overlays
     var boundaries_AkutanSource  = new GLatLngBounds(new GLatLng(5.1098560e+01,1.8729871e+02), new GLatLng(5.3498560e+01,1.9378204e+02));
     deformation_AkutanSource = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/AkutanSource.png", boundaries_AkutanSource);

     var boundaries_Andreanof061096  = new GLatLngBounds(new GLatLng(5.0933710e+01,1.8142524e+02), new GLatLng(5.2350380e+01,1.8399191e+02));
     deformation_Andreanof061096 = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Andreanof061096.png", boundaries_Andreanof061096);

     var boundaries_Cascadia  = new GLatLngBounds(new GLatLng(1.6691220e+01,2.3191585e+02), new GLatLng(5.1074550e+01,2.4236585e+02));
     deformation_Cascadia = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Cascadia.png", boundaries_Cascadia);

     var boundaries_Cascadia_Mw9  = new GLatLngBounds(new GLatLng(4.0033333e+01,2.3160000e+02), new GLatLng(5.0400000e+01,2.3710000e+02));
     deformation_Cascadia_Mw9 = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Cascadia_Mw9.png", boundaries_Cascadia_Mw9);

     var boundaries_HNO1993  = new GLatLngBounds(new GLatLng(4.1636492e+01,1.3888505e+02), new GLatLng(4.3291885e+01,1.3954127e+02));
     deformation_HNO1993 = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/HNO1993.png", boundaries_HNO1993);

     var boundaries_Ichinose  = new GLatLngBounds(new GLatLng(5.5400002e+01,2.0253999e+02), new GLatLng(6.2506668e+01,2.1525333e+02));
     deformation_Ichinose = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Ichinose.png", boundaries_Ichinose);

     var boundaries_Johnson  = new GLatLngBounds(new GLatLng(5.6116665e+01,2.0421666e+02), new GLatLng(6.1983334e+01,2.2171666e+02));
     deformation_Johnson = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Johnson.png", boundaries_Johnson);

     var boundaries_Johnson_Kodiak  = new GLatLngBounds(new GLatLng(5.6050000e+01,2.0435000e+02), new GLatLng(5.9950000e+01,2.1191667e+02));
     deformation_Johnson_Kodiak = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Johnson_Kodiak.png", boundaries_Johnson_Kodiak);

     var boundaries_Johnson_PWS  = new GLatLngBounds(new GLatLng(5.7116670e+01,2.0801667e+02), new GLatLng(6.1983330e+01,2.1628333e+02));
     deformation_Johnson_PWS = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Johnson_PWS.png", boundaries_Johnson_PWS);

     var boundaries_Kurils111506  = new GLatLngBounds(new GLatLng(4.5091750e+01,1.5006488e+02), new GLatLng(4.7891750e+01,1.5379821e+02));
     deformation_Kurils111506 = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Kurils111506.png", boundaries_Kurils111506);

     var boundaries_Pamplona  = new GLatLngBounds(new GLatLng(5.8900002e+01,2.0989999e+02), new GLatLng(6.2599998e+01,2.1916667e+02));
     deformation_Pamplona = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Pamplona.png", boundaries_Pamplona);

     var boundaries_RatIslands65  = new GLatLngBounds(new GLatLng(5.0689700e+01,1.7028518e+02), new GLatLng(5.3889700e+01,1.7976852e+02));
     deformation_RatIslands65 = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/RatIslands65.png", boundaries_RatIslands65);

     var boundaries_Suito  = new GLatLngBounds(new GLatLng(5.5366669e+01,2.0503334e+02), new GLatLng(6.2900002e+01,2.1873334e+02));
     deformation_Suito = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Suito.png", boundaries_Suito);

     var boundaries_Suito_Updated_KI  = new GLatLngBounds(new GLatLng(5.5300000e+01,2.0480000e+02), new GLatLng(5.9433333e+01,2.1123333e+02));
     deformation_Suito_Updated_KI = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Suito_Updated_KI.png", boundaries_Suito_Updated_KI);

     var boundaries_Suito_Updated_PWS  = new GLatLngBounds(new GLatLng(5.5800000e+01,2.0656667e+02), new GLatLng(6.3000000e+01,2.1803333e+02));
     deformation_Suito_Updated_PWS = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Suito_Updated_PWS.png", boundaries_Suito_Updated_PWS);

     var boundaries_Suito_kod_new  = new GLatLngBounds(new GLatLng(5.5366669e+01,2.0503334e+02), new GLatLng(5.9666668e+01,2.1096666e+02));
     deformation_Suito_kod_new = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Suito_kod_new.png", boundaries_Suito_kod_new);

     var boundaries_Suito_pws_new  = new GLatLngBounds(new GLatLng(5.5633331e+01,2.0713333e+02), new GLatLng(6.2900002e+01,2.1873334e+02));
     deformation_Suito_pws_new = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Suito_pws_new.png", boundaries_Suito_pws_new);

     var boundaries_Suito_updated  = new GLatLngBounds(new GLatLng(5.5266667e+01,2.0476667e+02), new GLatLng(6.3000000e+01,2.1806667e+02));
     deformation_Suito_updated = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/Suito_updated.png", boundaries_Suito_updated);

     var boundaries_def_shennan  = new GLatLngBounds(new GLatLng(5.5250000e+01,2.0476667e+02), new GLatLng(6.3000000e+01,2.1981666e+02));
     deformation_def_shennan = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/def_shennan.png", boundaries_def_shennan);

     var boundaries_def_shennan_Johnson  = new GLatLngBounds(new GLatLng(5.6100000e+01,2.0421667e+02), new GLatLng(6.1983332e+01,2.2196667e+02));
     deformation_def_shennan_Johnson = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/def_shennan_Johnson.png", boundaries_def_shennan_Johnson);

     var boundaries_def_shennan_SuitoOld  = new GLatLngBounds(new GLatLng(5.5350000e+01,2.0501667e+02), new GLatLng(6.2916665e+01,2.2050000e+02));
     deformation_def_shennan_SuitoOld = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/def_shennan_SuitoOld.png", boundaries_def_shennan_SuitoOld);

     var boundaries_shumagin_deform_cut  = new GLatLngBounds(new GLatLng(5.2666668e+01,1.9520000e+02), new GLatLng(5.8366669e+01,2.0839999e+02));
     deformation_shumagin_deform_cut = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/shumagin_deform_cut.png", boundaries_shumagin_deform_cut);

     var boundaries_test_4faults  = new GLatLngBounds(new GLatLng(5.8601270e+01,2.1271172e+02), new GLatLng(6.1801270e+01,2.3006172e+02));
     deformation_test_4faults = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/test_4faults.png", boundaries_test_4faults);

     var boundaries_test_dip3_dep1  = new GLatLngBounds(new GLatLng(5.9004220e+01,2.1381019e+02), new GLatLng(6.0804220e+01,2.2646019e+02));
     deformation_test_dip3_dep1 = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/test_dip3_dep1.png", boundaries_test_dip3_dep1);

     var boundaries_test_dip8_dep1  = new GLatLngBounds(new GLatLng(5.8725890e+01,2.1333345e+02), new GLatLng(6.1092550e+01,2.2676678e+02));
     deformation_test_dip8_dep1 = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/test_dip8_dep1.png", boundaries_test_dip8_dep1);

     var boundaries_test_dip8_dep10  = new GLatLngBounds(new GLatLng(5.8625890e+01,2.1301678e+02), new GLatLng(6.1309220e+01,2.1655011e+02));
     deformation_test_dip8_dep10 = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/test_dip8_dep10.png", boundaries_test_dip8_dep10);

     var boundaries_testr  = new GLatLngBounds(new GLatLng(5.5413040e+01,2.0319888e+02), new GLatLng(5.9313040e+01,2.1243221e+02));
     deformation_testr = new GGroundOverlay("http://burn.giseis.alaska.edu/deformations/testr.png", boundaries_testr);

     var boundaries_yakataga  = new GLatLngBounds(new GLatLng(5.8542070e+01,2.127056ddOverlay(fault_list[fault_counter-1].M);

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
 dLat/2) * Math.sin(dLat/2) +
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
 sort_pr:
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
j].point.y,'S','N',1);
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
window.open('/cgi-bin/export_points.cgi?'+gstr,'','toolbar=no,location=no,directories=no,sxport(){
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
  selObj.options[1].selectedr(value){
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
  var earth_omega   = document.tsunami_param = document.tsunami_parameters.time_interval.value;
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
     var str="http://burn.giseis.all = new GGeoXml(str);
     map.addOverlay(coastline_kml);
     old_coastline=coastline; 
  }
}
 
/*
  frmvalidlidator.EnableMsgsTogether();
 
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
*/
