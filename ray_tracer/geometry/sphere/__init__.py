from ray_tracer.vec3 import Point3D, Vector3D, dot
from ray_tracer.ray import Ray
from ray_tracer.hittable import Hittable, HitRecord


class Sphere(Hittable):
    def __init__(self, centre: Point3D, radius: float):
        super(Sphere, self).__init__()
        self.centre = centre
        self.radius = radius

    def hit(self, ray: Ray, t_min: float, t_max: float, hit_rec: HitRecord) -> bool:
        oc = ray.origin - self.centre
        a = ray.direction.l2_norm()
        half_b = dot(oc, ray.direction)
        c = oc.l2_norm() - self.radius ** 2

        discriminant = half_b ** 2 - a * c
        if discriminant < 0:
            return False

        sqrt_discriminant = discriminant ** 0.5
        root = (- half_b - sqrt_discriminant) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrt_discriminant) / a
            if root < t_min or root > t_max:
                return False

        hit_rec.t = root
        hit_rec.point = ray.at(hit_rec.t)
        outward_normal = (hit_rec.point - self.centre) / self.radius
        hit_rec.set_face_normal(ray, outward_normal)
        return True
