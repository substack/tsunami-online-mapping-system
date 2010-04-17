%clear all
%casename='test';

Data=load([casename,'.param']);
for iline=1:size(Data,1)
    Lon=Data(iline,1);
    Lat=Data(iline,2);

    if(Lon<0)
        Lon=360+Lon;
    end


    Length=Data(iline,8);
    Width=Data(iline,9);

    LengthDeg=Length/111000;
    WidthDeg=Width/111000;

    strike=Data(iline,4)/180*pi;

    M=[cos(strike) sin(strike);...
       sin(strike) -cos(strike)];

    L=[LengthDeg 0]';
    W=[0 WidthDeg]';

    F(:,1)=0*L;
    F(:,2)=M*L;
    F(:,3)=M*(L+W);
    F(:,4)=M*W;

    iL=6;
    iW=8;

    BBF(:,1)=M*( -(iL)*L    -iW*W);
    BBF(:,2)=M*((iL+1)*L    -iW*W);
    BBF(:,3)=M*((iL+1)*L+(iW+1)*W);
    BBF(:,4)=M*(-(iL)*L   +(iW+1)*W);

    minLon=min(BBF(1,:));
    maxLon=max(BBF(1,:));
    minLat=min(BBF(2,:));
    maxLat=max(BBF(2,:));

    dL=min(LengthDeg,WidthDeg)/50;

    tmp=-[dL:dL:-minLon];
    index=length(tmp):-1:1;
    LonGrid=[tmp(index) 0:dL:maxLon];
    CLon=length(tmp)+1;

    tmp=-[dL:dL:-minLat];
    index=length(tmp):-1:1;
    LatGrid=[tmp(index) 0:dL:maxLat];
    CLat=length(tmp)+1;

    fname=[casename,'.lon',num2str(iline,'%03d')];
    fid = fopen(fname, 'w');
    fprintf(fid, '%5d %10d\n', length(LonGrid), CLon);
    for i=1:length(LonGrid)
        fprintf(fid, '%5d %10.05f\n', i, LonGrid(i)+Lon);
    end
    fclose(fid);

    fname=[casename,'.lat',num2str(iline,'%03d')];
    fid = fopen(fname, 'w');
    fprintf(fid, '%5d %10d\n', length(LatGrid), CLat);
    for i=1:length(LatGrid)
        fprintf(fid, '%5d %10.05f\n', i, LatGrid(i)+Lat);
    end
    fclose(fid);

end
% 
% [Xg,Yg] = meshgrid(LonGrid, LatGrid);
% 
% plot([F(1,:) 0],[F(2,:) 0]);
% hold on
% plot([BBF(1,:) 0],[BBF(2,:) 0],'-r');
% plot(Xg,Yg,'g.')
% hold off
% 
