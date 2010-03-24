function type_dart(lon, lat, name, grid, group, desc) {
   this.lon   = lon;
   this.lat   = lat;
   this.name  = name;
   this.grid  = grid;
   this.group = group;
   this.desc  = desc;
}
 
function merge_dart() {
   var nm = new Object();
 
   nm[0] = new type_dart(178.270278, 48.942222, "DART_21414", "PA02", "dart", "NW Pacific" );
   nm[1] = new type_dart(-164.010556, 51.069444, "DART_46402", "PA02", "dart", "240 NM South of Dutch Harbor, AK" );
   nm[2] = new type_dart(-156.940000, 52.650000, "DART_46403", "PA02", "dart", "230 NM Southeast of Shumagin Island, AK" );
   nm[3] = new type_dart(-169.871389, 49.626111, "DART_46408", "PA02", "dart", "NW Pacific S AK" );
   nm[4] = new type_dart(-148.500000, 55.300000, "DART_46409", "PA02", "dart", "240 NM Southeast of Kodiak, AK" );
   nm[5] = new type_dart(-144.000000, 57.500000, "DART_46410", "PA02", "dart", "330 NM Southeast of Anchorage, AK" );
   nm[6] = new type_dart(-175.601111, 48.861111, "DART_46413", "PA02", "dart", "East of ADAK, AK" );
   nm[7] = new type_dart(-129.600000, 48.800000, "DART_46419", "PA02", "dart", "300 NM West-Northwest of Seattle, WA" );
   nm[8] = new type_dart(-125.005556, -8.488611, "DART_51406", "PA02", "dart", "2,900 NM Southeast of Hawaii" );
   nm[9] = new type_dart(-127.006944, 39.340000, "DART_46411", "PA02", "dart", "260 NM Northwest of San Francisco, CA" );
   return nm;
}
