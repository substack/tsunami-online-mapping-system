tmp_directory=.

rawfiles=$(ls -l $tmp_directory/Res_*.bin0000 2>/dev/null | awk '{print $8}')

n=0
size=0
for str in $rawfiles; do
  let n=n+1
  if [ $n = 1 ]; then
     size=$(ls ${str%.bin0000}* | wc | awk '{print $1}')
  fi
done
echo $n $size $tmp_directory> rawfiles.txt

for str in $rawfiles; do
   str_tmp=${str%.bin0000}
   echo ${str_tmp#$tmp_directory/} >> rawfiles.txt
done

./assembler

for str in $rawfiles; do
   str_tmp=${str%.bin0000}
   rm ${str_tmp}.bin*
done

rm -rf rawfiles.txt
mv *.nc ../post_processing  > /dev/null 2>&1
