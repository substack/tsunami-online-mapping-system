
cd temporarily
echo Post processing ...
./post.sh
cd ..


cd post_processing
iis=0  
files=$(ls nc_*.nc)
for f in ${files}; do
   f=${f%.nc}
   if [ ! -f ${f}.ps ]; then
      touch ${f}.make_ps
      iis=1
   fi
done

if [ "${iis}" -eq "1" ]; then
   ncl nc2eps.ncl
   rm -f *.make_ps
fi 
cd ..

rm -f post-processing.busy
