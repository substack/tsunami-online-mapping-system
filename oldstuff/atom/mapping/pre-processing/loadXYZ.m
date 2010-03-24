function [long_data, latg_data, depg_data, dlon, dlat]=loadXYZ(name)
xyzData=load(name);

len=size(xyzData,1);
ilat=sum(xyzData(:,1)==xyzData(1,1));
ilon=len/ilat;

raw_dep=zeros(ilon,ilat);

n=1;
while(n<=len)
  i=mod(n,ilon);
  if(i==0) 
    i=ilon;
  end
  j=floor((n-1)/ilon)+1;
  if(xyzData(n,3)~=99999)
    raw_dep(i,ilat-j+1)=xyzData(n,3);
  else
    raw_dep(i,ilat-j+1)=NaN;
  end
  n=n+1;
end
raw_lon=xyzData(1:ilon,1);
index=(raw_lon<0);
raw_lon(index)=raw_lon(index)+360;
raw_lat=xyzData(len:-ilon:1,2);

[long_data latg_data]=meshgrid(raw_lon, raw_lat);
depg_data=raw_dep';

dlon=(max(raw_lon)-min(raw_lon))/(length(raw_lon)-1);
dlat=(max(raw_lat)-min(raw_lat))/(length(raw_lat)-1);

