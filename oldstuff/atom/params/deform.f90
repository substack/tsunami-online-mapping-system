           PROGRAM OkadaDeformation
	   implicit none

!     I0 - x-coordinate of the reference point of the fault
!c           (the easternmost corner)
!c     J0 - y-coordinate of the reference point of the fault
!c     depth - Depth, m
!c     tlength - Length, m
!c     width - Width, m
!c     strike - Strike, degrees from North
!c     dip - Dip, degrees
!c     rake - Rake, degrees
!c     slip - Slip, meters


!c----------------------------------------------------------


      real,allocatable::SLS(:,:)
      integer I0,J0

      real,allocatable::DX(:),xlon(:),ylat(:),fault_lon(:)
      real,allocatable::fault_lat(:)

      real,allocatable::depth(:),tlength(:),width(:)
      real,allocatable::strike(:),dip(:),rake(:),slip(:)


      real DY
      integer if,jf,i,j,mi,mj,flag,nlines,iline,dummy
      Character*100 Str, Str2, casename


      real re,g,pi,rad

      real fif2,tcosf2,startlat, startlatf2
      real delxf2,delyf2,delhf2,tsinf2,gridf2


!c---Constants:

	re=6370.e05         !radius of Earth in cm
 	g=981.              !gravity in cm

	pi=4.*atan(1.)
	rad=pi/180.         !number of radians in one degree


!c----filse with fault parameters and grid coordinates--------

       open(unit=100,file='casename',status='old')
       read(100,*) casename
       casename=adjustl(casename)
       casename=trim(casename)
       close(100)


       nlines=0
       write(str,*) trim(casename)//'.param'
       str=adjustl(str)
       open(unit=10,file=trim(str),status='old')



       flag=0
       do while (flag.ge.0)
          read(10,*,IOSTAT=Flag) dy
          nlines=nlines+1
       end do
       close(10)
       nlines=nlines-1



      open(unit=10,file=trim(str),status='old')
      print *,nlines
      allocate(fault_lon(nlines),fault_lat(nlines),depth(nlines),strike(nlines),dip(nlines),  &
                 rake(nlines),slip(nlines),tlength(nlines),width(nlines))

      do iline=1,nlines       


        read(10,*)fault_lon(iline),fault_lat(iline),depth(iline),strike(iline),dip(iline),  &
                 rake(iline),slip(iline),tlength(iline),width(iline)

       write(str,'(I3.3)') iline     
       write(str2,*) trim(casename)//'.lon'//trim(str)
       str2=adjustl(str2)
       open(unit=11,file=trim(str2),status='old')
       read(11,*) mi,I0
       allocate(xlon(mi))
       do i=1,mi
           read(11,*) dummy,xlon(i)
       end do


       write(str,'(I3.3)') iline
       write(str2,*) trim(casename)//'.lat'//trim(str)
       str2=adjustl(str2)
       open(unit=12,file=trim(str2),status='old')
       read(12,*) mj,J0
       allocate(ylat(mj))
       do j=1,mj
           read(12,*) dummy,ylat(j)
       end do


       allocate(SLS(mi,mj),DX(mj))




	gridf2=(ylat(mj)-ylat(1))/dble(mj-1)         !grid interval in degrees
	delhf2=gridf2*rad                            !grid interval in radians

	delyf2=re*delhf2                             !space step in y direction (cm)

        startlat=ylat(1)                             !startlat for the big Pacific grid     
	startlatf2=startlat*rad   

!c-------------------------------------------------------------


	do j=1,mj
 	  fif2=startlatf2+delhf2*dble(j)    !changing latitude
	  tcosf2=cos(fif2)
	  tsinf2=sin(fif2)
	  delxf2=re*tcosf2*delhf2      !space step in x direction
	  DX(j)=delxf2*0.01            !space step in x-dir, meters
	end do

	DY=delyf2*0.01                 !space step along y in meters
             
       CALL DEFORM(mi,mj,I0,J0,depth(iline),tlength(iline),width(iline),strike(iline),dip(iline),rake(iline),slip(iline),DX,DY,SLS)
       
       write(str,'(I3.3)') iline
       write(str2,*) trim(casename)//'.def'//trim(str)
       str2=adjustl(str2)
       open(unit=13,file=trim(str2))

       do j=1,mj
          write(13,'(10000F10.5)') SLS(:,j)
       enddo
       close(13)
       deallocate(SLS,DX,xlon,ylat)


   enddo


       
        end


























































