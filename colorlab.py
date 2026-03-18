"""
colorlab, a color manipulation and conversion library.

Supported color spaces:
* sRGB
* Linear RGB
* Oklab
"""

import math

class Rgb:
    def __init__(self, red: int, green: int, blue: int):
        """
        Type for sRGB,
        uses integers from 0-255 to represent each color channel
        """
        self.red = red
        self.green = green
        self.blue = blue

class LinearRgb:
    def __init__(self, red: float, green: float, blue: float):
        """Linear float representation of RGB."""
        self.red = red
        self.green = green
        self.blue = blue

    @staticmethod
    def from_srgb(input_rgb: Rgb):
        """Convert from sRGB to linear RGB using the standard sRGB EOTF."""
        def to_linear(channel: int) -> float:
            c = channel / 255.0
            if c <= 0.04045:
                return c / 12.92
            return ((c + 0.055) / 1.055) ** 2.4

        red = to_linear(input_rgb.red)
        green = to_linear(input_rgb.green)
        blue = to_linear(input_rgb.blue)
        return LinearRgb(red, green, blue)

class Oklab:
    def __init__(self, lightness: float, a: float, b: float):
        """Type for oklab color space."""
        self.lightness = lightness
        self.a = a
        self.b = b

    @staticmethod
    def from_srgb(rgb: Rgb):
        linear_rgb = LinearRgb.from_srgb(rgb)

        # Adjust colors to account for human perception
        l = (0.4122214708 * linear_rgb.red + 0.5363325363 * linear_rgb.green +
            0.0514459929 * linear_rgb.blue)
        m = (0.2119034982 * linear_rgb.red + 0.6806995451 * linear_rgb.green +
            0.1073969566 * linear_rgb.blue)
        s = (0.0883024619 * linear_rgb.red + 0.2817188376 * linear_rgb.green +
            0.6299787005 * linear_rgb.blue)
        
        # Cube root color channels
        root_l = math.cbrt(l)
        root_m = math.cbrt(m)
        root_s = math.cbrt(s)

        # Convert cube rooted color channels to oklab color space
        oklab_lightness = (0.2104542553 * root_l + 0.7936177850 *
                           root_m - 0.0040720468 * root_s)
        oklab_a = (1.9779984951 * root_l - 2.4285922050 * root_m +
                   0.4505937099 * root_s)
        oklab_b = (0.0259040371 * root_l + 0.7827717662 * root_m -
                   0.8086757660 * root_s)

        return Oklab(oklab_lightness, oklab_a, oklab_b)