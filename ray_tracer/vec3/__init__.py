from __future__ import annotations
from dataclasses import dataclass
from typing import Union


# Exceptions and Errors for Vector class

class VectorIndexError(IndexError):
    def __init__(self, message):
        super(VectorIndexError, self).__init__(message)


class VectorTypeError(TypeError):
    def __init__(self, message):
        super(VectorTypeError, self).__init__(message)


# Base Vector class

@dataclass
class Vector:
    v1: Union[int, float] = 0.0
    v2: Union[int, float] = 0.0
    v3: Union[int, float] = 0.0

    @property
    def x(self) -> Union[int, float]:
        return self.v1

    @property
    def y(self) -> Union[int, float]:
        return self.v2

    @property
    def z(self) -> Union[int, float]:
        return self.v3

    def __neg__(self) -> Vector:
        return Vector(-self.v1, -self.v2, -self.v3)

    def __getitem__(self, index: int) -> Union[float, int]:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise VectorIndexError("vector out of range")

    def __len__(self) -> int:
        return 3

    def __add__(self, other: Vector) -> Vector:
        assert isinstance(other, Vector)
        return Vector(self.v1 + other.v1, self.v2 + other.v2, self.v3 + other.v3)

    def __sub__(self, other: Vector) -> Vector:
        assert isinstance(other, Vector)
        return Vector(self.v1 - other.v1, self.v2 - other.v2, self.v3 - other.v3)

    def __mul__(self, other: Union[Vector, int, float]) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.v1 * other.v1, self.v2 * other.v2, self.v3 * other.v3)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector(self.v1 * other, self.v2 * other, self.v3 * other)
        else:
            raise VectorTypeError("Input must be Vector, int or float")

    def __rmul__(self, other: Union[Vector, float, int]) -> Vector:
        return self * other

    def __truediv__(self, other: Union[Vector, float, int]) -> Vector:
        return (1.0 / other) * self

    def __iadd__(self, other: Vector) -> Vector:
        assert isinstance(other, Vector)
        self.v1 += other.v1
        self.v2 += other.v2
        self.v3 += other.v3
        return self

    def __imul__(self, other: Union[float, int]) -> Vector:
        self.v1 *= other
        self.v2 *= other
        self.v3 *= other
        return self

    def __itruediv__(self, other: Union[float, int]) -> Vector:
        return self.__imul__(1.0 / other)

    def print_vector(self) -> None:
        print(f'{self.v1} {self.v2} {self.v3}')

    def l2_norm_squared(self) -> float:
        return self.v1 ** 2 + self.v2 ** 2 + self.v3 ** 2

    def l2_norm(self) -> float:
        return self.l2_norm_squared() ** 0.5


# Type aliases for Vector

class Point3D(Vector):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super(Point3D, self).__init__(x, y, z)


class Colour(Vector):
    def __init__(self, r=0.0, g=0.0, b=0.0):
        super(Colour, self).__init__(r, g, b)


# Utility functions

def dot(u: Vector, v: Vector) -> Union[int, float]:
    return u.x * v.x + u.y * v.y + u.z * v.z


def cross(u: Vector, v: Vector) -> Vector:
    return Vector(u[1] * v[2] - u[2] * v[1],
                  u[2] * v[0] - u[0] * v[2],
                  u[0] * v[1] - u[1] * v[0])


def to_unit_vector(v: Vector) -> Vector:
    return v / v.l2_norm()
