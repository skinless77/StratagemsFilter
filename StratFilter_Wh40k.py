
import zipfile
import webbrowser
import os

from lxml import etree

# Import des sous factions

filename="RefSousFactions.txt"
with open(filename,"r") as f:lines=f.readlines()

sousFactionsRef=[elem.replace("\n","").upper() for elem in lines]



# Module d'import de roster au format .rosz

from tkinter import filedialog
 
filename=filedialog.askopenfilename(initialdir="/",title="Séléctionner votre roster .rosz",filetypes=())
#filename ="H:\Serveur\Projet Pyhton\Premier test\Iron Hands 500pts.rosz"

with zipfile.ZipFile(filename, 'r') as zip_ref:
	zip_ref.extractall()
	fichiers=zip_ref.namelist()


tree = etree.parse(fichiers[0])
root=tree.getroot()

unites=[]
faction=[]
categories=[]
sousFaction=""

factionsRef=[
"ADEPTA SORORITAS",
"ADEPTUS CUSTODES",
"ADEPTUS MECHANICUS",
"ASTRA MILITARUM",
"ASTRA CARTOGRAPHICA",
"GREY KNIGHTS",
"IMPERIAL KNIGHTS",
"CHAOS DAEMONS",
"CHAOS KNIGHTS",
"CHAOS SPACE MARINES",
"DEATH GUARD",
"INQUISITION",
"OFFICIO ASSASSINORUM",
"THOUSAND SONS",
"CRAFTWORLD",
"DRUKHRAI",
"HARLEQUINS",
"YNNARI",
"GENESTEALERS CULTS",
"NECRONS",
"ORKS",
"T'AU EMPIRE",
"TYRANIDS",
"ROGUE TRADERS"
]


for selection in tree.iter("{http://www.battlescribe.net/schema/rosterSchema}selection"):

	if selection.get("type")=="model" or selection.get("type")=="unit" :
		
		for categorie in selection.iter("{http://www.battlescribe.net/schema/rosterSchema}category"):
			cat=categorie.get("name").upper()
			categories.append(cat)
			if "FACTION" in cat:
				faction.append(cat)

		unite={
		"nom": selection.get("name"),
		"categories": categories
		}
		unites.append(unite)

	for elem in sousFactionsRef:
		if elem.upper() in selection.get("name").upper():
			sousFaction=elem.upper()

	if sousFaction is not None:
		categories.append(sousFaction)

fac=""

for line in faction:
	if "ADEPTA SORORITAS" in line:fac="AS"
	if "ADEPTUS CUSTODES" in line:fac="AC"
	if "ADEPTUS MECHANICUS" in line:fac="AdM"
	if "ASTRA CARTOGRAPHICA" in line:fac="CA"
	if "ASTRA MILITARUM" in line:fac="AM"
	if "GREY KNIGHTS" in line:fac="GK"
	if "IMPERIAL KNIGHTS" in line:fac="QJ"
	if "CHAOS DAEMONS" in line:fac="CD"
	if "CHAOS KNIGHTS" in line:fac="QT"
	if "CHAOS SPACE MARINES" in line:fac="CSM"
	if "DEATH GUARD" in line:fac="DG"
	if "INQUISITION" in line:fac="INQ"
	if "THOUSAND SONS" in line:fac="TS"
	if "CRAFTWORLD" in line:fac="CW"
	if "OFFICIO ASSASSINORUM" in line:fac="OA"
	if "DRUKHRAI" in line:fac="DRU"
	if "HARLEQUINS" in line:fac="HAR"
	if "YNNARI" in line:fac="YNN"
	if "GENESTEALERS CULTS" in line:fac="GC"
	if "NECRONS" in line:fac="NEC"
	if "ORKS" in line:fac="ORK"
	if "T'AU EMPIRE" in line:fac="TAU"
	if "TYRANIDS" in line:fac="TYR"
	if "ADEPTUS ASTARTES" in line:fac="SM"
	if "ROGUE TRADERS" in line:fac="RT"


categories=list(set(categories))
#print(fac)
print(categories)

# Recherche de sous-faction



# with open(fichiers[0]) as temp_f:
# 	datafile=temp_f.readlines()

# for elem in sousFactionsRef:
# 	for line in datafile:
# 		if elem.upper() in line.upper():
# 			sousFaction=elem.upper()

# if sousFaction is not None:
# 	categories.append(sousFaction)

# Module d'import de stratégèmes via wahapedia : http://wahapedia.ru/wh40k9ed/Stratagems.csv


import csv
import urllib.request

hdr={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
req=urllib.request.Request("http://wahapedia.ru/wh40k9ed/Stratagems.csv", None, headers=hdr)

response= urllib.request.urlopen(req,None)

cr=csv.DictReader(response.read().decode("utf-8").splitlines(),delimiter="|")

stratFaction=[]

chaineMotCleDebut='<span class="kwb">'
chaineMotCleFin='</span>'

stratDefinitive=[]

for row in cr:
	if row["\ufefffaction_id"]==fac:
		
		stratFaction.append(row)
		motCleStrat=[]
		idxDebut=0
		idxFin=0

		while idxFin>=0 and idxDebut>=0:
			
			idxDebut=row["description"].find(chaineMotCleDebut,idxFin+len(chaineMotCleFin))+len(chaineMotCleDebut)
			
			if idxDebut>17:
				
				idxFin=row["description"].find(chaineMotCleFin,idxDebut)
				
				if idxFin>0:
					motCleStrat.append(row["description"][idxDebut:idxFin])
			else:
				idxDebut=-1
				idxFin=-1

		# print(row["name"], motCleStrat)

		# Recherche de sous-faction

		ssFac=""
		for elem in sousFactionsRef:

			if elem in row["type"].upper():
				ssFac=elem
				motCleStrat.append(ssFac)



		stratValide=True
		for motCle in motCleStrat:
			
			motCleValide=False
			if row["name"].upper()=="WARRIOR OF LEGEND":
				print(row["name"].upper())
				print(motCleStrat)
				print(categories)

			for motCleListe in categories:
				if motCle in motCleListe:
					
					motCleValide=True
				else:
					pass
			if motCleValide==False:
				stratValide=False
			



		if stratValide:
			#print(row["name"], motCleStrat)
			stratDefinitive.append(row)

# Génération de la page Html

html='<html><head><meta charset="utf-8"><link rel="stylesheet" href="PageResultat.css" /><style></style><title>Ma page de test</title></head><body><div class="wrapper">'
contenu=""

for strat in stratDefinitive:
	contenuStrat=""
	contenuStrat+='<div class style="position:relative;margin:2px 8px 2px 8px"><div class="BreakInsideAvoid Corner7" style="padding:6px;max-width:460px;"><table collapse"="" border="0" cellpadding="0" cellspacing="0"><tbody><tr><td class="Corner7_1"></td><td class="Corner7_2"></td><td class="Corner7_3"></td></tr><tr><td class="Corner7_8"></td><td class="Corner7_9"><p class="stratName"><span>'+strat["name"]+'</span><span>CP:'+strat["cp_cost"]+'</span></p><p class="stratFaction">'+strat["type"]+'</p><p>'+strat["description"]+'</p></td><td class="Corner7_4"></td></tr><tr><td class="Corner7_7"></td><td class="Corner7_6"></td><td class="Corner7_5"></td></tr></tbody></table></div></div>'
	# contenuStrat.replace("NOM",strat["name"])
	# contenuStrat.replace("FACTION",strat["type"])
	# contenuStrat.replace("CONTENU",strat["description"])
	contenu+=contenuStrat


html+=contenu+"</div></body></html>"
 
hs = open("PageResultat.html", 'w')
hs.write(html)
 

# Génération de la page CSS

contenuCss=".BreakInsideAvoid{page-break-inside: avoid;break-inside: avoid;}.wrapper{width:1000px;-moz-column-count: 2;-moz-column-gap: 14px;-webkit-column-count: 2;Unexpected end of input-webkit-column-gap: 14px;column-count: 2;column-gap: 14px;}.kwb{font-weight:bold;}p{font-family: sans-serif;}.stratFaction{font-weight:bold;font-style:italic;}.stratName{justify-content: space-between;display:flex;background:linear-gradient(315deg, transparent 8px, #294a67 0);font-family : ConduitITC,charcoal,arial black;color:white;font-size:1.24em;font-weight:bold;padding : 0 12px 0 4px;}"

css = open("PageResultat.css", 'w')
css.write(contenuCss)

webbrowser.open('file://'+os.path.realpath("PageResultat.html"))
