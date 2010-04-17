C**************************************************************************
C *** CALCULATOIN FOR INITIAL TSUNAMI SOURCE ******
C         (= SEA BOTTOM DEFORMATION)
C
C            IMAMURA MODEL
C
C      (I0,J0): LOCATION OF FAULT IN THE COMPUTATIONAL REGION = (xia,yia)
C      RR; RADIUS OF EARTH

C      L ; FAULT LENGTH   = tlength
C      W ; FAULT WIDTH    = width
C      HH; DEPTH          = depth 
C      TH; DIP DIRECTION  = strike     
C      RD; SLIP ANGLE     = rake      
C      D ; DISLOCATION    = slip
C      DL; DIP ANGLE      = dip
c_________________________________________________________

        subroutine DEFORM(IF,JF,I0,J0,depth,tlength,width,
     *       strike,dip,rake,slip,DX,DY,SLS)

        PARAMETER(A=3.14159265,B=4.848E-06,RR=6.378E+6,E=1.745329252E-2)
        REAL L

          dimension DEF(IF,JF)
	  integer I0,J0
	  dimension SLS(IF,JF)

          dimension DX(JF)

          real depth,tlength,width
          real strike,dip,rake,slip


c----------------------------------------------------------

c        write(*,*)I0
c        write(*,*)J0


          HH=depth
          L=tlength
          W=width
          TH=strike
          DL=dip
          RD=rake
          D=slip

          isub=I0
          jsub=J0

	  write(*,*)I0,J0,HH,L,W,TH,DL,RD,D

!          XL=DX*(isub-1)    !for rectangular coordinates
!          YL=DY*(jsub-1)

          XL=DX(jsub)*(isub-1)    !for spherical coordinates
          YL=DY*(jsub-1)

          H1=HH/SIN(E*DL)
          H2=HH/SIN(E*DL)+W
          DS=-D*COS(E*RD)
          DD=D*SIN(E*RD)
c -  - - - - - - - - - - - - - 
          DO I=1,IF
          DO J=1,JF

!          XX=DX*(I-1)     !for rectangular coordinates
!          YY=DY*(J-1)

           XX=DX(jsub)*(I-1)  !for spherical coordinates
           YY=DY*(J-1)


          X1=(XX-XL)*SIN(E*TH)+(YY-YL)*COS(E*TH)-L/2.0
          X2=(XX-XL)*COS(E*TH)-(YY-YL)*SIN(E*TH)+HH/TAN(E*DL)
          X3=0.0

          CALL USCAL(X1,X2,X3,L/2.,H2,E*DL,F1)
          CALL USCAL(X1,X2,X3,L/2.,H1,E*DL,F2)

          CALL USCAL(X1,X2,X3,-L/2.,H2,E*DL,F3)
          CALL USCAL(X1,X2,X3,-L/2.,H1,E*DL,F4)
          CALL UDCAL(X1,X2,X3,L/2.,H2,E*DL,G1)
          CALL UDCAL(X1,X2,X3,L/2.,H1,E*DL,G2)
          CALL UDCAL(X1,X2,X3,-L/2.,H2,E*DL,G3)
          CALL UDCAL(X1,X2,X3,-L/2.,H1,E*DL,G4)

          US=(F1-F2-F3+F4)*DS/(12.0*A)
          UD=(G1-G2-G3+G4)*DD/(12.0*A)

          SLS(I,J)=US+UD

	end do
	end do

c----------------------------------------------------
          RETURN
          END
c******************************************************

      SUBROUTINE USCAL(X1,X2,X3,C,CC,DP,F)
      REAL K

      SN=SIN(DP)
      CS=COS(DP)
      C1=C
      C2=CC*CS
      C3=CC*SN
      R=SQRT((X1-C1)**2+(X2-C2)**2+(X3-C3)**2)
      Q=SQRT((X1-C1)**2+(X2-C2)**2+(X3+C3)**2)
      R2=X2*SN-X3*CS
      R3=X2*CS+X3*SN
      Q2=X2*SN+X3*CS
      Q3=-X2*CS+X3*SN
      H=SQRT(Q2**2+(Q3+CC)**2)
      K=SQRT((X1-C1)**2+Q2**2)
      A1=LOG(R+R3-CC)
      A2=LOG(Q+Q3+CC)
      A3=LOG(Q+X3+C3)
      B1=1+3.0*(TAN(DP))**2
      B2=3.0*TAN(DP)/CS
      B3=2.0*R2*SN
      B4=Q2+X2*SN
      B5=2.0*R2**2*CS
      B6=R*(R+R3-CC)
      B7=4.0*Q2*X3*SN**2
      B8=2.0*(Q2+X2*SN)*(X3+Q3*SN)
      B9=Q*(Q+Q3+CC)
      B10=4.0*Q2*X3*SN
      B11=(X3+C3)-Q3*SN
      B12=4.0*Q2**2*Q3*X3*CS*SN
      B13=2.0*Q+Q3+CC
      B14=Q**3*(Q+Q3+CC)**2
      F=CS*(A1+B1*A2-B2*A3)+B3/R+2*SN*B4/Q-B5/B6+(B7-B8)/B9+B10*B11/
     &  Q**3-B12*B13/B14
      RETURN
      END
c******************************************************
      SUBROUTINE UDCAL(X1,X2,X3,C,CC,DP,F)
      REAL K

      SN=SIN(DP)
      CS=COS(DP)
      C1=C
      C2=CC*CS
      C3=CC*SN
      R=SQRT((X1-C1)**2+(X2-C2)**2+(X3-C3)**2)
      Q=SQRT((X1-C1)**2+(X2-C2)**2+(X3+C3)**2)
      R2=X2*SN-X3*CS
      R3=X2*CS+X3*SN
      Q2=X2*SN+X3*CS
      Q3=-X2*CS+X3*SN
      H=SQRT(Q2**2+(Q3+CC)**2)
      K=SQRT((X1-C1)**2+Q2**2)
      A1=LOG(R+X1-C1)
      A2=LOG(Q+X1-C1)
      B1=Q*(Q+X1-C1)
      B2=R*(R+X1-C1)
      B3=Q*(Q+Q3+CC)
      D1=X1-C1
	  D2=X2-C2
	  D3=X3-C3
	  D4=X3+C3
	  D5=R3-CC
	  D6=Q3+CC
      T1=ATN(D1*D2,(H+D4)*(Q+H))
      T2=ATN(D1*D5,R2*R)
      T3=ATN(D1*D6,Q2*Q)
      F=SN*(D2*(2*D3/B2+4*D3/B1-4*C3*X3*D4*(2*Q+D1)/(B1**2*Q))
     &  -6*T1+3*T2-6*T3)+CS*(A1-A2-2*(D3**2)/B2-4*(D4**2-C3*X3)/
     &  B1-4*C3*X3*D4**2*(2*Q+X1-C1)/(B1**2*Q))+6*X3*(CS*SN*(2*D6/B1+D1/
     &  B3)-Q2*(SN**2-CS**2)/B1)
      RETURN
      END
C*****************************************************
      REAL FUNCTION ATN(AX,AY)
      DATA GX/1.0E-6/
      AAX=ABS(AX)
	  AAY=ABS(AY)
      P=AX*AY
      IF(AAX.LE.GX.AND.AAY.LE.GX)GOTO 10
      SR=ATAN2(AAX,AAY)
      ATN=SIGN(SR,P)
      RETURN
   10 WRITE(6,100)AX,AY
  100 FORMAT(1H ,"ATAN --    AX=",E15.7,2X,"AY=",E15.7)
      ATN=0.2
      END




























































