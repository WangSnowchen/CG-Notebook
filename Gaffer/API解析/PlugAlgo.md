## replacePlug
```python
GAFFER_API void replacePlug( GraphComponent *parent, PlugPtr plug );
#
#把Plug插头替换到GraphComponent上
Gaffer.PlugAlgo.replacePlug(root['Box1'],root['Box']['out'])
```
## dependsOnCompute
```python
GAFFER_API bool dependsOnCompute( const ValuePlug *plug );
#返回一个bool值如果plug的值由输出提供则为true
Gaffer.PlugAlgo.dependsOnCompute(root['MultiplyColor']['parameters']['a'])
```
## createPlugFromData
```python
GAFFER_API ValuePlugPtr createPlugFromData( const std::string &name, Plug::Direction direction, unsigned flags, const IECore::Data *value );
---
#创建plug来保存指定的数据
##################
#IECore.BoolData() )
#IECore.FloatData() )
#IECore.IntData() )
#IECore.BoolVectorData() )
#IECore.FloatVectorData() )
#IECore.IntVectorData() )
#IECore.StringData() )
#IECore.StringVectorData() )
#IECore.InternedStringVectorData() )
#IECore.Color4fData() )
#IECore.Color3fData() )
#IECore.V3fData() )
#IECore.V2fData() )
#IECore.V3iData() )
#IECore.V2iData() )
#IECore.Box3fData() )
#IECore.Box2fData() )
#IECore.Box3iData() )
#IECore.Box2iData() )
#IECore.M44fData() )
#################
#为节点创建自定义插头
valuePlug = Gaffer.PlugAlgo.createPlugFromData("stringName",Gaffer.Plug.Direction.In,Gaffer.Plug.Flags.Default,IECore.StringVectorData( ["1","2"] ))
root['Node'].addChild(valuePlug)
```