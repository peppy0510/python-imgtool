# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFilter


class imgtool():

    @classmethod
    def resize_image_width(self, image, width):
        percentage = 1.0 * width / image.size[0]
        height = int(image.size[1] * percentage)
        return image.resize((width, height), Image.ANTIALIAS)

    @classmethod
    def resize_image_height(self, image, height):
        percentage = 1.0 * height / image.size[1]
        width = int(image.size[0] * percentage)
        return image.resize((width, height), Image.ANTIALIAS)

    @classmethod
    def overlap_image_mask(self, image, mask):
        size = (image.size[0], image.size[1])
        alpha = 1.0 * mask[-1] / 255
        image = image.convert('RGBA')
        mask_image = Image.new('RGBA', size, color=mask[:3])
        image = Image.blend(image, mask_image, alpha)
        return image

    @classmethod
    def resize_align_image(self, image, resize, align=0):

        if align == 0:
            return image.resize(resize, Image.ANTIALIAS)

        if 1.0 * image.size[0] / image.size[1] > 1.0 * resize[0] / resize[1]:
            image = self.resize_image_height(image, resize[1])
        else:
            image = self.resize_image_width(image, resize[0])

        offset = [0, 0]
        if align in (2, 5, 8):
            offset[0] = round(0.5 * (resize[0] - image.size[0]))
        if align in (3, 6, 9):
            offset[0] = resize[0] - image.size[0]
        if align in (4, 5, 6):
            offset[1] = round(0.5 * (resize[1] - image.size[1]))
        if align in (7, 8, 9):
            offset[1] = resize[1] - image.size[1]

        return self.crop_image_size(image, (-int(offset[0]), -int(offset[1]), resize[0], resize[1]))

    @classmethod
    def crop_image_size(self, image, crop, color=None):
        x, y, width, height = crop
        size = (width, height)
        if color is None:
            color = (255, 255, 255, 255)
        else:
            color = (color[0], color[1], color[2], 255)
        new_image = Image.new('RGBA', size, color=color)
        new_image.paste(image, (-x, -y))
        image = new_image
        return image

    @classmethod
    def trim_image_size(self, image, size=(600, 600), crop=False, fill=False):
        if crop:
            image = ImageOps.fit(image, size, centering=(
                0.5, 0.5), method=Image.ANTIALIAS)
        else:
            if 1.0 * image.size[0] / image.size[1] < 1.0 * size[0] / size[1]:
                image = self.resize_image_height(image, size[1])
            else:
                image = self.resize_image_width(image, size[0])
            if fill:
                new_image = Image.new('RGBA', size, 255)
                margin_x = int(0.5 * (size[0] - image.size[0]))
                margin_y = int(0.5 * (size[1] - image.size[1]))
                new_image.paste(image, (margin_x, margin_y))
                image = new_image
        return image

    @classmethod
    def blur_image(self, image, radius=0):
        if radius != 0:
            image = image.filter(ImageFilter.GaussianBlur(radius=radius))
        return image

    @classmethod
    def circular_image(self, image, size=(100, 100), resampling=10):
        resampling_size = (size[0] * resampling, size[1] * resampling)
        image = self.trim_image_size(image, size=resampling_size, crop=True)
        mask = Image.new('L', resampling_size, 0)
        draw = ImageDraw.Draw(mask)
        lvr_margin, tvb_margin = (int(size[0] * 0.01), int(size[1] * 0.01))
        ellipse_size = (resampling_size[0] - lvr_margin,
                        resampling_size[1] - tvb_margin)
        draw.ellipse((lvr_margin, tvb_margin) + ellipse_size, fill=255)
        image.putalpha(mask)
        image = self.trim_image_size(image, size=size, crop=True)
        return image

    @classmethod
    def round_image_each_corner(self, image,
                                coordinations=(10, 10, 10, 10, 10, 10, 10, 10),
                                resampling=10):
        size = image.size

        coords = [v * resampling for v in coordinations]
        resampling_size = (size[0] * resampling, size[1] * resampling)
        image = self.trim_image_size(image, size=resampling_size, crop=True)

        alpha = Image.new('L', image.size, 255)

        # top left
        width, height = (coords[0], coords[1])
        circle = Image.new('L', (width * 2, height * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, width * 2, height * 2), fill=255)
        alpha.paste(circle.crop((0, 0, width, height)), (0, 0))
        # top right
        width, height = (coords[2], coords[3])
        circle = Image.new('L', (width * 2, height * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, width * 2, height * 2), fill=255)
        alpha.paste(circle.crop((width, 0, width * 2, height)),
                    (image.size[0] - width, 0))
        # bottom left
        width, height = (coords[4], coords[5])
        circle = Image.new('L', (width * 2, height * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, width * 2, height * 2), fill=255)
        alpha.paste(circle.crop((0, height, width, height * 2)),
                    (0, image.size[1] - height))
        # bottom right
        width, height = (coords[6], coords[7])
        circle = Image.new('L', (width * 2, height * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, width * 2, height * 2), fill=255)
        alpha.paste(circle.crop((width, height, width * 2, height * 2)),
                    (image.size[0] - width, image.size[1] - height))

        image.putalpha(alpha)
        image = self.trim_image_size(image, size=size, crop=True)
        return image

    @classmethod
    def round_image_corner(self, image, radius=100, resampling=10):
        size = image.size
        radius = radius * resampling
        resampling_size = (size[0] * resampling, size[1] * resampling)
        image = self.trim_image_size(image, size=resampling_size, crop=True)
        circle = Image.new('L', (radius * 2, radius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
        alpha = Image.new('L', image.size, 255)
        alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
        alpha.paste(circle.crop((radius, 0, radius * 2, radius)),
                    (image.size[0] - radius, 0))
        alpha.paste(circle.crop((0, radius, radius, radius * 2)),
                    (0, image.size[1] - radius))
        alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)),
                    (image.size[0] - radius, image.size[1] - radius))
        image.putalpha(alpha)
        image = self.trim_image_size(image, size=size, crop=True)
        return image


def __test__():
    import os
    current_path = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.join(current_path, '__test__')
    path = os.path.join(test_path, 'source.jpg')

    image = Image.open(path)

    imgtool.resize_image_width(image, 100).save(
        os.path.join(test_path, 'result.resize_image_width.png'), 'png')

    imgtool.resize_image_height(image, 100).save(
        os.path.join(test_path, 'result.resize_image_height.png'), 'png')

    imgtool.resize_align_image(image, resize=(100, 100), align=1).save(
        os.path.join(test_path, 'result.resize_align_image.png'), 'png')

    imgtool.crop_image_size(image, crop=(0, 0, 100, 100)).save(
        os.path.join(test_path, 'result.crop_image_size.png'), 'png')

    imgtool.trim_image_size(image, size=(100, 100), crop=False, fill=False).save(
        os.path.join(test_path, 'result.trim_image_size.png'), 'png')

    imgtool.circular_image(image, size=(100, 100)).save(
        os.path.join(test_path, 'result.circular_image.png'), 'png')

    imgtool.round_image_corner(image, radius=50).save(
        os.path.join(test_path, 'result.round_image_corner.png'), 'png')

    imgtool.blur_image(image, radius=5).save(
        os.path.join(test_path, 'result.blur_image.png'), 'png')

    imgtool.round_image_each_corner(
        image, coordinations=(100, 50, 0, 0, 0, 0, 100, 50)).save(
        os.path.join(test_path, 'result.round_image_each_corner.png'), 'png')


if __name__ == '__main__':
    __test__()
