function type_Whittier(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_Whittier() {
   var nm = new Object();
 
   nm[0] = new type_Whittier(-148.676944, 60.775278, "WT1", "WT15", "Whittier", "Depot Rd 1" );
   nm[1] = new type_Whittier(-148.673611, 60.776389, "WT3", "WT15", "Whittier", "Rail road tracks" );
   nm[2] = new type_Whittier(-148.678333, 60.775000, "WT4", "WT15", "Whittier", "Depot Rd 2" );
   nm[3] = new type_Whittier(-148.669167, 60.777778, "WT6", "WT15", "Whittier", "End of railroad tracks" );
   nm[4] = new type_Whittier(-148.665833, 60.777778, "WT7", "WT15", "Whittier", "Small harbor" );
   nm[5] = new type_Whittier(-148.693889, 60.777500, "WT8", "WT15", "Whittier", "Whittier creek, right bank" );
   nm[6] = new type_Whittier(-148.684722, 60.777222, "WT9", "WT15", "Whittier", "Water breaker" );
   nm[7] = new type_Whittier(-148.697778, 60.777500, "WT10", "WT15", "Whittier", "Whittier creek, left bank" );
   nm[8] = new type_Whittier(-148.710556, 60.775278, "WT11", "WT15", "Whittier", "West Camp Rd 1" );
   nm[9] = new type_Whittier(-148.705556, 60.776944, "WT12", "WT15", "Whittier", "West Camp Rd 2" );
   nm[10] = new type_Whittier(-148.715556, 60.774722, "WT13", "WT15", "Whittier", "West Camp Rd 3" );
   nm[11] = new type_Whittier(-148.721111, 60.776667, "WT14", "WT15", "Whittier", "Landing strip 1" );
   nm[12] = new type_Whittier(-148.718611, 60.777500, "WT15", "WT15", "Whittier", "Landing strip 2" );
   nm[13] = new type_Whittier(-148.715833, 60.778333, "WT16", "WT15", "Whittier", "Landing strip 3" );
   nm[14] = new type_Whittier(-148.688056, 60.775833, "WT17", "WT15", "Whittier", "Harbor parking" );
   nm[15] = new type_Whittier(-148.683056, 60.775278, "WT18", "WT15", "Whittier", "Rail road tracks" );
   nm[16] = new type_Whittier(-148.699167, 60.783056, "WT19", "WT15", "Whittier", "Passage Canal" );
   nm[17] = new type_Whittier(-148.552500, 60.813611, "WT20", "WT15", "Whittier", "Passage Canal entrance" );
   nm[18] = new type_Whittier(-148.561667, 60.792222, "WT21", "WT15", "Whittier", "Shotgun Cove, West" );
   nm[19] = new type_Whittier(-148.689167, 60.777500, "WT22", "WT15", "Whittier", "Whittier harbor" );
   nm[20] = new type_Whittier(-148.719444, 60.784722, "WT23", "WT15", "Whittier", "Passage Canal, North-West corner 1" );
   nm[21] = new type_Whittier(-148.721389, 60.784444, "WT24", "WT15", "Whittier", "Passage Canal, North-West corner 2" );
   nm[22] = new type_Whittier(-148.718611, 60.781667, "WT25", "WT15", "Whittier", "Passage Canal, West" );
   nm[23] = new type_Whittier(-148.566667, 60.782222, "WT26", "WT15", "Whittier", "Shotgun Cove, South" );
   nm[24] = new type_Whittier(-148.538611, 60.793056, "WT27", "WT15", "Whittier", "Shotgun Cove, East" );
   return nm;
}
