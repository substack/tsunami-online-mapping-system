#include <netcdf.h>
#include <stdio.h>
#include <stdlib.h>

FILE *f;
int main(int argc, char *argv[])
{
  int ctr;
  int ncid;                                /* netCDF ID */
  int var_id, t_id, h_id;               /* variable ID */
  static long var_index[] = {0, 100, 100};  /* where to get value from */
  


  float var_val,t_val,h_val; 


  if ( argc != 6 ){
    printf( "usage: %s filename", argv[0] );
  }
  else 
  {
    ncid = ncopen(argv[1], NC_NOWRITE);

    var_id = ncvarid (ncid, argv[2]);
    t_id   = ncvarid (ncid, "time");
    h_id   = ncvarid (ncid, "H");

    var_index[1]=atoi(argv[3]);
    var_index[2]=atoi(argv[4]);

    ncvarget1(ncid, var_id, var_index, &var_val);
    ncvarget1(ncid, h_id,   var_index, &h_val);
    nc_get_var_float (ncid, t_id, &t_val);
    nc_close(ncid);

    f = fopen(argv[5], "at");
    fprintf(f,"%f %f %f\n",t_val,var_val,h_val);
    fclose (f); 	
  }
return 0;
}

