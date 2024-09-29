from tkinter import *
from tkinter import colorchooser

# Создаем интерфейс
root = Tk()   
root.geometry("300x1000")  

# Определяем переменные
r_var = DoubleVar() 
g_var = DoubleVar()
b_var = DoubleVar() 
c_var = DoubleVar()
m_var = DoubleVar() 
y_var = DoubleVar()
k_var = DoubleVar() 
h_var = DoubleVar()
s_var = DoubleVar()
v_var = DoubleVar()

def rgb_to_cmyk(r, g, b):
    r_, g_, b_ = r / 255, g / 255, b / 255
    k = 1 - max(r_, g_, b_)
    
    if k == 1:
        return 0, 0, 0, 1  # Черный цвет
    
    c = (1 - r_ - k) / (1 - k)
    m = (1 - g_ - k) / (1 - k)
    y = (1 - b_ - k) / (1 - k)

    return c, m, y, k

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return r, g, b

def rgb_to_hsv(r, g, b):
    r_, g_, b_ = r / 255, g / 255, b / 255
    c_max = max(r_, g_, b_)
    c_min = min(r_, g_, b_)
    delta = c_max - c_min

    if delta == 0:
        h = 0
    elif c_max == r_:
        h = (60 * ((g_ - b_) / delta) + 360) % 360
    elif c_max == g_:
        h = (60 * ((b_ - r_) / delta) + 120) % 360
    else:
        h = (60 * ((r_ - g_) / delta) + 240) % 360

    s = 0 if c_max == 0 else (delta / c_max)
    v = c_max

    return h, s * 100, v * 100

def hsv_to_rgb(h, s, v):
    s /= 100
    v /= 100
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r_, g_, b_ = c, x, 0
    elif 60 <= h < 120:
        r_, g_, b_ = x, c, 0
    elif 120 <= h < 180:
        r_, g_, b_ = 0, c, x
    elif 180 <= h < 240:
        r_, g_, b_ = 0, x, c
    elif 240 <= h < 300:
        r_, g_, b_ = x, 0, c
    else:
        r_, g_, b_ = c, 0, x

    r = (r_ + m) * 255
    g = (g_ + m) * 255
    b = (b_ + m) * 255

    return r, g, b

def cmyk_to_hsv(c, m, y, k):
    return rgb_to_hsv(cmyk_to_rgb(c, m, y, k))

def hsv_to_cmyk(h, s, v):
    return rgb_to_cmyk(hsv_to_rgb(h, s, v))

def update_rgb(*args):
    r, g, b = r_var.get(), g_var.get(), b_var.get()
    c, m, y, k = rgb_to_cmyk(r, g, b)
    h, s, v = rgb_to_hsv(r, g, b)

    # Обновляем значения ползунков
    c_var.set(c * 100)
    m_var.set(m * 100)
    y_var.set(y * 100)
    k_var.set(k * 100)

    h_var.set(h)
    s_var.set(s)
    v_var.set(v)

def update_cmyk(*args):
    c, m, y, k = c_var.get() / 100, m_var.get() / 100, y_var.get() / 100, k_var.get() / 100
    r, g, b = cmyk_to_rgb(c, m, y, k)
    h, s, v = rgb_to_hsv(r, g, b)

    r_var.set(r)
    g_var.set(g)
    b_var.set(b)

    h_var.set(h)
    s_var.set(s)
    v_var.set(v)

def update_hsv(*args):
    h, s, v = h_var.get(), s_var.get(), v_var.get()
    r, g, b = hsv_to_rgb(h, s, v)
    c, m, y, k = rgb_to_cmyk(r, g, b)

    r_var.set(r)
    g_var.set(g)
    b_var.set(b)

    c_var.set(c * 100)
    m_var.set(m * 100)
    y_var.set(y * 100)
    k_var.set(k * 100)

def choose_color():
    # Открыть диалог выбора цвета
    color_code = colorchooser.askcolor(title="Выберите цвет")
    if color_code[0]:  # Если пользователь выбрал цвет
        r, g, b = int(color_code[0][0]), int(color_code[0][1]), int(color_code[0][2])
        r_var.set(r)
        g_var.set(g)
        b_var.set(b)

        update_rgb()

# Привязываем обновление к переменным
r_var.trace("w", update_rgb)
g_var.trace("w", update_rgb)
b_var.trace("w", update_rgb)

c_var.trace("w", update_cmyk)
m_var.trace("w", update_cmyk)
y_var.trace("w", update_cmyk)
k_var.trace("w", update_cmyk)

h_var.trace("w", update_hsv)
s_var.trace("w", update_hsv)
v_var.trace("w", update_hsv)

# Создаем ползунки
r_scalar = Scale(root, variable=r_var, from_=0, to=255, orient=HORIZONTAL, label='RGB - R')
g_scalar = Scale(root, variable=g_var, from_=0, to=255, orient=HORIZONTAL, label='RGB - G') 
b_scalar = Scale(root, variable=b_var, from_=0, to=255, orient=HORIZONTAL, label='RGB - B') 
c_scalar = Scale(root, variable=c_var, from_=0, to=100, orient=HORIZONTAL, label='CMYK - C') 
m_scalar = Scale(root, variable=m_var, from_=0, to=100, orient=HORIZONTAL, label='CMYK - M') 
y_scalar = Scale(root, variable=y_var, from_=0, to=100, orient=HORIZONTAL, label='CMYK - Y') 
k_scalar = Scale(root, variable=k_var, from_=0, to=100, orient=HORIZONTAL, label='CMYK - K') 
h_scalar = Scale(root, variable=h_var, from_=0, to=360, orient=HORIZONTAL, label='HSV - H')  
s_scalar = Scale(root, variable=s_var, from_=0, to=100, orient=HORIZONTAL, label='HSV - S') 
v_scalar = Scale(root, variable=v_var, from_=0, to=100, orient=HORIZONTAL, label='HSV - V')    

# Кнопка для выбора цвета
color_button = Button(root, text="Выбрать цвет", command=choose_color, bg="lightblue")
color_button.pack(pady=10)



# Располагаем элементы
r_scalar.pack(anchor=CENTER) 
g_scalar.pack(anchor=CENTER)  
b_scalar.pack(anchor=CENTER)  
c_scalar.pack(anchor=CENTER)  
m_scalar.pack(anchor=CENTER)  
y_scalar.pack(anchor=CENTER)  
k_scalar.pack(anchor=CENTER)
h_scalar.pack(anchor=CENTER)  
s_scalar.pack(anchor=CENTER)  
v_scalar.pack(anchor=CENTER)    

root.mainloop()
