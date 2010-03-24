#!/bin/bash

echo Content-type: text/html
echo ""


#Parsing available lists of points
list_scripts=$(ls ../htdocs/scripts/param_*.js)
let i=0
for file in $list_scripts; do
  file=${file##../htdocs/scripts/param_}
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

    <title>ATOM workload</title>
    
    <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAG07sBB-qC9yaNXELGJpf5BRrbJnNmETF966luGlbSTr_RfkmQBR_r9lzzhGueAMWoH_XbKNIdXA-uw" type="text/javascript"></script>
    <script type="text/javascript">document.write('<script type="text/javascript" src="/scripts/extlargemapcontrol'+(document.location.search.indexOf('packed')>-1?'_packed':'')+'.js"><'+'/script>');</script>


    <script src="http://burn.giseis.alaska.edu/scripts/sprintf.js" type="text/javascript"></script>
EOM
for ((i=0;i<=${iscripts};i+=1)); do 
    file=${scripts[$i]}
    echo '    <script src="http://burn.giseis.alaska.edu/scripts/param_'$file'.js" type="text/javascript"></script>'
done
cat << EOM


    <script type="text/javascript">
  
   
    //<![CDATA[
     
       var fancy_lon=1;
       var fancy_lat=1;
      
       var sort_type=1;
       var sort_previous=1;
       var sort_direction=-1; 

       var lastFocus=-1;

       var display_np   = 0;
       var display_p    = 0;
       var display_pp   = 20;


       function load() {
          var l=updateMarkerTable();
          if(l>0) updagePages(l);
       }

function set_lat(){
  fancy_lat*=-1;
  updateMarkerTable();
}

function set_lon(){
  fancy_lon*=-1;
  updateMarkerTable();
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
   var l=updateMarkerTable();
   updagePages(l);
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
   for (var i = 0; i < parent.opener.fault_counter; i++){
      if (parent.opener.fault_list[i] != null){
         indices[n] = i;
         switch(sort_type){
            case 1:
               field[n]   = parent.opener.fault_list[i].id; break;
            case 2:
               field[n]   = parent.opener.fault_list[i].depth; break;
            case 3:
               field[n]   = parent.opener.fault_list[i].slip; break;
            case 4:
               field[n]   = parent.opener.fault_list[i].name; break;
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




function updateMarkerTable(){
       
	var mytable = document.getElementById("myTable");
	var mytbody = document.getElementById("myTbody");
	var myNewtbody = document.createElement("tbody");
	myNewtbody.id = "myTbody";
	var docFragment = document.createDocumentFragment();
	var trElem, tdElem, txtNode, link, cbx;

        var indices = bubbleSort();
        var ii=display_p*display_pp; 

        var totalM0=0;


        for (var i = ii; i < Math.min(indices.length,ii+display_pp); i++) {

              var j = indices[i];

	      trElem = document.createElement("tr");
              trElem.id = parent.opener.fault_list[j].value;
              trElem.className = "tr1";
               


	      tdElem = document.createElement("td");
	      tdElem.className = "colr";
              tdElem.id = parent.opener.fault_list[j].value;
	      cbx = document.createElement("input");
	      cbx.setAttribute("type", "checkbox");  
	      cbx.setAttribute("name", parent.opener.fault_list[j].id);  
              cbx.setAttribute("id", parent.opener.fault_list[j].value); 
              cbx.setAttribute("onclick", "parent.opener.fault_list[this.id].checked*=-1;"); 
              if(parent.opener.fault_list[j].checked == 1)
                  cbx.setAttribute("checked", true);  
              tdElem.appendChild(cbx); 
              trElem.appendChild(tdElem);


              tdElem = document.createElement("td");
	      tdElem.className = "colname";
              tdElem.id = parent.opener.fault_list[j].name;
              tdElem.value=j;
              tdElem.setAttribute("onclick", "val=prompt('Current name', this.id); parent.opener.fault_list[this.value].name=val; updateMarkerTable();"); 
              txtNode = document.createTextNode(parent.opener.fault_list[j].name);
              tdElem.appendChild(txtNode); 
              trElem.appendChild(tdElem);

             

              var flat;
              tdElem = document.createElement("td");
	      tdElem.className = "col1";
              if(fancy_lat>0)
                 flat=parent.opener.fault_list[j].lat;
              else
                 flat=parent.opener.fault_list[j].lat0;
              tdElem.id=flat;
              tdElem.value=j;
              tdElem.setAttribute("onclick", "var tt=sprintf('%7.3f',parent.opener.Deg2Dec(this.id)); val=prompt('Current latitude '+tt, this.id); parent.opener.updateLat(this.value,val); updateMarkerTable();"); 
              txtNode = document.createTextNode(flat);
              tdElem.appendChild(txtNode); 
              trElem.appendChild(tdElem);

              var flon;
              tdElem = document.createElement("td");
	      tdElem.className = "col2";
              if(fancy_lon>0)
                 flon=parent.opener.fault_list[j].lon;
              else
                 flon=parent.opener.fault_list[j].lon0;
              tdElem.id = flon
              tdElem.value=j;
              tdElem.setAttribute("onclick", "var tt=sprintf('%7.3f',parent.opener.Deg2Dec(this.id)); val=prompt('Current latitude '+tt, this.id); parent.opener.updateLon(this.value,val); updateMarkerTable();"); 
              txtNode = document.createTextNode(flon);
              tdElem.appendChild(txtNode); 
              trElem.appendChild(tdElem);
              

              tdElem = document.createElement("td");
              tdElem.className = "col3";
	      tdElem.id = parent.opener.fault_list[j].depth;
              if(tdElem.id=='---' || isNaN(tdElem.id) ) tdElem.style.backgroundColor="#ffcccc";
              tdElem.value=j;
              tdElem.setAttribute("onclick", "val=prompt('Current value', this.id); parent.opener.fault_list[this.value].depth=sprintf('%5.1f',val); updateMarkerTable();"); 
              txtNode = document.createTextNode(parent.opener.fault_list[j].depth); 
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "col4";
              tdElem.id = parent.opener.fault_list[j].slip;
              if(tdElem.id=='---' || isNaN(tdElem.id) ) tdElem.style.backgroundColor="#ffcccc";
              tdElem.value=j;
              tdElem.setAttribute("onclick", "val=prompt('Current value', this.id); parent.opener.fault_list[this.value].slip=sprintf('%5.1f',val); updateMarkerTable();"); 
              txtNode = document.createTextNode(parent.opener.fault_list[j].slip);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "col5";
              tdElem.id = parent.opener.fault_list[j].length;
              if(tdElem.id=='---' || isNaN(tdElem.id) ) tdElem.style.backgroundColor="#ffcccc";
              tdElem.value=j;
              tdElem.setAttribute("onclick", "val=prompt('Current value', this.id); parent.opener.updateLength(this.value,val); updateMarkerTable();"); 
              txtNode = document.createTextNode(parent.opener.fault_list[j].length);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "col6";
              if( isNaN(parent.opener.fault_list[j].width) )
                 tdElem.id = '---';
              if(tdElem.id=='---') tdElem.style.backgroundColor="#ffcccc";
              if( isNaN(parseFloat(parent.opener.fault_list[j].width)) )
                 txtNode = document.createTextNode('---');
              else
                 txtNode = document.createTextNode(sprintf('%5.1f',Math.abs(parent.opener.fault_list[j].width)));
              tdElem.value=j;
              tdElem.setAttribute("onclick", "val=prompt('Current value', Math.abs(this.id)); parent.opener.updateWidth(this.value,val); updateMarkerTable();"); 
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "col7";
              tdElem.id = parent.opener.fault_list[j].strike;
              if(tdElem.id=='---' || isNaN(tdElem.id) ) tdElem.style.backgroundColor="#ffcccc";
              tdElem.value=j;
              tdElem.setAttribute("onclick", "val=prompt('Current value', sprintf('%5.1f',this.id)); parent.opener.updateStrike(this.value,val); updateMarkerTable();"); 
              if(!isNaN(tdElem.id)) 
                  txtNode = document.createTextNode(sprintf('%5.1f',parent.opener.fault_list[j].strike));
              else
                  txtNode = document.createTextNode('---');
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);



              tdElem = document.createElement("td");
              tdElem.className = "col8";
              tdElem.id = parent.opener.fault_list[j].dip;
              if(tdElem.id=='---' || isNaN(tdElem.id) ) tdElem.style.backgroundColor="#ffcccc";
              tdElem.value=j;
              tdElem.setAttribute("onclick", "val=prompt('Current value', this.id); parent.opener.fault_list[this.value].dip=sprintf('%5.1f',val); updateMarkerTable();"); 
              txtNode = document.createTextNode(parent.opener.fault_list[j].dip);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "col9";
              tdElem.id = parent.opener.fault_list[j].rake;
              if(tdElem.id=='---' || isNaN(tdElem.id) ) tdElem.style.backgroundColor="#ffcccc";
              tdElem.value=j;
              tdElem.setAttribute("onclick", "val=prompt('Current value', this.id); parent.opener.fault_list[this.value].rake=sprintf('%5.1f',val); updateMarkerTable();"); 
              txtNode = document.createTextNode(parent.opener.fault_list[j].rake);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);


              parent.opener.computeFaultMw(j);

              totalM0=totalM0+parent.opener.fault_list[j].M0;
              
              tdElem = document.createElement("td");
              tdElem.className = "col10";
              tdElem.id = parent.opener.fault_list[j].Mw;
              if(!isNaN(tdElem.id)) 
                  txtNode = document.createTextNode(sprintf('%3.1f',parent.opener.fault_list[j].Mw));
              else
                  txtNode = document.createTextNode('');
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);


              tdElem = document.createElement("td");
	      tdElem.className = "col11";
              tdElem.id = parent.opener.fault_list[j].id;
              tdElem.value=j;
              tdElem.setAttribute("onclick", "FaultMarkersFocus(this.value);updateMarkerTable();"); 
              if(parent.opener.fault_list[j].focus==1) {
                   tdElem.style.backgroundColor="#F88017";
                   txtNode = document.createTextNode('Free');
              }
              else 
                txtNode = document.createTextNode('Fixed');
              tdElem.appendChild(txtNode); 
              trElem.appendChild(tdElem);


              docFragment.appendChild(trElem);
	}
	myNewtbody.appendChild(docFragment);
	mytable.replaceChild(myNewtbody, mytbody);

        var totalMw=Math.log(totalM0)/Math.log(10)/1.5 - 10.73;
        document.faults.EqMw.value=sprintf("%5.1f",totalMw)

        parent.opener.redrawBBs();
        return indices.length;
}


function SelectAll() {
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
        parent.opener.fault_list[tbody.childNodes[i].id-1].checked=1;
        tbody.childNodes[i].childNodes[0].childNodes[0].checked=true;
   }
}

function DeselectAll() {
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
        parent.opener.fault_list[tbody.childNodes[i].id-1].checked=-1;
        tbody.childNodes[i].childNodes[0].childNodes[0].checked=false;
   }
}

function Add(){
   var crd=parent.opener.map.getCenter();

   c=-1;
   for (var i = 0; i < parent.opener.fault_counter; i++)
      if (parent.opener.fault_list[i] != null) c++;
   if(c == -1)
     addASingleFaultName('new',crd.x,crd.y,5000,0,10,0,1,200000,20000);
   else
     addASingleFaultName('new',crd.x,crd.y,parent.opener.fault_list[c].depth*1000,
                                           parent.opener.fault_list[c].strike,
                                           parent.opener.fault_list[c].dip,
                                           parent.opener.fault_list[c].rake,
                                           parent.opener.fault_list[c].slip,
                                           parent.opener.fault_list[c].length*1000,
                                           parent.opener.fault_list[c].width*1000);
   FaultMarkersFocus(parent.opener.fault_counter-1);
}
function addASingleFaultName(name,lon,lat,depth,strike,dip,rake,slip,length,width){
  var c = addASingleFault(lon,lat,depth,strike,dip,rake,slip,length,width);
  parent.opener.fault_list[c].name = name;
}


function addASingleFault(lon,lat,depth,strike,dip,rake,slip,length,width){
   var pi = 3.141592653589793; 
   var crd = new GLatLng(lat, lon);
   var M=parent.opener.createEQMarker(crd);
   var c=parent.opener.fault_counter-1;
   parent.opener.fault_list[c].name='TBD';
   parent.opener.fault_list[c].M=M;
   parent.opener.fault_list[c].M.flag_clicked=1;
   parent.opener.map.addOverlay(parent.opener.fault_list[c].M);

   parent.opener.fault_list[c].M.FaultMarker = parent.opener.createFaultMarker(c,crd);
   parent.opener.fault_list[c].M.FaultMarker.flag_clicked=1;
   parent.opener.map.addOverlay(parent.opener.fault_list[c].M.FaultMarker);

   parent.opener.updateLength(c,length/1000);
   parent.opener.updateStrike(c,strike);

   parent.opener.fault_list[c].M.FaultMarker.WidthMarker = parent.opener.createWidthMarker(c,crd);
   parent.opener.map.addOverlay(parent.opener.fault_list[c].M.FaultMarker.WidthMarker);
   parent.opener.updateWidth(c,width*Math.cos(dip/180*pi)/1000);

   parent.opener.fault_list[c].depth=depth/1000;
   parent.opener.fault_list[c].slip=slip;
   parent.opener.fault_list[c].dip=dip;
   parent.opener.fault_list[c].rake=rake;
   FaultMarkersFocus(c);
   return c;
}


function mergeDeformations(value){
          var str = "return add_"+value+"();"
          var f = new Function(str); 
          var m2add=f();
          
          var l=updateMarkerTable();
          updagePages(l);
}

function Remove(){
   var str = prompt('Are you sure to remove subfault '+id+'?\nPlease, type "yes" to confirm.');
   if(str.toLowerCase() == 'yes'){
      var tbody = document.getElementById("myTbody");
      for (var i = 0; i< tbody.childNodes.length; i++){
         if(tbody.childNodes[i].childNodes[0].childNodes[0].checked == 1){
            var id=tbody.childNodes[i].childNodes[0].childNodes[0].name;
         
            f=parent.opener.fault_list[tbody.childNodes[i].id-1];
            
            if(f.M.FaultMarker!=null){
               parent.opener.map.removeOverlay(f.M.FaultMarker.polygonFault);
               parent.opener.map.removeOverlay(f.M.FaultMarker);
               if(f.M.FaultMarker.WidthMarker!=null){
                 parent.opener.map.removeOverlay(f.M.FaultMarker.WidthMarker.polygonFault);
                 parent.opener.map.removeOverlay(f.M.FaultMarker.WidthMarker);
               }
            }

            if(f.M!=null)
               parent.opener.map.removeOverlay(f.M);

            parent.opener.fault_list[tbody.childNodes[i].id-1]=null;
         }        
      }
   }
   setTimeout("Refresh();",50);
}


function FaultMarkersFocus(i){
   f=parent.opener.fault_list[i];

   var focus = f.focus;
   if(focus == 1){
      f.M.hide();
      if(f.M.FaultMarker!=null){
         f.M.FaultMarker.hide();
         if(f.M.FaultMarker.WidthMarker!=null)
            f.M.FaultMarker.WidthMarker.hide();
      }
      parent.opener.fault_list[i].focus=0;
   }
   else{
      f.M.show();
      if(f.M.FaultMarker!=null){
         f.M.FaultMarker.show();
         if(f.M.FaultMarker.WidthMarker!=null)
            f.M.FaultMarker.WidthMarker.show();
      }
      parent.opener.fault_list[i].focus=1;
   }
}



function Refresh(){
   var l=updateMarkerTable();
   updagePages(l);
   DeselectAll();
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





    //]]>
    </script>

<style type="text/css">
table {width:100%}
.tableWrapper {text-align:center}
.tr0 {background-color:#ffffcc}
.tr1 {background-color:#ccffcc}
.colr {width:3%}
.colname {width:5%}
.col1 {width:13%}
.col2 {width:13%}
.col3 {width:10%}
.col4 {width:10%}
.col5 {width:10%}
.col6 {width:10%}
.col7 {width:5%}
.col8 {width:5%}
.col9 {width:5%}
.col10 {width:5%}
.col11 {width:6%}
</style>


  </head>
  <body onload="load()" >
<div style="width:800px;background-color:#eeeeee">
<FORM NAME="faults">
<table cellspacing="0" cellpadding="0" border="0">
   <tr><td> 
      <table cellspacing="0" cellpadding="0" border="0">   
         <tr>
            <td align="left">
                <input type="button" value="Add Subfault"    onclick="Add();   var l=updateMarkerTable();updagePages(l);" />

                 <select id="select_markers" onchange='mergeDeformations(this.options[this.selectedIndex].value)'>
                               <option selected>Import subfaults</option>
EOM
for ((i=0;i<=${iscripts};i+=1)); do 
    file=${scripts[$i]}
    echo '    <option value="'$file'">' $file '</option>'
done
cat << EOM
                               </select>
                <input type="button" value="Remove Subfault" onclick="Remove();var l=updateMarkerTable();updagePages(l);" />
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
               <th></th>
               <th><a href="javascript:set_sorting(4)">ID<img id="DR4" border="0" src="http://burn.giseis.alaska.edu/ico_sortDown.gif" /> </a></th>
               <th>Lat <a href="javascript:set_lat()">(D/D)</a></th>
               <th>Lon <a href="javascript:set_lon()">(D/D)</a></th>
               <th><a href="javascript:set_sorting(2)">Depth<img id="DR2" border="0" src=""/></a></th>
               <th><a href="javascript:set_sorting(3)">Slip <img id="DR3" border="0" src=""/></a></th>
               <th>Length </th>
               <th>Width, SPrj</th>
               <th>Strike </th>
               <th>Dip </th>
               <th>Rake </th>
               <th>M<sub>w</sub></th>
               <th><a href="javascript:set_sorting(1)">Fixed/Free<img id="DR1" border="0" src="http://burn.giseis.alaska.edu/ico_sortDown.gif" /> </a></th>
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
            </td>
            <td align="right">
             Earthquake M<sub>w</sub>: 
             <input type="text" name="EqMw" value="" size="10" readonly/>
            </td>
            <td align="right">  
               Earthquake name: 
               <input type="text" name="eqname" value="test" size="10"/>
               <input type="button" value="Compute" onclick="parent.opener.FaultExport();" />
            </td>  
         </tr>
      </table> 
   </td></tr>
</table>
</form>
</div>

<form action="/cgi-bin/upload_okada.pl" method="post" enctype="multipart/form-data" target="_blank" onsubmit="setTimeout('window.location.reload();',5000);">
     <p>Upload Okada parameters: <input type="file" name="file_name" /></p>
     <input type="hidden" value="../htdocs/deformations" name="directory" />
     <input type="hidden" value="" name="path" />
     <p><input type="submit" name="Submit" value="Upload" /></p>
    </form>

</body>
</html>
EOM
