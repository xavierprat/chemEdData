import json
import gzip

#todo: get more properties. Run the fg detector from openbabel on the organic collection
relevantLabels = [
["Alkane"],
["Alkene"],
["Alkyne"],
["Alcohol"],
["Halo_alkane","Alkylchloride","Alkylfluoride","Alkylbromide"],
["Ketone"],
["Aldehyde"],
["Amine"],
["Carboxylic","Carboxylic_acid"],
["Ester","Carboxylic_ester"],
["Amide"],
["Ether"],
["Aromatic"],
["Chiral","Chiral_center_specified"],
]
relevantProperties = [
["ThermoStatistics","transData"],
["Boiling Point","bp"],
["Melting Point","mp"]
]
def sortByMass(results):
    bymass = {}
    for name in results:
        bymass[name] = float(results[name]["mass"])
    bymassSorted = sorted(bymass, key=bymass.get)
    sortedResults = []
    for name in bymassSorted:
        sortedResults.append( { name.capitalize(): results[name]})
    return sortedResults
def makeHtmlFormula(formula):
    text = ""
    prev = ""
    for s in formula:
        if s.isdigit() and prev != '(':
            text += '<sub>'+s+'</sub>'
        else:
            text += s
        prev = s
    return text

def getFgAndLabels(mol):
    labels = []
    if "FG" not in mol: return ""
    for fg in mol["FG"]:
        for relFG in relevantLabels:
            #we accept it if it just contains the words
            if fg in relFG:
                if relFG[0] not in labels: labels.append(relFG[0])

    return ';'.join(labels)
def getProperties(mol):
    props = []
    return ';'.join(props)

with gzip.open("../data/models360json/models360compData.json.gz","rb") as f:
    models360 = json.loads(f.read().decode("ascii"))
modelsList = sortByMass(models360)

###Models
out = open("models.html","w")
with open("tableMol.html","r") as f:
    tableHeader = f.read();
out.write(tableHeader)
out.write("<tbody>\n")
#name, image?, mass, natoms, ncarbons, formula, properties available
for molecule in modelsList:
    for name,mol in molecule.iteritems():
        print "parsing ",name
        text = '<tr>'
        text += '<td>'+name+'</td>'
        formula = makeHtmlFormula(mol["formula"])
        text += '<td>'+formula+'</td>'
        text += '<td>'+mol["mass"]+'</td>'
        text += '<td>'+mol["natoms"]+'</td>'
        if "ncarbons" in mol:
            text += '<td>'+mol["ncarbons"]+'</td>'
        else:
            text += '<td>0</td>'

        labels = getFgAndLabels(mol)
        text += '<td>'+labels+'</td>'
        #props = getProperties(mol)
        #text += '<td>'+props+'</td>'
        text += '</tr>'
        text += "\n"
        out.write(text)
out.write("</tbody>\n")

out.close()

with gzip.open("../data/chemdata/organic/organic.json.gz","rb") as f:
    organic = json.loads(f.read().decode("ascii"))
organicList = sortByMass(organic)

###Organic
out = open("organic.html","w")
with open("tableMol.html","r") as f:
    tableHeader = f.read();
out.write(tableHeader)
out.write("<tbody>\n")
#name, image?, mass, natoms, ncarbons, formula, properties available
for molecule in organicList:
    for name,mol in molecule.iteritems():
        print "parsing ",name
        text = '<tr>'
        text += '<td>'+name+'</td>'
        text += '<td>'+mol["formula"]+'</td>'
        text += '<td>'+mol["mass"]+'</td>'
        text += '<td>'+mol["natoms"]+'</td>'
        #formula = makeHtmlFormula(mol["formula"])
        if "ncarbons" in mol:
            text += '<td>'+mol["ncarbons"]+'</td>'
        else:
            text += '<td>0</td>'

        labels = getFgAndLabels(mol)
        text += '<td>'+labels+'</td>'
        #props = getProperties(mol)
        #text += '<td>'+props+'</td>'
        text += '</tr>'
        text += "\n"
        out.write(text)
out.write("</tbody>\n")

out.close()

with gzip.open("../data/chemdata/elements/elements.json.gz","rb") as f:
    elements = json.loads(f.read().decode("ascii"))
elementList = sortByMass(elements)

###Elements
out = open("elements.html","w")
with open("tableElement.html","r") as f:
    tableHeader = f.read();
out.write(tableHeader)
out.write("<tbody>\n")
#name, image?, mass, natoms, ncarbons, formula, properties available
for molecule in elementList:
    for name,mol in molecule.iteritems():
        print "parsing ",name
        text = '<tr>'
        text += '<td>'+mol["name"]+'</td>'
        text += '<td>'+name+'</td>'
        text += '<td>'+mol["mass"]+'</td>'
        text += '<td>'+mol["period"]+'</td>'
        try:
            text += '<td>'+mol["group"]+'</td>'
        except:
            text += '<td></td>'
        try:
            text += '<td>'+mol["electronegativity"]+'</td>'
        except:
            text += '<td></td>'
        try:
            text += '<td>'+mol["radii"]["calculate"]+'</td>'
        except:
            text += '<td></td>'
        try:
            text += '<td>'+mol["ie"][0]+'</td>'
        except:
            text += '<td></td>'
        text += '</tr>'
        text += "\n"
        out.write(text)
out.write("</tbody>\n")

out.close()
