from machine import Pin
import rp2
import array
import time

# Programa PIO para WS2812
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 3
    T2 = 6
    T3 = 4
    # Transmite un bit (ciclo alto + ciclo bajo)
    wrap_target()
    out(x, 1)              .side(0) [T3 - 1]
    jmp(not_x, "do_zero")  .side(1) [T1 - 1]
    jmp("bit_end")         .side(1) [T2 - 1]
    label("do_zero")
    nop()                  .side(0) [T2 - 1]
    label("bit_end")
    wrap()

# Configura el estado PIO
# Cambia el pin según tu conexión
PIN_NUM = 16
NUM_LEDS = 25

# Inicializa el estado PIO
sm = rp2.StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(PIN_NUM))
sm.active(1)

# Función para enviar datos a los LEDs
def send_pixels(pixels):
    # Convierte colores RGB a GRB para WS2812
    buf = array.array("I", [((g << 16) | (r << 8) | b) for r, g, b in pixels])
    sm.put(buf, 8)  # Envía los datos al PIO

# Apaga todos los LEDs
def clear():
    send_pixels([(0, 0, 0)] * NUM_LEDS)

# Ciclo principal
try:
    while True:
        # Encender todos los LEDs en rojo tenue
        send_pixels([(10, 0, 0)] * NUM_LEDS)
        time.sleep(1)
        
        # Cambiar a verde tenue
        send_pixels([(0, 10, 0)] * NUM_LEDS)
        time.sleep(1)
        
        # Cambiar a azul tenue
        send_pixels([(0, 0, 10)] * NUM_LEDS)
        time.sleep(1)
        
        clear()
        time.sleep(1)

except KeyboardInterrupt:
    clear()
