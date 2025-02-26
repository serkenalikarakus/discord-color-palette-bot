import webcolors
from PIL import Image
import io
import colorsys
import numpy as np

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def get_color_name(hex_color):
    """Get the closest color name for a hex color"""
    try:
        # Convert hex to RGB
        rgb = hex_to_rgb(hex_color)

        # Try to get exact color name
        try:
            return webcolors.rgb_to_name(rgb)
        except ValueError:
            pass

        # Find closest color
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - rgb[0]) ** 2
            gd = (g_c - rgb[1]) ** 2
            bd = (b_c - rgb[2]) ** 2
            min_colors[(rd + gd + bd)] = name

        return min_colors[min(min_colors.keys())]
    except Exception as e:
        print(f"Error getting color name: {str(e)}")
        return None

def create_color_image(color):
    """Create a small image of a single color"""
    img = Image.new('RGB', (100, 100), color)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def generate_palette_from_color(color):
    """Generate a color palette from input color"""
    try:
        # Handle hex color
        if color.startswith('#'):
            base_color = color
        else:
            # Handle color name
            try:
                base_color = webcolors.name_to_hex(color.lower())
            except ValueError:
                return None

        # Convert base color to HSV
        rgb = hex_to_rgb(base_color)
        hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

        # Generate palette
        palette = []
        h, s, v = hsv

        # Add base color
        palette.append(base_color)

        # Add analogous colors (30, 60 degrees on both sides)
        for angle in [-60, -30, 30, 60]:
            new_h = (h + angle/360) % 1.0
            rgb = colorsys.hsv_to_rgb(new_h, s, v)
            rgb_int = tuple(int(x * 255) for x in rgb)
            palette.append(rgb_to_hex(rgb_int))

        # Add complementary color (180 degrees)
        comp_h = (h + 0.5) % 1.0
        rgb = colorsys.hsv_to_rgb(comp_h, s, v)
        rgb_int = tuple(int(x * 255) for x in rgb)
        palette.append(rgb_to_hex(rgb_int))

        # Add split complementary colors (150 and 210 degrees from base)
        for angle in [-150, 150]:
            new_h = (h + angle/360) % 1.0
            rgb = colorsys.hsv_to_rgb(new_h, s, v)
            rgb_int = tuple(int(x * 255) for x in rgb)
            palette.append(rgb_to_hex(rgb_int))

        # Add shades and tints
        for v_mod in [-0.4, -0.2, 0.2, 0.4]:
            new_v = max(0.1, min(0.9, v + v_mod))
            rgb = colorsys.hsv_to_rgb(h, s, new_v)
            rgb_int = tuple(int(x * 255) for x in rgb)
            palette.append(rgb_to_hex(rgb_int))

        return palette
    except Exception as e:
        print(f"Error generating palette: {str(e)}")
        return None