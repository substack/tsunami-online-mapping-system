

function fault(id, lon, lat, depth, slip, length, width, strike, dip, rake) {
          this.id=id;
          this.lon = lon;
          this.lat = lat;
          this.depth = depth;
          this.slip = slip;
          this.length = length;
          this.width = width;
          this.strike = strike;
          this.dip  = dip;
          this.rake  = rake;
          this.M = null;
          this.focus = 1;
          this.M0=0;
          this.name=id;

          this.value = fault_counter;
          this.checked = 0;
       }

       function addFault(id, lon, lat, depth, slip, length, width, strike, dip, rake) {
             fault_list[fault_counter++] = new fault(id, lon, lat, depth, slip, length, width, strike, dip, rake);
       }



function my_mouseup(e){
   rd_start=0;
}

function my_mouseover(e){
    if (!e) e= event;
    var imgX,imgY;
    if (e.pageX == null){
       // IE case
       var d= (document.documentElement && 
               document.documentElement.scrollLeft != null) ?
               document.documentElement : document.body;
       imgX= e.clientX + d.scrollLeft;
       imgY= e.clientY + d.scrollTop;
    }
    else{
       // all other browsers
       imgX= e.pageX;
       imgY= e.pageY;
    }

    imgX=Math.max(Math.min(imgX,790),10);
    imgY=Math.max(Math.min(imgY,490),10);

  if(rd_start==1){
    var TlcLatLng = map.fromContainerPixelToLatLng(new GPoint(0,0),true); 
    var TlcDivPixel = map.fromLatLngToDivPixel(TlcLatLng); 

    var W0DivPixel = map.fromLatLngToDivPixel(new GLatLng(fault_list[rd_number].lat0,fault_list[rd_number].lon0)); 
   
    var imgX0=W0DivPixel.x-TlcDivPixel.x;
    var imgY0=W0DivPixel.y-TlcDivPixel.y;


    var strike = fault_list[rd_number].strike;
    var rake=Math.abs(imgX-imgX0);
    var dip=Math.abs(imgY-imgY0);

    dip=Math.min(dip,180);
    rake=Math.min(rake,360);

    fault_list[rd_number].rake=sprintf('%5.1f',rake);
    fault_list[rd_number].dip=sprintf('%5.1f',dip);
    var l=newdefwindow.window.updateMarkerTable();
    newdefwindow.window.updagePages(l);

    //jg.clear();
    //jg.drawLine(imgX0, imgY0, imgX,imgY);
    redrawBBs();
   }
}

function redrawBBs(){
    jg.setColor("#aa0000"); // red
    jg.setStroke(1);  
    jg.clear();
    for(var i=0;i<fault_counter;i++){
       if(fault_list[i] != null){
          var strike = parseFloat(fault_list[i].strike);
          var dip  = parseFloat(fault_list[i].dip);
          var rake = parseFloat(fault_list[i].rake);
          if( rake != '---' && strike != '---' && dip != '---')
             drawBB(strike,dip,rake,i,15);
          //alert("i="+i+" S="+strike+" D="+dip+" R="+rake);
       }
    }
    jg.paint();
}


function drawBB(strike,dip,rake,n,r){
    var TlcLatLng = map.fromContainerPixelToLatLng(new GPoint(0,0),true); 
    var TlcDivPixel = map.fromLatLngToDivPixel(TlcLatLng); 

    var W0DivPixel = map.fromLatLngToDivPixel(new GLatLng(fault_list[n].lat0,fault_list[n].lon0)); 
   
    var imgX0=W0DivPixel.x-TlcDivPixel.x;
    var imgY0=W0DivPixel.y-TlcDivPixel.y;

    if(imgX0<50)  return;
    if(imgY0<50)  return;
    if(imgX0>750) return;
    if(imgY0>450) return;

//    jg.clear();
    bb(90+strike, dip, rake, imgX0, imgY0, r);
    jg.drawEllipse(imgX0-r, imgY0-r, 2*r, 2*r);
//    jg.paint();
}


function bb(s1, d1, r1, cx, cy, D){

  var pi = 3.141592653589793;
  var r2d = 180/pi;
  var d2r = pi/180;
 
  var mech = 0;

  if(r1 > 180){ r1 = r1 - 180; mech = 1;}

  if(r1 < 0){   r1 = r1 + 180; mech = 1;}

// Get azimuth and dip of second plane
  var AP = AuxPlane(s1,d1,r1);
  var s2 = AP.strike;
  var d2 = AP.dip;
  var r2 = AP.rake;

  

  var P;
  if (mech > 0)
    P = 2;
  else
    P = 1;

  if (d1 >= 90)
    d1 = 89.9999;

  if (d2 >= 90)
    d2 = 89.9999;


  var cphi, sphi, d, m;
  var phiN=11;

  var phi = new Array();
  var l1 = new Array();
  var l2 = new Array();
  

  for (var i=1;i<=phiN;i++){
    phi[i]=(i-1)*pi/(phiN-1);
    cphi = Math.cos(phi[i]);   sphi = Math.sin(phi[i]);
    
    d = 90 - d1;   m = 90;
    l1[i] = Math.sqrt(d*d/(sphi*sphi + cphi*cphi*d*d/m/m));
    
    d = 90 - d2;    m = 90;
    l2[i] = Math.sqrt(d*d/(sphi*sphi + cphi*cphi*d*d/m/m));
  }

   
  var inc = 10;
  var X1 = new Array();
  var Y1 = new Array();
  for(var i=1;i<=phiN;i++){
    X1[i]=l1[i]*Math.cos(phi[i]+s1*d2r);
    Y1[i]=l1[i]*Math.sin(phi[i]+s1*d2r);
  }

  

  var Xs1 = new Array();
  var Ys1 = new Array();  
  var X2 = new Array();
  var Y2 = new Array(); 
  var th2 = new Array(); 

  if(P == 1){
    var lo = s1 - 180;
    var hi = s2;
    if (lo > hi)
        inc = -inc;
    
    var th1=mylin(s1-180,s2,inc);
    for (var i=1;i<=th1.L;i++){
        Xs1[i]=90*Math.cos(th1.A[i]*d2r);
        Ys1[i]=90*Math.sin(th1.A[i]*d2r);
    }
    for (var i=1;i<=phiN;i++){
       X2[i]=l2[i]*Math.cos(phi[i]+s2*d2r);
       Y2[i]=l2[i]*Math.sin(phi[i]+s2*d2r);
    }
    th2=mylin(s2+180,s1,-inc);
  }
  else{
    var hi = s1 - 180;
    var lo = s2 - 180;
    if (lo > hi)
        inc = -inc;
    
    var th1=mylin(hi,lo,-inc);
    for (var i=1;i<=th1.L;i++){
        Xs1[i]=90*Math.cos(th1.A[i]*d2r);
        Ys1[i]=90*Math.sin(th1.A[i]*d2r);
    }
    for (var i=1;i<=phiN;i++){
       X2[i]=l2[phiN-i+1]*Math.cos(phi[phiN-i+1]+s2*d2r);
       Y2[i]=l2[phiN-i+1]*Math.sin(phi[phiN-i+1]+s2*d2r);
    }
    th2=mylin(s2,s1,inc);
 }

var Xs2 = new Array();
var Ys2 = new Array(); 
for (var i=1;i<=th2.L;i++){
    Xs2[i]=90*Math.cos(th2.A[i]*d2r);
    Ys2[i]=90*Math.sin(th2.A[i]*d2r);
}

var X = [];
var Y = [];

for(var i=1;i<=phiN;   i++){ X.push(X1[i]);  Y.push(Y1[i]); }
for(var i=1;i<=th1.L;i++){ X.push(Xs1[i]); Y.push(Ys1[i]);}
for(var i=1;i<=phiN;   i++){ X.push(X2[i]);  Y.push(Y2[i]); }
for(var i=1;i<=th2.L;i++){ X.push(Xs2[i]); Y.push(Ys2[i]); }

for(var i=0;i<2*phiN+th1.L+th2.L; i++){
   X[i] = X[i] * D/90 + cx;
   Y[i] = Y[i] * D/90 + cy;
}

jg.fillPolygon(X, Y);

}


function mylin(x0,x1,dx){
   var n=Math.round((x1-x0)/dx);
   var A = new Array();

   for(var i=1;i<=n+1;i++)
      A[i]=x0+(i-1)*dx;

   this.A=A;
   this.L=n+1;
   return this;
}

function AuxPlane(s1,d1,r1){
//%function [strike, dip, rake] = AuxPlane(s1,d1,r1);
//% Get Strike and dip of second plane, adapted from Andy Michael bothplanes.c

   var r2d = 180/3.1415926535;

   var z = (s1+90)/r2d;
   var z2 = d1/r2d;
   var z3 = r1/r2d;

   /* slick vector in plane 1 */
   var sl1 = -Math.cos(z3)*Math.cos(z)-Math.sin(z3)*Math.sin(z)*Math.cos(z2);
   var sl2 = Math.cos(z3)*Math.sin(z)-Math.sin(z3)*Math.cos(z)*Math.cos(z2);
   var sl3 = Math.sin(z3)*Math.sin(z2);



   var sd = strikedip(sl2,sl1,sl3);
   this.strike = sd.strike;
   this.dip = sd.dip;

   var n1 =  Math.sin(z)* Math.sin(z2);  /* normal vector to plane 1 */
   var n2 =  Math.cos(z)* Math.sin(z2);
   var n3 =  Math.cos(z2);
   var h1 = -sl2; /* strike vector of plane 2 */
   var h2 = sl1;
    /* note h3=0 always so we leave it out */

   z = h1*n1 + h2*n2;
   z = z/Math.sqrt(h1*h1 + h2*h2);
   z = Math.acos(z);

   if(sl3 > 0)
      this.rake = z*r2d;
   if(sl3 <= 0)
      this.rake = -z*r2d;
   return this;
}

function strikedip(n, e, u){
  // Finds strike and dip of plane given normal vector having components n, e, and u
  // Adapted from Andy Michaels stridip.c
   
   var r2d = 180/3.14159265359;
   if(u<0){n=-n; e=-e; u=-u;}

   var strike = Math.atan2(e,n)*r2d;
   strike-=90;

   while (strike >= 360)
        strike-=360;

   while (strike < 0)
        strike+=360;

   this.strike=strike;

   var x = Math.sqrt(n*n + e*e);
   this.dip = Math.atan2(x,u)*r2d;

   return this;
}
