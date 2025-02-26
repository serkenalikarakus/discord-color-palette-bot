from PIL import Image, ImageDraw, ImageFont
import os
import uuid

def create_palette_image(colors):
    """Create an image showing the color palette"""
    # Image dimensions
    width = 800
    height = 400
    padding = 20
    color_height = 60
    spacing = 10

    # Create new image with a dark background
    img = Image.new('RGB', (width, height), '#2C2F33')
    draw = ImageDraw.Draw(img)

    # Group colors by type
    color_groups = [
        (colors[0:1], "Base"),
        (colors[1:5], "Analogous"),
        (colors[5:6], "Complementary"),
        (colors[6:8], "Split Complementary"),
        (colors[8:], "Shades & Tints")
    ]

    # Current y position
    y = padding

    try:
        # Try to load a system font
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw each group
    for colors_in_group, group_name in color_groups:
        # Draw group title
        draw.text((padding, y), group_name, fill='white', font=font)
        y += 25

        # Calculate width for each color in this group
        group_width = width - (2 * padding)
        color_width = (group_width - (len(colors_in_group) - 1) * spacing) // len(colors_in_group)

        # Draw colors in this group
        for i, color in enumerate(colors_in_group):
            x = padding + i * (color_width + spacing)

            # Draw color rectangle
            draw.rectangle([(x, y), (x + color_width, y + color_height)], fill=color)

            # Draw background for text (semi-transparent black)
            text_bg_height = 20
            draw.rectangle(
                [(x, y + color_height - text_bg_height), 
                 (x + color_width, y + color_height)],
                fill='#000000'
            )

            # Draw hex code with improved visibility
            text_y = y + color_height - text_bg_height + 2
            draw.text((x + 5, text_y), color, fill='white', font=small_font)

        # Move to next group
        y += color_height + spacing + 10

        # Draw separator line between groups (except for the last group)
        if group_name != "Shades & Tints":
            separator_y = y - 5
            draw.line([(padding, separator_y), (width - padding, separator_y)], 
                     fill='#4A4A4A', width=1)

    # Save image
    os.makedirs('static/palettes', exist_ok=True)
    filename = f"palette_{uuid.uuid4().hex[:8]}.png"
    filepath = f"static/palettes/{filename}"
    img.save(filepath)

    return filepath