function type_test(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_test() {
   var nm = new Object();
 
   nm[0] = new type_test(-160.751944, 53.461944, "ggg", "AU24", "test", "tth" );
   return nm;
}
