
## Installation

```bash
pip install git+http://east-control.com:9000/pockestra/python-imgtool.git
```

```bash
pip uninstall imgtool
```

## Example

```python
from PIL import Image
from imgtool import imgtool
image = Image.open(path)
imgtool.resize_image_width(image, 100)
imgtool.resize_image_height(image, 100)
imgtool.resize_align_image(image, resize=(100, 100), align=1)
imgtool.crop_image_size(image, crop=(0, 0, 100, 100))
imgtool.trim_image_size(image, size=(100, 100), crop=False, fill=False)
imgtool.circular_image(image, size=(100, 100))
imgtool.round_image_corner(image, radius=50)
imgtool.blur_image(image, radius=5)
imgtool.round_image_each_corner(image, coordinations=(100, 50, 0, 0, 0, 0, 100, 50))
```

## Repository

```bash
git clone http://east-control.com:9000/pockestra/python-imgtool.git
```
