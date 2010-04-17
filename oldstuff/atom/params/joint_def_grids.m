% clear all
% casename='test';

Data=load([casename,'.param']);

for iline=1:size(Data,1)
    
    fname=[casename,'.lon',num2str(iline,'%03d')];
    tmp=load(fname);
    grid(iline).lon=tmp(2:length(tmp),2);
    grid(iline).minlon=min(grid(iline).lon);
    grid(iline).maxlon=max(grid(iline).lon);

   
    fname=[casename,'.lat',num2str(iline,'%03d')];
    tmp=load(fname); 
    grid(iline).lat=tmp(2:length(tmp),2);
    grid(iline).minlat=min(grid(iline).lat);
    grid(iline).maxlat=max(grid(iline).lat);
    
    
    [grid(iline).glon  grid(iline).glat]=meshgrid(grid(iline).lon, grid(iline).lat);
    fname=[casename,'.def',num2str(iline,'%03d')];
    grid(iline).gdef=load(fname);
    
    grid(iline).gdef(isnan(grid(iline).gdef))=0;
    grid(iline).gdef(isinf(grid(iline).gdef))=0;
end

abslonmin=min([grid.minlon]);
abslonmax=max([grid.maxlon]);

abslatmin=min([grid.minlat]);
abslatmax=max([grid.maxlat]);


Lon=abslonmin:1/60:abslonmax;
Lat=abslatmin:1/60:abslatmax;

[GLon  GLat]=meshgrid(Lon, Lat);

DEF=0*GLon;
for iline=1:size(Data,1)
    partial_def = interp2(grid(iline).glon, grid(iline).glat, grid(iline).gdef, GLon, GLat);
    partial_def(isnan(partial_def))=0;
    DEF=DEF+partial_def;
    iline;
end
% DEF(abs(DEF)<0.1)=NaN;
% figure(10)
% contourf(GLon, GLat,  DEF, [-3:0.5:3])

fname=[casename,'.xyz'];
fid = fopen(fname, 'w');


chunk =zeros(length(Lon),3);
adjdep=zeros(length(Lon),1);
chunki=1:length(Lon);

for jj=1:size(GLon,1)
    chunk(:,1)=GLon(jj,chunki);
    chunk(:,2)=GLat(jj,chunki);
    chunk(:,3)=DEF(jj,chunki);
    fprintf(fid, '%9.5f %9.5f %8.3f\n', chunk');
%    for jj=1:size(GLon,2)
%        fprintf(fid, '%10.5f %10.5f %9.2f\n',GLon(ii,jj), GLat(ii,jj), DEF(ii,jj));
%    end
end
fclose(fid)
