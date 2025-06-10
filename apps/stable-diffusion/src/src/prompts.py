default_prompts = {
    "character": "A detailed portrait of a fantasy character, dramatic lighting, ultra-realistic",
    "animal": "A photorealistic image of a wild animal in its natural habitat",
    "object": "A high-resolution render of a futuristic object, studio lighting",
    "architecture": "A stunning architectural design, modern style, exterior, daylight"
}

def get_default_prompt(image_type):
    return default_prompts.get(image_type, "A beautiful image")