from pathlib import Path
from ray_tracer.vec3 import Vector3D, Point3D, Colour, to_unit_vector, dot
from ray_tracer.ray import Ray

BASE_DIR = Path('./misc')
IMAGE_FILE_NAME = 'red_sphere_in_background.ppm'
OUTPUT_IMAGE_FILE = BASE_DIR.joinpath(IMAGE_FILE_NAME)


def hit_sphere(center: Point3D, radius: float, ray: Ray) -> bool:
    oc: Vector3D = ray.origin - center
    a = dot(ray.direction, ray.direction)
    b = 2 * dot(ray.direction, oc)
    c = dot(oc, oc) - radius ** 2
    discriminant = b ** 2 - 4 * a * c
    return discriminant > 0


def ray_colour(r: Ray) -> Colour:
    if hit_sphere(Point3D(0, 0, -1), 0.5, r):
        return Colour(1, 0, 0)
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
