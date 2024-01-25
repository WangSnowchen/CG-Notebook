#Button上点击后，更新文件选择器的预设值

import pathlib
from collections import OrderedDict

node = plug.node()
directory = node["directory"].getValue()
files = list( pathlib.Path( directory ).glob( "*.exr" ) )



fileNames = IECore.StringVectorData( [ f.stem for f in files ] )
filePaths = IECore.StringVectorData( [ str(f) for f in files ] )
###
NewfilePaths = []
for i in filePaths:
	i = i.split(".")
	i[-2] = '####'
	c = ".".join(i)
	NewfilePaths.append(c)
NewfilePaths = list(OrderedDict.fromkeys(NewfilePaths))
filePaths = IECore.StringVectorData( [ str(f) for f in NewfilePaths ] )
###
NewfileNames = []
for i in fileNames:
	i = i.split(".")
	c = ".".join(i[:-1])
	NewfileNames.append(c)
fileNames = IECore.StringVectorData( NewfileNames )
node["filesFound"].setValue( filePaths )

Gaffer.Metadata.registerValue( node["fileChooser"], "presetNames", fileNames )
Gaffer.Metadata.registerValue( node["fileChooser"], "presetValues", filePaths )