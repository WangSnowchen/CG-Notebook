#节点上添加一个按钮，点击即可获取当前文件夹下最新一张图片并显示在节点上。
root = plug.node().scriptNode()
import os
folder_path = '/mnt/proj/pj2023dy001/sequences/s9010/s9010_0030/lighting/review'
def get_latest_image(folder):
    images = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith((".png", ".jpg", ".jpeg"))]
    latest_image = max(images, key=os.path.getctime)
    return latest_image
    
latest_image_path = get_latest_image(folder_path)
a = (f'<img src="{latest_image_path}" alt="" width="300">')
Gaffer.Metadata.registerValue( root['Node'], 'description', a )