function [plong, platg, pdepg, cvector] = AdjustNorthWest(long, latg, depg, pvector, cvector)

pe=pvector.east;
pw=pvector.west;
ps=pvector.south;
pn=pvector.north;

nlat=length(latg(:,1));
if(latg(1,1)>latg(nlat,1))
  % Grid is oriented from North -> South
  % Need from South -> North
  index=nlat:-1:1;
  longm=long(index,:);
  latgm=latg(index,:);
  depgm=depg(index,:);
else
  longm=long;
  latgm=latg;
  depgm=depg;
end

nlon=length(long(1,:));
if(long(1,1)>long(1,nlon))
  % Grid is oriented from East -> West
  % Need from West -> East
  index=nlon:-1:1;
  longmm=longm(:,index);
  latgmm=latgm(:,index);
  depgmm=depgm(:,index);
else
  longmm=longm;
  latgmm=latgm;
  depgmm=depgm;
end


%Padding the circumference of the domain


lon0=longmm(1,1);    lat0=latgmm(1,1);
lon1=longmm(1,nlon); lat1=latgmm(nlat,1);

dlon=(lon1-lon0)/(nlon-1);
dlat=(lat1-lat0)/(nlat-1);
lon0=lon0-dlon*pe; lon1=lon1+dlon*pw;
lat0=lat0-dlat*ps; lat1=lat1+dlat*pn;
loni=linspace(lon0,lon1,nlon+pe+pw);
lati=linspace(lat0,lat1,nlat+ps+pn);

[plong, platg]=meshgrid(loni,lati);
pdepg=zeros(pn+ps+nlat,pe+pw+nlon);
pdepg=pdepg+NaN;

%WARNING
%In the padded longitude and latitude vectors edge elements are zeros
%In the padded bathymetry vector the new elements are NaNs
plong(ps+1:ps+nlat,pw+1:pw+nlon)=longmm;
platg(ps+1:ps+nlat,pw+1:pw+nlon)=latgmm;
pdepg(ps+1:ps+nlat,pw+1:pw+nlon)=depgmm;

cvector.east=cvector.east+pw;
cvector.west=cvector.west+pw;
cvector.north=cvector.north+ps;
cvector.south=cvector.south+ps;