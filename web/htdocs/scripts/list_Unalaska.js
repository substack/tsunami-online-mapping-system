function type_Unalaska(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_Unalaska() {
   var nm = new Object();
 
   nm[0] = new type_Unalaska(-166.484444, 53.908056, "UN1", "UN03", "Unalaska", "Unalaska" );
   nm[1] = new type_Unalaska(-165.632500, 54.051111, "UN2", "UN03", "Unalaska", "South of Akutan" );
   return nm;
}
