<?php
if (isset($_GET["collection"])){
  $collection = $_GET["collection"];
}
if (! isset($collection)){
  $collection = "models360";
  $activeTab = 0;
}
elseif ($collection == "models360" ) { $activeTab = 0; }
elseif ($collection == "organic" ) { $activeTab = 1; }
elseif ($collection == "elements" ) { $activeTab = 2; };

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
	<title>ChemData tables</title>
	<meta name="author" content="Xavier Prat-Resina" />
  <!-- jquery + jqueryui -->
  <script src="../<?php echo "$JQUERY_DIR"; ?>/jquery.min.js"></script>
  <link rel="stylesheet" href="../<?php echo "$JQUERYUICSS_DIR"; ?>/jquery-ui.css">
  <script src="../<?php echo "$JQUERYUI_DIR"; ?>/jquery-ui.min.js"></script>

  <!--Datatables for jquery 2 -->
  <script type="text/javascript" src="../<?php echo "$DATATABLES_DIR";?>/datatables.min.js"></script>
  <link rel="stylesheet" type="text/css" href="../<?php echo "$DATATABLES_DIR";?>/datatables.min.css"/>

  <script type="text/javascript" src="tables.js"> </script>
  <script type="text/javascript">
    $(document).ready(function() {
      // Setup - add a text input to each footer cell
      $('#molTable tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
      } );

      // DataTable
      var table = $('#molTable').DataTable({
        "order": [[ 2, "asc" ]],
        scrollY: 400,
        paging: false
      });

      $('#molTable tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
        updateOutput(table);
      } );

      // Apply the search
      table.columns().every( function () {
        var that = this;
        $( 'input', this.footer() ).on( 'keyup change', function () {
          if ( that.search() !== this.value ) {
            that
             .search( this.value )
             .draw();
          }
        });
      });
      $("#collectionTabs").tabs({
        active: <?php echo $activeTab; ?>
      });
      $("#outputTabs").tabs();
      $('#buttonAll').click( function(){
        $('table tr').each( function(){
          $(this).addClass('selected');
          updateOutput(table);
        });
      });
      $('#buttonNone').click( function(){
        $('table tr').each( function(){
          $(this).removeClass('selected');
          updateOutput(table);
        });
      });
      $("button").button();
      $("#googleExport").click(function(){
        var win = window.open('https://docs.google.com/spreadsheets/d/1K91zGrzELMN1v6Onu8hc_c7ZTAW9CtAeK5OKSwSYjVQ/copy', '_blank');
        if (win) {
          //Browser has allowed it to be opened
          win.focus();
        } else {
          //Browser has blocked it
          alert('Please allow popups for this website');
        }
      });
      $("#collectionTabs li a").click(function(){
        var collectionToLoad = $(this).attr("id").replace("load_","") ;
        var url = window.location.href.split('?')[0];
        url += "?collection="+collectionToLoad;
        window.location.href = url;
        //alert(url);
        location.load(url);
      })
    });
  </script>

</head>
<body>
  <div id="header">
    <h1>ChemData Search Interface</h1>
  </div>
  <div id="middle">
    <div id="collectionTabs">
      <ul>
        <li> <a id="load_models360" href="#models360Tab">Models360 collection</a> </li>
        <li> <a id="load_organic" href="#organicTab">Organic ChemData collection</a></li>
        <li> <a id="load_elements" href="#elementsTab">Elements collection</a></li>
      </ul>
      <div id="models360Tab"> </div>
      <div id="organicTab"> </div>
      <div id="elementsTab"> </div>
    </div>
    <div id="data">
      <table id="molTable" class="display" cellspacing="0" width="100%">
          <?php if ($collection == "models360"){
            echo file_get_contents('models.html');
          }elseif ($collection == "organic"){
            echo file_get_contents('organic.html');
          }elseif ($collection == "elements"){
            echo file_get_contents('elements.html');
          }else{
            exit("Wrong collection $collection");
          } ?>
      </table>
    <button id="buttonNone">Select None</button>
    <button id="buttonAll">Select All</button>
    </div>
    <div id="outputTabs">
      <ul>
        <li> <a href="#json">Text/JSON</a> </li>
        <li> <a href="#jsmol">JSmol</a> </li>
        <!--li> <a href="#xy">Plot</a> </li-->
      </ul>
      <div id="json">

        <div id="APIurl">
          API URL: <input type="text" size="100" />
        </div>
        <div id="APIiframe">
          <iframe id="frame" width="100%"></iframe>
        </div>
        <button id="googleExport">Export to GoogleSpreadSheets</button>
      </div>
      <div id="jsmol">

        <div id="APIurlJsmol">
          API URL: <input type="text" size="100" />
        </div>
        <div id="APIJsmoliframe">
          <iframe id="jsmolframe" width="100%" height="500"></iframe>
        </div>
      </div>
      <div id="xy">

      </div>

    </div>
  </div>
  <div id="footer">
    <hr/>
    <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/80x15.png" /></a> This site is developed and maintained by <a href="https://sites.google.com/a/r.umn.edu/prat-resina/">Xavier Prat-Resina</a> (pratr001 at r.umn.edu) , University of Minnesota Rochester, 2016
    <br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.
    <br>The data represented here is a compilation from different datasets:<a href="http://www.chemeddl.org/">"ChemEd DL"</a> and <a href="http://chemdata.r.umn.edu/chemedXdata">ChemEd X Data</a>
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
                  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
                    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

        ga('create', 'UA-41317211-1', 'umn.edu');
        ga('send', 'pageview');

    </script>
  </div>
</body>
</html>
