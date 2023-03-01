from abc import ABC, abstractmethod
from dataclasses import dataclass

from ray_tracer.vec3 import Vector3D, Point3D, dot
from ray_tracer.ray import Ray


@dataclass
class HitRecord:
    point: Point3D = Point3D(0.0, 0.0, 0.0)
    normal: Vector3D = Vector3D(0.0, 0.0, 0.0)
    t: float = 0.0
    front_face: bool = False

    def set_face_normal(self, ray: Ray, outward_normal: Vector3D):
        self.front_face = dot(ray.direction, outward_normal) < 0.0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable(ABC):

    @abstractmethod
    def hit(self, ray: Ray, t_min: float, t_max: float, hit_rec: HitRecord) -> bool:
        pass
