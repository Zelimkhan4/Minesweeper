import os
import sys
import pygame
# Функция-обёртка для загрузки изображения
# colorkey - цвет заднего фона
# size - размер до которого нужно сжать или расширить изображение
def load_image(filename, size=None, colorkey=None):
    fullname = os.path.join('image', filename)
    
    # Проверка существования файла
    if not os.path.isfile(fullname):
        print(f"Такого файла {fullname} не существует!")
        sys.exit()

    
    image = pygame.image.load(fullname)
    
    if colorkey is not None:
        # Если изображение не прозрачное
        # Просто делаем прозрачным переданный цвет
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image.convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image