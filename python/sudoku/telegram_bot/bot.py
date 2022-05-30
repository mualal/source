from aiogram import Bot, Dispatcher, executor, types
from lib import sudoku_detection, solver_algorithm_x
import configparser
import os
import datetime
import cv2
import tensorflow as tf

config = configparser.ConfigParser()
config.read('settings.ini')

try:
    bot = Bot(token=config['Bot']['token'])
    dp = Dispatcher(bot)
except KeyError:
    exit('Error: no bot token provided')


downloads_directory = 'downloaded_photos'
if not os.path.exists(downloads_directory):
    os.makedirs(downloads_directory)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Привет! Я готов решить судоку по изображению. Отвечу на любое присланное мне изображение')


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo_process(message: types.Message):
    photo_path = os.path.join(downloads_directory, datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.jpg')

    # download photo
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, photo_path)

    # solve sudoku if found
    image = cv2.imread(photo_path)
    preprocessed_cells, _ = sudoku_detection.full_pipeline(image)
    path_to_neural_net = '../ml_model/neural_net_classifier_2.h5'
    model = tf.keras.models.load_model(path_to_neural_net)

    if preprocessed_cells is not None:
        sudoku_to_solve = sudoku_detection.recognize_digits(preprocessed_cells, model)
        solution = solver_algorithm_x.solver_pipeline(sudoku_to_solve)
        print(sudoku_to_solve)
        print(solution)
        if type(solution) is not str:
            # generate image with solution
            solution_image = cv2.imread('empty_sudoku_field.png')
            width = solution_image.shape[0] // 9
            for i in range(9):
                for j in range(9):
                    p_left = (j * width, i * width)
                    p_right = ((j + 1) * width, (i + 1) * width)
                    center = ((p_left[0] + p_right[0]) // 2, (p_left[1] + p_right[1]) // 2)

                    text_size, _ = cv2.getTextSize(
                        text=str(int(solution[i][j])),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=2.5,
                        thickness=3
                    )

                    center = (center[0] - text_size[0] // 2, center[1] + text_size[1] // 2)

                    cv2.putText(
                        img=solution_image,
                        text=str(int(solution[i][j])),
                        org=center,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=3,
                        color=(0, 0, 0),
                        thickness=2
                    )
            solution_photo_path = photo_path[:-4] + '_solution' + '.jpg'
            cv2.imwrite(solution_photo_path, solution_image)

            # send photo
            await message.answer_photo(types.InputFile(solution_photo_path))
        else:
            # send reply
            await message.reply('Не удалось верно распознать 🧐 или судоку на изображении '
                                'противоречит правилам / не имеет решения.\n'
                                'Попробуйте сделать более качественный снимок 🖼')
    else:
        # send reply
        await message.reply('Не нашёл судоку на данном изображении 🙁')


if __name__ == '__main__':
    executor.start_polling(dp)
