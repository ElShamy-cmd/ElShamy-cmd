import argparse
from diffusers import StableDiffusionPipeline
from prompts import get_default_prompt
from utils import get_output_path

def main():
    parser = argparse.ArgumentParser(description="Generate images with Stable Diffusion")
    parser.add_argument("--type", choices=["character", "animal", "object", "architecture"], required=True, help="Type of image to generate")
    parser.add_argument("--prompt", type=str, help="Custom prompt for image generation")
    args = parser.parse_args()

    prompt = args.prompt if args.prompt else get_default_prompt(args.type)

    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe = pipe.to("cpu")  # Change to "cuda" if you have a GPU

    image = pipe(prompt).images[0]
    output_path = get_output_path(args.type)
    image.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    main()