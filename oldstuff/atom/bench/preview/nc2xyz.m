function nc2xyz(gname, step)
  grid=netcdf(['../post_processing/nc_',gname,num2str(step,'%0.7d'),'.nc']);

  lon=grid.VarArray(1,11).Data/pi*180; nlon=length(lon);
  lat=grid.VarArray(1,10).Data/pi*180; nlat=length(lat);

  %min_water_depth=0.01;
  %Z=double(reshape(grid.VarArray(1,3).Data,nlat,nlon));
  %DZ=double(reshape(grid.VarArray(1,4).Data,nlat,nlon));
  %Z(DZ<min_water_depth)=NaN;

  H      =double(reshape(grid.VarArray(1,5).Data,nlon,nlat));
  MaxDZ  =double(reshape(grid.VarArray(1,6).Data,nlon,nlat));
  MaxFlux=double(reshape(grid.VarArray(1,8).Data,nlon,nlat));

  filename=strcat([gname,'.H','.xyz']);
  saveXYZ(filename,H,lon,lat)

  filename=strcat([gname,'.max_dz','.xyz']);
  saveXYZ(filename,MaxDZ,lon,lat)

  filename=strcat([gname,'.max_fl','.xyz']);
  saveXYZ(filename,MaxFlux,lon,lat)
  return


function saveXYZ(filename,var,lon,lat)

  nlon=length(lon);
  nlat=length(lat);
  chunk=zeros(nlat,3);
  chunki=1:nlat;

  fid = fopen(filename,'wt');
  for ii=1:nlon
    chunk(:,1)=lat;
    chunk(:,2)=lon(nlon-ii+1);
    chunk(:,3)=var(nlon-ii+1,chunki);

    fprintf(fid, '%10.6f %10.6f %6.2f \n',chunk');
  end
  fclose(fid);
