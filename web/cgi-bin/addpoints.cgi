#!/bin/bash

echo Content-type: text/html
echo ""

#Parsing incomming parameters
line=$(env | grep QUERY_STRING | sed 's/QUERY_STRING=//' | sed 's/|G==/ /g'); points=(${line})


cat << EOM

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
   <script src="http://burn.giseis.alaska.edu/scripts/gen_validatorv31.js" type="text/javascript"></script>
   <script type="text/javascript">
    //<![CDATA[
          var frmvalidator;
EOM
echo '          var filename="'$points'";'
cat << EOM

          function save(){

            var name = document.parameters.listname.value;

            if(name == "listname"){
               alert("Please enter an original list name.");
               return;
            }

            document.parameters.reset();
            if(document.error_disp_handler.all_msgs.length == 0)
               document.parameters.listname.value = name;
            else
               return;

            window.open('/cgi-bin/addpoints_final.cgi?'+filename+'&'+name,'toolbar=no,location=no,directories=no,status=no,menubar=no,width=500,height=700');
            self.close();
         }
    //]]>
   </script>
</head>


<body>

  Please enter the list name: <br />

  <form name="parameters">
      <input type="text" name="listname" value="listname"/>
       <input type="button" value="Save list" onclick="save();" />
      <div id='parameters_errorloc' class='error_strings'></div> 
  </form>

  <script language="JavaScript" type="text/javascript">

  frmvalidator  = new Validator_onreset("parameters");
  frmvalidator.EnableOnPageErrorDisplaySingleBox();
  frmvalidator.EnableMsgsTogether();

  frmvalidator.addValidation("listname","req","Please enter the list name.");
  frmvalidator.addValidation("listname","maxlen=12");
  frmvalidator.addValidation("listname","alpha");
</script>



<hr />
<h3> Points to save:</h3>
<code>
EOM
cat ../htdocs/$points | sed 's/  /\&nbsp /g' | sed 's/$/<br \/>/'

cat << EOM
</code>
  </body>
</html>

EOM
