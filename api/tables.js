function updateOutput(table){
  var collection = $("#collectionTabs ul li.ui-state-active a").attr("id");
  collection = collection.replace("load_","");
  $("#test").empty();
  var listOfNames = $.map(table.rows('.selected').data(), function (item) {
    if (collection == "elements" ) {
      //for elements the API needs the symbol not the name
      return item[1];
    }else{
      return item[0];
    }
  });
  //check which collection is loaded by checking which tab is active
  var url = 'http://chemdata.r.umn.edu/chemEdData/api/index.py?collection='+collection+'&name='+listOfNames.join(";")
  $("#APIurl input").val(url);
  $("#frame").attr('src',url);
  //jsmol tab
  var url = 'http://chemdata.r.umn.edu/chemEdData/api/index.py?collection='+collection+'&name='+listOfNames.join(";")+'&jsmol=all';
  $("#APIurlJsmol input").val(url);
  $("#jsmolframe").attr('src',url);
}
