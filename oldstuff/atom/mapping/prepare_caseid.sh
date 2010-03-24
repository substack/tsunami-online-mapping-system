#!/bin/bash --login 

. /usr/share/modules/init/bash 
module load matlab
. /u1/uaf/nicolsky/.profile 


model_dir=/wrkdir/nicolsky/bench
cur_dir=/wrkdir/nicolsky/mapping
pre_dir=$cur_dir/pre-processing

cd ${cur_dir} 

matlab_execution=1
matlab_skip=1

if [ "$1" == "" ]; then
  echo Type Case ID; 
  read id
  str_ID=$(printf "%6.6d" $id)
  CaseID=CASE_${str_ID}
  
  echo Execute a Matlab script [yes/no]?; 
  read yesno
  if [ "${yesno}" == "yes" ]; then
     matlab_execution=1
  else
     matlab_execution=0
    
     echo Just skip it [yes/no]?; 
     read yesno
     if [ "${yesno}" == "yes" ]; then
        matlab_skip=1
     else
        matlab_skip=0
     fi
  fi
else
  CaseID=$1
fi

echo ' '
echo 'Accessing burn.giseis.alaska.edu'
echo 'Copying files: '
mkdir -p ${pre_dir}/${CaseID}/tmp
scp -r burn.giseis.alaska.edu:/export/burn/nicolsky/mapping/${CaseID}/* ${pre_dir}/${CaseID}


name=$(grep Name               $pre_dir/${CaseID}/readme.txt | sed 's/=//' | awk '{print $2}')
deformation=$(grep Deformation $pre_dir/${CaseID}/readme.txt | sed 's/=//' | awk '{print $2}')
cputime=$(grep CPU             $pre_dir/${CaseID}/readme.txt | sed 's/=//' | awk '{print $2}')
nodes=$(grep Nodes             $pre_dir/${CaseID}/readme.txt | sed 's/=//' | awk '{print $2}')
nodetype=$(grep NodeType       $pre_dir/${CaseID}/readme.txt | sed 's/=//' | awk '{print $2}')
queuetype=$(grep QueueType     $pre_dir/${CaseID}/readme.txt | sed 's/=//' | awk '{print $2}')

echo '------------------------------------------------------------'
echo '------------------------------------------------------------'
echo '    Calculating scenario "'$name'". Deformation "'$deformation'"'
echo '------------------------------------------------------------'
echo '------------------------------------------------------------'


cd $pre_dir

echo "CaseID='"${CaseID}"';" > ${CaseID}.m
cat prepare_caseid.m      >> ${CaseID}.m

if [ "${matlab_execution}" -eq "1" ]; then
  matlab -nosplash -nodisplay < ${CaseID}.m 
fi
if [ "${matlab_skip}" -eq "0" ]; then
   exit
fi
##> /dev/null
cd $cur_dir



DESTINATION=$cur_dir/${CaseID}

mkdir -p $DESTINATION


cp    ${pre_dir}/${CaseID}/tmp/gBath*            $DESTINATION


cp    ${model_dir}/tmp                           $DESTINATION
cp    ${model_dir}/pp.sh                         $DESTINATION
cp    ${model_dir}/run.sh                        $DESTINATION
cp    ${model_dir}/cleanup.sh                    $DESTINATION
cp -r ${model_dir}/temporarily                   $DESTINATION
cp -r ${model_dir}/post_processing               $DESTINATION
cp -r ${model_dir}/iNetCDF                       $DESTINATION

cp -r ${model_dir}/preview                       $DESTINATION
cp    ${pre_dir}/${CaseID}/tmp/*.preview         $DESTINATION/preview  2>/dev/null

cp    ${pre_dir}/${CaseID}/list_points.tmp       $DESTINATION
cp    ${pre_dir}/${CaseID}/restart.tmp           $DESTINATION
cp    ${pre_dir}/${CaseID}/readme.txt            $DESTINATION
cp    ${pre_dir}/${CaseID}/readme.html           $DESTINATION


mkdir -p $DESTINATION/minit
cp -r ${pre_dir}/${CaseID}/*                     $DESTINATION/minit
cp    ${pre_dir}/${CaseID}/tmp/animate_oGrid.mat $DESTINATION/minit

echo 'Cleaning up and creating a PBS script'




./prepare_pbs.sh $DESTINATION ${CaseID} $cputime $nodes $nodetype $queuetype

#rm -rf ${pre_dir}/${CaseID}


exit
 
