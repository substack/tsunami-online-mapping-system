#!/bin/bash --login

. /usr/share/modules/init/bash
module load matlab
. /u1/uaf/nicolsky/.profile

#handles process id
function find_pid {
   ftmp=$1.ppid.tmp
   fout=$1.ppid
   
   if [ -f ${ftmp} ]; then
      id=$(head -1 ${ftmp})
      sed -i '1,1d' ${ftmp}
      echo ${id} >> ${fout}
   else
      return
   fi
     
   nps=${#prs[@]}
   for ((i=0;i<nps;i++)); do
      if [ "${prt[$i]}" -eq "${id}" ]; then
          echo  ${prs[$i]} >> ${ftmp}
      fi
   done
   if [ ! -s ${ftmp} ]; then
      rm -f ${ftmp}
      return
   else
      find_pid $1
   fi
} #end find_pid

map_dir=/export/burn/nicolsky/mapping

cd /wrkdir/nicolsky/mapping
str_start=$(date)



if [ -f monitor.busy ]; then
   echo 'Started at',${str_start}
   echo 'Have done nothing'
   echo 'Finished at',$(date)
   exit
else
   touch monitor.busy
   
#copies all files based on their status(pending, removing...)
   scp burn.giseis.alaska.edu:/export/burn/nicolsky/mapping/*.pending   .   2>/dev/null
   scp burn.giseis.alaska.edu:/export/burn/nicolsky/mapping/*.removing  .   2>/dev/null
   scp burn.giseis.alaska.edu:/export/burn/nicolsky/mapping/*.pausing   .   2>/dev/null
   scp burn.giseis.alaska.edu:/export/burn/nicolsky/mapping/*.resuming  .   2>/dev/null
   scp burn.giseis.alaska.edu:/export/burn/nicolsky/mapping/*.archiving .   2>/dev/null 
   scp burn.giseis.alaska.edu:/export/burn/nicolsky/mapping/ccron       .   2>/dev/null 



   if [ -f ccron ]; then
      crontab -r
      ssh burn.giseis.alaska.edu "rm -f /export/burn/nicolsky/mapping/ccron"
      str=$(cat ccron)
      if [ "$str" == "low" ]; then
         crontab /u1/uaf/nicolsky/scripts/cron_tab_low
      else
         crontab /u1/uaf/nicolsky/scripts/cron_tab_high
      fi
   fi
  
   
   ./prepare_def.sh &
   
    
#prepare a list of files in the various statuses
   pending_files=$(ls  *.pending  2>/dev/null)
   removing_files=$(ls *.removing 2>/dev/null)
   removed_files=$(ls  *.removed  2>/dev/null)
 
   archiving_files=$(ls *.archiving  2>/dev/null)
   archived_files=$(ls  *.archived   2>/dev/null)
 
   resuming_files=$(ls  *.resuming   2>/dev/null)
   

  
   paused_files=$(ls    *.paused  2>/dev/null)
   for file in ${paused_files}; do
      ID=${file%.paused}
      rm -f ${ID}.pausing
   done

  
   
   for file in ${removed_files}; do
      ID=${file%.removed}
      if [ ! -f ${ID}.pending ]; then
         rm -f ${ID}.removed
      fi
   done
   
   for file in ${archived_files}; do
      ID=${file%.archived}
      if [ ! -f ${ID}.pending ]; then
         rm -f ${ID}.archived
      fi
   done
   

   
   touch workload_burn.sh
   chmod 700 workload_burn.sh

   #Checking for pending cases
   for file in ${pending_files}; do
      ID=${file%.pending}
      
      if [ -f ${ID}.removed ]; then
         rm -rf ${ID}*
         touch ${ID}.removed
         break
      fi
      if [ -f ${ID}.removing ]; then
         break
      fi
      
      
      if [ -f ${ID}.archived ]; then
         rm -r ${ID}*
         touch ${ID}.archived
         break
      fi
      if [ -f ${ID}.archiving ]; then
         break
      fi


    
      if [ ! -f ${ID}.wpbs ]; then
         ./prepare_job.sh $ID
      fi
      
      if [ -f ${ID}.processed ]; then
         rm -f ${ID}.pending
      else 
         ./${ID}.wpbs > ${ID}.log 2>&1 &
          mv ${ID}.pending ${ID}.processed  
      fi
   done
   
   
   for file in ${resuming_files}; do
      ID=${file%.resuming}
      
      if [ ! -f ${ID}.resumed ]; then
         if [ -f ${ID}.prepared ]; then
         if [ -f ${ID}.paused ]; then
            mv ${ID}.resuming ${ID}.resumed
            ./${ID}.wpbs > ${ID}.log 2>&1 &
            rm -f ${ID}.pausing
            rm -f ${ID}.paused
         fi
         if [ -f ${ID}.error ]; then
            mv ${ID}.resuming ${ID}.resumed
            ./${ID}.wpbs > ${ID}.log 2>&1 &
            rm -f ${ID}.error
         fi
         fi
      else
         rm -f ${ID}.resuming         
      fi
   done
   
   #Removing a case
   ps -elf | grep nicolsky > mapping.ppid.tmp
   for file in ${removing_files}; do
      ID=${file%.removing}
      if [ ! -f ${ID}.removed ]; then
      if [ -f ${ID}.log ]; then
         prs=($(cat mapping.ppid.tmp | awk '{print $4}' | sed 's/ //g'))
         prt=($(cat mapping.ppid.tmp | awk '{print $5}' | sed 's/ //g'))

         ppid=$(grep ${ID}_PID ${ID}.log | awk '{print $2}')
         echo ${ppid} > ${ID}.ppid.tmp
         rm -f ${ID}.ppid
         touch ${ID}.ppid
         find_pid ${ID}
 
         prs=($(cat ${ID}.ppid))
         for ((i=0; i<${#prs[@]}; i++)); do
            kill -9 ${prs[$i]}
         done
         mv ${ID}.log tmp
      fi
      fi
      
      
      qid=$(qstat | grep ${ID} | awk '{print $1}' | sed 's/\./ /g' | awk '{print $1}')
      if [ "${qid}" != "" ]; then
         qdel ${qid}
      fi
     
      rm -rf ${ID}*
      rm -f pre-processing.busy
      touch ${ID}.removed
   done
   
   #Archive a case
   for file in ${archiving_files}; do
      ID=${file%.archiving}
      if [ ! -f ${ID}.archived ]; then
         destination=$(cat ${file})
         mv ${ID}* ARCHIVE_${destination}
         p=ARCHIVE_${destination}/${ID}/post_processing
         scp ${p}/nc_* burn.giseis.alaska.edu:${map_dir}/${p}
      fi
      touch ${ID}.archived
   done
   
   
   
   #Creating a status file
   rm -f status
   touch status
   active_files=$(ls *.status 2>/dev/null)
   for file in ${active_files}; do
      ID=${file%.status}
      
      if [ -f ${ID}.processed ]; then
         name=$(cat ${ID}.processed)
      else
         name=$(cat ${ID}.pending)
      fi
      state=$(cat ${ID}.status | awk '{print $1}')
      
      #if [ "${state}" == "Computing" ]; then
         progress=$(cat ${ID}.status | awk '{print $4}')
         elapsed=$(cat ${ID}.status | awk '{print $3}')
      #else
      #   progress=0
      #   elapsed='' 
      #fi
      
      echo ${ID}, ${name}, $state, $progress, $elapsed >> status
   done
   
   
   #Create a update status
   cronstr=$(crontab -l | tail -1 | awk '{print $1}')

   if [ "$cronstr" == "*" ]; then
      echo "Workload information is updated every minute." > cronfrequency
   else
      mins0=$(echo $cronstr | awk -F',' '{for (i=1; i<=NF-1; i++) printf("%s, ",$i)}')
      mins1=$(echo $cronstr | awk -F',' '{printf("%s",$NF)}')
      echo "Workload information is updated every "${mins0}" and "${mins1}"th minute." > cronfrequency
      if [ "$cronstr" == "" ]; then
         echo "Workload information is not updated." > cronfrequency
      fi
   fi
   echo '<BR /> Last updated on' $(date) >> cronfrequency
   
   
   #Creating a archive status file
   rm -f archive
   touch archive
   archive_files=$(ls ARCHIVE_*/*.status 2>/dev/null)
   
   for file in ${archive_files}; do
      file=${file%.status}
      tmp=${file##ARCHIVE_}
      D=$(echo $tmp | awk -F'/' '{print $1}')
      ID=$(echo $tmp | awk -F'/' '{print $2}')
      name=$(cat ${file}.processed)
      echo ${D}';'${ID}';'$name >> archive
   done
   
   
   #qmap | grep nodes: > current_nodes
   perl nodes_avail > current_nodes
   echo 'chmod 644 /usr/local/apache2/htdocs/mapping/current_nodes' >> workload_burn.sh
   echo 'chmod 644 /usr/local/apache2/htdocs/mapping/status' >> workload_burn.sh
   echo 'chmod 644 /usr/local/apache2/htdocs/mapping/archive' >> workload_burn.sh
   echo 'chmod 644 /usr/local/apache2/htdocs/mapping/cronfrequency' >> workload_burn.sh
   
   scp current_nodes    burn.giseis.alaska.edu:/usr/local/apache2/htdocs/mapping/
   scp status           burn.giseis.alaska.edu:/usr/local/apache2/htdocs/mapping/
   scp archive          burn.giseis.alaska.edu:/usr/local/apache2/htdocs/mapping/
   scp cronfrequency    burn.giseis.alaska.edu:/usr/local/apache2/htdocs/mapping/
   
   scp workload_burn.sh burn.giseis.alaska.edu:/export/burn/nicolsky/mapping
   scp *.processed      burn.giseis.alaska.edu:/export/burn/nicolsky/mapping   2>/dev/null
   scp *.removed        burn.giseis.alaska.edu:/export/burn/nicolsky/mapping   2>/dev/null
   scp *.paused         burn.giseis.alaska.edu:/export/burn/nicolsky/mapping   2>/dev/null
   scp *.resumed        burn.giseis.alaska.edu:/export/burn/nicolsky/mapping   2>/dev/null
   scp *.archived       burn.giseis.alaska.edu:/export/burn/nicolsky/mapping   2>/dev/null
   
   ssh burn.giseis.alaska.edu '/export/burn/nicolsky/mapping/workload_burn.sh'
   rm -f workload_burn.sh
   

   rm -f monitor.busy   
fi

echo 'Started at',${str_start}
echo 'Finished at',$(date)
