#include <netcdf.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//cc gg.c -o ll2data -L/export/burn/nicolsky/local/lib -lnetcdf -I/export/burn/nicolsky/local/include/ -lm

int bSearch(float L[], int size, float value)
{
  int high, low, mid; //mid will be the index of
  int found = 0;      //target when it’s found.

  low = 0;
  high = size-1;

  while ((low <= high) && !found) {
    mid = (high + low)/2;
    if (L[mid] == value){
      found = 1;
      return mid;
    }
    else if (value < L[mid])
      high = mid- 1;// reduce to the low// half of the array
    else
      low = mid + 1; //reduce to the top //of the array
  }
  return low-1;
}


float values[] = { 10, 20, 25, 40, 90, 100 };

int ddmain ()
{
  int pItem;
  int key = 21;
  for (int i=0;i<110;i++){
     pItem = bSearch (values,  6, i);
     printf ("%i  --- %d is in the array.\n",i,pItem);
  }
  return 0;
}



FILE *f;
int main(int argc, char *argv[])
{
  int ctr;
  int ncid;                                /* netCDF ID */
  int var_id, t_id, h_id;               /* variable ID */
  static long var_index[] = {0, 100, 100};  /* where to get value from */
  
  long start[] = {0}; /* start at first value */

  float *x, *y;
  float xq, yq;
  long xsize[] = {0}, ysize[]={0};

  float var_val,t_val,h_val; 


  //if ( argc != 6 ){
  //  printf( "usage: %s filename", argv[0] );
  //}
  //else 
  //{
    ncid = ncopen(argv[1], NC_NOWRITE);

    var_id = ncvarid (ncid, argv[2]);
    t_id   = ncvarid (ncid, "time");
    h_id   = ncvarid (ncid, "H");

    xq=atof(argv[3]);
    yq=atof(argv[4]);

    //printf("%f\n",xq);
    //printf("%f\n",yq);

    int xid = ncdimid(ncid, "x");
    int yid = ncdimid(ncid, "y");

    ncdiminq(ncid, xid, 0, xsize);
    ncdiminq(ncid, yid, 0, ysize);

    //printf("%dx%d\n",*xsize,*ysize);

    int xval_id = ncvarid (ncid, "x");
    int yval_id = ncvarid (ncid, "y");
    x = (float *) malloc((*xsize)*sizeof(float));
    y = (float *) malloc((*ysize)*sizeof(float));

    ncvarget(ncid, xval_id, start, xsize, x);
    ncvarget(ncid, yval_id, start, ysize, y);

    for(int i=0;i<(*xsize);i++)
       x[i]=x[i]/3.141592*180.0;
    for(int i=0;i<(*ysize);i++)
       y[i]=y[i]/3.141592*180.0;

    //for(int i=0;i<(*xsize);i+=200)
    //   printf("x[%d]=%f\n",i,x[i]);
    //for(int i=0;i<(*ysize);i+=200)
    //   printf("y[%d]=%f\n",i,y[i]);


    int pxItem = bSearch (x, *xsize, xq);
    if(pxItem<0)         pxItem=0;
    if(pxItem>(*xsize))  pxItem=(*xsize);

    int pyItem = bSearch (y, *ysize, yq);
    if(pyItem<0)         pyItem=0;
    if(pyItem>(*ysize))  pyItem=(*ysize);

    var_index[1]=pyItem;
    var_index[2]=pxItem;

    //printf("x[%d]=%f   %f x[%d]=%f\n",pxItem,x[pxItem],xq,pxItem+1,x[pxItem+1]);
    //printf("y[%d]=%f   %f y[%d]=%f\n",pyItem,y[pyItem],yq,pyItem+1,y[pyItem+1]);
    //printf("%d %d\n",pxItem,pyItem);

    ncvarget1(ncid, var_id, var_index, &var_val);
    ncvarget1(ncid, h_id,   var_index, &h_val);
    nc_get_var_float (ncid, t_id, &t_val);
    nc_close(ncid);

    f = fopen(argv[5], "at");
    fprintf(f,"%f %f %f\n",t_val,var_val,h_val);
    fclose (f); 	
  //}
return 0;
}

