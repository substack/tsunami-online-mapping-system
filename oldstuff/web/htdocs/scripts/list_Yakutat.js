function type_Yakutat(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_Yakutat() {
   var nm = new Object();
 
   nm[0] = new type_Yakutat(-139.735556, 59.546667, "Yak1", "YK15", "Yakutat", "Yakutat tidal station" );
   nm[1] = new type_Yakutat(-140.079722, 59.594722, "Yak2", "YK03", "Yakutat", "Yakutat Bay entrance" );
   return nm;
}
