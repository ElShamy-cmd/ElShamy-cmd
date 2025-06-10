import gradio as gr
import torch
from PIL import Image
import numpy as np
from config.config_manager import ConfigManager
from config.model_config import ModelConfig, DEFAULT_CONFIGS
from generate import get_pipeline
from advanced_generation import generate_img2img, generate_inpaint, prepare_image

# Initialize configuration
config_manager = ConfigManager()
config = config_manager.load_config()

def text2img(
    prompt: str,
    negative_prompt: str,
    model_name: str,
    scheduler: str,
    steps: int,
    guidance: float,
    width: int,
    height: int,
    num_images: int,
    seed: int
):
    """Text to image generation interface."""
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

    return images

def img2img(
    init_image: Image.Image,
    prompt: str,
    negative_prompt: str,
    model_name: str,
    scheduler: str,
    steps: int,
    guidance: float,
    strength: float,
    num_images: int,
    seed: int
):
    """Image to image generation interface."""
    # Update config
    config.model_id = DEFAULT_CONFIGS[model_name].model_id
    config.scheduler = scheduler
    config.num_inference_steps = steps
    config.guidance_scale = guidance
    config.num_images = num_images
    config.seed = seed if seed > 0 else None
    config.negative_prompt = negative_prompt

    # Generate images
    images = generate_img2img(
        config=config,
        init_image=init_image,
        prompt=prompt,
        strength=strength
    )

    return images

def inpaint(
    init_image: Image.Image,
    mask_image: Image.Image,
    prompt: str,
    negative_prompt: str,
    model_name: str,
    scheduler: str,
    steps: int,
    guidance: float,
    num_images: int,
    seed: int
):
    """Inpainting interface."""
    # Update config
    config.model_id = DEFAULT_CONFIGS[model_name].model_id
    config.scheduler = scheduler
    config.num_inference_steps = steps
    config.guidance_scale = guidance
    config.num_images = num_images
    config.seed = seed if seed > 0 else None
    config.negative_prompt = negative_prompt

    # Generate images
    images = generate_inpaint(
        config=config,
        init_image=init_image,
        mask_image=mask_image,
        prompt=prompt
    )

    return images

def create_interface():
    """Create the Gradio interface."""
    with gr.Blocks(title="Stable Diffusion Web UI") as interface:
        gr.Markdown("# Stable Diffusion Web UI")
        
        with gr.Tabs():
            with gr.TabItem("Text to Image"):
                with gr.Row():
                    with gr.Column():
                        prompt = gr.Textbox(label="Prompt", lines=3)
                        negative_prompt = gr.Textbox(label="Negative Prompt", lines=2)
                        model_name = gr.Dropdown(
                            choices=list(DEFAULT_CONFIGS.keys()),
                            value="sd-v1-5",
                            label="Model"
                        )
                        scheduler = gr.Dropdown(
                            choices=["default", "ddim", "dpm++", "euler", "euler_a", "lms", "pndm", "unipc"],
                            value="default",
                            label="Scheduler"
                        )
                        with gr.Row():
                            steps = gr.Slider(1, 100, value=50, label="Steps")
                            guidance = gr.Slider(1.0, 20.0, value=7.5, label="Guidance Scale")
                        with gr.Row():
                            width = gr.Slider(256, 1024, value=512, step=64, label="Width")
                            height = gr.Slider(256, 1024, value=512, step=64, label="Height")
                        with gr.Row():
                            num_images = gr.Slider(1, 4, value=1, step=1, label="Number of Images")
                            seed = gr.Number(value=-1, label="Seed (-1 for random)")
                        generate_btn = gr.Button("Generate")
                    with gr.Column():
                        output_gallery = gr.Gallery(label="Generated Images")
                
                generate_btn.click(
                    fn=text2img,
                    inputs=[
                        prompt, negative_prompt, model_name, scheduler,
                        steps, guidance, width, height, num_images, seed
                    ],
                    outputs=output_gallery
                )

            with gr.TabItem("Image to Image"):
                with gr.Row():
                    with gr.Column():
                        init_image = gr.Image(label="Initial Image", type="pil")
                        prompt = gr.Textbox(label="Prompt", lines=3)
                        negative_prompt = gr.Textbox(label="Negative Prompt", lines=2)
                        model_name = gr.Dropdown(
                            choices=list(DEFAULT_CONFIGS.keys()),
                            value="sd-v1-5",
                            label="Model"
                        )
                        scheduler = gr.Dropdown(
                            choices=["default", "ddim", "dpm++", "euler", "euler_a", "lms", "pndm", "unipc"],
                            value="default",
                            label="Scheduler"
                        )
                        with gr.Row():
                            steps = gr.Slider(1, 100, value=50, label="Steps")
                            guidance = gr.Slider(1.0, 20.0, value=7.5, label="Guidance Scale")
                        strength = gr.Slider(0.0, 1.0, value=0.75, label="Strength")
                        with gr.Row():
                            num_images = gr.Slider(1, 4, value=1, step=1, label="Number of Images")
                            seed = gr.Number(value=-1, label="Seed (-1 for random)")
                        generate_btn = gr.Button("Generate")
                    with gr.Column():
                        output_gallery = gr.Gallery(label="Generated Images")
                
                generate_btn.click(
                    fn=img2img,
                    inputs=[
                        init_image, prompt, negative_prompt, model_name, scheduler,
                        steps, guidance, strength, num_images, seed
                    ],
                    outputs=output_gallery
                )

            with gr.TabItem("Inpainting"):
                with gr.Row():
                    with gr.Column():
                        init_image = gr.Image(label="Initial Image", type="pil")
                        mask_image = gr.Image(label="Mask Image", type="pil")
                        prompt = gr.Textbox(label="Prompt", lines=3)
                        negative_prompt = gr.Textbox(label="Negative Prompt", lines=2)
                        model_name = gr.Dropdown(
                            choices=list(DEFAULT_CONFIGS.keys()),
                            value="sd-v1-5",
                            label="Model"
                        )
                        scheduler = gr.Dropdown(
                            choices=["default", "ddim", "dpm++", "euler", "euler_a", "lms", "pndm", "unipc"],
                            value="default",
                            label="Scheduler"
                        )
                        with gr.Row():
                            steps = gr.Slider(1, 100, value=50, label="Steps")
                            guidance = gr.Slider(1.0, 20.0, value=7.5, label="Guidance Scale")
                        with gr.Row():
                            num_images = gr.Slider(1, 4, value=1, step=1, label="Number of Images")
                            seed = gr.Number(value=-1, label="Seed (-1 for random)")
                        generate_btn = gr.Button("Generate")
                    with gr.Column():
                        output_gallery = gr.Gallery(label="Generated Images")
                
                generate_btn.click(
                    fn=inpaint,
                    inputs=[
                        init_image, mask_image, prompt, negative_prompt, model_name, scheduler,
                        steps, guidance, num_images, seed
                    ],
                    outputs=output_gallery
                )

    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(share=True) 