function type_Aleutians(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_Aleutians() {
   var nm = new Object();
 
   nm[0] = new type_Aleutians(-169.947500, 56.890833, "AU1", "AU24", "Aleutians", "St Paul" );
   nm[1] = new type_Aleutians(-160.535556, 55.288889, "AU2", "AU24", "Aleutians", "Popof Strait" );
   nm[2] = new type_Aleutians(-162.314722, 55.007500, "AU3", "AU24", "Aleutians", "King Cove" );
   nm[3] = new type_Aleutians(-162.653889, 55.211667, "AU4", "AU24", "Aleutians", "Cold Bay" );
   nm[4] = new type_Aleutians(-163.392222, 54.865278, "AU5", "AU24", "Aleutians", "False Pass" );
   nm[5] = new type_Aleutians(-168.879722, 52.947500, "AU6", "AU08", "Aleutians", "Nikolski" );
   return nm;
}
