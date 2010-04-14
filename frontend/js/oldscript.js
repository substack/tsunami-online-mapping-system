var counter = 0;
var list = new Array();

var sort_type=1;
var sort_previous=1;
var sort_direction=1; 

var lastFocus=-1;

var display_np   = 0;
var display_p    = 0;
var display_pp   = 10;

function type_scenario(id, name, status, completed, t) {
    this.id   = id;
    this.name   = name;
    this.status  = status;
    if ( status != " Completed" )
        this.completed  = sprintf("%.2f\%", completed);
    else
        this.completed  = sprintf("%.2f\%", 100);
    if (t == null || t == "" || t == " ")
        this.time= 0;
    else
        this.time = t; 
    this.value = counter;
    this.checked = -1;
    this.lock = 0;
    if ( status == " Paused" || status == " Completed" || status == " Error") 
        this.lock = -1;
    this.timereq='';
    this.nodes='';
    this.nodetype='';
    this.creator='';
}

function updateAttr(id,timereq,nodes,nodetype,creator,id_size){
    for (var i=0; i<counter; i++) {
        if (list[i].id == id){
            list[i].timereq=timereq;
            list[i].nodes=nodes;
            list[i].nodetype=nodetype;
            list[i].creator=creator;
            list[i].id_size=id_size;
        }
    }
}

function addScenario(id, name, status, completed,t) {
    if( id != "" ) {
        list[counter++] = new type_scenario(id, name, status, completed,t);
    }
}

function updatingScenario(id, name, status, completed,t) {
    for (var i=0; i<counter; i++) {
        if (list[i].id == id){
            list[i].status=status;
            list[i].lock=completed;
            //list[i].time="";
        }
    }
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
   for (var i = 0; i < counter; i++){
      if (list[i] != null){
         indices[n] = i;
         switch(sort_type){
            case 1:
               field[n]   = list[i].id; break;
            case 2:
               field[n]   = list[i].name; break;
            case 3:
               field[n]   = list[i].status; break;
            case 4:
               field[n]   = list[i].completed; break;
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


function showPBS(id){
   window.open('/cgi-bin/show_pbs.cgi?'+id,'','toolbar=yes,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no,width=900,height=600');
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
              trElem.id = list[j].value;
              trElem.className = "tr1";
               


          tdElem = document.createElement("td");
          tdElem.className = "colr";
              tdElem.id = list[j].value;
          cbx = document.createElement("input");
          cbx.setAttribute("type", "checkbox");  
          cbx.setAttribute("name", list[j].id);  
              cbx.setAttribute("id", list[j].value); 
              if(list[j].checked == 1)
                  cbx.setAttribute("checked", true);  
              tdElem.appendChild(cbx); 
              trElem.appendChild(tdElem);



              tdElem = document.createElement("td");
              tdElem.className = "col0";
          tdElem.id = list[j].value;
              link = document.createElement("a");
          link.setAttribute("name", list[j].value);
          link.setAttribute("href", 'javascript:showPBS("'+list[j].id+'");');  //;
              link.appendChild(document.createTextNode(list[j].id));
              tdElem.appendChild(link);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
          tdElem.className = "col1";
              tdElem.id = list[j].value;
              txtNode = document.createTextNode(list[j].name);
              tdElem.appendChild(txtNode); 
              trElem.appendChild(tdElem);
              

              tdElem = document.createElement("td");
              tdElem.className = "col2";
          tdElem.id = list[j].value;
              if(list[j].status==' Computing') tdElem.style.backgroundColor="#aaffaa";
              if(list[j].status=='Pausing') tdElem.style.backgroundColor="#ffffaa";
              if(list[j].status==' Paused') tdElem.style.backgroundColor="#dddd88";
              if(list[j].status==' Error')     tdElem.style.backgroundColor="#ffaaaa";
              txtNode = document.createTextNode(list[j].status); 
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);



              tdElem = document.createElement("td");
              tdElem.className = "col3";
              tdElem.id = list[j].value;
              txtNode = document.createTextNode(list[j].completed);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "col4";
              tdElem.id = list[j].value;
              if(list[j].status !='Removing') 
                txtNode = document.createTextNode(list[j].time+"/"+list[j].timereq);
              else
                txtNode = document.createTextNode("");
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "col5";
              tdElem.id = list[j].value;
              txtNode = document.createTextNode(list[j].nodes);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "col6";
              tdElem.id = list[j].value;
              txtNode = document.createTextNode(list[j].nodetype);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

              tdElem = document.createElement("td");
              tdElem.className = "col7";
              tdElem.id = list[j].value;
              txtNode = document.createTextNode(list[j].creator);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

          tdElem = document.createElement("td");
              tdElem.className = "col8";
              tdElem.id = list[j].value;
              txtNode = document.createTextNode(list[j].id_size);
              tdElem.appendChild(txtNode);
              trElem.appendChild(tdElem);

   
              docFragment.appendChild(trElem);
    }
    
    myNewtbody.appendChild(docFragment);
    mytable.replaceChild(myNewtbody, mytbody);
    return indices.length;
}


function SelectAll() {
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
        list[tbody.childNodes[i].id-1].checked=1;
        tbody.childNodes[i].childNodes[0].childNodes[0].checked=true;
   }
}

function DeselectAll() {
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
        list[tbody.childNodes[i].id-1].checked=-1;
        tbody.childNodes[i].childNodes[0].childNodes[0].checked=false;
   }
}

function Remove(){
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
      if(tbody.childNodes[i].childNodes[0].childNodes[0].checked == 1){
         var id=tbody.childNodes[i].childNodes[0].childNodes[0].name;
         if (list[tbody.childNodes[i].id-1].lock != -100 ){
            var str = prompt('Are you sure to remove '+id+'?\nPlease, type "yes" to confirm.');
            if(str.toLowerCase() == 'yes')
              removingPBS(id);
         }
         else
            alert(id + " is archiving. You cannot remove it any longer.");
      }
   }
   setTimeout("Refresh();",50);
}
function Archive(){
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
      if(tbody.childNodes[i].childNodes[0].childNodes[0].checked == 1){
         var id=tbody.childNodes[i].childNodes[0].childNodes[0].name;
         if (list[tbody.childNodes[i].id-1].lock == -1 ){
            var str = prompt('Are you sure to archive '+id+'?\nPlease, type "yes" to confirm.');
            if(str.toLowerCase() == 'yes')
              archivingPBS(id);
         }
         else
            alert("Please pause or complete " + id + " before archiving.");
      }
   }
   setTimeout("Refresh();",50);
}

function Pause(){
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
      if(tbody.childNodes[i].childNodes[0].childNodes[0].checked == 1){
         var id=tbody.childNodes[i].childNodes[0].childNodes[0].name;
         if (list[tbody.childNodes[i].id-1].lock == -100 )
            alert(id+' is archiving. You cannot perform any operations on it any longer.');
         else
            if (list[tbody.childNodes[i].id-1].lock == 0 ){
               var str = prompt('Are you sure to pause '+id+'?\nPlease, type "yes" to confirm.');
               if(str.toLowerCase() == 'yes')
                 pausingPBS(id);
            }
            else{
               if (list[tbody.childNodes[i].id-1].lock == -1 )
                 alert(id +" is already paused.");
               else
                 alert(id +" is being paused. Please wait!");
            }
      }
   }
   setTimeout("Refresh();",50);
}
function Continue(){
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
      if(tbody.childNodes[i].childNodes[0].childNodes[0].checked == 1){
         var id=tbody.childNodes[i].childNodes[0].childNodes[0].name;
         if (list[tbody.childNodes[i].id-1].lock == -100 )
            alert(id+' is archiving. You cannot perform any operations on it any longer.');
         else
            if (list[tbody.childNodes[i].id-1].lock == -1 ){
               var str = prompt('Are you sure to resume '+id+'?\nPlease, type "yes" to confirm.');
               if(str.toLowerCase() == 'yes')
                 continuePBS(id);
            }
            else{
               if (list[tbody.childNodes[i].id-1].lock == 1 )
                 alert("Please wait to resume "+id+" scenario.");
               else
                 alert(id + " is already executing!");
            }
      }
   }
   setTimeout("Refresh();",50);
}

function Preview(){
   var tbody = document.getElementById("myTbody");
   for (var i = 0; i< tbody.childNodes.length; i++){
      if(tbody.childNodes[i].childNodes[0].childNodes[0].checked == 1){
         var id=tbody.childNodes[i].childNodes[0].childNodes[0].name;
         if (list[tbody.childNodes[i].id-1].lock == -100 )
            alert(id+' is archiving. You cannot perform any operations on it any longer.');
         else
            previewPBS(id);
      }
   }
   setTimeout("Refresh();",50);
}

function removingPBS(id){
   window.open('/cgi-bin/priv/remove_pbs.cgi?'+id,'','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no,width=500,height=10');
}

function archivingPBS(id){
    var options_destination = document.points.select_folder.selectedIndex;
    if (options_destination == 0){
        alert('You did not select a community');
    }
    else{
        var destination=document.points.select_folder.options[options_destination].value;
        window.open('/cgi-bin/priv/archive_pbs.cgi?'+id+'|'+destination,'','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no,width=500,height=10');
   }
}
function pausingPBS(id){
    window.open('/cgi-bin/priv/pause_pbs.cgi?'+id,'','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no,width=500,height=10');
}
function continuePBS(id){
    window.open('/cgi-bin/priv/continue_pbs.cgi?'+id,'','toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no,width=500,height=10');
}
function previewPBS(id){
    window.open('/cgi-bin/show_community_GM.cgi?ID='+id,'','toolbar=yes,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=no,width=800,height=900');
}


function Refresh(){
    window.location.reload();
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
    if (ic<0) {
        display_p=Math.max(0,display_p);
    }
    else {
        display_p=Math.min(display_np-1,display_p);
    }
    var selObj = document.getElementById('select_page');
    selObj.options[display_p+1].selected=true;
    updateMarkerTable();
}
