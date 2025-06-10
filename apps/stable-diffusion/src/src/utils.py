import os
from datetime import datetime
from pathlib import Path

def get_output_path(image_type: str, index: int = None) -> str:
    """Generate output path for the generated image."""
    # Create assets directory if it doesn't exist
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Create type-specific directory
    type_dir = assets_dir / image_type
    type_dir.mkdir(exist_ok=True)
    
    # Generate filename with timestamp and optional index
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{image_type}_{timestamp}"
    if index is not None:
        filename += f"_{index}"
    filename += ".png"
    
    return str(type_dir / filename)