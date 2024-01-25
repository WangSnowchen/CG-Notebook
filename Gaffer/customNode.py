import Gaffer
import GafferScene
import GafferArnold
import ofUsdGaffer
import ofNode
import GafferOSL
import GafferUI
import IECore
import imath

from ofUsdGaffer import manageRenderQuality
from ofUsdGaffer import manageLightSetup
from ofUsdGaffer import manageLightBlockers
from ofUsdGaffer import manageArnoldAovs
from ofUsdGaffer import manageObjectSets

print("Custom Node Imported")

def __setBoxPlugUI(node):
    Gaffer.Metadata.registerValue(node, "noduleLayout:customGadget:addButtonTop:visible",False)
    Gaffer.Metadata.registerValue(node, "noduleLayout:customGadget:addButtonBottom:visible",False)
    Gaffer.Metadata.registerValue(node, "noduleLayout:customGadget:addButtonLeft:visible",False)
    Gaffer.Metadata.registerValue(node, "noduleLayout:customGadget:addButtonRight:visible",False)
def __setNodeUIColor(node,r,g,b):
    Gaffer.Metadata.registerValue( node, "nodeGadget:color", imath.Color3f( [r,g,b] ) )

def ofCenterControl():
    return Gaffer.Node("of_Center_Control")
def ofCenterControlPostCreator(node,menu):
    Gaffer.Metadata.registerValue(node, 'description', '修改节点、节点连接线、节点注释的颜色工具' )
    node['user'].addChild(Gaffer.StringPlug("Preview_Target",defaultValue = 'proxy'))
    Gaffer.Metadata.registerValue(node["user"]["Preview_Target"], 'description','显示模式')
    Gaffer.Metadata.registerValue(node["user"]["Preview_Target"], 'plugValueWidget:type', 'GafferUI.PresetsPlugValueWidget')
    Gaffer.Metadata.registerValue(node["user"]["Preview_Target"], 'preset:Proxy','proxy')
    Gaffer.Metadata.registerValue(node["user"]["Preview_Target"], 'preset:Render','render')
    node['user'].addChild(Gaffer.StringPlug("Switch"))
    Gaffer.Metadata.registerValue(node["user"]["Switch"], 'description', '点击切换')
    Gaffer.Metadata.registerValue(node["user"]["Switch"], 'plugValueWidget:type', 'GafferUI.ButtonPlugValueWidget' )
    Gaffer.Metadata.registerValue(node["user"]["Switch"], 'buttonPlugValueWidget:clicked',
    """
root = plug.node().scriptNode()
PreviewTarget = root['of_Center_Control']['user']['Preview_Target'].getValue()
root['CommonEdits']['PurposeVisibility']['previewTarget'].setValue(PreviewTarget)
    """
    )
    Gaffer.Metadata.registerValue(node["user"]["Switch"], 'layout:accessory', True )
    node['user'].addChild(Gaffer.Color3fPlug("connectionsColor",defaultValue = imath.Color3f( 1, 1, 1 )))
    Gaffer.Metadata.registerValue(node["user"]["connectionsColor"], 'description', '连接线颜色' )
    node['user'].addChild(Gaffer.BoolPlug("Set_connections_color"))
    Gaffer.Metadata.registerValue(node["user"]["Set_connections_color"], 'plugValueWidget:type', 'GafferUI.ButtonPlugValueWidget' )
    Gaffer.Metadata.registerValue(node["user"]["Set_connections_color"], 'divider', False )
    Gaffer.Metadata.registerValue(node["user"]["Set_connections_color"], 'layout:accessory', True )
    Gaffer.Metadata.registerValue(node["user"]["Set_connections_color"], 'description', '设置连接线颜色' )
    Gaffer.Metadata.registerValue(node["user"]["Set_connections_color"], 'buttonPlugValueWidget:clicked',
    """
import imath
root = plug.node().scriptNode()
colorValue = root['of_Center_Control']['user']['connectionsColor'].getValue()
for node in root.selection():
    nodeName = node.getChild('in')
    Gaffer.Metadata.registerValue( nodeName, "connectionGadget:color", imath.Color3f(colorValue[0], colorValue[1], colorValue[2]))
    """
    )
    node['user'].addChild(Gaffer.Color3fPlug("nodeColor", defaultValue = imath.Color3f( 1, 1, 1 ) ) )
    Gaffer.Metadata.registerValue(node["user"]["nodeColor"], 'description', '节点颜色' )
    node['user'].addChild(Gaffer.BoolPlug("Set_node_color"))
    Gaffer.Metadata.registerValue(node["user"]["Set_node_color"], 'plugValueWidget:type', 'GafferUI.ButtonPlugValueWidget' )
    Gaffer.Metadata.registerValue(node["user"]["Set_node_color"], 'layout:accessory', True )
    Gaffer.Metadata.registerValue(node["user"]["Set_node_color"], 'description', '设置节点颜色' )
    Gaffer.Metadata.registerValue(node["user"]["Set_node_color"], 'buttonPlugValueWidget:clicked',
    """
import imath
root = plug.node().scriptNode()
colorValue = root['of_Center_Control']['user']['nodeColor'].getValue()
nodeName = root.selection()
for node in nodeName:
    Gaffer.Metadata.registerValue( node, "nodeGadget:color", imath.Color3f(colorValue[0], colorValue[1], colorValue[2]) )
    """
    )
    node['user'].addChild(Gaffer.Color3fPlug("Annotate_Color", defaultValue = imath.Color3f( 1, 1, 1 ) ) )
    Gaffer.Metadata.registerValue(node["user"]["Annotate_Color"], 'description', '节点注释颜色' )
    node['user'].addChild(Gaffer.StringPlug("Annotate_str"))
    Gaffer.Metadata.registerValue(node["user"]["Annotate_str"], 'description', '输入注释内容' )
    node['user'].addChild(Gaffer.StringPlug("Type",defaultValue = '0'))
    Gaffer.Metadata.registerValue(node["user"]["Type"], 'description', '注释行' )
    Gaffer.Metadata.registerValue(node["user"]["Type"], 'plugValueWidget:type', 'GafferUI.PresetsPlugValueWidget' )
    Gaffer.Metadata.registerValue(node["user"]["Type"], 'preset:check01', '0' )
    Gaffer.Metadata.registerValue(node["user"]["Type"], 'preset:check02', '1' )
    Gaffer.Metadata.registerValue(node["user"]["Type"], 'preset:check03', '2' )
    Gaffer.Metadata.registerValue(node["user"]["Type"], 'preset:check04', '3' )
    node['user'].addChild(Gaffer.BoolPlug("ADD"))
    Gaffer.Metadata.registerValue(node["user"]["ADD"], 'description', '添加注释' )
    Gaffer.Metadata.registerValue(node["user"]["ADD"], 'plugValueWidget:type', 'GafferUI.ButtonPlugValueWidget' )
    Gaffer.Metadata.registerValue(node["user"]["ADD"], 'buttonPlugValueWidget:clicked',
    """
import imath
root = plug.node().scriptNode()
stdName = root['of_Center_Control']['user']['Type'].getValue()
AnnotateStr = root['of_Center_Control']['user']['Annotate_str'].getValue()
colorValue = root['of_Center_Control']['user']['Annotate_Color'].getValue()
nodeName = root.selection()
for node in nodeName:
    Gaffer.MetadataAlgo.addAnnotation( node, stdName, Gaffer.MetadataAlgo.Annotation( AnnotateStr, imath.Color3f(colorValue[0], colorValue[1], colorValue[2]))
    """
    )
    node['user'].addChild(Gaffer.BoolPlug("REMOVE"))
    Gaffer.Metadata.registerValue(node["user"]["REMOVE"], 'description', '删除注释' )
    Gaffer.Metadata.registerValue(node["user"]["REMOVE"], 'plugValueWidget:type', 'GafferUI.ButtonPlugValueWidget' )
    Gaffer.Metadata.registerValue(node["user"]["REMOVE"], 'divider', True )
    Gaffer.Metadata.registerValue(node["user"]["REMOVE"], 'buttonPlugValueWidget:clicked',
    """
root = plug.node().scriptNode()
nodeName = root.selection()
stdName = root['of_Center_Control']['user']['Type'].getValue()
for node in nodeName:
    Gaffer.MetadataAlgo.removeAnnotation( node, stdName ) 
    """
    )
    node['user'].addChild(Gaffer.BoolPlug("Open_Project_File"))
    Gaffer.Metadata.registerValue(node["user"]["Open_Project_File"], 'plugValueWidget:type', 'GafferUI.ButtonPlugValueWidget' )
    Gaffer.Metadata.registerValue(node["user"]["Open_Project_File"], 'buttonPlugValueWidget:clicked',
    """
import subprocess
import os
root = plug.node().scriptNode()
currentFilePath = root['fileName'].getValue()
currentFilePath = os.path.dirname(currentFilePath)
subprocess.Popen('gio open "%s"' % currentFilePath, shell=True)
    """
    )
    Gaffer.Metadata.registerValue(node["user"]["Open_Project_File"], 'description', '' )
    
    __setNodeUIColor(node,0.38,0.20,0.27)

def lightFogZ():
    return Gaffer.Box("Fog_Z")
def lightFogZPostCreator(node,menu):

    node.addChild(GafferScene.ShaderAssignment("ShaderAssignment"))
    node.addChild(GafferArnold.ArnoldShader( "Matte" ))
    node.addChild(GafferScene.PathFilter( "PathFilter" ))
    node.addChild(GafferScene.PathFilter( "PathFilter1" ))
    node.addChild(GafferScene.Prune( "Prune" ))
    node.addChild(GafferArnold.ArnoldAtmosphere( "ArnoldAtmosphere" ))
    node.addChild(GafferArnold.ArnoldShader( "Fog" ))

    node['Matte'].loadShader( "matte" )
    node['Fog'].loadShader( "fog" )
    node['ShaderAssignment']['shader'].setInput(node['Matte']['out'])
    node['ShaderAssignment']['filter'].setInput(node['PathFilter1']['out'])
    node['Prune']['in'].setInput(node['ShaderAssignment']['out'])
    node['Prune']['filter'].setInput(node['PathFilter']['out'])
    node['ArnoldAtmosphere']['in'].setInput(node['Prune']['out'])
    node['ArnoldAtmosphere']['shader'].setInput(node['Fog']['out'])

    node['Fog']['parameters']['height'].setValue(0)
    node['PathFilter1']['paths'].setValue(IECore.StringVectorData(["..."]))

    ofUsdGaffer.unpack_box_node(node)

def pointVisualizer():
    return Gaffer.Box("Point_Visualizer")
def pointVisualizerPostCreator(node,menu):
    __setBoxPlugUI(node)
    __setNodeUIColor(node,0.38,0.20,0.27)

    node.addChild(GafferScene.MeshToPoints( "MeshToPoints" ))
    node.addChild(GafferOSL.OSLObject( "OSLObject" ))
    node.addChild(GafferScene.DeletePoints( "DeletePoints" ))
    node.addChild(GafferScene.OpenGLAttributes())
    node.addChild(GafferScene.Parent( "Parent" ))
    node.addChild(GafferScene.PathFilter( "PathFilter" ))
    node.addChild(GafferOSL.OSLCode( "OSLCode" ))
    node.addChild(Gaffer.Dot( "Dot" ))

    node['OSLObject']['primitiveVariables'].addChild(Gaffer.NameValuePlug( "customInt", Gaffer.IntPlug()))
    node['OSLObject']['primitiveVariables']['NameValuePlug']['name'].setValue('deletePoints')
    node['OSLCode']['parameters'].addChild(Gaffer.IntPlug( "vertexIndex",defaultValue = 0))
    node['OSLCode']['out'].addChild(Gaffer.IntPlug( "deletePoints", direction = Gaffer.Plug.Direction.Out, defaultValue = 0))
    node["MeshToPoints"]["adjustBounds"].setValue( False )
    node['DeletePoints']['adjustBounds'].setValue( False )
    node["OpenGLAttributes"]["attributes"]["pointsPrimitiveGLPointWidth"]["value"].setValue( 60.0 )
    node["OpenGLAttributes"]["attributes"]["pointsPrimitiveGLPointWidth"]["enabled"].setValue( True )
    node["Parent"]["parent"].setValue( '/' )
    node["OSLCode"]["code"].setValue(
        """
int shadingIndex;
getattribute( "shading:index", shadingIndex );
deletePoints = shadingIndex != vertexIndex;
        """
    )

    node['Dot'].setup(GafferScene.ScenePlug("in"))
    node['MeshToPoints']['in'].setInput(node['Dot']['out'])
    node['OSLObject']['in'].setInput(node['MeshToPoints']['out'])
    node['DeletePoints']['in'].setInput(node['OSLObject']['out'])
    node['OpenGLAttributes']['in'].setInput(node['DeletePoints']['out'])
    node['Parent']['in'].setInput(node['Dot']['out'])
    node['Parent']['children']['child0'].setInput(node['OpenGLAttributes']['out'])
    node["OSLObject"]["primitiveVariables"]["NameValuePlug"]["value"].setInput(node["OSLCode"]["out"]["deletePoints"] )
    node["MeshToPoints"]["filter"].setInput( node["PathFilter"]["out"] )
    node["OSLObject"]["filter"].setInput( node["PathFilter"]["out"] )
    node["OpenGLAttributes"]["filter"].setInput( node["PathFilter"]["out"] )
    node["DeletePoints"]["filter"].setInput( node["PathFilter"]["out"] )

    Gaffer.PlugAlgo.promote(node['Dot']['in'])
    Gaffer.PlugAlgo.promote(node['OSLCode']['parameters']['vertexIndex'])
    Gaffer.PlugAlgo.promote(node['Parent']['out'])
    Gaffer.PlugAlgo.promote(node['PathFilter']['paths'])

def lightSettingTemplate():
    return Gaffer.Box("Light_Setting_Template")
def lightSettingTemplatePostCreator(node,menu):
    #渲染器设置
    arnoldOptions = GafferArnold.ArnoldOptions("ArnoldOptions")
    node.addChild(arnoldOptions)
    Gaffer.NodeAlgo.applyUserDefaults( arnoldOptions )
    #添加灯光雾
    arnoldAtmosphere = GafferArnold.ArnoldAtmosphere("ArnoldAtmosphere")
    node.addChild(arnoldAtmosphere)
    atmosphereShader = GafferArnold.ArnoldShader("AtmosphereVolume")
    node.addChild(atmosphereShader)
    atmosphereShader.loadShader( "atmosphere_volume" )
    arnoldAtmosphere['shader'].setInput(atmosphereShader['out'])
    arnoldAtmosphere['in'].setInput(arnoldOptions['out'])
    arnoldAtmosphere['enabled'].setValue(False)
    #添加渲染质量切换
    manager = manageRenderQuality.RenderQualityManager()
    renderQuality = manager.container()
    node.addChild(renderQuality)
    renderQuality['in'].setInput(arnoldAtmosphere['out'])
    #添加灯光设置
    lightSetup = manageLightSetup.LightSetupManager()
    lightContainer = lightSetup.container()
    node.addChild(lightContainer)
    lightContainer['in'].setInput(renderQuality['out'])
    #添加默认domeLight HDR贴图
    manageLightSetup.create_image_shader(lightContainer)
    #添加path过滤
    pathFilter = GafferScene.PathFilter("PathFilter")
    node.addChild(pathFilter)
    node['ShaderTweaks']['filter'].setInput(pathFilter['out'])
    #添加blocker
    blockerSetup = manageLightBlockers.LightBlockerManager()
    blockerContainer = blockerSetup.container()
    node.addChild(blockerContainer)
    blockerContainer['in'].setInput(node['ShaderTweaks']['out'])
    #添加AOV
    aovSetup = manageArnoldAovs.ArnoldAovManager()
    aovContainer = aovSetup.container()
    node.addChild(aovContainer)
    aovContainer['in'].setInput(blockerContainer['out'])
    #CreateCoordinateSystems
    createLocators = ofNode.processorNodes.CoordinateSystemCreator( "CreateCoordinateSystems" )
    node.addChild(createLocators)
    createLocators['in'].setInput(aovContainer['out']) 
    #SetupAimConstraints
    aimConstraints = ofNode.processorNodes.SetupAimConstraints( "SetupAimConstraints" )
    node.addChild(aimConstraints)
    aimConstraints['in'].setInput(createLocators['out'])
    #CreateObjectSets
    objectSetSetup = manageObjectSets.ObjectSetManager()
    objectSetContainer = objectSetSetup.container()
    node.addChild(objectSetContainer)
    objectSetContainer['in'].setInput(aimConstraints['out'])
    #StandardOptions
    node.addChild(GafferScene.StandardOptions("StandardOptions"))
    node['StandardOptions']['in'].setInput(objectSetContainer['out'])
    ofUsdGaffer.unpack_box_node(node)

def filterResults():
    return GafferScene.FilterResults("FilterResults")
def filterResultsPostCreator(node,menu):
    node.setName("FilterResults")







## UI
pathName = "/Wangxuechen"
nodeMenu = GafferUI.NodeMenu.acquire( application )
##Utility
nodeMenu.append(
    path = pathName+"/Utility/Center_Control", 
    nodeCreator = ofCenterControl, 
    postCreator = ofCenterControlPostCreator, 
    searchText = "Center_Control" 
)

nodeMenu.append(
    path = pathName+"/Utility/Point_Visualizer", 
    nodeCreator = pointVisualizer, 
    postCreator = pointVisualizerPostCreator, 
    searchText = "Point_Visualizer" 
)

nodeMenu.append(
    path = pathName+"/Utility/Filter_Results", 
    nodeCreator = filterResults, 
    postCreator = filterResultsPostCreator, 
    searchText = "Filter_Results" 
)
##Template
nodeMenu.append(
    path = pathName+"/Template/Light_Setting_Template", 
    nodeCreator = lightSettingTemplate, 
    postCreator = lightSettingTemplatePostCreator, 
    searchText = "light_setting_template" 
)
##Light
nodeMenu.append(
    path = pathName+"/Light/Light_Fog_Z", 
    nodeCreator = lightFogZ, 
    postCreator = lightFogZPostCreator, 
    searchText = "Fog_Z" 
)