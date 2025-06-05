# Stable Diffusion Project

This project sets up a reproducible environment for generating images using Stable Diffusion.

## Setup

1. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the image generation script:
    ```bash
    python src/generate.py
    ```

## Requirements

- Python 3.8+
- (Optional) CUDA-enabled GPU for faster inference

## Output

Generated images will be saved in the `assets/` directory.