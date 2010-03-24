
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"  
;************************************************

setvalues NhlGetWorkspaceObjectId()
     "wsMaximumSize": 43554432
end setvalues

begin


    files=systemfunc("ls *.make_ps")
    nfiles=dimsizes(files)
  
    do i = 0, nfiles-1
      fi = stringtochar(files(i))
      nfi = dimsizes(fi)-2;
      fo=chartostring(fi(0:nfi-8))
      

        a = addfile(fo+".nc","r")
        dd=dimsizes(a->Z(0,:,:))
        

        varDZ = a->DZ(0, 2:dd(0)-2, 2:dd(1)-2)
        var   =  a->Z(0, 2:dd(0)-2, 2:dd(1)-2)  

        var@_FillValue = 100

        if (any(isnan_ieee(var))) then
          var(:,:)=100.0
        end if

        var = where(varDZ.gt.0.01, var, 100.0)

        if ((max(var)-min(var)).le.1e-5) then
          var = generate_2d_array(20,20,1,2,0,dimsizes(var))*1e-5
          var = where(varDZ.gt.0.01, var, 100.0)
        end if

        print("i="+i+" "+fo)
        


        t = a->time
  
        pi=3.1415927  
        lon=(a->x(2:dd(1)-2))*180/pi
        lat=(a->y(2:dd(0)-2))*180/pi

  
  
;************************************************
; create plot
;************************************************
        wks = gsn_open_wks("ps",fo)              ; open a ps file
        gsn_define_colormap(wks,"BlWhRe")

        colors = gsn_retrieve_colormap(wks)     ; retrieve color map for editing. dimensioned (103,3)
        colors(101,:) = (/ .5, .5, .5 /)     ; replace the last color with a medium gray
        colors(102,:) = (/ .5, .5, .5 /)     ; replace the last color with a medium gray
        gsn_define_colormap(wks,colors)
          

        res                       = True               ; plot mods desired
        res@cnFillOn              = True               ; turn on color fill
        res@cnFillMode            = "RasterFill"       ; raster mode (req for mem)
        res@gsnSpreadColors       = True               ; use full range of colors
        res@cnLinesOn             = False
        
 
        ;res@gsnSpreadColors   = True
        res@gsnSpreadColorStart   =  2  
        res@gsnSpreadColorEnd     =  100
        res@cnMissingValFillColor =  102        ; color missing values

 

        res@sfYArray              = lat               ; use eta for y axis
        res@sfXArray              = lon               ; use lat for x axis
        res@tiXAxisString         = "Longitude (deg)"       ; X axis label.
        res@tiXAxisFontHeightF = 0.017
        res@tiYAxisString         = "Latitude (deg)"        ; Y axis label.
        res@tiYAxisFontHeightF = 0.017
  
        ;res@tiMainString         = "Sea level, m"             ; main title

        res@gsnLeftString   = "Sea Level, m"               ; add the gsn titles
        res@gsnCenterString = ""
        res@gsnRightString  = "Time, "+t+" s"

 
 
        res@tmXBLabelFont = 25           ; Change font of labels.
        res@tmXBLabelFontHeightF = 0.015 ; Change font height of labels.
        res@tmYLLabelFont = 25           ; Change font of labels.
        res@tmYLLabelFontHeightF = 0.015 ; Change font height of labels.

 
  
        ;res@cnLevelSelectionMode = "ManualLevels"     ; set manual contour levels
        ;res@cnMinLevelValF       =  -3.5              ; set min contour level
        ;res@cnMaxLevelValF       =   3.5              ; set max contour level
        ;res@cnLevelSpacingF      =   0.5              ; set contour spacing

        res@cnLevelSelectionMode  = "ExplicitLevels"   ; set explicit contour levels
        levels = new(15,float)
        do ii = 0,14
          levels(ii) = -3.5+ii*0.5
        end do
        res@cnLevels              = levels; 
        
        
 
        res@cnInfoLabelOn = False                     ; turn off contour info label
        res@lbLabelBarOn= False


        res@lbAutoManage          = False             ; we control label bar
        res@pmLabelBarDisplayMode = "Always"          ; turns on label bar
        res@lbOrientation         = "Vertical"        ; ncl default is vertical
        res@pmLabelBarSide        = "Right"           ; default is right
        res@lbLabelStride         = 2                 ; skip every other label
        res@pmLabelBarWidthF      = 0.1               ; default is shorter
        res@pmLabelBarHeightF     = 0.6               ; default is taller
        res@lbLabelFontHeightF    = .018              ; default is HUGE
        res@lbPerimOn             = False             ; default has box

      
        plot = gsn_csm_contour(wks, var, res)     ; create plot


    if(isdefined("var").eq."True") then
      delete(var)
      delete(varDZ)
      delete(lon)
      delete(lat)
      delete(res)
      ;delete(levels)
    end if
  end do
  
end
