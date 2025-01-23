import pygame as pg
from math import cos, sin, pi
from random import uniform

def generate_stain(surf: pg.Surface, center: tuple[float, float], radius: float, color: tuple[int, int, int], max_distance: float = 0.0) -> None:
    """Paint a 'random' ink stain in the 'surf' Surface."""
    points: list[tuple[int, int]] = [ # random circle-like polygon
        (
            round(cos(i * 2 * pi / 50) * (radius - uniform(0, radius * 0.1)) + center[0]),
            round(sin(i * 2 * pi / 50) * (radius - uniform(0, radius * 0.1)) + center[1])
        )
        for i in range(50)
    ]

    rnd_circles_points: list[tuple[tuple[int, int], int]] = [ # random points to generate a circle
        (
            (
                round(cos(i * 2 * pi / 20) * (radius - uniform(radius * 0.2, radius * 0.4)) + center[0]),
                round(sin(i * 2 * pi / 20) * (radius - uniform(radius * 0.2, radius * 0.4)) + center[1])
            ),
            round(uniform(radius * 0.2, radius * 0.4))
        )
        for i in range(20)
    ]

    for _ in range(20): # Random small circles around the main stain
        ang = uniform(0, 2 * pi)
        rad = uniform(radius, max(radius, max_distance - radius * 0.1))
        rnd_circles_points.append(
            (
                (
                    round(cos(ang) * rad + center[0]),
                    round(sin(ang) * rad + center[1])
                ),
                round(uniform(radius * 0.01, radius * 0.1))
            )
        )
    
    pg.draw.polygon(surf, color, points)
    for i in rnd_circles_points:
        pg.draw.circle(surf, color, i[0], i[1])
