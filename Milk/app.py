from flask import Flask, render_template, request, jsonify, send_file
import os
from datetime import datetime
import sys
import torch
from pathlib import Path

# Add the stable-diffusion-project to Python path
sys.path.append(str(Path(__file__).parent.parent / 'stable-diffusion-project'))
from src.generate import get_pipeline
from src.advanced_generation import generate_img2img, generate_inpaint
from src.config.config_manager import ConfigManager
from src.config.model_config import ModelConfig, DEFAULT_CONFIGS

app = Flask(__name__)

# Initialize configuration
config_manager = ConfigManager()
config = config_manager.load_config()

# Ensure upload directories exist
UPLOAD_FOLDER = 'static/uploads'
GENERATED_FOLDER = 'static/generated'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get('prompt')
        negative_prompt = data.get('negative_prompt', '')
        model_name = data.get('model', 'sd-v1-5')
        scheduler = data.get('scheduler', 'default')
        steps = int(data.get('steps', 50))
        guidance = float(data.get('guidance', 7.5))
        width = int(data.get('width', 512))
        height = int(data.get('height', 512))
        num_images = int(data.get('num_images', 1))
        seed = int(data.get('seed', -1))

        # Update config
        config.model_id = DEFAULT_CONFIGS[model_name].model_id
        config.scheduler = scheduler
        config.num_inference_steps = steps
        config.guidance_scale = guidance
        config.width = width
        config.height = height
        config.num_images = num_images
        config.seed = seed if seed > 0 else None
        config.negative_prompt = negative_prompt

        # Generate images
        pipe = get_pipeline(config)
        images = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance,
            width=width,
            height=height,
            num_images_per_prompt=num_images
        ).images

        # Save images
        image_paths = []
        for i, image in enumerate(images):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{timestamp}_{i}.png"
            image_path = os.path.join(GENERATED_FOLDER, filename)
            image.save(image_path)
            image_paths.append(f"/static/generated/{filename}")

        return jsonify({
            'success': True,
            'images': image_paths
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/img2img', methods=['POST'])
def img2img():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image_file = request.files['image']
        prompt = request.form.get('prompt')
        negative_prompt = request.form.get('negative_prompt', '')
        strength = float(request.form.get('strength', 0.75))
        model_name = request.form.get('model', 'sd-v1-5')
        scheduler = request.form.get('scheduler', 'default')
        steps = int(request.form.get('steps', 50))
        guidance = float(request.form.get('guidance', 7.5))
        num_images = int(request.form.get('num_images', 1))
        seed = int(request.form.get('seed', -1))

        # Save uploaded image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(UPLOAD_FOLDER, f"input_{timestamp}.png")
        image_file.save(image_path)

        # Update config
        config.model_id = DEFAULT_CONFIGS[model_name].model_id
        config.scheduler = scheduler
        config.num_inference_steps = steps
        config.guidance_scale = guidance
        config.num_images = num_images
        config.seed = seed if seed > 0 else None
        config.negative_prompt = negative_prompt

        # Generate images
        from PIL import Image
        init_image = Image.open(image_path)
        images = generate_img2img(
            config=config,
            init_image=init_image,
            prompt=prompt,
            strength=strength
        )

        # Save generated images
        image_paths = []
        for i, image in enumerate(images):
            filename = f"generated_{timestamp}_{i}.png"
            output_path = os.path.join(GENERATED_FOLDER, filename)
            image.save(output_path)
            image_paths.append(f"/static/generated/{filename}")

        return jsonify({
            'success': True,
            'images': image_paths
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 