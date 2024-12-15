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
    # Protocolo WS2812 con temporización ajustada
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0) [2]  # T0H
    jmp(not_x, "do_zero")   .side(1) [2]  # T1H o T0H
    jmp("bitloop_end")      .side(1) [4]  # T1L
    label("do_zero")
    nop()                   .side(0) [4]  # T0L
    label("bitloop_end")
    wrap()

# Configura el estado PIO
PIN_NUM = 16       # Cambia al pin que estás usando
NUM_LEDS = 25      # Número de LEDs en tu matriz

# Inicializa el estado PIO
sm = rp2.StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(PIN_NUM))
sm.active(1)

# Función para enviar datos a los LEDs
def send_pixels(pixels):
    # Convierte colores RGB a GRB para WS2812
    buf = array.array(
        "I", [(g << 16) | (r << 8) | b for r, g, b in pixels]
    )
    sm.put(buf, 8)  # Envía los datos al PIO

# Función para apagar todos los LEDs
def clear():
    send_pixels([(0, 0, 0)] * NUM_LEDS)

# Función para el efecto de barrido de un color
def color_wipe(color, wait):
    for i in range(NUM_LEDS):
        pixels = [(0, 0, 0)] * NUM_LEDS  # Apaga todos los LEDs
        pixels[i] = color  # Enciende el LED actual con el color dado
        send_pixels(pixels)
        time.sleep(wait)

# Lista de colores para el ciclo
colors = [(10, 0, 0), (0, 10, 0), (0, 0, 10)]  # Rojo, Verde, Azul

# Ciclo principal sin usar itertools.cycle
try:
    while True:
        for color in colors:
            color_wipe(color, 0.05)
except KeyboardInterrupt:
    clear()  # Apaga los LEDs al salir

