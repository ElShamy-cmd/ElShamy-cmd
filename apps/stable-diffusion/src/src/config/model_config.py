from dataclasses import dataclass
from typing import Optional, Dict, Any
from diffusers import (
    DDIMScheduler,
    DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    LMSDiscreteScheduler,
    PNDMScheduler,
    UniPCMultistepScheduler
)

@dataclass
class ModelConfig:
    model_id: str = "runwayml/stable-diffusion-v1-5"
    device: str = "cpu"  # or "cuda" for GPU
    num_inference_steps: int = 50
    guidance_scale: float = 7.5
    width: int = 512
    height: int = 512
    seed: Optional[int] = None
    scheduler: str = "default"  # Options: "default", "ddim", "euler", "euler_a", "dpm++", "lms", "pndm", "unipc"
    negative_prompt: str = ""
    num_images: int = 1
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ModelConfig':
        return cls(**{k: v for k, v in config_dict.items() if k in cls.__dataclass_fields__})

# Default configurations for different models
DEFAULT_CONFIGS = {
    "sd-v1-5": ModelConfig(
        model_id="runwayml/stable-diffusion-v1-5",
        num_inference_steps=50,
        guidance_scale=7.5
    ),
    "sd-v2-1": ModelConfig(
        model_id="stabilityai/stable-diffusion-2-1",
        num_inference_steps=50,
        guidance_scale=7.5
    ),
    "sdxl": ModelConfig(
        model_id="stabilityai/stable-diffusion-xl-base-1.0",
        num_inference_steps=50,
        guidance_scale=7.5,
        width=1024,
        height=1024
    ),
    "sd-v1-4": ModelConfig(
        model_id="CompVis/stable-diffusion-v1-4",
        num_inference_steps=50,
        guidance_scale=7.5
    ),
    "sd-v2-1-base": ModelConfig(
        model_id="stabilityai/stable-diffusion-2-1-base",
        num_inference_steps=50,
        guidance_scale=7.5
    ),
    "sdxl-refiner": ModelConfig(
        model_id="stabilityai/stable-diffusion-xl-refiner-1.0",
        num_inference_steps=50,
        guidance_scale=7.5,
        width=1024,
        height=1024
    )
}

# Scheduler mapping
SCHEDULER_MAPPING = {
    "ddim": DDIMScheduler,
    "dpm++": DPMSolverMultistepScheduler,
    "euler": EulerDiscreteScheduler,
    "euler_a": EulerAncestralDiscreteScheduler,
    "lms": LMSDiscreteScheduler,
    "pndm": PNDMScheduler,
    "unipc": UniPCMultistepScheduler
} 