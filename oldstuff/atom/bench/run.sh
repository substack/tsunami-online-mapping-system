if [ ! -n "$1" ]; then
    echo usage:     ./restart.sh N
    echo 'N is the number of processes'
else

    if [  -n "$2" ]; then
        tvdebug="-tv -timeout 5000"
        echo Debug mode is activated
    else
        tvdebug=""
    fi

    echo Reading a configuration file for the model
    step=$(sed 's/ //g' restart.tmp | sed 's/=/ /g' | awk '{print $2}' | head -1 | tail -1)
    dt=$(sed 's/ //g' restart.tmp | sed 's/=/ /g' | awk '{print $2}' | head -2 | tail -1)
    dtout=$(sed 's/ //g' restart.tmp | sed 's/=/ /g' | awk '{print $2}' | head -3 | tail -1)
    ttime=$(sed 's/ //g' restart.tmp | sed 's/=/ /g' | awk '{print $2}' | head -4 | tail -1)
    radius=$(sed 's/ //g' restart.tmp | sed 's/=/ /g' | awk '{print $2}' | head -5 | tail -1)
    gravity=$(sed 's/ //g' restart.tmp | sed 's/=/ /g' | awk '{print $2}' | head -6 | tail -1)
    omega=$(sed 's/ //g' restart.tmp | sed 's/=/ /g' | awk '{print $2}' | head -7 | tail -1)



    if [ $step -eq "0" ]; then
        echo Start new computations
        echo 

        time=0
        restart=0
    else
        echo Trying to resume old computations at step $step
        echo 
        restart=1
        flag_resume=1

        #Construct a list of grids to be deassembled
        grep '<Root' gBath_topology | sed 's/>//g' | awk '{print $2}' >  tmp.txt
        grep '<Grid' gBath_topology | sed 's/>//g' | awk '{print $2}' >> tmp.txt

        nfiles=$(wc tmp.txt | awk '{print $1}')
        echo $nfiles > iNetCDF/rawfiles.txt

        for ((n=1; n <= nfiles ; n++)); do
            gridname=$(head -$n tmp.txt | tail -1)
            printf '%s %s%7.7d%s\n' ${gridname} nc_${gridname} $step .nc >> iNetCDF/rawfiles.txt
            
            tmpNetCDFName=$(printf '%s%7.7d%s' nc_${gridname} $step .nc)

            cp post_processing/$tmpNetCDFName iNetCDF
            #Testing if the file exists
            file_exist=$(ls iNetCDF | grep $tmpNetCDFName)
            
            if [ -n "$file_exist" ]; then
                flag_resume=$(($flag_resume*1))
            else
                flag_resume=$(($flag_resume*0))
                echo Could not find file $tmpNetCDFName with the previous runs. Try another step.
            fi
        done
        rm -rf tmp.txt

        if [ $flag_resume -eq "1" ]; then
            echo Successfully found all NetCDF files to restore the previous model state
            time=$(ncdump -v time iNetCDF/$tmpNetCDFName | grep data -A 1000 | grep time | sed 's/[a-Z;= ]//g')
            echo Now preparing a restart file at $(printf '%f' $time) seconds corresponding to step $step
            cd iNetCDF

            ./deassembler

            mv iBath_* ../.
            cd ../.

            rm -rf ./temporarily/Grid_*
            rm -rf ./temporarily/Mortar_*
        else
            echo Forced to start computations from the beginning
            echo 
            time=0
            step=0
            restart=0

            echo "Are you sure you want to start new computations, type [yes/no], followed by [ENTER]:"
            read yes_no
            if [ "$yes_no" == "yes" ]; then
                echo Start new computations
                echo 
            else
                echo "You are not sure..."
                echo "Do want to copy required files:"
                for ((n=1; n <= nfiles ; n++)); do
                    echo '  ' $(head -$(($n+1)) iNetCDF/rawfiles.txt | tail -1 | awk '{print $2}')
                done
                echo "Type [yes/no], followed by [ENTER]:"
                read yes_no
                if [ "$yes_no" == "yes" ]; then
                    echo Copying files
                    for ((n=1; n <= nfiles ; n++)); do
                        ifile=$(head -$(($n+1)) iNetCDF/rawfiles.txt | tail -1 | awk '{print $2}')
                        cp -v post_processing/$ifile   iNetCDF
                    done
                    echo 'Exectute this script again...'
                else
                    echo 'Bye...'
                fi
                exit
            fi 
        fi
        rm -rf rawfiles.txt
    fi

    rm -rf temporarily/Point_*.ts.tmp
    echo 
    echo Executing %  mpirun -np $1 $tvdebug ./tmp -restart $restart -time $time -step $step -dt $dt -dtout $dtout -ttime $ttime -omega $omega -radius $radius
    mpirun -np $1 $tvdebug ./tmp -restart $restart -time $time -step $step -dt $dt -dtout $dtout -ttime $ttime -omega $omega -radius $radius
    
fi

