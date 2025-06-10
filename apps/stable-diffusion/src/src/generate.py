import argparse
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionXLPipeline
from prompts import get_default_prompt
from utils import get_output_path
from config.config_manager import ConfigManager
from config.model_config import ModelConfig, SCHEDULER_MAPPING

def get_pipeline(config: ModelConfig):
    """Initialize the appropriate pipeline based on model configuration."""
    if "xl" in config.model_id.lower():
        pipe = StableDiffusionXLPipeline.from_pretrained(config.model_id)
    else:
        pipe = StableDiffusionPipeline.from_pretrained(config.model_id)
    
    # Set scheduler if specified
    if config.scheduler != "default" and config.scheduler in SCHEDULER_MAPPING:
        scheduler_class = SCHEDULER_MAPPING[config.scheduler]
        pipe.scheduler = scheduler_class.from_config(pipe.scheduler.config)
    
    pipe = pipe.to(config.device)
    return pipe

def main():
    parser = argparse.ArgumentParser(description="Generate images with Stable Diffusion")
    parser.add_argument("--type", choices=["character", "animal", "object", "architecture"], required=True, help="Type of image to generate")
    parser.add_argument("--prompt", type=str, help="Custom prompt for image generation")
    parser.add_argument("--model", type=str, default="sd-v1-5", help="Model to use (sd-v1-5, sd-v2-1, sdxl, sd-v1-4, sd-v2-1-base, sdxl-refiner)")
    parser.add_argument("--steps", type=int, help="Number of inference steps")
    parser.add_argument("--guidance", type=float, help="Guidance scale")
    parser.add_argument("--seed", type=int, help="Random seed for generation")
    parser.add_argument("--scheduler", type=str, choices=["default", "ddim", "dpm++", "euler", "euler_a", "lms", "pndm", "unipc"], help="Scheduler to use")
    parser.add_argument("--negative-prompt", type=str, help="Negative prompt")
    parser.add_argument("--num-images", type=int, default=1, help="Number of images to generate")
    parser.add_argument("--width", type=int, help="Image width")
    parser.add_argument("--height", type=int, help="Image height")
    args = parser.parse_args()

    # Initialize configuration
    config_manager = ConfigManager()
    config = config_manager.load_config(args.model)

    # Update config with command line arguments
    if args.steps:
        config.num_inference_steps = args.steps
    if args.guidance:
        config.guidance_scale = args.guidance
    if args.seed:
        config.seed = args.seed
    if args.scheduler:
        config.scheduler = args.scheduler
    if args.negative_prompt:
        config.negative_prompt = args.negative_prompt
    if args.num_images:
        config.num_images = args.num_images
    if args.width:
        config.width = args.width
    if args.height:
        config.height = args.height

    # Get prompt
    prompt = args.prompt if args.prompt else get_default_prompt(args.type)

    # Initialize pipeline
    pipe = get_pipeline(config)

    # Set random seed if specified
    if config.seed is not None:
        torch.manual_seed(config.seed)
        if config.device == "cuda":
            torch.cuda.manual_seed(config.seed)

    # Generate images
    images = pipe(
        prompt,
        negative_prompt=config.negative_prompt,
        num_inference_steps=config.num_inference_steps,
        guidance_scale=config.guidance_scale,
        width=config.width,
        height=config.height,
        num_images_per_prompt=config.num_images
    ).images

    # Save images
    for i, image in enumerate(images):
        output_path = get_output_path(args.type, index=i if len(images) > 1 else None)
        image.save(output_path)
        print(f"Image {i+1} saved to {output_path}")

if __name__ == "__main__":
    main()