import os

def get_output_path(image_type):
    filename = f"{image_type}.png"
    return os.path.join(os.path.dirname(__file__), "../assets", filename)