import pymel.core as pm
import os

def getdir():
	# full_Path = pm.renderSettings(firstImageName = 1,fullPathTemp = 1)[0]
	# dir = full_Path.replace('\\','/')
	# dir = dir.split('/')
	# dir.pop()
	# new_dir = '/'.join(dir)
	# os.startfile(new_dir)

	#author = wuxiaomeng
	from lightToolkitMayaUtil import getRenderImageDir as Renderimage
	Renderimage.get_render_image_dir()
