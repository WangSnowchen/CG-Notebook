r = 1
g = 0.59
b = 0.37
##在有色彩空间的情况下，v值默认情况下是0.822
v = 0.822
mayaIntensity = 1
nukeIntensity = 2
 
cmax = max(r,g,b)
cmin = min(r,g,b)
delta = cmax-cmin
if delta == 0:
    h = 0
elif cmax == r:
    h = ((g-b)/delta)%6
elif cmax == g:
    h = (b-r)/delta+2
else:
    h = (r-g)/delta+4
finalNukeIntensity = mayaIntensity * nukeIntensity
 
h = "{:.2f}".format(h * 60)
s = "{:.2f}".format(0 if cmax == 0 else (delta / cmax) - 0.1)
v = "{:.2f}".format(v)
print(h,s,v,finalNukeIntensity)