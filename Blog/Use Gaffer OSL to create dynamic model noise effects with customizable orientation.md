# Use Gaffer OSL to create dynamic model noise effects with customizable orientation.

![alt text](<../../png/GafferPng/GIF 2024-3-11 22-02-16.gif>)

The inspiration came when I was using VOP to connect nodes in houdini and realized that there are nodes similar to AA noise in the OSL section in Gaffer, 'PointNoise'.  
![alt text](../../png/GafferPng/Snipaste_2024-03-11_22-12-22.png)

So I made the whole noise move with time by doing a noise process on the X and Z vectors of the P attribute and replacing the Y vector with a Time float in Global.  
![alt text](../../png/GafferPng/Snipaste_2024-03-11_22-13-13.png)

Then control the area where the noise is generated by doing a Remap on the Y vector on the P attribute alone.  
![alt text](../../png/GafferPng/Snipaste_2024-03-11_22-13-49.png)

This is then added to the default P property to get the effect we want.  
![alt text](../../png/GafferPng/Snipaste_2024-03-11_22-14-23.png)
