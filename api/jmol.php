<?php
#possible keywords: header=yes/no, mol=cirID, size=x, multiple=yes/no, buttons=(mep,dipole,symm,charges,all,none)
if ( isset($_GET['header'] )){
	$header = $_GET['header'];
  if ( $header != "no" ){ $header = "yes";};
}else{
	$header = "yes";
};

if ( isset($_GET['multiple'])){
	$multiple = $_GET['multiple'];
	if ( $multiple != "yes" ){ $multiple = "no";};
}else{
	$multiple = "no";
}

if ( isset( $_GET['mol'])){
	$mol = $_GET['mol'];
	if ( $multiple == "yes"){
		$mols = explode(";",$mol);
	}else{
		$mols = array($mol);
	}
}else{
	if ( $multiple == "yes"){
		$mols = array("CH3Cl","CH3OH","CH3F");
	}else{
		$mols = array("CH3Cl");
	}
}
if ( isset( $_GET['size'])){
	$appletSize = $_GET['size'];
}else{
	$appletSize = "310";
}
if ( isset( $_GET['buttons'])){
	$appletButtons = $_GET['buttons'];
}else{
	$appletButtons = "yes";
}
if ( isset( $_GET['sync_buttons'])){
	$sync_buttons = $_GET['sync_buttons'];
}else{
	$sync_buttons = "no";
}
if ( isset( $_GET['header'])){
	$sync_buttons = $_GET['header'];
}else{
	$sync_buttons = "yes";
}

$libs_dir = fopen("../libs_dir.txt","r");
if ($libs_dir){
	while (($line = fgets($libs_dir)) !== false) {
		$args = explode("=",$line);
		$libname = trim($args[0]);
		$libpath =  trim($args[1]);
		$$libname = $libpath;
	}
}else{
	error_log("libs_dir.txt file not available",0);
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title>jmol</title>
	<meta name="author" content="Xavier Prat-Resina" />
	<!-- jquery + jqueryui -->
	<script src="../<?php echo "$JQUERY_DIR"; ?>/jquery.min.js"></script>
	<link rel="stylesheet" href="../<?php echo "$JQUERYUICSS_DIR"; ?>/jquery-ui.css">
	<script src="../<?php echo "$JQUERYUI_DIR"; ?>/jquery-ui.min.js"></script>

	<script type="text/javascript" src="../<?php echo "$JSMOL_DIR";?>/jsmol/JSmol.min.nojq.js"></script>
	<script type="text/javascript">
	var inchikeys = [];
	//var names = [];
	var nMols;
	var applets = [];
	function writeMenu(i){
		var text = '<div class="jmolMenus" id="menu'+i+'">';
		text += ' \
		<h4><span style="float:left">Show/Hide properties</span>\
		<span style="float:right">'+inchikeys[i]+'</span></h4><br>\
		<button class="mep">MEP</button>\
		<button class="chg">Partial Charges</button>\
		<button class="mdipole">Molecular Dipole</button>\
		<button class="bdipole">Bond Dipoles</button>\
		<button class="symm">Symmetry</button>\
		';
		text += "</div>";
		return text;
	}
	function giveJmolObject(n){
		//not more than ten working applets
		switch(n){
			case '0': return jmolApplet0;break;
			case '1': return jmolApplet1;break;
			case '2': return jmolApplet2;break;
			case '3': return jmolApplet3;break;
			case '4': return jmolApplet4;break;
			case '5': return jmolApplet5;break;
			case '6': return jmolApplet6;break;
			case '7': return jmolApplet7;break;
			case '8': return jmolApplet8;break;
			case '9': return jmolApplet9;break;
		};
		return jmolApplet0;
	}
	function showPG0(applet){
		Jmol.script(applet, 'select *;if (symm0) {draw delete;set echo off;symm0 = null} else {point0 = \'Group= \'+script("calculate pointgroup"); set echo top left; echo @point0;draw pointgroup; symm0=1;}');
	}
  function getQueryURL(variable){
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
      var pair = vars[i].split("=");
      if(pair[0] == variable){return pair[1];}
    }
    return(false)
  }
	Jmol.setDocument(0);
	$(document).ready(function(){
		var hash = document.location.hash;
		inchikeys = ["<?php echo implode('","',$mols); ?>"];
		nMols = inchikeys.length;
 		for (var i=0;i<nMols;i++){
			$("#jmols").append('<div id="frame'+i+'" style="float:left;width:320px"></div>');
			$("#frame"+i).append('<div style="width:310px" id="thisJmol'+i+'" ></div>');
			$("#frame"+i).append('<div style="width:310px" id="thisButton'+i+'"></div>');
			var file;
			$.ajax({
				url: "https://cactus.nci.nih.gov/chemical/structure/"+inchikeys[i]+"/file?format=sdf&get3d=true",
				async: false,
				dataType: "text",
				success: function(data){
					//9999.9999
					file = 'load inline "'+data.replace(/\n/g,'\n').split("$$$$")[0].replace(/9999.9999/g,"0000.0000")+'$$$$";';
				}
			});
			var loadMol = file+'; set echo bottom center; font echo 16 sanserif bold;echo '+inchikeys[i];
			var Info = { use: "HTML5",
			width : <?php echo $appletSize;?>,
			serverURL: "http://<?php echo $YOUR_SERVER . "/" . $ROOT_DIR . "/" . $JSMOL_DIR ;?>/jsmol/php/jsmol.php",
			j2sPath: "../<?php echo $JSMOL_DIR;?>/jsmol/j2s", script : loadMol};
			var thisApplet = Jmol.getAppletHtml("jmolApplet"+i,Info);
			$("#thisJmol"+i).html(thisApplet);
			applets.push(thisApplet);
			<?php if ( $appletButtons == "yes"){ ?>
			var text = writeMenu(i);
			$("#thisButton"+i).html(text);
			<?php } ?>
		}
		$("button").click(function(){
			var type = $(this).attr("class");
			var thisMol = $(this).closest('.jmolMenus').attr('id').replace("menu","");
			var thisApplet = giveJmolObject(thisMol);
			switch(type){
				case 'mep':
					Jmol.script(thisApplet,'select *;if ($s0) {isosurface s0 delete} else {calculate partialcharge;isosurface s0 vdw map MEP translucent}');
					break;
				case 'chg':
					Jmol.script(thisApplet,'select *;if (c0) {labels off;c0=null} else {calculate partialCharge; label %3.2[partialCharge];c0=1}');
					break;
				case 'mdipole':
					Jmol.script(thisApplet,'select *;if (dipMol0) {dipole molecular delete;dipMol0 = null;} else {calculate partialCharge; dipole calculate molecular width 0.1 offset 1.0;dipMol0=1 }');
					break;
				case 'bdipole':
					Jmol.script(thisApplet,'select *;if (dipBond0) {dipole bonds delete;dipBond= null} else {calculate partialCharge; dipole calculate bonds width 0.05 offset 1.0;dipBond0=1;}');
					break;
				case 'symm':
					showPG0(thisApplet);
					break;
			}
		});

		$( "#menuButtons" ).buttonset();
		$( "#graphTabs" ).buttonset();

		$('input[name="dragMin"]').attr('checked',false);
		$('input[name="dragMin"]').change( function(){
			if ( $('input[name="dragMin"]').is(':checked')){
				for (var i=0;i<nMols;i++){
					var thisApplet = giveJmolObject(i.toString());
					Jmol.script(thisApplet,"set picking dragMinimize");
				}
			}else{
				for (var i=0;i<nMols;i++){
					var thisApplet = giveJmolObject(i.toString());
					Jmol.script(thisApplet,"set picking off");
				}
			}
		});
                $('input[name="sync"]').attr('checked',false);
                $('input[name="sync"]').change( function(){
                    if ( $('input[name="sync"]').is(':checked')){
                            Jmol.script(jmolApplet0,"sync * on; sync * \"set syncMouse TRUE\"");
                    }else{
                            Jmol.script(jmolApplet0,"sync * off",jmolApplet0);
                    }
                });
	});
	</script>
</head>
<body>
<div id="content">
      <div id="plotTitle" style="width:600px;text-align:center">
				<?php if ( $sync_buttons == "yes"){?>
        <input type="checkbox" name="sync">Synchronize mouse</input>
        <input type="checkbox" name="dragMin">Drag and minimize</input>
				<?php } ?>
      </div>
      <div id="jmols">
      </div>
</div>
</body>
</html>
