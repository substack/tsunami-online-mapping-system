function type_Plafker(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_Plafker() {
   var nm = new Object();
 
   nm[0] = new type_Plafker(-146.338889, 59.443056, "Middleton", "PW08", "Plafker", "Middleton Island" );
   nm[1] = new type_Plafker(-142.430000, 60.063333, "CapeYak", "PA02", "Plafker", "Cape Yakataga" );
   nm[2] = new type_Plafker(-148.943056, 59.961667, "WhidbeyBay", "PW24", "Plafker", "Whidbey Bay" );
   nm[3] = new type_Plafker(-151.416667, 59.235278, "RockyBay", "PW24", "Plafker", "Rocky Bay" );
   nm[4] = new type_Plafker(-148.527500, 59.997778, "PugetBay", "PW08", "Plafker", "Puget Bay" );
   nm[5] = new type_Plafker(-149.425556, 60.109167, "Seward", "SE08", "Plafker", "Seward" );
   return nm;
}
