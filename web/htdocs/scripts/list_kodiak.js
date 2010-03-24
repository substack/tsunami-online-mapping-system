function type_kodiak(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_kodiak() {
   var nm = new Object();
 
   nm[0] = new type_kodiak(-152.443611, 57.601111, "Kalsin", "KD03", "kodiak", "Kalsin Bay, Kodiak" );
   nm[1] = new type_kodiak(-152.407222, 57.785278, "KodiakCity", "KC01", "kodiak", "Kodiak City, Kodiak" );
   nm[2] = new type_kodiak(-152.489167, 57.736389, "NavalStation", "NS01", "kodiak", "Naval Station, Kodiak" );
   nm[3] = new type_kodiak(-153.761667, 56.877222, "Kaguyak", "KD08", "kodiak", "Kaguyak Bay, Kodiak" );
   nm[4] = new type_kodiak(-153.294444, 57.195278, "OldHarbor", "KD08", "kodiak", "Old Harbor, Kodiak" );
   nm[5] = new type_kodiak(-152.768611, 57.490556, "SalteryCove", "KD08", "kodiak", "Saltery Cove, Kodiak" );
   nm[6] = new type_kodiak(-152.145833, 57.619444, "Chiniak", "KD08", "kodiak", "Cape Chiniak, Kodiak" );
   return nm;
}
