import pymel.core as pm
import sys

tl_path = '//storage1.of3d.com/tankprojects/ofLibrary/lgtLib/tools&plugins/hq_yongzhicheng_movie/light_tools/light_tools'
if tl_path not in sys.path:
    sys.path.append(tl_path)

from via import light_type_list




def light_invert():
    global visible_light
    if ('visible_light' in locals() or 'visible_light' in globals()) and len(visible_light) != 0:
        pm.showHidden(visible_light)
        visible_light = []
    
    else:
        visible_light = []
        for light_type in light_type_list:
            sl = pm.ls(type=light_type)
            for element_sl in sl:
                tfm = pm.listTransforms(element_sl)[0]
                if pm.getAttr('%s.visibility' % tfm) == 1 and pm.getAttr('%s.visibility' % element_sl) == 1:
                    visible_light.append(tfm)
    
        lgt = []
        sl_lgt = pm.ls(sl=1)
        for i in sl_lgt:
            if pm.getAttr('%s.visibility' % i) == 1:
                lgt.append(i)
    
        for i in lgt:
            visible_light.remove(i)
    
        pm.hide(visible_light)


