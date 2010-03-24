function type_tg(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_tg() {
   var nm = new Object();
 
   nm[0] = new type_tg(-135.359722, 57.054167, "Sitka", "JU24", "tg", "Sitka tide gauge" );
   nm[1] = new type_tg(-126.900000, 50.750000, "AlertBay", "PA02", "tg", "Alert Bay tide gauge" );
   nm[2] = new type_tg(-123.000000, 48.450000, "FridayHarbor", "PA02", "tg", "Friday Harbor tide gauge" );
   nm[3] = new type_tg(-123.200000, 49.116667, "Steveston", "PA02", "tg", "Steveston tide gauge" );
   nm[4] = new type_tg(-132.099167, 52.664167, "TasuSound", "PA02", "tg", "Tasu Sound tide gauge" );
   nm[5] = new type_tg(-124.599167, 48.439167, "NeahBay", "PA02", "tg", "Neah Bay tide gauge" );
   nm[6] = new type_tg(-125.930000, 49.070000, "Tofino", "PA02", "tg", "Tofino tide gauge" );
   nm[7] = new type_tg(-122.299167, 37.733056, "Alameda", "PA02", "tg", "Alameda tide gauge" );
   nm[8] = new type_tg(-122.466667, 37.799167, "Presidio", "PA02", "tg", "Presidio tide gauge" );
   nm[9] = new type_tg(-118.503889, 33.960278, "SantaMonica", "PA02", "tg", "Santa Monica tide gauge" );
   nm[10] = new type_tg(-155.034167, 19.761389, "Hilo", "PA02", "tg", "Hilo tide gauge" );
   nm[11] = new type_tg(-131.667778, 55.335833, "Ketchikan", "JU24", "tg", "Ketchikan tide gauge" );
   nm[12] = new type_tg(-139.735556, 59.546667, "Yakutat", "YK03", "tg", "Yakutat tide gauge" );
   nm[13] = new type_tg(-130.355833, 54.239444, "PrinceRupert", "JU24", "tg", "Prince Rupert tide gauge" );
   return nm;
}
