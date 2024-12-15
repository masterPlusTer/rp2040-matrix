from machine import Pin
import rp2
import array
import time

# Programa PIO para WS2812
@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=24,
)
def ws2812():
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0) [2]
    jmp(not_x, "do_zero")   .side(1) [2]
    jmp("bitloop_end")      .side(1) [4]
    label("do_zero")
    nop()                   .side(0) [4]
    label("bitloop_end")
    wrap()

# Configuración
PIN_NUM = 16
NUM_LEDS = 25
MATRIX_WIDTH = 5
MATRIX_HEIGHT = 5

# Inicializa el estado PIO
sm = rp2.StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(PIN_NUM))
sm.active(1)

# Función para enviar datos a los LEDs
def send_pixels(pixels):
    buf = array.array(
        "I", [(g << 16) | (r << 8) | b for r, g, b in pixels]
    )
    sm.put(buf, 8)

# Función para actualizar la matriz de LEDs según el bitmap
def update_matrix():
    pixels = []
    for row in bitmap:
        pixels.extend(row)  # Convierte la matriz 2D en una lista lineal
    send_pixels(pixels)

# Bitmap inicial (matriz vacía)
bitmap = [[(0, 0, 0) for _ in range(MATRIX_WIDTH)] for _ in range(MATRIX_HEIGHT)]

# Función para limpiar el bitmap
def clear_bitmap():
    for y in range(MATRIX_HEIGHT):
        for x in range(MATRIX_WIDTH):
            bitmap[y][x] = (0, 0, 0)

# Diccionario de letras representadas como bitmaps
letters = {
    "A": [
        [0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
    ],
    "B": [
        [1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
    ],
    "C": [
        [0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "D": [
        [1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
    ],
    "E": [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
    ],
    "F": [
        [1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ],
    "G": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "H": [
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
    ],
    "I": [
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
    ],
    "J": [
        [0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "K": [
        [1, 0, 0, 1, 0],
        [1, 0, 1, 0, 0],
        [1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0],
    ],
    "L": [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    "M": [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
    ],
    "N": [
        [1, 0, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 1, 1],
        [1, 0, 0, 0, 1],
    ],
    "O": [
        [0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "P": [
        [1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ],
    "Q": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 1],
    ],
    "R": [
        [1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0],
    ],
    "S": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
    ],
    "T": [
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    "U": [
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "V": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
    ],
    "W": [
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1],
    ],
    "X": [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ],
    "Y": [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
    ],
    "Z": [
        [1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 1, 1, 1, 1],
    ],
    
    " ": [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    "/": [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ],
     "-": [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    "0": [
        [0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "1": [
        [0, 0, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
    ],
    "2": [
        [0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [1, 1, 1, 1, 0],
    ],
    "3": [
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "4": [
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
    ],
    "5": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "6": [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "7": [
        [1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ],
    "8": [
        [0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 0, 0],
    ],
    "9": [
        [0, 1, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 1, 0, 0],
    ],
    "+": [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ],
    "=": [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ],
}

# Función para mostrar texto en una marquesina con colores opcionales
def scroll_text_with_colors(text, colors=None, delay=0.2):
    # Colores predeterminados
    default_colors = [
        (10, 0, 0),  # Rojo
        (0, 10, 0),  # Verde
        (0, 0, 10),  # Azul
        (10, 10, 0), # Amarillo
        (0, 10, 10), # Cian
        (10, 0, 10), # Magenta
    ]
    
    # Si no se especifican colores o hay menos colores que letras, asignar colores predeterminados cíclicamente
    if colors is None or len(colors) < len(text):
        colors = [default_colors[i % len(default_colors)] for i in range(len(text))]

    # Convertir texto a bitmaps con una columna de separación
    buffer = []
    color_map = []  # Mapa de colores para cada columna
    for i, char in enumerate(text):
        if char in letters:
            letter = letters[char]
            # Añadir columnas de la letra al buffer
            for col in range(5):  # Cada letra es de 5 columnas
                buffer.append([letter[row][col] for row in range(5)])
                color_map.append(colors[i])  # Asignar color para cada columna
            # Añadir una columna vacía (separación)
            buffer.append([0, 0, 0, 0, 0])
            color_map.append((0, 0, 0))  # Color negro para la separación
    
    # Desplazar el buffer
    for offset in range(len(buffer) - MATRIX_WIDTH + 1):
        clear_bitmap()
        for y in range(5):  # Filas
            for x in range(5):  # Columnas visibles
                if buffer[offset + x][y]:
                    bitmap[y][x] = color_map[offset + x]
                else:
                    bitmap[y][x] = (0, 0, 0)
        update_matrix()
        time.sleep(delay)

# Ciclo principal
try:
    while True:
        # Ejemplo con colores automáticos
        scroll_text_with_colors(
            "AQUI PUEDES ESCRIBIR TEXTO LIBREMENTE SIN PREOCUPARTE POR LOS COLORES   ---    ",  # Texto a mostrar
            delay=0.1
        )
        # Ejemplo con colores personalizados
        scroll_text_with_colors(
            "TEXTO CON COLORES PREDEFINIDOS", 
            colors=[(10, 0, 0), (0, 10, 0), (0, 0, 10), (10, 10, 0), (0, 10, 10), (0, 0, 10), (10, 10, 0), (0, 10, 10), (0, 0, 10), (10, 10, 0), (0, 10, 10), (0, 0, 10), (10, 10, 0), (0, 10, 10), (0, 0, 10), (10, 10, 0), (0, 10, 10), (0, 0, 10), (10, 10, 0), (0, 10, 10), (0, 0, 10), (10, 10, 0), (0, 10, 10), (0, 0, 10), (10, 10, 0), (0, 10, 10), (0, 0, 10), (10, 10, 0), (0, 10, 10), (0, 0, 10), (10, 10, 0), (0, 10, 10)],
            delay=0.2
        )
except KeyboardInterrupt:
    clear_bitmap()
    send_pixels([(0, 0, 0)] * NUM_LEDS)  # Apaga los LEDs

