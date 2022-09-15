from PIL import Image, ImageDraw, ImageFilter, ImageOps
import os


def get_imlist(
    path: str
) -> list:
    """
    получить список имён всех png-файлов в каталоге
    @param path: путь к каталогу
    @return: список имён всех png-файлов в каталоге
    """
    return [os.path.join(
        path, f
    ) for f in os.listdir(path) if f.endswith('.png') and not f.startswith('.') and not '_new' in f]


'''
def mask(low, high):
    return [x if low <= x <= high else 0 for x in range(0, 256)]
'''


if __name__ == "__main__":

    list_of_images = get_imlist(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'img'
    ))

    for im in list_of_images:
        pil_im = Image.open(im).convert('RGB')
        print(pil_im.size)

        if pil_im.size[0] != 2362:
            draw = ImageDraw.Draw(pil_im)
            if pil_im.size[0] == 2368:
                draw.rectangle((1620, 0, 1620+270, 290), fill='white')
            else:
                draw.rectangle((1550, 0, 1550+280, 273), fill='white')
        
        pil_im = pil_im.resize((int(3*300), int(3*200)), Image.LANCZOS)
        pil_im = pil_im.filter(ImageFilter.SHARPEN)
        # pil_im = pil_im.point(mask(210, 256) + mask(210, 256) + mask(210, 256))
        
        pil_mask = pil_im.convert('L')
        threshold = 245
        pil_mask = pil_mask.point(lambda p: 255 if p > threshold else 0)
        pil_mask = ImageOps.invert(pil_mask)

        pil_im.putalpha(pil_mask)
        pil_im.load()
        background = Image.new('RGB', pil_im.size, (255, 255, 255))
        background.paste(pil_im, mask=pil_im.split()[3])

        new_filename = im[:-4]+'_new.jpg'
        background.save(new_filename, quality=80)
