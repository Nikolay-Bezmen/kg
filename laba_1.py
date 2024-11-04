import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
import colorsys



def update_from_rgb():
    r = r_value.get()
    g = g_value.get()
    b = b_value.get()

    c, m, y, k = rgb_to_cmyk(r, g, b)
    c_value.set(c)
    m_value.set(m)
    y_value.set(y)
    k_value.set(k)

    h, s, v = rgb_to_hsv(r, g, b)
    h_value.set(h)
    s_value.set(s)
    v_value.set(v)

    update_color_display(r, g, b)

def update_from_cmyk():
    c = c_value.get()
    m = m_value.get()
    y = y_value.get()
    k = k_value.get()

    r, g, b = cmyk_to_rgb(c, m, y, k)
    r_value.set(r)
    g_value.set(g)
    b_value.set(b)

    h, s, v = rgb_to_hsv(r, g, b)
    h_value.set(h)
    s_value.set(s)
    v_value.set(v)

    update_color_display(r, g, b)

def update_from_hsv():
    h = h_value.get()
    s = s_value.get()
    v = v_value.get()

    r, g, b = hsv_to_rgb(h, s, v)
    r_value.set(r)
    g_value.set(g)
    b_value.set(b)

    c, m, y, k = rgb_to_cmyk(r, g, b)
    c_value.set(c)
    m_value.set(m)
    y_value.set(y)
    k_value.set(k)

    update_color_display(r, g, b)

def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1

    r_prime = r / 255
    g_prime = g / 255
    b_prime = b / 255

    k = 1 - max(r_prime, g_prime, b_prime)

    if k == 1:
        return 0, 0, 0, 1
    
    c = (1 - r_prime - k) / (1 - k)
    m = (1 - g_prime - k) / (1 - k)
    y = (1 - b_prime - k) / (1 - k)

    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)

    return int(r), int(g), int(b)

def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return int(h * 360), int(s * 100), int(v * 100)

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h / 360, s / 100, v / 100)
    return int(r * 255), int(g * 255), int(b * 255)

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[0]
    if color_code:
        r, g, b = map(int, color_code)
        r_value.set(r)
        g_value.set(g)
        b_value.set(b)
        update_from_rgb()

def update_color_display(r, g, b):
    color_hex = f"#{r:02x}{g:02x}{b:02x}"
    color_display.config(bg=color_hex)


root = tk.Tk()
root.geometry("700x500")
root.title("Color Model Converter")

color_display = tk.Label(root, bg="black", width=20, height=4)
color_display.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

#RGB Inputs
rgb_label = ttk.Label(root, text="RGB:")
rgb_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

r_value = tk.IntVar()
g_value = tk.IntVar()
b_value = tk.IntVar()

r_entry = ttk.Entry(root, textvariable=r_value, width=5)
r_entry.grid(row=1, column=1, padx=5, pady=5)

g_entry = ttk.Entry(root, textvariable=g_value, width=5)
g_entry.grid(row=1, column=2, padx=5, pady=5)

b_entry = ttk.Entry(root, textvariable=b_value, width=5)
b_entry.grid(row=1, column=3, padx=5, pady=5)

r_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", variable=r_value, command=lambda _: update_from_rgb())
r_slider.grid(row=2, column=1, sticky="we", padx=5, pady=5)

g_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", variable=g_value, command=lambda _: update_from_rgb())
g_slider.grid(row=2, column=2, sticky="we", padx=5, pady=5)

b_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", variable=b_value, command=lambda _: update_from_rgb())
b_slider.grid(row=2, column=3, sticky="we", padx=5, pady=5)

# CMYK Inputs
cmyk_label = ttk.Label(root, text="CMYK:")
cmyk_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

c_value = tk.DoubleVar()
m_value = tk.DoubleVar()
y_value = tk.DoubleVar()
k_value = tk.DoubleVar()

c_entry = ttk.Entry(root, textvariable=c_value, width=5)
c_entry.grid(row=3, column=1, padx=5, pady=5)

m_entry = ttk.Entry(root, textvariable=m_value, width=5)
m_entry.grid(row=3, column=2, padx=5, pady=5)

y_entry = ttk.Entry(root, textvariable=y_value, width=5)
y_entry.grid(row=3, column=3, padx=5, pady=5)

k_entry = ttk.Entry(root, textvariable=k_value, width=5)
k_entry.grid(row=3, column=4, padx=5, pady=5)

c_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", variable=c_value, command=lambda _: update_from_cmyk())
c_slider.grid(row=4, column=1, sticky="we", padx=5, pady=5)

m_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", variable=m_value, command=lambda _: update_from_cmyk())
m_slider.grid(row=4, column=2, sticky="we", padx=5, pady=5)

y_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", variable=y_value, command=lambda _: update_from_cmyk())
y_slider.grid(row=4, column=3, sticky="we", padx=5, pady=5)

k_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, orient="horizontal", variable=k_value, command=lambda _: update_from_cmyk())
k_slider.grid(row=4, column=4, sticky="we", padx=5, pady=5)

# HSV Inputs
hsv_label = ttk.Label(root, text="HSV:")
hsv_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")

h_value = tk.IntVar()
s_value = tk.IntVar()
v_value = tk.IntVar()

h_entry = ttk.Entry(root, textvariable=h_value, width=5)
h_entry.grid(row=5, column=1, padx=5, pady=5)

s_entry = ttk.Entry(root, textvariable=s_value, width=5)
s_entry.grid(row=5, column=2, padx=5, pady=5)

v_entry = ttk.Entry(root, textvariable=v_value, width=5)
v_entry.grid(row=5, column=3, padx=5, pady=5)

h_slider = tk.Scale(root, from_=0, to=360, orient="horizontal", variable=h_value, command=lambda _: update_from_hsv())
h_slider.grid(row=6, column=1, sticky="we", padx=5, pady=5)

s_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", variable=s_value, command=lambda _: update_from_hsv())
s_slider.grid(row=6, column=2, sticky="we", padx=5, pady=5)

v_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", variable=v_value, command=lambda _: update_from_hsv())
v_slider.grid(row=6, column=3, sticky="we", padx=5, pady=5)

choose_color_button = ttk.Button(root, text="Choose Color", command=choose_color)
choose_color_button.grid(row=7, column=0, pady=10)


r_entry.bind("<KeyRelease>", lambda event: int(update_from_rgb()))
g_entry.bind("<KeyRelease>", lambda event: int(update_from_rgb()))
b_entry.bind("<KeyRelease>", lambda event: int(update_from_rgb()))

c_entry.bind("<KeyRelease>", lambda event: update_from_cmyk())
m_entry.bind("<KeyRelease>", lambda event: update_from_cmyk())
y_entry.bind("<KeyRelease>", lambda event: update_from_cmyk())
k_entry.bind("<KeyRelease>", lambda event: update_from_cmyk())

h_entry.bind("<KeyRelease>", lambda event: int(update_from_hsv()))
s_entry.bind("<KeyRelease>", lambda event: int(update_from_hsv()))
v_entry.bind("<KeyRelease>", lambda event: int(update_from_hsv()))

root.mainloop()
