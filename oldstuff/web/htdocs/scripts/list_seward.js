function type_seward(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_seward() {
   var nm = new Object();
 
   nm[0] = new type_seward(-149.430556, 60.106944, "SewardWF", "SE15", "seward", "Seward waterfront" );
   nm[1] = new type_seward(-149.433333, 60.118056, "SewardDock", "SE15", "seward", "Seward harbor" );
   nm[2] = new type_seward(-149.439444, 60.116667, "SewardRoad", "SE15", "seward", "Seward highway, south" );
   nm[3] = new type_seward(-149.425000, 60.118056, "SewardODock", "SE15", "seward", "Cruise ship terminal" );
   nm[4] = new type_seward(-149.436111, 60.100000, "SewardSLife", "SE15", "seward", "Sea Life Center" );
   nm[5] = new type_seward(-149.436111, 60.115278, "SewardHotel", "SE15", "seward", "Seward jetty" );
   nm[6] = new type_seward(-149.405556, 60.125000, "SewardAir1", "SE15", "seward", "Airport runway, south" );
   nm[7] = new type_seward(-149.419444, 60.127778, "SewardAir2", "SE15", "seward", "Airport facilities" );
   nm[8] = new type_seward(-149.412500, 60.130000, "SewardAir3", "SE15", "seward", "Airport runway, middle" );
   nm[9] = new type_seward(-149.419444, 60.134722, "SewardAir4", "SE15", "seward", "Airport runway, north" );
   nm[10] = new type_seward(-149.431944, 60.127778, "SewardHwy", "SE15", "seward", "Seward Highway, north" );
   nm[11] = new type_seward(-149.431944, 60.070833, "SewardLWF1", "SE15", "seward", "Lowell Point, south" );
   nm[12] = new type_seward(-149.434722, 60.070833, "SewardL1", "SE15", "seward", "Lowell Point, campground" );
   nm[13] = new type_seward(-149.436111, 60.077778, "SewardLWF2", "SE15", "seward", "Lowell Point, north" );
   nm[14] = new type_seward(-149.441667, 60.076389, "SewardL2", "SE15", "seward", "Lowell Point, Spruce Creek" );
   nm[15] = new type_seward(-149.354167, 60.086667, "SewardFJWF1", "SE15", "seward", "Fourth of July Point, harbor" );
   nm[16] = new type_seward(-149.348611, 60.086667, "SewardFJ1", "SE15", "seward", "Fourth of July Point, dock facilities" );
   nm[17] = new type_seward(-149.361111, 60.000000, "SewardBay", "SE15", "seward", "Resurrection Bay entrance" );
   return nm;
}
