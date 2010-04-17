
name=$1
echo ${name} > casename
#echo Preparing $name deformation. Please wait.


echo "casename='${name}';" >  prepare_grids.m
cat prepare_def_grids.m >> prepare_grids.m

octave prepare_grids.m
./a.out

echo "clear all;" >  joint_grids.m
echo "casename='${name}';" >>  joint_grids.m
cat joint_def_grids.m >> joint_grids.m


flag=0
while [ "${flag}" -eq "0" ]; do
   #Check Matlab licenses
   str=$(lmstat -f Matlab | grep "Users of Matlab: " | sed 's/[a-zA-Z:;()]//g')
   issued=$(echo $str | awk '{print $1}')
   used=$(echo   $str | awk '{print $2}')
   if [ "${issued}" -ne "${used}" ]; then
      matlab -nosplash -nodisplay < joint_grids.m
      flag=1 
   else
      sleep 5
   fi
done

rm -f ${name}.def*
rm -f ${name}.lat*
rm -f ${name}.lon*

mv $name.xyz ..
