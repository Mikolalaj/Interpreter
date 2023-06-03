from objects import Cuboid


cube = Cuboid(width=2, height=3, length=4)
objectType = type(cube)
print(objectType.__bases__)
