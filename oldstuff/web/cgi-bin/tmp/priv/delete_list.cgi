#!/bin/bash

echo Content-type: text/html
echo ""

#Parsing available deformations
llists=$(ls ../../htdocs/grids/list_points.*)
let i=0
for file in $llists; do
  file=${file##../../htdocs/grids/list_points.} 
  lists[i]=$file
  let i=i+1 
done
ilists=$((${#lists[@]}-1))


cat << EOM
<HTML>
<HEAD><TITLE>Delete a list of marker points</TITLE>
<script language="JavaScript" type="text/javascript">
<!--

var NS4 = (navigator.appName == "Netscape" && parseInt(navigator.appVersion) < 5);

function addOption(theSel, theText, theValue)
{
  var newOpt = new Option(theText, theValue);
  var selLength = theSel.length;
  theSel.options[selLength] = newOpt;
}

function deleteOption(theSel, theIndex)
{ 
  var selLength = theSel.length;
  if(selLength>0)
  {
    theSel.options[theIndex] = null;
  }
}

function moveOptions(theSelFrom, theSelTo)
{
  
  var selLength = theSelFrom.length;
  var selectedText = new Array();
  var selectedValues = new Array();
  var selectedCount = 0;
  
  var i;
  
  // Find the selected Options in reverse order
  // and delete them from the 'from' Select.
  for(i=selLength-1; i>=0; i--)
  {
    if(theSelFrom.options[i].selected)
    {
      selectedText[selectedCount] = theSelFrom.options[i].text;
      selectedValues[selectedCount] = theSelFrom.options[i].value;
      deleteOption(theSelFrom, i);
      selectedCount++;
    }
  }
  
  // Add the selected text/values in reverse order.
  // This will add the Options to the 'to' Select
  // in the same order as they were in the 'from' Select.
  for(i=selectedCount-1; i>=0; i--)
  {
    addOption(theSelTo, selectedText[i], selectedValues[i]);
  }
  
  if(NS4) history.go(0);
}


function Finalize(theSelFrom)
{
  
  var selLength = theSelFrom.length;
  var selectedText = new Array();
  var selectedValues = new Array();
  var selectedCount = 0;
  
  var i;
  
  // Find the selected Options in reverse order
  // and delete them from the 'from' Select.
  for(i=selLength-1; i>=0; i--)
  {
      selectedText[selectedCount] = theSelFrom.options[i].text;
      selectedValues[selectedCount] = theSelFrom.options[i].value;
      deleteOption(theSelFrom, i);
      selectedCount++;
  }
  
  // Add the selected text/values in reverse order.
  // This will add the Options to the 'to' Select
  // in the same order as they were in the 'from' Select.

  var str="";

  for(i=selectedCount-1; i>=0; i--)
    str += selectedText[i] + "|";
  if(str == "")
    alert("Please select sources to delete.")
  else
    window.open('/cgi-bin/priv/delete_list_final.cgi'+'?'+str,'toolbar=no,location=no,directories=no,status=no,menubar=no,width=500,height=700');
}

//-->
</script>


</HEAD>
<BODY>
<form action="yourpage.asp" method="post">
<table border="0">
        
<tr>        <th WIDTH=200>Available lists</th>  <th WIDTH=100></th>  <th WIDTH=200>Candidates for removal</th> </tr>
	<tr>
		<td>
			<select name="sel1" size="10" multiple="multiple">
EOM
for ((i=0;i<=$ilists;i+=1)); do 
    file=${lists[$i]}
    echo '                        <option value="list_'$file'">'$file'</option>'
done
cat << EOM
			</select>
		</td>
		<td align="center" valign="middle">
			<input type="button" value="--&gt;"
			 onclick="moveOptions(this.form.sel1, this.form.sel2);" /><br />
			<input type="button" value="&lt;--"
			 onclick="moveOptions(this.form.sel2, this.form.sel1);" />
		</td>
		<td>
			<select name="sel2" size="10"  multiple="multiple">
			</select>
                        
		</td>
	</tr>
</table>
<br /> <br />
<input type="button" value="Delete" onclick="Finalize(this.form.sel2);" /> 

</form>

</BODY>
</HTML>
EOM
