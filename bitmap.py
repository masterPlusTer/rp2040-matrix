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

# Bitmap manualmente editable
# Cada celda es un color en formato (R, G, B)
bitmap = [
    [(5, 0, 0), (0, 1, 1), (0, 0, 0), (0, 0, 1), (0, 0, 0)],  # Fila 0
    [(0, 2, 0), (10, 0, 0), (10, 3, 0), (10, 0, 0), (3, 0, 0)],  # Fila 1
    [(0, 4, 6), (10, 5, 3), (0, 10, 0), (10, 0, 0), (0, 0, 0)],  # Fila 2
    [(0, 0, 0), (10, 0, 0), (10, 0, 0), (10, 0, 0), (0, 0, 0)],  # Fila 3
    [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],  # Fila 4
]

# Función para imprimir el bitmap (para depuración)
def print_bitmap():
    for row in bitmap:
        print(row)

# Ciclo principal
try:
    while True:
        # Actualiza la matriz de LEDs según el bitmap actual
        update_matrix()
        print_bitmap()  # Muestra el estado actual del bitmap en la consola
        time.sleep(1)

        # Cambia manualmente un píxel en el bitmap
        bitmap[2][2] = (0, 0, 10)  # Cambia el píxel central a azul
        bitmap[1][1] = (0, 10, 0)  # Cambia un píxel a verde
        update_matrix()
        print_bitmap()  # Muestra los cambios en la consola
        time.sleep(1)

except KeyboardInterrupt:
    # Apaga los LEDs al salir
    send_pixels([(0, 0, 0)] * NUM_LEDS)

