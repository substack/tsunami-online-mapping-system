function type_Cordova(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_Cordova() {
   var nm = new Object();
 
   nm[0] = new type_Cordova(-145.766111, 60.544722, "CR1", "CR15", "Cordova", "Cordova, Harbor" );
   nm[1] = new type_Cordova(-145.761944, 60.545000, "CR2", "CR15", "Cordova", "Cordova, Waterfront" );
   nm[2] = new type_Cordova(-145.764167, 60.541944, "CR3", "CR15", "Cordova", "Cordova, Pier" );
   nm[3] = new type_Cordova(-145.761111, 60.538889, "CR4", "CR15", "Cordova", "Cordova, Orca St" );
   nm[4] = new type_Cordova(-145.754722, 60.540000, "CR5", "CR15", "Cordova", "Cordova, Copper River Hwy" );
   nm[5] = new type_Cordova(-145.777222, 60.543889, "CR6", "CR15", "Cordova", "Cordova, Orca Inlet" );
   nm[6] = new type_Cordova(-145.762500, 60.551111, "CR7", "CR15", "Cordova", "Cordova, Docks" );
   nm[7] = new type_Cordova(-145.760556, 60.550556, "CR8", "CR15", "Cordova", "Cordova, Inland docks" );
   nm[8] = new type_Cordova(-145.756667, 60.554444, "CR9", "CR15", "Cordova", "Cordova, Shipping yards" );
   nm[9] = new type_Cordova(-145.750833, 60.557778, "CR10", "CR15", "Cordova", "Cordova, Docks" );
   nm[10] = new type_Cordova(-145.743333, 60.561944, "CR11", "CR15", "Cordova", "Cordova, New England Canary Rd" );
   nm[11] = new type_Cordova(-145.717500, 60.580000, "CR12", "CR15", "Cordova", "Cordova, Canary" );
   nm[12] = new type_Cordova(-145.791111, 60.525278, "CR13", "CR15", "Cordova", "Cordova, Prince William Marina Rd" );
   nm[13] = new type_Cordova(-145.789722, 60.523889, "CR14", "CR15", "Cordova", "Cordova, Old Saw Mill Rd" );
   nm[14] = new type_Cordova(-145.773056, 60.535556, "CR15", "CR15", "Cordova", "Cordova, near Whiskey Ridge Rd" );
   nm[15] = new type_Cordova(-145.777778, 60.535833, "CR16", "CR15", "Cordova", "Cordova, Technological structures" );
   nm[16] = new type_Cordova(-145.763889, 60.548056, "CR17", "CR15", "Cordova", "Cordova, Docks" );
   nm[17] = new type_Cordova(-145.761111, 60.546389, "CR18", "CR15", "Cordova", "Cordova, Railroad Av" );
   nm[18] = new type_Cordova(-145.763889, 60.547222, "CR19", "CR15", "Cordova", "Cordova, Alaska Marine Hwy" );
   nm[19] = new type_Cordova(-145.760833, 60.543611, "CR20", "CR15", "Cordova", "Cordova, N Railroad Av" );
   nm[20] = new type_Cordova(-145.759444, 60.541667, "CR21", "CR15", "Cordova", "Cordova, Saw Mill Rd" );
   nm[21] = new type_Cordova(-145.769444, 60.597500, "CR22", "CR15", "Cordova", "Cordova, Deep Bay" );
   nm[22] = new type_Cordova(-145.643611, 60.655278, "CR23", "CR15", "Cordova", "Cordova, Nelson Bay" );
   nm[23] = new type_Cordova(-145.800278, 60.570833, "CR24", "CR15", "Cordova", "Cordova, Shipyard Bay" );
   nm[24] = new type_Cordova(-145.871944, 60.522500, "CR25", "CR15", "Cordova", "Cordova, Orca Inlet entrance" );
   nm[25] = new type_Cordova(-145.888333, 60.598889, "CR26", "CR15", "Cordova", "Cordova, Orca Bay entrance" );
   return nm;
}
