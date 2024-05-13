import GafferUI
import Gaffer
import GafferDispatch
import functools
import imath
import IECore
import os
import subprocess




def registerAnnotation( menu):
    scriptWindow = menu.ancestor( GafferUI.ScriptWindow )
    script = scriptWindow.scriptNode()
    mainWindow = GafferUI.ScriptWindow.acquire( script )

    selected = script.selection()
    if selected.size():
        current_annotation = Gaffer.Metadata.value(selected[0], "annotation:greeting:text")
        initial_text = current_annotation if current_annotation else ""
        d = GafferUI.TextInputDialogue( initialText=initial_text, title="Annotation", confirmLabel="Set" )
        c = GafferUI.ColorChooserDialogue( title="Select Color",color=imath.Color3f(1),cancelLabel="Cancel",confirmLabel="OK")
        text = d.waitForText( parentWindow =  mainWindow )
        color = c.waitForColor( parentWindow = mainWindow )
        for node in selected:
            if text:
                Gaffer.Metadata.registerValue(node, "annotation:greeting:text", text)
                Gaffer.Metadata.registerValue(node, "annotation:greeting:color", color)
            else:
                Gaffer.Metadata.deregisterValue(node, "annotation:greeting:text")
                Gaffer.Metadata.registerValue(node, "annotation:greeting:color", color)
def OpenThisFileGRF(menu):
    scriptWindow = menu.ancestor( GafferUI.ScriptWindow )
    script = scriptWindow.scriptNode()
    current_file = script['fileName'].getValue()
    current_file = os.path.dirname(current_file)
    subprocess.Popen('gio open "%s"' % current_file, shell=True)
def ChangeNodeColor(menu):
    scriptWindow = menu.ancestor( GafferUI.ScriptWindow )
    script = scriptWindow.scriptNode()
    mainWindow = GafferUI.ScriptWindow.acquire( script )

    selected = script.selection()
    if selected.size():
        c = GafferUI.ColorChooserDialogue( title="Select Color",color=imath.Color3f(1),cancelLabel="Cancel",confirmLabel="OK")
        color = c.waitForColor( parentWindow = mainWindow )
        for node in selected:
            if color:
                Gaffer.Metadata.registerValue(node, "nodeGadget:color", color)
            else:
                Gaffer.Metadata.registerValue(node, "nodeGadget:color", color)
def resetVisualiserScale(menu):
    scriptWindow = menu.ancestor( GafferUI.ScriptWindow )
    script = scriptWindow.scriptNode()
    mainWindow = GafferUI.ScriptWindow.acquire( script )
    scene_viewer = mainWindow.getLayout().editor(GafferUI.Viewer)
    scene_view = scene_viewer.view()
    scene_view["drawingMode"]["visualiser"]["scale"].setValue(1.0)
def changeToolOrientation(menu):
    #更改旋转位移工具的轴向为自身坐标系
    scriptWindow = menu.ancestor( GafferUI.ScriptWindow )
    script = scriptWindow.scriptNode()
    mainWindow = GafferUI.ScriptWindow.acquire( script )
    scene_viewer = mainWindow.getLayout().editor(GafferUI.Viewer)
    scene_view = scene_viewer.view()
    scene_view["tools"]["TranslateTool"]["orientation"].setValue(0)
    scene_view["tools"]["RotateTool"]["orientation"].setValue(0)






GafferUI.ScriptWindow.menuDefinition(application).append(
	"/WXC/tools/" + "registerAnnotation",
	{
		"command" : functools.partial( registerAnnotation ) , 
		"label" : "registerAnnotation"
	}
)
GafferUI.ScriptWindow.menuDefinition(application).append(
	"/WXC/tools/" + "OpenThisFileGRF",
	{
		"command" : functools.partial( OpenThisFileGRF ) , 
		"label" : "OpenThisFileGRF"
	}
)
GafferUI.ScriptWindow.menuDefinition(application).append(
	"/WXC/tools/" + "ChangeNodeColor",
	{
		"command" : functools.partial( ChangeNodeColor ) , 
		"label" : "ChangeNodeColor"
	}
)
GafferUI.ScriptWindow.menuDefinition(application).append(
	"/WXC/tools/" + "resetVisualiserScale",
	{
		"command" : functools.partial( resetVisualiserScale ) , 
		"label" : "resetVisualiserScale"
	}
)
GafferUI.ScriptWindow.menuDefinition(application).append(
	"/WXC/tools/" + "changeToolOrientation",
	{
		"command" : functools.partial( changeToolOrientation ) , 
		"label" : "changeToolOrientation"
	}
)