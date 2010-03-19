 %name='CR15';
 %step='0000';
 %ID='CASE_000436';

%Load GeoTIFF image
step=str2num(step);
load([name, '.image'], '-mat');
load([name, '.frame'], '-mat');
try
   load([name, '.line'] , '-mat');
   for i=1:length(IL)
     IL(i).X=360+IL(i).X;
   end
  ynLine=1;
catch
  ynLine=0;
end




min_water_depth=0.01;
grid=netcdf(['../post_processing/nc_',name,num2str(step,'%0.7d'),'.nc']);

lat=grid.VarArray(1,11).Data/pi*180; nlon=length(lat);
lon=grid.VarArray(1,10).Data/pi*180; nlat=length(lon);

H    =double(reshape(grid.VarArray(1,5).Data,nlon,nlat));  
MaxDZ=double(reshape(grid.VarArray(1,6).Data,nlon,nlat));

f=figure(1);
for n=1:length(frame)
  index_I=frame(n).i0:frame(n).si:frame(n).i0+frame(n).di;
  index_J=frame(n).j0:frame(n).sj:frame(n).j0+frame(n).dj;

  ILon=I_lon(index_I,index_J)-slon_image;
  ILat=I_lat(index_I,index_J)-slat_image;
  IDat=I_data(index_I,index_J);
  
  minLon=min(min(ILon));
  maxLon=max(max(ILon));

  minLat=min(min(ILat));
  maxLat=max(max(ILat));

  contourf(ILon,ILat,IDat,'EdgeColor','none')
  colormap gray
  hold on
  if(ynLine==1)
    for i=1:length(IL)
      plot(IL(i).X-slon_line,IL(i).Y-slat_line,'-y','LineWidth',0.5)
    end
  end
  lont=lon( (minLon<lon) & (lon<maxLon));
  latt=lat( (minLat<lat) & (lat<maxLat));
  
  MaxDZt=MaxDZ((minLat<lat) & (lat<maxLat), (minLon<lon) & (lon<maxLon));
  Ht    =H    ((minLat<lat) & (lat<maxLat), (minLon<lon) & (lon<maxLon));
  
  contour(lont, latt, MaxDZt,[min_water_depth min_water_depth*1.0001],'-r','LineWidth',0.5);
  contour(lont, latt, Ht,    [0.0 min_water_depth],'-b','LineWidth',0.5);

  hold off
  set(f,'Position',[100 100 600 600*2*(maxLat-minLat)/(maxLon-minLon)]);  
  set(gca,'PlotBoxAspectRatio',[1 1*2*(maxLat-minLat)/(maxLon-minLon) 1])
   %
  print(['MAP_',name,'_',ID,'_',num2str(n,'%2.2d'),'.eps'],'-depsc')
  print(['MAP_',name,'_',ID,'_',num2str(n,'%2.2d'),'.png'],'-dpng')
end
