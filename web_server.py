from flask import Flask, send_from_directory, render_template
import os
import logging
from color_utils import get_color_name

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/palettes/<path:filename>')
def serve_palette(filename):
    """Serve generated palette images"""
    return send_from_directory('static/palettes', filename)

@app.route('/palette/<colors>')
def show_palette(colors):
    """Show color palette with visual representation"""
    try:
        # Parse colors from URL-safe format
        color_list = colors.split(',')

        # Get descriptions for the colors
        descriptions = [
            "Base Color",
            "Analogous Color (-60°)",
            "Analogous Color (-30°)",
            "Analogous Color (+30°)",
            "Analogous Color (+60°)",
            "Complementary Color",
            "Split Complementary (-150°)",
            "Split Complementary (+150°)",
            "Darker Shade (-40%)",
            "Slight Shade (-20%)",
            "Light Tint (+20%)",
            "Bright Tint (+40%)"
        ]

        # Create list of (color, name, description) tuples
        colors_data = []
        for color, desc in zip(color_list, descriptions):
            name = get_color_name(color) or "Custom Color"
            colors_data.append((color, name, desc))

        return render_template('palette.html', colors=colors_data)
    except Exception as e:
        logger.error(f"Error showing palette: {str(e)}")
        return render_template('error.html', error="Error displaying color palette")

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static/palettes', exist_ok=True)

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)