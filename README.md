# Video Cropper

A Python script for cropping videos while preserving audio with an intuitive GUI interface.

## Features
- 🎥 MP4 video support
- 🔊 Audio preservation
- 🖱️ Interactive crop area selection
- 📐 Customizable aspect ratios
- 👆 Draw-to-crop functionality

## Dependencies
```python
opencv-python
tkinter
Pillow
moviepy
```

## Installation
```bash
pip install opencv-python pillow moviepy
```
*Note: tkinter usually comes with Python installation*

## Usage
1. Run the script
2. Select video file
3. Draw rectangle for crop area
4. Choose aspect ratio (optional)
5. Process video

## Key Components
- OpenCV: Video frame processing
- tkinter: GUI interface
- Pillow: Image conversion
- MoviePy: Audio handling

## Supported Features
- MP4 video format
- Original audio preservation
- Custom crop dimensions
- Aspect ratio presets
- Real-time preview

## Technical Implementation
- Frame-by-frame processing
- Non-destructive editing
- Memory-efficient processing
- Progress tracking

## Output
- Cropped MP4 with audio
- Original quality preservation
- Maintains video metadata
