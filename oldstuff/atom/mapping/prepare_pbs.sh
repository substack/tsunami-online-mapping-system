#echo 'Number of nodes (1,2,3,...?)'
#read npr
#echo 'Type of nodes (4,16) way?'
#read wyn
#echo 'Walltime in hours (1,2,3,...)'
#read wlt
#echo 'Queue type (standard, debug, ...)?'
#read qtp

if [ "$6" == "standard" ]; then
  npr=$4
  wyn=$5
  wlt=$3
  qtp=standard
fi

if [ "$6" == "background" ]; then
  npr=$4
  wyn=$5
  wlt=$3
  qtp=background
fi

if [ "$6" == "debug" ]; then
  npr=$4
  wyn=$5
  wlt=1
  qtp=debug
fi


cat > $2.pbs <<EOF
#PBS -q $qtp
#PBS -l select=${npr}:ncpus=${wyn}:node_type=${wyn}way
#PBS -l walltime=${wlt}:00:00
#PBS -j oe

cd $1
./run.sh $(($npr*$wyn))
EOF


