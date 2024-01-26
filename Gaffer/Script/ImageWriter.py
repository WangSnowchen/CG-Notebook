a = parent["ArnoldRender"]["out"]["globals"]
aovname = []
for key,value in a.items():
	if "output" in key:
		aovnamelist = value.getName()
		aovnamelist = aovnamelist.split("/")[-1].split(".")[0]
		aovname.append(aovnamelist)
parent["CollectImages7"]["rootLayers"] = IECore.StringVectorData( aovname )