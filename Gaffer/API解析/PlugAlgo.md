# Gaffer.PlugAlgo
## replacePlug
```python
GAFFER_API void replacePlug( GraphComponent *parent, PlugPtr plug );
#
#把Plug插头替换到GraphComponent上
Gaffer.PlugAlgo.replacePlug(root['Box1'],root['Box']['out'])
```
![](/png/Gif/Peek%202024-01-17%2016-04.gif)

## dependsOnCompute
```python
GAFFER_API bool dependsOnCompute( const ValuePlug *plug );
#返回一个bool值如果plug的值由输出提供则为true
Gaffer.PlugAlgo.dependsOnCompute(root['MultiplyColor']['parameters']['a'])
```
![](/png/Gif/Peek%202024-01-17%2016-10.gif)
## createPlugFromData
```python
GAFFER_API ValuePlugPtr createPlugFromData( const std::string &name, Plug::Direction direction, unsigned flags, const IECore::Data *value );
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
![](/png/Gif/Peek%202024-01-17%2022-24.gif)
## getValueAsData
```python
GAFFER_API IECore::DataPtr getValueAsData( const ValuePlug *plug );
#返回plug数值
Gaffer.PlugAlgo.getValueAsData(root['Node']['stringName'])
```
![](/png/Gif/Peek%202024-01-17%2022-28.gif)
## setValueFromData
```python
GAFFER_API bool setValueFromData( ValuePlug *plug, const IECore::Data *value );
#设置plug数值，返回一个bool值（true or false）
Gaffer.PlugAlgo.setValueFromData(root['Box']['StringPlug'],IECore.StringData("a"))
```
![](/png/Gif/Peek%202024-01-18%2017-05.gif)
```python
#还是设置plug数值
GAFFER_API bool setValueFromData( const ValuePlug *plug, ValuePlug *leafPlug, const IECore::Data *value );
Gaffer.PlugAlgo.setValueFromData(root['Flat']['parameters']['color'],root['Flat']['parameters']['color']["r"],IECore.Color3fData(imath.Color3f( 0.1, 0.1, 0.1 )))
```
![](/png/Gif/Peek%202024-01-18%2017-44.gif)
## canSetValueFromData
```python
GAFFER_API bool canSetValueFromData( const ValuePlug *plug, const IECore::Data *value = nullptr );
#如果可以从 Data 中设置给定插头的值，则返回 true
Gaffer.PlugAlgo.canSetValueFromData(root['Flat']['parameters']['color'])
Gaffer.PlugAlgo.canSetValueFromData(root['Flat']['parameters']['color'],IECore.StringData())
```
![](/png/Gif/Peek%202024-01-18%2017-49.gif)
## canPromote
```python
GAFFER_API bool canPromote( const Plug *plug, const Plug *parent = nullptr );
#如果调用 'promote（ plug， parent ）' 将
#成功，否则为 false。
Gaffer.PlugAlgo.canPromote(root['Box']['OSLObject']['in'])
```
![](/png/Gif/Peek%202024-01-29%2020-32.gif)
## promote
```python
GAFFER_API Plug *promote( Plug *plug, Plug *parent = nullptr, const IECore::StringAlgo::MatchPattern &excludeMetadata = "layout:*" );
#提升内部插头，返回新创建的外部插头。
Gaffer.PlugAlgo.promote(root['Box']['OSLObject']['in'])
```
![](/png/Gif/Peek%202024-01-29%2020-37.gif)
## promoteWithName
```python
GAFFER_API Plug *promoteWithName( Plug *plug, const IECore::InternedString &name, Plug *parent = nullptr, const IECore::StringAlgo::MatchPattern &excludeMetadata = "layout:*" );
#作为“promote”，但通过提供 name 参数，您可以跳过额外的
#升级后重命名步骤
Gaffer.PlugAlgo.promoteWithName(root['Box']['OSLObject']['useTransform'],IECore.InternedString("test"))
```
![](/png/Gif/Peek%202024-01-29%2020-52.gif)
## unpromote
```python
GAFFER_API void unpromote( Plug *plug );
#取消升级以前升级的插件，删除
#尽可能使用外部插头。
Gaffer.PlugAlgo.unpromote(root['Box']['OSLObject']['useTransform'])
```
![](/png/Gif/Peek%202024-01-29%2020-55.gif)