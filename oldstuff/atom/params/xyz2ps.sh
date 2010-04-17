server=burn.giseis.alaska.edu
remote_path=/usr/local/apache2/htdocs/deformations

deformation=$1
deformation=${deformation%.xyz}
echo Processing \"$deformation\" deformation model
matlab -nosplash -nodisplay -r "filename='$deformation'; draw_deformation();exit;" > /dev/null

convert -density 300 -channel RGBA ${deformation}.eps ${deformation}t.png
convert -transparent white -alpha on ${deformation}t.png ${deformation}st.png
convert ${deformation}st.png -channel Alpha -evaluate Divide 2 ${deformation}.png

rm -rf ${deformation}t.png ${deformation}st.png

scp $deformation.png    $server:$remote_path
scp $deformation.extent $server:$remote_path
scp $deformation.xyz    $server:$remote_path
#ssh $server "chmod 777 $remote_path"
ssh $server "chmod 644 $remote_path/$deformation.*"
#ssh $server "chmod 755 $remote_path"

#mailx -s tester xxx@yyy.com <<EOT
#tester body
#EOT
