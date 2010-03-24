function type_Akutan(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_Akutan() {
   var nm = new Object();
 
   nm[0] = new type_Akutan(-165.785556, 54.130833, "AK2", "AK15", "Akutan", "Akutan cannery" );
   nm[1] = new type_Akutan(-165.774167, 54.132500, "AK1", "AK15", "Akutan", "Akutan town" );
   nm[2] = new type_Akutan(-165.717222, 54.133056, "AK3", "AK15", "Akutan", "Akutan bay entrance" );
   return nm;
}
