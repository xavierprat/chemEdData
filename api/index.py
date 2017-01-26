#! /usr/bin/python
import os
import sys
import json
import gzip
import urllib
import urllib2

#define directories
libs_file = open("../libs_dir.txt","r")
for line in libs_file.readlines():
    args = line.split("=")
    lib_name = args[0].strip()
    lib_dir = args[1].strip()
    exec( "%s = '%s'" % (lib_name,lib_dir))

htmlHead = "Content-type: text/html\n"
print htmlHead

def showMainPaige():
    print "<h1>This is the ChemEdData API</h1>"
    print '<h1>Click <a href="tables.php">here</a> to navigate all the data available</h1>'
    sys.exit(0)

def throwError(message):
    print "<h1>I made a Boo Boo</h1>"
    print "<h1>"+message+"</h1>"
    sys.exit(1)

def sortByMass(results):
    bymass = {}
    for name in results:
        bymass[name] = float(results[name]["mass"])
    bymassSorted = sorted(bymass, key=bymass.get)
    sortedResults = []
    for name in bymassSorted:
        sortedResults.append( { name.capitalize(): results[name]})
    return sortedResults
def printImage(imgFile):
    data_uri = open(imgFile, 'rb').read().encode('base64').replace('\n', '')
    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
    print img_tag



url = os.environ['QUERY_STRING']
if len(url) == 0: showMainPaige()
url = url.split("&")
query = {}
#defaults
query["collection"]="organic"
query["type"]="compounds"

for option in url:
    #an equal sign is used in Smiles
    fields = option.split("=")
    try:
        #urllib.unquote(urllib.unquote('FireShot3%2B%25282%2529.png'))
        thisOption = urllib.unquote(urllib.unquote(fields[1]))
        if fields[0] == "propout" :
            #some propout options are case sensistive
            query[fields[0].lower()] = thisOption
        else:
            query[fields[0].lower()] = thisOption.lower()
    except:
        throwError("Remember to write '=' for each option")

results = {}

#COLLECTION
if query["collection"] == "models360":
    with gzip.open("../data/models360/models360.json.gz","rb") as f:
        data = json.loads(f.read().decode("ascii"))
elif query["collection"] == "organic":
    with gzip.open("../data/chemdata/organic/organic.json.gz","rb") as f:
        data = json.loads(f.read().decode("ascii"))
elif query["collection"] == "inorganic":
    with gzip.open("../data/chemdata/inorganic/inorganic.json.gz","rb") as f:
        data = json.loads(f.read().decode("ascii"))
elif query["collection"] == "elements":
    with gzip.open("../data/chemdata/elements/elements.json.gz","rb") as f:
        data = json.loads(f.read().decode("ascii"))
else:
    #throw error
    throwError("Unidentified collection")
    #leave

#Name is the unique identifier for each entry
if 'name' in query:
    names = query['name'].split(';')
    for name in names:
        if name in data:
            #this will just override if it has been found before
            results[name] = data[name]
elif 'inchikey' in query:
    inchikeys = query['inchikey'].split(';')
    for inchikey in inchikeys:
        for name in data:
            mol = data[name]
            if mol["ids"]["inchikey"] == inchikey:
                results[name] = mol
elif 'cir' in query:
#https://cactus.nci.nih.gov/chemical/structure/dihydrogen%20dioxide/file?format=sdf&get3d=True
#https://cactus.nci.nih.gov/chemical/structure/anyInputId/anyOutputId
    #this is deprecrated, wild search is for compounds out of our collection
    cirs = query["cir"].split(';')
    for cir in cirs:
        #get the inchikey from CIR
        found = False
        thisResponse = urllib2.urlopen("https://cactus.nci.nih.gov/chemical/structure/"+cir+"/inchikey")
        thisText = thisResponse.read()
        thisText = thisText.replace("InChIKey=","")
        for name in data:
            mol = data[name]
            if mol["ids"]["inchikey"] == inchikey:
                results[name] = mol

else:
    #no name specified. we load the whole thing
    results = data



#Property Input
if 'fg' in query:
    newResults = {}
    fgs = query['fg'].split(';')
    #giving different propins are not exclusive (and) rather inclusive (or)
    for fg in fgs:
        fg = fg.lower().capitalize()
        for name,mol in results.iteritems():
            try:
                if fg in mol['FG']:
                    newResults[name] = mol
            except:
                continue
    results = newResults

#More property Input
if 'natoms' in query:
    #giving different propins are not exclusive (and) rather inclusive (or)
    if query["collection"] == "elements": throwError("Natoms not applicable to elements")
    natomsArray = query['natoms'].split(';')
    newResults = {}
    for natom in natomsArray:
        for name,mol in results.iteritems():
            if natom == mol["natoms"]:
                newResults[name] = mol
    results = newResults

#More property Input
if 'ncarbons' in query:
    if query["collection"] == "elements": throwError("Ncarbons not applicable to elements")
    #giving different propins are not exclusive (and) rather inclusive (or)
    ncarbonsArray = query['ncarbons'].split(';')
    newResults = {}
    for ncarbon in ncarbonsArray:
        for name,mol in results.iteritems():
            if ncarbon == mol["ncarbons"]:
                newResults[name] = mol
    results = newResults

#conditions for matches to have a certain property value
if 'propin' in query:
    propIn = query['propin']
    propInArray = propIn.split(';')

#This sorts by mass and capitalizes. Then this is a list not a dict anymore
sortedResults = []
sortedResults = sortByMass(results)

#Property Output

if 'propout' in query:
    listTextOut = []
    propout = query['propout']
    propArray = propout.split(';')
    for molecule in sortedResults:
        for name,mol in molecule.iteritems():
            textOut = {}
            thisResult = {}
            for prop in propArray:
                if "-" in prop:
                    firstCat = prop.split("-")[0]
                    secondCat = prop.split("-")[1]
                    try:
                        thisResult[prop] = mol[firstCat][secondCat]
                    except:
                        thisResult[prop] = firstCat+secondCat
                elif prop not in mol:
                    #throwError("This property does not exist for "+name)
                    thisResult[prop] = None
                else:
                    thisResult[prop] = mol[prop]
            textOut[name] = thisResult
            listTextOut.append(textOut)

    print json.dumps(listTextOut,indent=1)

elif 'jsmol' in query:
    options = query['jsmol'].split(';')
    #This tool is only useful for Models360 collection where GaussianFiles are stored
    if query["collection"] == "models360":
        jmolBodyTemplate = "jmolBody.html"
    else:
        #jump to use jmol.php?mol=name
        #print("Location:http://chemdata.r.umn.edu/chemEdData/api/jmol.php\r\n")
        myJmols = []
        for molecule in sortedResults:
            for name,mol in molecule.iteritems():
                myJmols.append(mol["name"].title())
        if len(myJmols) > 1:
            stringOfMols = ';'.join(myJmols)
            print '<meta http-equiv="refresh" content="0; URL=\'jmol.php?mol='+stringOfMols+'&multiple=yes\'" />'
        elif len(myJmols) == 1:
            print '<meta http-equiv="refresh" content="0; URL=\'jmol.php?mol='+myJmols[0]+'\'" />'
        quit()

    if "nohead" not in options:
        with open("jmolHead.html","r") as jmolHead:
            head = jmolHead.read()
            head = head.replace("JQUERY_DIR",JQUERY_DIR)
            head = head.replace("JQUERYUI_DIR",JQUERYUI_DIR)
            head = head.replace("JSMOL_DIR",JSMOL_DIR)
            print head

    #This info sets the size
    with open("jmolInfo.html","r") as jmolInfo:
        info = jmolInfo.read()
        info = info.replace("YOUR_SERVER",YOUR_SERVER)
        info = info.replace("ROOT_DIR",ROOT_DIR)
        info = info.replace("JSMOL_DIR",JSMOL_DIR)
        for opt in options:
            if opt.isdigit():
                info = info.replace("300",opt)
        print info

    i=0
    for molecule in sortedResults:
        for name,mol in molecule.iteritems():
            gaussianFile = mol["gaussianFile"]
            print mol["name"].title()
            with open(jmolBodyTemplate,"r") as jmolBody:
                body = jmolBody.read()
                body = body.replace("jmolApplet0","jmolApplet"+str(i))
                #temporary until I upload all data
                body = body.replace("GaussianDir","/data/import360")
                body = body.replace("GaussianName",gaussianFile)
                print body
            i+=1
    if "nohead" not in options:
        with open("jmolTail.html","r") as jmolTail:
            tail = jmolTail.read()
            print tail


    #for name,mol in results.iteritems():
    #    a=1

#    if "vib" in options:
#        includeVibJsmol()
#    if "main" in options:
#        includeMainJsmol()
#    if "mo" in options:
#        includeMOJsmol()
#    if "symm" in options:
#        includeSymmJsmol()
#    if "size" in options:
#        a=1
#    else:
#        size = "500x500"
elif 'xyscatter' in query:
    a=1
elif 'file' in query:
    fileType = query["file"]
    for name,mol in results.iteritems():
        print "hello"
elif 'image' in query:
    extension = query["image"]
    if query["collection"] == "models360":
        if extension == "nrt":
            for name,mol in results.iteritems():
                found = False
                for f in mol["files"]:
                    if f.endswith(".sdf"):
                        found = True
                        nrt = f.replace("sdf","svg")
                        print '<p><img src="/data/import360/nrt/' +nrt+'" width="500" />'
                if not found: print '<p>No NRT was calculated for ',name

        elif extension == "png" or extension == "jpeg":
            for name,mol in results.iteritems():
                found = False
                for f in mol["files"]:
                    if f.endswith(extension):
                        found = True
                        #print '<img src="/data/import360/' +f+'" width="100" />'
                        imgFile = "/var/www/data/import360/"+f
                        printImage(imgFile)
                        #sys.stdout.write( "Content-type: image/png\r\n\r\n" + file(imgFile,"rb").read() )
                        #with open("/var/www/data/import360/"+f) as imgFile:
                    #        print imgFile.read()
                if not found: print '<p>No image was made for ',name
        else:
            throwError("Unrecognized extension for images in this collection")

    elif query["collection"] == "organic":
        if extension == "svg" or extension == "png":
            for name in results:
                #print '<img src="/data/chemdata/organic/svg/' +name.lower()+'.'+extension+'" width="100" />'
                imgFile = '/var/www/data/chemdata/organic/svg/' +name.lower()+'.'+extension
                printImage(imgFile)
                #with open("/var/www/data/chemdata/organic/svg/"+name.lower()+"."+extension,"r") as f:
                #    print f.read()
        else:
            throwError("Unrecognized extension for images in this collection")
    else:
        throwError("No images for this collection")
else:
    #pretty JSON is the default
    print json.dumps(sortedResults,indent=1)
