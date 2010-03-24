
ID=$1 
#CASE_000038

cat << EOF > ${ID}.wpbs
#!/bin/bash --login

. /usr/share/modules/init/bash
module load ncl-5.1.0
. /u1/uaf/nicolsky/.profile

echo ${ID}_PID \$\$
str_start=\$(date)


cd /wrkdir/nicolsky/mapping
if [ -f ${ID}.resuming ]; then
   echo Resuming > ${ID}.status
else
   echo Pending > ${ID}.status
fi





if [ ! -f ${ID}.prepared ]; then
   flag=0
   while [ "\${flag}" -eq "0" ]; do
     #Check Matlab licenses
     str=\$(lmstat -f Matlab | grep "Users of Matlab: " | sed 's/[a-zA-Z:;()]//g')
     issued=\$(echo \$str | awk '{print \$1}')
     used=\$(echo   \$str | awk '{print \$2}')
     if [ "\${issued}" -eq "\${used}" ]; then
        echo ML-Error : No Matlab licenses are currently available > ${ID}.status
     else
        echo Pre-processing > ${ID}.status
        ./prepare_caseid.sh $ID
        touch ${ID}.prepared
        flag=1 
     fi
     sleep 1
   done
else
   cd ${ID}
   ./pp.sh
   cd ..
fi




echo Queued > ${ID}.status
qsub $ID.pbs


ispaused=0

flag=0
first_time=0
while [ "\${flag}" -eq "0" ]; do

   if [ ! -f monitor.busy ]; then
   
   
   #How much progress has been done
   current=\$(grep Step ${ID}/restart.tmp | awk -F'=' '{print \$2}')
   dt=\$(grep Computation ${ID}/restart.tmp | awk -F'=' '{print \$2}')
   total=\$(grep Termination ${ID}/restart.tmp | awk -F'=' '{print \$2}')
   total=\$(printf "%10f" \${total})
   dt=\$(printf "%10f" \${dt})
   completed=\$(echo "scale=3;100*\${dt}*\${current}/\${total}" | bc)
   completed=\$(printf "%3f" \${completed})
   
   
   if [ "\${first_time}" -eq "1" ]; then
      #How much time is spent
      SDate=\$(cat ${ID}/started_at)
      str=\$(date)
      CDate=\$(date -d "\${str}" +%s)
      elapsed=\$((\${CDate}-\${SDate}))    
      elapsed=\$(echo "scale=0; \$elapsed/60" | bc)
   else
      elapsed=0
   fi
   

   if [ -f ${ID}.pausing ]; then
      job_id=\$(qstat | grep ${ID} | awk -F'.' '{print \$1}')
      if [ "\${job_id}" != "" ]; then
         qdel \${job_id}
      fi
      ispaused=1
      #mv ${ID}.pausing ${ID}.paused
      rm -f ${ID}.resuming
      rm -f ${ID}.resumed
      echo Paused : \${elapsed} \${completed} > ${ID}.status
   fi
   
   str=\$(qstat | grep $ID.pbs | awk '{print \$5}')
   
    
   if [ "\$str" == "R" ]; then
      if [ "\${first_time}" -eq "0" ]; then
         str=\$(date)
         echo \$(date -d "\${str}" +%s) > ${ID}/started_at
         first_time=1
      fi
      
      
      echo Computing : \${elapsed} \${completed} > ${ID}.status
      
      if [ ! -f ${ID}/preview/ts_preview.busy ]; then
         touch ${ID}/preview/ts_preview.busy
         cd ${ID}/preview
         ./ts_preview.sh ${ID} &
         cd ../.. 
      fi
      
      if [ ! -f ${ID}/post-processing.busy ]; then
         touch ${ID}/post-processing.busy
         cd ${ID}
         ./pp.sh ${ID} &
         cd ..
      fi
      
      if [ ! -f ${ID}/preview/animation_preview.busy ]; then
         touch ${ID}/preview/animation_preview.busy
         cd ${ID}/preview
         ./animation_preview.sh ${ID} &
         cd ../.. 
      fi
      
      
   elif [ "\$str" == "" ]; then

      #Preview time series   
      while [ -f ${ID}/preview/ts_preview.busy ]; do
         sleep 1
      done
      cd ${ID}/preview
      ./ts_preview.sh ${ID} &
      cd ../..
      
    
      #Post process data
      while [ -f ${ID}/post-processing.busy ]; do
         sleep 1
      done
      cd ${ID}
      ./pp.sh
      
      #Preview the animation
      while [ -f ${ID}/preview/animation_preview.busy ]; do
         sleep 1
      done
      cd preview
      ./animation_preview.sh ${ID} &
    
      #Preview the rest
      ./preview.sh ${ID}
      cd ../..
      
    
   
      completedc=\$(echo "scale=0;\${completed}/100" | bc)
      if [ "\${completedc}" -eq "1" ]; then
         echo Finished : \${elapsed} \${completed} > ${ID}.status
         flag=1  
      else
         if [ "\${ispaused}" -eq "1" ]; then
            echo Paused : \${elapsed} \${completed} > ${ID}.status
            touch ${ID}.paused    
            flag=3 
         else 
            echo Error > ${ID}.status
            touch ${ID}.error
            rm -f ${ID}.resuming
            rm -f ${ID}.resumed    
            flag=2 
         fi
      fi

      echo   'chmod 644 /usr/local/apache2/htdocs/mapping/'${ID}'.pbs.*' > ${ID}_tmp.sh
      chmod 700 ${ID}_tmp.sh
      scp ${ID}.pbs.* burn.giseis.alaska.edu:/usr/local/apache2/htdocs/mapping/
      scp ${ID}_tmp.sh burn.giseis.alaska.edu:/export/burn/nicolsky/mapping
      ssh burn.giseis.alaska.edu '/export/burn/nicolsky/mapping/${ID}_tmp.sh'
      rm -f ${ID}_tmp.sh
   fi
   fi
   
   sleep 30
done



if [ "\$flag" -eq "1" ]; then
   echo Completed : \${elapsed} 100 > ${ID}.status
fi


echo 'Started at',\${str_start}
echo 'Finished at',\$(date)
EOF
chmod 700  ${ID}.wpbs
