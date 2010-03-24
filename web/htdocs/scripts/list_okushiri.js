function type_okushiri(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_okushiri() {
   var nm = new Object();
 
   nm[0] = new type_okushiri(140.517500, 42.984167, "Iwanai", "OK08", "okushiri", "Tidal station" );
   nm[1] = new type_okushiri(140.135000, 41.867778, "Esashi", "OK08", "okushiri", "Tidal station" );
   return nm;
}
