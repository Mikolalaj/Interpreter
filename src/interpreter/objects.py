from abc import ABC, abstractmethod
import math


class Object(ABC):
    @abstractmethod
    def getSurfaceArea(self):
        raise NotImplementedError

    @abstractmethod
    def getVolume(self):
        raise NotImplementedError

    @abstractmethod
    def display(self):
        raise NotImplementedError


class Sphere(Object):
    def __init__(self, radius: float):
        self.radius = radius

    def getSurfaceArea(self) -> float:
        return 4 * math.pi * self.radius**2

    def getVolume(self) -> float:
        return 4 / 3 * math.pi * self.radius**3

    def display(self) -> None:
        print(f"Sphere: radius={self.radius}")

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Sphere) and self.radius == __value.radius

    def __str__(self) -> str:
        return f"Sphere: radius={self.radius}"

    def __repr__(self) -> str:
        return f"Sphere: radius={self.radius}"


class ObjectWithBaseArea(Object):
    @abstractmethod
    def getBaseArea(self):
        raise NotImplementedError


class Cuboid(ObjectWithBaseArea):
    def __init__(self, width: float, length: float, height: float):
        self.width = width
        self.length = length
        self.height = height

    def getSurfaceArea(self) -> float:
        return 2 * (self.width * self.length + self.width * self.height + self.length * self.height)

    def getVolume(self) -> float:
        return self.width * self.length * self.height

    def display(self) -> None:
        print(f"Cuboid: width={self.width} length={self.length} height={self.height}")

    def getBaseArea(self) -> float:
        return self.width * self.length

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, Cuboid)
            and self.width == __value.width
            and self.length == __value.length
            and self.height == __value.height
        )

    def __str__(self) -> str:
        return f"Cuboid: width={self.width} length={self.length} height={self.height}"

    def __repr__(self) -> str:
        return f"Cuboid: width={self.width} length={self.length} height={self.height}"


class Pyramid(ObjectWithBaseArea):
    def __init__(self, width: float, length: float, height: float):
        self.width = width
        self.length = length
        self.height = height

    def getSurfaceArea(self) -> float:
        return (
            self.width * self.length
            + self.width * math.sqrt((self.length / 2) ** 2 + self.height**2)
            + self.length * math.sqrt((self.width / 2) ** 2 + self.height**2)
        )

    def getVolume(self) -> float:
        return self.width * self.length * self.height / 3

    def getBaseArea(self) -> float:
        return self.width * self.length

    def display(self) -> None:
        print(f"Pyramid: width={self.width} length={self.length} height={self.height}")

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, Pyramid)
            and self.width == __value.width
            and self.length == __value.length
            and self.height == __value.height
        )

    def __str__(self) -> str:
        return f"Pyramid: width={self.width} length={self.length} height={self.height}"

    def __repr__(self) -> str:
        return f"Pyramid: width={self.width} length={self.length} height={self.height}"


class Cone(ObjectWithBaseArea):
    def __init__(self, radius: float, height: float):
        self.radius = radius
        self.height = height

    def getSurfaceArea(self) -> float:
        return math.pi * self.radius * (self.radius + math.sqrt(self.height**2 + self.radius**2))

    def getVolume(self) -> float:
        return math.pi * self.radius**2 * self.height / 3

    def getBaseArea(self) -> float:
        return math.pi * self.radius**2

    def display(self) -> None:
        print(f"Cone: radius={self.radius} height={self.height}")

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Cone) and self.radius == __value.radius and self.height == __value.height

    def __str__(self) -> str:
        return f"Cone: radius={self.radius} height={self.height}"

    def __repr__(self) -> str:
        return f"Cone: radius={self.radius} height={self.height}"


class Cylinder(ObjectWithBaseArea):
    def __init__(self, radius: float, height: float):
        self.radius = radius
        self.height = height

    def getSurfaceArea(self) -> float:
        return 2 * math.pi * self.radius * (self.radius + self.height)

    def getVolume(self) -> float:
        return math.pi * self.radius**2 * self.height

    def getBaseArea(self) -> float:
        return math.pi * self.radius**2

    def display(self) -> None:
        print(f"Cylinder: radius={self.radius} height={self.height}")

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Cylinder) and self.radius == __value.radius and self.height == __value.height

    def __str__(self) -> str:
        return f"Cylinder: radius={self.radius} height={self.height}"

    def __repr__(self) -> str:
        return f"Cylinder: radius={self.radius} height={self.height}"


class Tetrahedron(ObjectWithBaseArea):
    def __init__(self, edge: float):
        self.edge = edge

    def getSurfaceArea(self) -> float:
        return math.sqrt(3) * self.edge**2

    def getVolume(self) -> float:
        return math.sqrt(2) * self.edge**3 / 12

    def getBaseArea(self) -> float:
        return math.sqrt(3) * self.edge**2 / 4

    def display(self) -> None:
        print(f"Tetrahedron: edge={self.edge}")

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Tetrahedron) and self.edge == __value.edge

    def __str__(self) -> str:
        return f"Tetrahedron: edge={self.edge}"

    def __repr__(self) -> str:
        return f"Tetrahedron: edge={self.edge}"
