a = root['ImageReader']['out']["metadata"].getValue()
b = list(set(a.keys()))
c = [value for value in b if isinstance(value, str) and "RGBA_" in value]
d = []
for i in c:
	i = i.split("/")[-2]
	d.append(i)
e = list(set(d))
print(e)
