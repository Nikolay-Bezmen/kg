import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label, Frame, Canvas
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

IMAGE_DISPLAY_SIZE = (400, 400)

def load_image():
    global img, img_path
    img_path = filedialog.askopenfilename()
    img = cv2.imread(img_path)
    resized_img = resize_image(img)
    display_image(resized_img)

def resize_image(img):
    height, width = IMAGE_DISPLAY_SIZE
    img_resized = cv2.resize(img, (width, height))
    return img_resized

# Функция для отображения изображения в GUI
def display_image(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk

# Функция для линейного контрастирования
def linear_contrast():
    if img is not None:
        img_contrast = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        resized_img = resize_image(img_contrast)
        display_image(resized_img)

# Функция для эквализации гистограммы (по всем каналам RGB)
def histogram_equalization_rgb():
    if img is not None:
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        img_eq = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        resized_img = resize_image(img_eq)
        display_image(resized_img)

# Функция для эквализации гистограммы (по яркости в HSV)
def histogram_equalization_hsv():
    if img is not None:
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_hsv[:, :, 2] = cv2.equalizeHist(img_hsv[:, :, 2])
        img_eq = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
        resized_img = resize_image(img_eq)
        display_image(resized_img)

# Функция для отображения гистограммы изображения
def show_histogram():
    if img is not None:
        plt.clf()  # Очистить прошлые графики
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist, color=col)
        plt.xlim([0, 256])
        plt.title("Гистограмма изображения")
        plt.xlabel("Яркость")
        plt.ylabel("Количество пикселей")
        plt.show()

# Функция для медианной фильтрации (устранение шума)
def median_filter():
    if img is not None:
        img_median = cv2.medianBlur(img, 5)
        resized_img = resize_image(img_median)
        display_image(resized_img)

# Функция для морфологической обработки (эрозия)
def morphological_erosion():
    if img is not None:
        kernel = np.ones((5,5), np.uint8)
        img_eroded = cv2.erode(img, kernel, iterations=1)
        resized_img = resize_image(img_eroded)
        display_image(resized_img)

# Функция для морфологической обработки (дилатация)
def morphological_dilation():
    if img is not None:
        kernel = np.ones((5,5), np.uint8)
        img_dilated = cv2.dilate(img, kernel, iterations=1)
        resized_img = resize_image(img_dilated)
        display_image(resized_img)

# Настройка окна GUI
root = Tk()
root.title("Обработка изображений")

# Создаем фрейм для размещения изображения
image_frame = Frame(root)
image_frame.pack()

# Создаем Canvas для изображения с фиксированными размерами
canvas = Canvas(image_frame, width=IMAGE_DISPLAY_SIZE[0], height=IMAGE_DISPLAY_SIZE[1])
canvas.pack()

# Кнопки для различных функций
btn_load = Button(root, text="Загрузить изображение", command=load_image)
btn_load.pack()

btn_contrast = Button(root, text="Линейное контрастирование", command=linear_contrast)
btn_contrast.pack()

btn_hist_eq_rgb = Button(root, text="Эквализация гистограммы (RGB)", command=histogram_equalization_rgb)
btn_hist_eq_rgb.pack()

btn_hist_eq_hsv = Button(root, text="Эквализация гистограммы (HSV)", command=histogram_equalization_hsv)
btn_hist_eq_hsv.pack()

btn_histogram = Button(root, text="Показать гистограмму", command=show_histogram)
btn_histogram.pack()

btn_median = Button(root, text="Медианный фильтр", command=median_filter)
btn_median.pack()

btn_erosion = Button(root, text="Морфологическая эрозия", command=morphological_erosion)
btn_erosion.pack()

btn_dilation = Button(root, text="Морфологическая дилатация", command=morphological_dilation)
btn_dilation.pack()

root.mainloop()
