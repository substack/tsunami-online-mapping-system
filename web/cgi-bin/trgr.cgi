#!/bin/bash


analyze_tree()
{
  local level=$1
  local index
  local n=0

  if [ "${level}" != " " ]; then
    for index in ${!grids[*]}; do
      if [ "${parents[$index]}" == "$level" ]; then
        analyze_tree ${index}
        children[$index]=$?
        let n=n+1
      fi
    done
  fi
  return $n
}

summurize_tree()
{
  local level=$1
  local index
  local n=1

  if [ "${level}" != " " ]; then
    for index in ${!grids[*]}; do
      if [ "${parents[$index]}" == "$level" ]; then
        summurize_tree ${index}
        let n=n+$?
      fi
    done
  fi
  nephews[$level]=$n
  return $n
}



print_string()
{
  name=$2
  desc=$(head -1 $gpath/$name.readme)
  desc=$(echo $desc)
  pth=$(tail -1 $gpath/$name.readme)
  pth=$(echo $pth)
  if [ "${name:4:4}" != "e" ]; then
    echo $1'<input type="checkbox" onClick="parent.dynamic.boxclick(this,'"'"$name"'"');"><a href="/'$pth$name'.xyz.gz">'$name'</a>('$desc')<BR>'
  else
    echo $1'<input type="checkbox" onClick="parent.dynamic.boxclick(this,'"'"$name"'"');"><a href="/'$pth$name'.xyz.gz">'$name'</a> <FONT COLOR="#FF0000"><b>('$desc')</b></FONT><BR>'
  fi
}

print_tree()
{
  local level=$1
  local s=$2

  local step=$3

  local index
  local str

  if [ "${level}" != " " ]; then
    for index in ${!grids[*]}; do
      if [ "${parents[$index]}" == "$level" ]; then
        let step=step-1
        if [[ $step -gt 0 ]]; then
           if [[ ${children[$level]} -gt 1 && ${nephews[$level]} -gt 1 ]]; then
              str=$s'&nbsp|&nbsp&nbsp'
           else
              str=$s'&nbsp&nbsp&nbsp'
           fi
        else
           str=$s'&nbsp&nbsp&nbsp'
        fi
        print_string $s ${grids[$index]}
        print_tree ${index} $str ${children[$index]}
      fi
    done
  fi
}





echo Content-type: text/html
echo ""


gpath=../htdocs/grids
spaces="      "
grids=($(ls ${gpath}/*.parent))

for index in ${!grids[*]}; do
  p=${grids[$index]%.parent}
  p=${p##${gpath}/}
  grids[$index]=$p
  children[$index]=0
  nephews[$index]=0
  parents[$index]=$(cat ${gpath}/$p.parent)
done

for index in ${!grids[*]}; do
    pname=${parents[$index]}
    for i in ${!grids[*]}; do
        if [ "$pname" == "${grids[$i]}" ]; then
           parents[$index]=$i
        fi
    done
    if [ "${grids[$index]}" == "PA02" ]; then
       root=$index
    fi
done

analyze_tree $root
children[$root]=$?
summurize_tree $root




cat<< EOM

<html>
<head>
  <Style>
    BODY, P,TD{ font-family: Arial,Verdana,Helvetica, sans-serif; font-size: 10pt }
    A{font-family: Arial,Verdana,Helvetica, sans-serif;}
    B {	font-family : Arial, Helvetica, sans-serif;	font-size : 12px;	font-weight : bold;}
    .error_strings{ font-family:Verdana; font-size:10px; color:#660000;}
    </Style>
</head>
<body>

<FORM>

<h2>Topology of grids</h2>
<font  face="monospace">
<input type="checkbox" onClick="parent.dynamic.boxclick(this, 'PA02');"><a href='grids/PA02.xyz.gz'>PA02</a> (2 arc-minute grid for the Pacific Ocean)<BR>


EOM

print_tree $root '&nbsp&nbsp' ${children[$root]}

#for index in ${!grids[*]}; do
#  printf "%4d: %5s %5s %5s %5s\n"  $index ${grids[$index]} ${parents[$index]}. ${children[$index]} ${nephews[$index]}
#done


cat << EOM
</font>
</FORM>

</body></html>

EOM



  #str=$str
