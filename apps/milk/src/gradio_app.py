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