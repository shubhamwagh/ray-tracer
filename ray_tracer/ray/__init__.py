from dataclasses import dataclass
from ray_tracer.vec3 import Vector3D, Point3D
from vec3 import Vector3D


@dataclass
class Ray:
    """
    P(t) = A + t * b
    """
    origin: Point3D
    direction: Vector3D

    def at(self, t: float) -> Point3D:
        p = self.origin + t * self.direction
        return Point3D(p.x, p.y, p.z)
