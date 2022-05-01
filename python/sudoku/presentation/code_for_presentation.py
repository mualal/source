import cv2
import matplotlib.pyplot as plt

frame_to_preprocess = cv2.imread('../images/Sudoku_example2.jpg')

axs = [None] * 6

fig1, ((axs[0], axs[1], axs[2]), (axs[3], axs[4], axs[5])) = plt.subplots(nrows=2, ncols=3, figsize=(12, 12))

# transform to GRAY colors
frame_gray = cv2.cvtColor(frame_to_preprocess, cv2.COLOR_BGR2GRAY)
axs[0].imshow(frame_gray, cmap='gray')
axs[0].set_title('(1) В оттенках серого', fontsize=15)

# Gaussian blurring
frame_blur = cv2.GaussianBlur(frame_gray, (9, 9), 0)
axs[1].imshow(frame_blur, cmap='gray')
axs[1].set_title('(2) Размытие по Гауссу', fontsize=15)


# adaptive thresholding (to create binary black-white image)
frame_threshold = cv2.adaptiveThreshold(frame_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
axs[2].imshow(frame_threshold, cmap='gray')
axs[2].set_title('(3) Бинанарное изображение \n (только чёрный и белый)', fontsize=15)


# invert colors (white to black and black to white)
frame_inverted = cv2.bitwise_not(frame_threshold, 0)
axs[3].imshow(frame_inverted, cmap='gray')
axs[3].set_title('(4) Инвертированное чёрно-белое \n изображение', fontsize=15)

# kernel for morphological transformation
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

# opening transformation (erosion followed by dilation), useful in removing noise
frame_morph = cv2.morphologyEx(frame_inverted, cv2.MORPH_OPEN, kernel)
axs[4].imshow(frame_morph, cmap='gray')
axs[4].set_title('(5) Удалён шум', fontsize=15)

# dilation, increases the white region in the image
frame_morph = cv2.dilate(frame_morph, kernel, iterations=1)
axs[5].imshow(frame_morph, cmap='gray')
axs[5].set_title('(6) Увеличено количество белого', fontsize=15)

for ax in axs:
    ax.axis('off')

fig1.tight_layout()
plt.savefig('../images/to_black_white.png', format='png', dpi=150)
