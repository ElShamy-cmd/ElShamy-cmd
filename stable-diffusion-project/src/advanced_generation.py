import torch
from PIL import Image
from diffusers import (
    StableDiffusionImg2ImgPipeline,
    StableDiffusionInpaintPipeline,
    StableDiffusionXLImg2ImgPipeline,
    StableDiffusionXLInpaintPipeline
)
from config.model_config import ModelConfig, SCHEDULER_MAPPING

def get_img2img_pipeline(config: ModelConfig):
    """Initialize the appropriate img2img pipeline based on model configuration."""
    if "xl" in config.model_id.lower():
        pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(config.model_id)
    else:
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(config.model_id)
    
    # Set scheduler if specified
    if config.scheduler != "default" and config.scheduler in SCHEDULER_MAPPING:
        scheduler_class = SCHEDULER_MAPPING[config.scheduler]
        pipe.scheduler = scheduler_class.from_config(pipe.scheduler.config)
    
    pipe = pipe.to(config.device)
    return pipe

def get_inpaint_pipeline(config: ModelConfig):
    """Initialize the appropriate inpainting pipeline based on model configuration."""
    if "xl" in config.model_id.lower():
        pipe = StableDiffusionXLInpaintPipeline.from_pretrained(config.model_id)
    else:
        pipe = StableDiffusionInpaintPipeline.from_pretrained(config.model_id)
    
    # Set scheduler if specified
    if config.scheduler != "default" and config.scheduler in SCHEDULER_MAPPING:
        scheduler_class = SCHEDULER_MAPPING[config.scheduler]
        pipe.scheduler = scheduler_class.from_config(pipe.scheduler.config)
    
    pipe = pipe.to(config.device)
    return pipe

def prepare_image(image_path: str, target_size: tuple = None) -> Image.Image:
    """Load and prepare an image for processing."""
    image = Image.open(image_path).convert("RGB")
    if target_size:
        image = image.resize(target_size, Image.Resampling.LANCZOS)
    return image

def generate_img2img(
    config: ModelConfig,
    init_image: Image.Image,
    prompt: str,
    strength: float = 0.75
) -> list[Image.Image]:
    """Generate images using image-to-image generation."""
    pipe = get_img2img_pipeline(config)
    
    # Set random seed if specified
    if config.seed is not None:
        torch.manual_seed(config.seed)
        if config.device == "cuda":
            torch.cuda.manual_seed(config.seed)
    
    images = pipe(
        prompt=prompt,
        negative_prompt=config.negative_prompt,
        image=init_image,
        strength=strength,
        num_inference_steps=config.num_inference_steps,
        guidance_scale=config.guidance_scale,
        num_images_per_prompt=config.num_images
    ).images
    
    return images

def generate_inpaint(
    config: ModelConfig,
    init_image: Image.Image,
    mask_image: Image.Image,
    prompt: str
) -> list[Image.Image]:
    """Generate images using inpainting."""
    pipe = get_inpaint_pipeline(config)
    
    # Set random seed if specified
    if config.seed is not None:
        torch.manual_seed(config.seed)
        if config.device == "cuda":
            torch.cuda.manual_seed(config.seed)
    
    images = pipe(
        prompt=prompt,
        negative_prompt=config.negative_prompt,
        image=init_image,
        mask_image=mask_image,
        num_inference_steps=config.num_inference_steps,
        guidance_scale=config.guidance_scale,
        num_images_per_prompt=config.num_images
    ).images
    
    return images 