from pathlib import Path
from ray_tracer.vec3 import Vector3D, Point3D, Colour, to_unit_vector, dot
from ray_tracer.ray import Ray

BASE_DIR = Path('./misc')
IMAGE_FILE_NAME = 'sphere_with_surface_normals.ppm'
OUTPUT_IMAGE_FILE = BASE_DIR.joinpath(IMAGE_FILE_NAME)


def hit_sphere(center: Point3D, radius: float, ray: Ray) -> float:
    oc: Vector3D = ray.origin - center
    a = ray.direction.l2_norm()  # dot(ray.direction, ray.direction)
    half_b = dot(ray.direction, oc)
    c = oc.l2_norm() - radius ** 2
    discriminant = half_b ** 2 - a * c
    if discriminant < 0:
        return -1
    else:
        return (- half_b - discriminant ** 0.5) / a


def ray_colour(r: Ray) -> Colour:
    sphere_centre = Point3D(0, 0, -1)
    t = hit_sphere(sphere_centre, 0.5, r)
    if t > 0:
        unit_normal_vector = to_unit_vector(r.at(t) - Vector3D(sphere_centre.x, sphere_centre.y, sphere_centre.z))
        return 0.5 * Colour(unit_normal_vector.x + 1, unit_normal_vector.y + 1, unit_normal_vector.z + 1)
    unit_direction = to_unit_vector(r.direction)
    t: float = 0.5 * (unit_direction.y + 1.0)
    colour: Vector3D = (1.0 - t) * Colour(1.0, 1.0, 1.0) + t * Colour(0.5, 0.7, 1.0)
    return Colour(colour.x, colour.y, colour.z)


def unnormalise_pixel_colour(colour: Colour) -> Colour:
    colour *= 255.999
    return Colour(int(colour.x), int(colour.y), int(colour.z))


def main() -> None:
    # Image
    aspect_ratio = 16.0 / 9.0
    image_width = 400
    image_height = int(image_width / aspect_ratio)
    max_colour = 255

    # Camera
    viewport_height = 2.0
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1.0

    origin = Point3D(0, 0, 0)
    horizontal = Vector3D(viewport_width, 0, 0)
    vertical = Vector3D(0, viewport_height, 0)
    # lower left corner coordinate vector of viewport
    # TODO add proper transformation between canvas and viewport
    lower_left_corner = origin - horizontal * 0.5 - vertical * 0.5 - Vector3D(0, 0, focal_length)

    # Render
    with open(OUTPUT_IMAGE_FILE.as_posix(), 'w') as image_file:
        image_file.write(f'P3\n{image_width} {image_height} \n{max_colour}\n')
        for j in range(image_height - 1, -1, -1):
            for i in range(0, image_width, 1):
                u = i / (image_width - 1)
                v = j / (image_height - 1)
                r = Ray(origin, lower_left_corner + u * horizontal + v * vertical - origin)
                colour = unnormalise_pixel_colour(ray_colour(r))
                image_file.write(f'{colour.x} {colour.y} {colour.z}\n')


if __name__ == "__main__":
    main()
