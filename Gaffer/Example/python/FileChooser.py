import Gaffer
import IECore
import imath

Gaffer.Metadata.registerValue( parent, "serialiser:milestoneVersion", 1, persistent=False )
Gaffer.Metadata.registerValue( parent, "serialiser:majorVersion", 3, persistent=False )
Gaffer.Metadata.registerValue( parent, "serialiser:minorVersion", 3, persistent=False )
Gaffer.Metadata.registerValue( parent, "serialiser:patchVersion", 0, persistent=False )

__children = {}

__children["FileChooser"] = Gaffer.Box( "FileChooser" )
parent.addChild( __children["FileChooser"] )
__children["FileChooser"].addChild( Gaffer.StringPlug( "button", defaultValue = '', flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic, ) )
__children["FileChooser"].addChild( Gaffer.StringPlug( "directory", defaultValue = '', flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic, ) )
__children["FileChooser"].addChild( Gaffer.StringVectorDataPlug( "filesFound", defaultValue = IECore.StringVectorData( [  ] ), flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic, ) )
__children["FileChooser"].addChild( Gaffer.StringPlug( "fileChooser", defaultValue = '', flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic, ) )
__children["FileChooser"].addChild( Gaffer.StringPlug( "choice", defaultValue = '', flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic, ) )
__children["FileChooser"].addChild( Gaffer.V2fPlug( "__uiPosition", defaultValue = imath.V2f( 0, 0 ), flags = Gaffer.Plug.Flags.Default | Gaffer.Plug.Flags.Dynamic, ) )
Gaffer.Metadata.registerValue( __children["FileChooser"], 'uiEditor:emptySections', IECore.StringVectorData( [  ] ) )
Gaffer.Metadata.registerValue( __children["FileChooser"], 'uiEditor:emptySectionIndices', IECore.IntVectorData( [  ] ) )
Gaffer.Metadata.registerValue( __children["FileChooser"], 'noduleLayout:customGadget:addButtonTop:visible', False )
Gaffer.Metadata.registerValue( __children["FileChooser"], 'noduleLayout:customGadget:addButtonBottom:visible', False )
Gaffer.Metadata.registerValue( __children["FileChooser"], 'noduleLayout:customGadget:addButtonLeft:visible', False )
Gaffer.Metadata.registerValue( __children["FileChooser"], 'noduleLayout:customGadget:addButtonRight:visible', False )
Gaffer.Metadata.registerValue( __children["FileChooser"]["button"], 'nodule:type', '' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["button"], 'plugValueWidget:type', 'GafferUI.ButtonPlugValueWidget' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["button"], 'buttonPlugValueWidget:clicked', 'import pathlib\nfrom collections import OrderedDict\n\nnode = plug.node()\ndirectory = node["directory"].getValue()\nfiles = list( pathlib.Path( directory ).glob( "*.exr" ) )\n\n\n\nfileNames = IECore.StringVectorData( [ f.stem for f in files ] )\nfilePaths = IECore.StringVectorData( [ str(f) for f in files ] )\n###\nNewfilePaths = []\nfor i in filePaths:\n\ti = i.split(".")\n\ti[-2] = \'####\'\n\tc = ".".join(i)\n\tNewfilePaths.append(c)\nNewfilePaths = list(OrderedDict.fromkeys(NewfilePaths))\nfilePaths = IECore.StringVectorData( [ str(f) for f in NewfilePaths ] )\n###\nNewfileNames = []\nfor i in fileNames:\n\ti = i.split(".")\n\tc = ".".join(i[:-1])\n\tNewfileNames.append(c)\nfileNames = IECore.StringVectorData( NewfileNames )\nnode["filesFound"].setValue( filePaths )\n\nGaffer.Metadata.registerValue( node["fileChooser"], "presetNames", fileNames )\nGaffer.Metadata.registerValue( node["fileChooser"], "presetValues", filePaths )' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["button"], 'label', 'Update File Chooser' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["button"], 'description', '' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["button"], 'layout:section', 'Settings' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["button"], 'layout:index', 1 )
Gaffer.Metadata.registerValue( __children["FileChooser"]["button"], 'layout:accessory', True )
Gaffer.Metadata.registerValue( __children["FileChooser"]["directory"], 'nodule:type', '' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["directory"], 'layout:section', 'Settings' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["directory"], 'plugValueWidget:type', 'GafferUI.FileSystemPathPlugValueWidget' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["directory"], 'divider', False )
Gaffer.Metadata.registerValue( __children["FileChooser"]["directory"], 'layout:index', 0 )
Gaffer.Metadata.registerValue( __children["FileChooser"]["filesFound"], 'nodule:type', '' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["filesFound"], 'layout:section', 'Settings.Debug' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["filesFound"], 'layout:index', 4 )
Gaffer.Metadata.registerValue( __children["FileChooser"]["fileChooser"], 'nodule:type', '' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["fileChooser"], 'presetNames', IECore.StringVectorData( [  ] ) )
Gaffer.Metadata.registerValue( __children["FileChooser"]["fileChooser"], 'presetValues', IECore.StringVectorData( [  ] ) )
Gaffer.Metadata.registerValue( __children["FileChooser"]["fileChooser"], 'plugValueWidget:type', 'GafferUI.PresetsPlugValueWidget' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["fileChooser"], 'layout:section', 'Settings' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["fileChooser"], 'layout:index', 2 )
Gaffer.Metadata.registerValue( __children["FileChooser"]["fileChooser"], 'divider', False )
Gaffer.Metadata.registerValue( __children["FileChooser"]["fileChooser"], 'presetsPlugValueWidget:allowCustom', True )
__children["FileChooser"]["choice"].setInput( __children["FileChooser"]["fileChooser"] )
Gaffer.Metadata.registerValue( __children["FileChooser"]["choice"], 'nodule:type', '' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["choice"], 'layout:section', 'Settings.Debug' )
Gaffer.Metadata.registerValue( __children["FileChooser"]["choice"], 'layout:index', 3 )
__children["FileChooser"]["__uiPosition"].setValue( imath.V2f( 2.8000052, 9.59999943 ) )


del __children

