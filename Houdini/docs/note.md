# 3D Viewports

1. 视窗通过鼠标旋转缩放位移的时候，很不习惯，即使选择保持中心旋转，有时候也会出现一些问题，比如怎么旋转位移都转不到自己想看到的面。

>  1. 首先，在3D视图的右上角，点击显示选项按钮，选择`Guides`选项卡，勾选`View pivot`。
>  2. `Edit` ▸ `Preferences` ▸ `3D Viewports` and click `Maintain viewport pivot when panning`.
>  3. `Edit` ▸ `Preferences` ▸ `3D Viewports` and turn on `Automatically set view pivot on selection`.

# 模块

SOP_Geometry

mat_VOP_shader

rop_render_cache_export

dop_dynamic

chop_keyframe

top_PDG_automatic

shop_old_shader_plugins

lop_USD

cop2_composite

# group

![](/png/houdini/Snipaste_2024-02-12_22-12-25.png)

# 求一段管状模型的圆心轴

![alt text](../../png/houdini/Snipaste_2024-02-13_02-42-26.png)

通过groupexpend的step属性步进式的环选择管状模型的点，然后通过fuse焊接每一个环的点，求出中心点，通过add连接成线条。