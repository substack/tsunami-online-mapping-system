%clear all
%gname='SE15';
%step=60;

min_water_depth=0.01;

%Generate MaxDZ and MaxFlux files
nc2xyz(gname,step);

%[long, latg, defg, dlon, dlat]=loadXYZ('SE15.max_dz.xyz');
%contour(long,latg,defg,[0 1])
%return

%Generate KML inundation line
directory='';
filename=[gname,'.max_dz'];
xyz2kml();
