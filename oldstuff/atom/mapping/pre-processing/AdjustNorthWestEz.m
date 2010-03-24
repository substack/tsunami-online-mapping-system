function [longmm, latgmm, depgmm] = AdjustNorthWestEz(long, latg, depg)


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


