from tkinter import Tk, Frame, Canvas, Button, Label, IntVar, ALL
import random
from pygame import mixer

x, y = 15, 15
direction = ''
posicion_x = 15
posicion_y = 15
posicion_food = (15, 15)
posicion_snake = [(75, 75)]
nueva_posicion = [(15, 15)]
mixer.init()

# Variables for time limit and quantity
time_limit = 60  # Time limit in seconds
quantity = 0  # Initial quantity

def coordenadas_snake():
    global direccion, posicion_snake, x, y, nueva_posicion
    if direction == 'up':  # arriba
        y = y - 30
        nueva_posicion[0:] = [(x, y)]
        if y >= 495:
            y = 15
        elif y <= 0:
            y = 465
    elif direction == 'down':  # abajo
        y = y + 30
        nueva_posicion[0:] = [(x, y)]
        if y >= 495:
            y = 15
        elif y <= 0:
            y = 15
    elif direction == 'left':  # izquierda
        x = x - 30
        nueva_posicion[0:] = [(x, y)]
        if x >= 495:
            x = 0
        elif x <= 0:
            x = 465
    elif direction == 'right':  # derecha
        x = x + 30
        nueva_posicion[0:] = [(x, y)]
        if x >= 495:
            x = 15
        elif x <= 0:
            x = 15
    posicion_snake = nueva_posicion + posicion_snake[:-1]
    for parte, lugar in zip(canvas.find_withtag("snake"), posicion_snake):
        canvas.coords(parte, lugar)

def direccion(event):
    global direction
    if event.keysym == 'Left':
        if direction != 'right':
            direction = 'left'
    elif event.keysym == 'Right':
        if direction != 'left':
            direction = 'right'
    elif event.keysym == 'Up':
        if direction != 'down':
            direction = 'up'
    elif event.keysym == 'Down':
        if direction != 'up':
            direction = 'down'

def movimiento():
    global posicion_food, posicion_snake, nueva_posicion, quantity, time_limit
    posiciones = [15, 45, 75, 105, 135, 165, 195, 225, 255, 285, 315, 345, 375, 405, 435, 465]
    coordenadas_snake()
    if posicion_food == posicion_snake[0]:
        n = len(posicion_snake)
        quantity += 1  # Increase the quantity
        cantidad['text'] = 'Cantidad 🍎 : {}'.format(quantity)
        posicion_food = (random.choice(posiciones), random.choice(posiciones))
        posicion_snake.append(posicion_snake[-1])
        mixer.music.load("C:\\Users\\an\\Desktop\\JUEGO CULEBRITA\\Juego Snake_audio_snake.mp3")
        mixer.music.play(loops=0)
        if posicion_food not in posicion_snake:
            canvas.coords(canvas.find_withtag("food"), posicion_food)
        canvas.create_text(*posicion_snake[-1], text='▀', fill='green2', font=('Arial', 20), tag='snake')
    if posicion_snake[-1] == nueva_posicion[0] and len(posicion_snake) >= 4:
        cruzar_snake()

    for i in posicion_snake:
        if len(posicion_snake) == 257:
            maximo_nivel()

    # Decrease the time limit and check if time is up
    time_limit -= 0.3
    time_label['text'] = 'Tiempo restante: {:.1f}s'.format(time_limit)
    if time_limit <= 0:
        tiempo_agotado()
    else:
        cantidad.after(300, movimiento)

def cruzar_snake():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       text=f"Intentelo\n de Nuevo \n\n 🍎", fill='red', font=('Arial', 20, 'bold'))

def maximo_nivel():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       text=f"EXELENTE\n\n °° FIN °° \n\n 🍎🍎🍎", fill='green2', font=('Arial', 35, 'bold'))

def tiempo_agotado():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       text=f"Tiempo Agotado\n\n °° FIN °° \n\n 🍎🍎🍎", fill='orange', font=('Arial', 35, 'bold'))

def salir():
    ventana.destroy()
    ventana.quit()

ventana = Tk()
ventana.config(bg='black')
ventana.title('Juego Snake')
ventana.geometry('485x510')
ventana.resizable(0, 0)

frame_1 = Frame(ventana, width=485, height=25, bg='black')
frame_1.grid(column=0, row=0)
frame_2 = Frame(ventana, width=485, height=490, bg='black')
frame_2.grid(column=0, row=1)

ventana.bind("<KeyPress-Left>", direccion)
ventana.bind("<KeyPress-Right>", direccion)
ventana.bind("<KeyPress-Up>", direccion)
ventana.bind("<KeyPress-Down>", direccion)

canvas = Canvas(frame_2, bg='black', width=479, height=479)
canvas.pack()

for i in range(0, 460, 30):
    for j in range(0, 460, 30):
        canvas.create_rectangle(i, j, i + 30, j + 30, fill='gray10')

canvas.create_text(75, 75, text='🍎', fill='red2', font=('Arial', 18), tag='food')

button1 = Button(frame_1, text='Salir', bg='orange', command=salir)
button1.grid(row=0, column=0, padx=20)

button2 = Button(frame_1, text='Iniciar', bg='aqua', command=movimiento)
button2.grid(row=0, column=1, padx=20)

cantidad = Label(frame_1, text='Cantidad 🍎 : {}'.format(quantity), bg='black', fg='red',
                 font=('Arial', 12, 'bold'))
cantidad.grid(row=0, column=2, padx=20)

time_label = Label(frame_1, text='Tiempo restante: {}s'.format(time_limit), bg='black', fg='white',
                   font=('Arial', 12, 'bold'))
time_label.grid(row=0, column=3, padx=20)

# Timer function to decrease time limit
def timer():
    global time_limit
    time_limit -= 0.1
    time_label['text'] = 'Tiempo restante: {:.1f}s'.format(time_limit)
    if time_limit <= 0:
        tiempo_agotado()
    else:
        ventana.after(100, timer)

ventana.after(100, timer)  # Start the timer

ventana.mainloop()
