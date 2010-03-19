function depgc_mm=Smoothen_grid_boundaries(longc, latgc, depgc, depgf, cvector, ratio, stol, niterations, Verbose)

%Verbose=0;      %Verbose
%niterations=200; %Number of smoothing operations


ilo=cvector.south;  iup=cvector.north;
jlo=cvector.west;   jup=cvector.east;

rx=ratio(1);     ry=ratio(2);
drx=floor(rx/2); dry=floor(ry/2);

%Create a temporary coarse grid
depgc_m=depgc;
% Over an area of the coarse grid that is coinside with the domain of the
% fine grid, we perform the following averaging. 
%
%    Fine       Coarse 
%  -------     -------  
%  |1|n|n|     |     |
%  -------     |     |   \sum_{not NaN elements in the fine} Bath_f~Bath_c
%  |4|n|6|====>|     |
%  -------     |     |
%  |7|8|9|     |     |
%  -------     -------
%
% Note that we do not generate new wet points in the coarse grid, since we
% can occasionally make wet points at the boundary of two grids. This new
% points at the boundary can lead to potential problems to exchange fluxes
%

for i_coarse=ilo:iup
  for j_coarse=jlo:jup
    
    if(~isnan(depgc(i_coarse,j_coarse)))
      i_fine=ry*(i_coarse-ilo);
      is=i_fine+1;
      ie=i_fine+ry;

      j_fine=rx*(j_coarse-jlo);
      js=j_fine+1;
      je=j_fine+rx;



      p=depgf(is:ie,js:je);
      index=~isnan(p);
      v=sum(p(index));
      w=sum(sum(index));
    
      if(w>0)
        depgc_m(i_coarse,j_coarse)=v/w;
      else
        depgc_m(i_coarse,j_coarse)=NaN;
      end
    end
  end
end

%After averaging updated grid cell can have bathymetry different from its
%orginal version. Hence, a jump in bathymetry can occur at the interface of
%two grids. We smooth bathymetry only within the coarse grid and only within 
% ${stol} band around the interface, by applying a 'cross' interative
% filter.
depgc_mm=depgc_m;
for i=1:niterations
  for i_coarse=ilo-stol:iup+stol
    for j_coarse=jlo-stol:jup+stol
      if((ilo<=i_coarse)&&(i_coarse<=iup)&&(jlo<=j_coarse)&&(j_coarse<=jup))
        depgc_mm(i_coarse,j_coarse)=depgc_m(i_coarse,j_coarse);
      else
        s=0;
        weight=0;
        val=depgc_mm(i_coarse,j_coarse);
        if(~isnan(val))
          s=s+val;
          weight=weight+1;
        end
        val=depgc_mm(i_coarse+1,j_coarse);
        if(~isnan(val))
          s=s+val;
          weight=weight+1;
        end
        val=depgc_mm(i_coarse-1,j_coarse);
        if(~isnan(val))
          s=s+val;
          weight=weight+1;
        end
        val=depgc_mm(i_coarse,j_coarse+1);
        if(~isnan(val))
          s=s+val;
          weight=weight+1;
        end
        val=depgc_mm(i_coarse,j_coarse-1);
        if(~isnan(val))
          s=s+val;
          weight=weight+1;
        end
        if((weight>0)&&(~isnan(depgc_mm(i_coarse,j_coarse))))
          depgc_mm(i_coarse,j_coarse)=s/weight;
        else
          depgc_mm(i_coarse,j_coarse)=NaN;
        end
      end
    end
  end
end


if(Verbose>0)
  %Display the result
  tol=0;
  lon0=longc(ilo-tol,jlo-tol);  lat0=latgc(ilo-tol,jlo-tol);
  lon1=longc(iup+tol,jup+tol);  lat1=latgc(iup+tol,jup+tol);
  line0x=[lon0 lon0 lon1 lon1 lon0];
  line0y=[lat0 lat1 lat1 lat0 lat0];
  
  tol=stol;
  lon0=longc(ilo-tol,jlo-tol);  lat0=latgc(ilo-tol,jlo-tol);
  lon1=longc(iup+tol,jup+tol);  lat1=latgc(iup+tol,jup+tol);
  line1x=[lon0 lon0 lon1 lon1 lon0];
  line1y=[lat0 lat1 lat1 lat0 lat0];
  
  tol=floor(stol*1.5);
  nlon=length(depgc(1,:));
  nlat=length(depgc(:,1));
  imin=max(ilo-tol,1); imax=min(iup+tol,nlat);
  jmin=max(jlo-tol,1); jmax=min(jup+tol,nlon);
  
  depgc_mm_tmp=depgc_mm(imin:imax,jmin:jmax);
  longcmm_tmp=longc(imin:imax,jmin:jmax);
  latgcmm_tmp=latgc(imin:imax,jmin:jmax);
  
  maxd=max(max(depgc_mm_tmp));
  mind=min(min(depgc_mm_tmp));
  
  figure(Verbose+1000)
  contourf(longcmm_tmp,latgcmm_tmp,depgc_mm_tmp,linspace(mind,maxd,25))
  hold on
  index=isnan(depgc_mm_tmp);
  plot(longcmm_tmp(index),latgcmm_tmp(index),'g.')
  plot(line0x,line0y,'-y','LineWidth',1)
  plot(line1x,line1y,'-y','LineWidth',1)
  hold off
  dx=(lon1-lon0)/100*2;
  dy=(lat1-lat0)/100*2;
  axis([lon0-dx  lon1+dx lat0-dy  lat1+dy])
  title('Nans are green points')
end

