```vex
@N = set(0,0,1);
float angle = chf("angle");
@angle = angle;

vector axis = chv("axis");
v@axis = axis;

vector4 orientation = quaternion(radians(angle), axis);
@N = qrotate(orientation, @N);


vector up = set(0,1,0);
v@up = up;
vector4 Neworientation = quaternion(radians(angle), @N);
v@up = qrotate(Neworientation, @up);
```