# Deploying Milk Webapp on Gradio

This guide provides instructions for deploying the Milk webapp using Gradio's hosting platform.

## Prerequisites

1. A Gradio account (sign up at https://gradio.app)
2. Python 3.8+ installed
3. Stable Diffusion models downloaded and placed in the `models` directory
4. Git installed

## Local Setup

1. Install Gradio and other dependencies:
```bash
pip install gradio
pip install -r requirements.txt
```

2. Create a new file called `gradio_app.py` in your project directory:
```python
import gradio as gr
from app import app, generate_image, img2img

# Create Gradio interface for text-to-image
def gradio_text2img(prompt, negative_prompt, model, scheduler, steps, guidance, width, height, num_images, seed):
    result = generate_image(
        prompt=prompt,
        negative_prompt=negative_prompt,
        model=model,
        scheduler=scheduler,
        steps=steps,
        guidance=guidance,
        width=width,
        height=height,
        num_images=num_images,
        seed=seed
    )
    return result['images']

# Create Gradio interface for image-to-image
def gradio_img2img(image, prompt, negative_prompt, strength, model, steps, guidance, num_images, seed):
    result = img2img(
        image=image,
        prompt=prompt,
        negative_prompt=negative_prompt,
        strength=strength,
        model=model,
        steps=steps,
        guidance=guidance,
        num_images=num_images,
        seed=seed
    )
    return result['images']

# Create the Gradio interface
with gr.Blocks(title="Milk - AI Image Generation") as demo:
    gr.Markdown("# Milk - AI Image Generation")
    
    with gr.Tabs():
        with gr.TabItem("Text to Image"):
            with gr.Row():
                with gr.Column():
                    prompt = gr.Textbox(label="Prompt", lines=3)
                    negative_prompt = gr.Textbox(label="Negative Prompt", lines=2)
                    with gr.Row():
                        model = gr.Dropdown(
                            choices=["sd-v1-5", "sd-v2-1", "sdxl"],
                            value="sd-v1-5",
                            label="Model"
                        )
                        scheduler = gr.Dropdown(
                            choices=["default", "ddim", "dpm++", "euler", "euler_a"],
                            value="default",
                            label="Scheduler"
                        )
                    with gr.Row():
                        steps = gr.Slider(1, 100, value=50, step=1, label="Steps")
                        guidance = gr.Slider(1, 20, value=7.5, step=0.1, label="Guidance Scale")
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
                fn=gradio_text2img,
                inputs=[prompt, negative_prompt, model, scheduler, steps, guidance, width, height, num_images, seed],
                outputs=output_gallery
            )
        
        with gr.TabItem("Image to Image"):
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(label="Input Image", type="filepath")
                    img2img_prompt = gr.Textbox(label="Prompt", lines=3)
                    img2img_negative_prompt = gr.Textbox(label="Negative Prompt", lines=2)
                    with gr.Row():
                        strength = gr.Slider(0, 1, value=0.75, step=0.01, label="Strength")
                        img2img_model = gr.Dropdown(
                            choices=["sd-v1-5", "sd-v2-1", "sdxl"],
                            value="sd-v1-5",
                            label="Model"
                        )
                    with gr.Row():
                        img2img_steps = gr.Slider(1, 100, value=50, step=1, label="Steps")
                        img2img_guidance = gr.Slider(1, 20, value=7.5, step=0.1, label="Guidance Scale")
                    with gr.Row():
                        img2img_num_images = gr.Slider(1, 4, value=1, step=1, label="Number of Images")
                        img2img_seed = gr.Number(value=-1, label="Seed (-1 for random)")
                    transform_btn = gr.Button("Transform Image")
                
                with gr.Column():
                    img2img_output_gallery = gr.Gallery(label="Generated Images")
            
            transform_btn.click(
                fn=gradio_img2img,
                inputs=[input_image, img2img_prompt, img2img_negative_prompt, strength, img2img_model, 
                       img2img_steps, img2img_guidance, img2img_num_images, img2img_seed],
                outputs=img2img_output_gallery
            )

# Launch the app
if __name__ == "__main__":
    demo.launch()
```

## Deploying to Gradio

1. Create a new repository on GitHub and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Go to https://gradio.app and sign in to your account

3. Click on "Create New Space"

4. Fill in the following details:
   - Name: "milk" (or your preferred name)
   - SDK: Gradio
   - Space SDK: Gradio
   - Repository: Your GitHub repository URL
   - Branch: main
   - Python file: gradio_app.py
   - Hardware: Select appropriate GPU (if available)

5. Click "Create Space"

## Environment Variables

Set up the following environment variables in your Gradio space settings:

1. Go to your space settings
2. Add the following environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`
   - Any other environment variables required by your application

## Monitoring and Maintenance

1. Monitor your space's performance in the Gradio dashboard
2. Check the logs for any errors
3. Monitor your GPU usage and quotas
4. Keep your dependencies updated

## Troubleshooting

1. If the app fails to deploy:
   - Check the build logs
   - Verify all dependencies are in requirements.txt
   - Ensure the Python version is compatible

2. If the app deploys but doesn't work:
   - Check the runtime logs
   - Verify environment variables are set correctly
   - Test the app locally first

3. If you hit resource limits:
   - Optimize your model loading
   - Reduce the number of workers
   - Consider upgrading your Gradio plan

## Security Considerations

1. Keep your API keys and secrets secure
2. Use environment variables for sensitive data
3. Implement rate limiting if needed
4. Monitor for abuse

For additional help or issues, please refer to the Gradio documentation or open an issue in your repository. 