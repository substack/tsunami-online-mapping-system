%clear all
global oGrid


overlap=5;  %It was 20 before
iterations=100;
width=3; %It was 4

overlap=min(width+1,overlap);


standard_grid_path='/lustre/wrkdir/nicolsky/mapping/grids/DEM/';
modified_grid_path=['/lustre/wrkdir/nicolsky/mapping/pre-processing/',CaseID,'/'];
path_save=[modified_grid_path,'tmp/'];

%Read the grid tree
disp(' ');
disp(' ');
disp('Successfully read grid topology');
[list, dlist, ilist]=initializeTree([modified_grid_path, 'grid_tree.xml']);
for f=ilist
    grid_xml=['grid_',list(f).name,'.xml'];

    strLocal=['Accessing a modified copy of ', grid_xml];
    try
        iGrid(f)=readGridStructure([modified_grid_path, grid_xml]);
        strLocal=[strLocal, ' - Yes'];
        disp(strLocal);
    catch
        strDepos=['Accessing a standard copy of ', grid_xml];
        try
            iGrid(f)=readGridStructure([standard_grid_path, grid_xml]);
            strDepos=[strDepos, ' - Yes'];
            disp(strDepos);
        catch
            strLocal=['   ',strLocal, ' - No'];
            strDepos=['   ',strDepos, ' - No'];
            
            disp(['Failed to read grid XML file ', grid_xml,'.']);
            disp(strLocal);
            disp(strDepos);
            return
        end
    end
    
end
for f=ilist
  iGrid(f).parent=list(f).parent;
  iGrid(f).children=list(f).children;
  iGrid(f).nchildren=sum(list(f).children~=-1);
  if(iGrid(f).parent==0)
    iGrid(f).ratio=[1 1];
  end
end



%Iterate grids from the smallest to the largest in geometrical terms
for f=ilist
  [iGrid(f).original.long, iGrid(f).original.latg, iGrid(f).original.depg, iGrid(f).dlon, iGrid(f).dlat]=loadXYZ(iGrid(f).bathymetry_file);
  [iGrid(f).original.long, iGrid(f).original.latg, iGrid(f).original.depg] = AdjustNorthWestEz(iGrid(f).original.long, iGrid(f).original.latg, iGrid(f).original.depg);
  if(strcmp(iGrid(f).bathymetry_units,'cm'))
    iGrid(f).original.depg=iGrid(f).original.depg/100;
  end
  
  %Cut grids according to embeding ratios
  max_i=floor(size(iGrid(f).original.depg,1)/iGrid(f).ratio(2))*iGrid(f).ratio(2);
  max_j=floor(size(iGrid(f).original.depg,2)/iGrid(f).ratio(1))*iGrid(f).ratio(1);
  iGrid(f).original.long=iGrid(f).original.long(1:max_i,1:max_j);
  iGrid(f).original.latg=iGrid(f).original.latg(1:max_i,1:max_j);
  iGrid(f).original.depg=iGrid(f).original.depg(1:max_i,1:max_j);
  
  %Custom fixes to bathymetry files
%  if(strcmp(iGrid(f).name,'SE02')==1)
%    index=(iGrid(f).original.long<213.2)&(iGrid(f).original.long>212.4)&(iGrid(f).original.latg<60.4)&(iGrid(f).original.latg>60.1);
%    iGrid(f).original.depg(index)=-100;
%  end
%   if(strcmp(iGrid(f).name,'PW24')==1)
%     index=(iGrid(f).original.long<213.1)&(iGrid(f).original.long>212.9)&(iGrid(f).original.latg<60.6)&(iGrid(f).original.latg>60.215);
%     iGrid(f).original.depg(index)=NaN;
%      index=(iGrid(f).original.long<210.4)&(iGrid(f).original.long>210.36)&(iGrid(f).original.latg<59.54)&(iGrid(f).original.latg>59.502);
%      iGrid(f).original.depg(index)=-100;
%   end

 if(strcmp(iGrid(f).name,'PA02')==1)
    index=(iGrid(f).original.long<126.4)&(iGrid(f).original.long>125.6)&(iGrid(f).original.latg<10.4);
    iGrid(f).original.depg(index)=NaN;
  end

  if(strcmp(iGrid(f).name,'SE08')==1)
    index=(iGrid(f).original.long<210.01)&(iGrid(f).original.long>210)&(iGrid(f).original.latg<59.8)&(iGrid(f).original.latg>59.74);
    iGrid(f).original.depg(index)=NaN;
  end
  if(strcmp(iGrid(f).name,'SE03')==1)
    index=(iGrid(f).original.long<210.379)&(iGrid(f).original.long>210.376)&(iGrid(f).original.latg<59.84)&(iGrid(f).original.latg>59.8);
    iGrid(f).original.depg(index)=NaN;
  end
  if(strcmp(iGrid(f).name,'PW03')==1)
    index=(iGrid(f).original.long<213.41)&(iGrid(f).original.long>213.35)&(iGrid(f).original.latg<61.160)&(iGrid(f).original.latg>61.145);
    iGrid(f).original.depg(index)=NaN;
  end
  
  if(strcmp(iGrid(f).name,'CR15')==1)
    index=(iGrid(f).original.long<214.11)&(iGrid(f).original.latg>60.69);
    iGrid(f).original.depg(index)=NaN;
  end
  
  
  if(strcmp(iGrid(f).name,'WT15')==1)
    index=(iGrid(f).original.long>211.5035)&(iGrid(f).original.latg>60.7795)&(iGrid(f).original.latg<60.7820);
    iGrid(f).original.depg(index)=NaN;
    
    index=(iGrid(f).original.long>211.5035)&(iGrid(f).original.latg>60.8060)&(iGrid(f).original.latg<60.8070);
    iGrid(f).original.depg(index)=NaN; 
    
    index=(iGrid(f).original.long>211.5035)&(iGrid(f).original.latg>60.8285)&(iGrid(f).original.latg<60.8295);
    iGrid(f).original.depg(index)=NaN; 
     
  end
  
%   if(strcmp(iGrid(f).name,'NS01')==1)
%     iGrid(f).original.depg=iGrid(f).original.depg-3;
%   end
  

  iGrid(f).long=iGrid(f).original.long;
  iGrid(f).latg=iGrid(f).original.latg;
  iGrid(f).depg=iGrid(f).original.depg;

  if(strcmp(iGrid(f).type,'propagation')==1)
    iGrid(f).depg(iGrid(f).depg>0)=NaN;
    
    %THERE IS ALSO ANOTHER PLACE, DOWN THERE    HERE
    %iGrid(f).depg((iGrid(f).depg<=0)&(-10<iGrid(f).depg))=-10;
  end
  
    %Auxilary variables
    %Number of points in longitude and latitude directions
    iGrid(f).nlon=size(iGrid(f).depg,2);
    iGrid(f).nlat=size(iGrid(f).depg,1);
    %Coordinates of the north east corner in the parent grid
    iGrid(f).c.east =iGrid(f).c.west +iGrid(f).nlon/iGrid(f).ratio(1)-1;
    iGrid(f).c.north=iGrid(f).c.south+iGrid(f).nlat/iGrid(f).ratio(2)-1;
    %Construction of the padding vector
    iGrid(f).p.east=0;    iGrid(f).p.north=0;
    iGrid(f).p.west=0;    iGrid(f).p.south=0;
    
    %The child grid should be completely submerged into the parent grid
    %Hence we have to pad the parent grid around its borders
    for i=1:iGrid(f).nchildren
      c=iGrid(f).children(i);
      tmp_north=max(iGrid(c).c.north-iGrid(f).nlat+overlap, iGrid(f).p.north);
      if(tmp_north>0)
        iGrid(f).p.north=round(tmp_north/iGrid(f).ratio(2)+0.5)*iGrid(f).ratio(2);
      else
        iGrid(f).p.north=0;
      end
      
      tmp_east=max(iGrid(c).c.east-iGrid(f).nlon+overlap, iGrid(f).p.east);
      if(tmp_east>0)
        iGrid(f).p.east=round(tmp_east/iGrid(f).ratio(1)+0.5)*iGrid(f).ratio(1);
      else
        iGrid(f).p.east=0;
      end
    end
    
    %Adjust grid such that (1,1) element is the uttermost south-west point
    %and pad the grid according to  iGrid(f).p vector
    [iGrid(f).long, iGrid(f).latg, iGrid(f).depg, iGrid(f).c] = ...
            AdjustNorthWest(iGrid(f).long, iGrid(f).latg, iGrid(f).depg, iGrid(f).p, iGrid(f).c);

    %Update a number of points in longitude and latitude directions
    iGrid(f).nlon=size(iGrid(f).depg,2);
    iGrid(f).nlat=size(iGrid(f).depg,1);
    %Update coordinates of the north east corner in the parent grid
    iGrid(f).c.east =iGrid(f).c.west +iGrid(f).nlon/iGrid(f).ratio(1)-1;
    iGrid(f).c.north=iGrid(f).c.south+iGrid(f).nlat/iGrid(f).ratio(2)-1;
          
    for i=1:iGrid(f).nchildren
      c=iGrid(f).children(i);
      iGrid(f).depg=Smoothen_grid_boundaries(iGrid(f).long, iGrid(f).latg, iGrid(f).depg, iGrid(c).depg, iGrid(c).c, iGrid(c).ratio, width, iterations, f*10+i);
    end
    
    if(strcmp(iGrid(f).type,'propagation')==1)
      iGrid(f).depg(iGrid(f).depg>0)=NaN;
      %iGrid(f).depg((iGrid(f).depg<=0)&(-10<iGrid(f).depg))=-10;
    end
end


for f=dlist
  iGrid(f).depg(isnan(iGrid(f).depg))=100;
  
  if(strcmp(iGrid(f).type,'propagation')~=1)
    save([path_save, iGrid(f).name,'.preview'],'f','-ASCII');
  end
end



for f=dlist
  oGrid(f).name    =iGrid(f).name;
  oGrid(f).type    =iGrid(f).type;
  oGrid(f).color   =iGrid(f).color;
  oGrid(f).ratio_x =iGrid(f).ratio(1);
  oGrid(f).ratio_y =iGrid(f).ratio(2);
  oGrid(f).friction=iGrid(f).friction;
  oGrid(f).c       =iGrid(f).c;
  oGrid(f).parent  =iGrid(f).parent;
  if(iGrid(f).children~=-1)
    oGrid(f).children =iGrid(f).children;
  else
    oGrid(f).children =[];
  end
  
  p =oGrid(f).parent;
  rx=oGrid(f).ratio_x;
  ry=oGrid(f).ratio_y;
    
  if(p==0)
    %Geometrical dimensions of the grid cell
    oGrid(f).dlon=iGrid(f).dlon;
    oGrid(f).dlat=iGrid(f).dlat;
    %Lower left corner of the grid
    oGrid(f).lon0=iGrid(f).long(1,1);
    oGrid(f).lat0=iGrid(f).latg(1,1);
    %Strip south & west
    oGrid(f).s.west=0;
    oGrid(f).s.south=0;
    %Number of cells in lateral and vertical directions
    oGrid(f).nlon=iGrid(f).nlon;
    oGrid(f).nlat=iGrid(f).nlat;
    %Setting up the bathymetry
    oGrid(f).depg=iGrid(f).depg;
    
    for i=1:oGrid(f).nlon
      oGrid(f).depg(1:2,i)=oGrid(f).depg(3,i);
      oGrid(f).depg(oGrid(f).nlat-2:oGrid(f).nlat,i)=oGrid(f).depg(oGrid(f).nlat-2,i);
    end
    for i=1:oGrid(f).nlat
      oGrid(f).depg(i,1:2)=oGrid(f).depg(i,3);
      oGrid(f).depg(i,oGrid(f).nlon-2:oGrid(f).nlon)=oGrid(f).depg(i,oGrid(f).nlon-2);
    end
  else
    %Geometrical dimensions of the grid cell    
    oGrid(f).dlon=oGrid(p).dlon/rx;
    oGrid(f).dlat=oGrid(p).dlat/ry;
    
    dx=oGrid(f).dlon;
    dy=oGrid(f).dlat;
    %Lower left corner of the grid
    oGrid(f).lon0=oGrid(p).loni(oGrid(f).c.west -oGrid(p).s.west )+(rx-3)/2*dx;
    oGrid(f).lat0=oGrid(p).lati(oGrid(f).c.south-oGrid(p).s.south)+(ry-3)/2*dy;
    %Strip south & west
    oGrid(f).s.west=rx-2;
    oGrid(f).s.south=ry-2;
    %Number of cells in lateral and vertical directions
    
    dlon=floor((iGrid(f).nlon-1/2-rx)/rx)*rx+3;
    dlat=floor((iGrid(f).nlat-1/2-ry)/ry)*ry+3;
%     lon1=oGrid(p).loni(oGrid(f).c.west) -(rx-1)/2*dx + (iGrid(f).nlon-1)*dx;
%     lat1=oGrid(p).lati(oGrid(f).c.south)-(ry-1)/2*dy + (iGrid(f).nlat-1)*dy;
%     dlon=floor((lon1-(oGrid(f).lon0+dx*3/2))/(rx*dx))*rx+3;
%     dlat=floor((lat1-(oGrid(f).lat0+dy*3/2))/(ry*dy))*ry+3;
    
    oGrid(f).nlon=dlon;   %Two ghost points on the left + 1 on the right 
    oGrid(f).nlat=dlat;   %Two ghost points on the left + 1 
    %Setting up the bathymetry
    oGrid(f).depg=iGrid(f).depg(ry-1:ry-2+oGrid(f).nlat,rx-1:rx-2+oGrid(f).nlon);
  end
  
  %Auxilarily variables
  %Upper Right corner of the grid
  oGrid(f).lon1=oGrid(f).lon0+oGrid(f).dlon*(oGrid(f).nlon-1);
  oGrid(f).lat1=oGrid(f).lat0+oGrid(f).dlat*(oGrid(f).nlat-1);
  %Creating a visualization/interpolation mesh
  oGrid(f).loni=linspace(oGrid(f).lon0,oGrid(f).lon1,oGrid(f).nlon);
  oGrid(f).lati=linspace(oGrid(f).lat0,oGrid(f).lat1,oGrid(f).nlat);
  [oGrid(f).long oGrid(f).latg]=meshgrid(oGrid(f).loni,oGrid(f).lati);
  oGrid(f).mean_lat=mean(oGrid(f).lati);
  oGrid(f).mean_lon=mean(oGrid(f).loni);
end



% 
% figure(1)
% for i=dlist
%   xline=[oGrid(i).lon0 oGrid(i).lon0 oGrid(i).lon1 oGrid(i).lon1 oGrid(i).lon0];
%   yline=[oGrid(i).lat0 oGrid(i).lat1 oGrid(i).lat1 oGrid(i).lat0 oGrid(i).lat0];
%   plot(xline,yline, strcat(oGrid(i).color,'*-'))
%   if(i==1)
%     hold on
%   end
%   plot(oGrid(i).long,oGrid(i).latg,strcat('.',oGrid(i).color));
% end
% hold off

disp(' ');
strDefor=['Accessing deformation file ', iGrid(1).deformation_file];
find_xyz = strfind(iGrid(1).deformation_file, '.xyz');
find_mrx = strfind(iGrid(1).deformation_file, '.mrx');
flag=0;
if(isempty(find_xyz)~=1)
    flag=1;
    try
        [Dlong, Dlatg, Ddefg, Ddlon, Ddlat]=loadXYZ(iGrid(1).deformation_file);
        if(strcmp(iGrid(1).deformation_units,'cm'))
            Ddefg=Ddefg/100;
        end
        strDefor=[strDefor, ' - Yes'];
    catch
        strDefor=[strDefor, ' - No'];
    end
end
if(isempty(find_mrx)~=1)
    flag=1;
    try
        Ddefg=load(iGrid(1).deformation_file);
        Dlong=iGrid(1).original.long;
        Dlatg=iGrid(1).original.latg;
        if(strcmp(iGrid(1).deformation_units,'cm'))
            Ddefg=Ddefg/100;
        end
        strDefor=[strDefor, ' - Yes'];
    catch
        strDefor=[strDefor, ' - No'];
    end
end

if(flag==0)
  disp(strDefor);
  return
else
  disp(strDefor);
end

for i=dlist
  oGrid(i).defg=interp2(Dlong,Dlatg,Ddefg,oGrid(i).long,oGrid(i).latg);
  index=isnan(oGrid(i).defg);
  oGrid(i).defg(index)=0;
end

%Get a friction coefficient from the first grid and use it every where
friction=iGrid(1).friction;
disp(['Bottom friction ', num2str(friction),'.']);

%Update a sea level
SeaLevel=iGrid(1).level;
disp(['Global sea level is shifted by ', num2str(SeaLevel),' meters.']);

Bathymetry_type=iGrid(1).bath_prepost;
if( Bathymetry_type == 0 )
   disp(['Post-earthquake bathymetry.']);
else
   disp(['Pre-earthquake bathymetry.']);
end

filename=[path_save, 'gBath_topology'];
fid = fopen(filename,'wb');
fprintf(fid,'%s\n',strcat(['<Root ', oGrid(1).name,'>' ]));
tree_print(1,fid);
fprintf(fid,'%s\n',strcat(['</Root ', oGrid(1).name,'>' ]));
fclose(fid);


for i=ilist
  %%%Save Grid Geometry
  filename=strcat([path_save, 'gBath_',oGrid(i).name]);
  fid = fopen(strcat(filename,'.bin'),'wb');
  fwrite(fid,[oGrid(i).lon0, oGrid(i).lat0, oGrid(i).dlon, oGrid(i).dlat]/180*pi,'double');  %Save in radians
  fwrite(fid,[oGrid(i).nlon, oGrid(i).nlat, oGrid(i).ratio_x, oGrid(i).ratio_y],'double');
  fwrite(fid,[friction, 0.0, 0.0, 0.0],'double');
  
  chunk=zeros(oGrid(i).nlat,4);
  adjdep=zeros(oGrid(i).nlat,1);
  
  chunki=1:oGrid(i).nlat;
    
  for ii=1:oGrid(i).nlon
    adjdep=SeaLevel-oGrid(i).depg(chunki,ii)-Bathymetry_type*oGrid(i).defg(chunki,ii);
      
    if(strcmp(oGrid(i).type,'propagation')==1)
      adjdep(adjdep<0)=-100;
      %HERE
      %%adjdep((adjdep>=0)&(adjdep<10))=10;
    end
        
    chunk(:,1)=adjdep;
    chunk(:,2)=oGrid(i).defg(chunki,ii);
    fwrite(fid, chunk', 'double');
    %for jj=1:oGrid(i).nlat
    %  newBath=SeaLevel-oGrid(i).depg(jj,ii)-Bathymetry_type*oGrid(i).defg(jj,ii);
    %  fwrite(fid,[newBath, oGrid(i).defg(jj,ii), 0, 0],'double');
    %end
  end
  fclose(fid);
end

save([path_save, 'animate_oGrid'],'oGrid');

