import numpy as np
import pygame

# Parametri per la generazione del suono
SAMPLE_RATE = 44100

# Frequenze delle note
NOTES = {
    "La#5": 932.33,
    "DO#6": 1108.73,
    "RE#5": 622.25,
    "FA5": 698.46,
    "FA#5": 739.99,
    "SOL#5": 830.61
}

def generate_tone(frequency, duration, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    return tone

def play_sound(tone):
    pygame.mixer.init(frequency=SAMPLE_RATE)
    sound = np.array(tone * 32767, dtype=np.int16)
    sound = np.repeat(sound[:, np.newaxis], 2, axis=1)  # Stereo
    sound = pygame.sndarray.make_sound(sound)
    return sound

def draw_buttons(screen, font, selected_note):
    x, y = 50, 50
    button_width, button_height = 100, 50
    for note in NOTES:
        rect = pygame.Rect(x, y, button_width, button_height)
        color = (0, 255, 0) if note == selected_note else (0, 0, 255)
        pygame.draw.rect(screen, color, rect)
        text_surf = font.render(note, True, (255, 255, 255))
        screen.blit(text_surf, (x + 10, y + 10))
        y += button_height + 10

def get_note_from_position(pos):
    x, y = 50, 50
    button_width, button_height = 100, 50
    for note in NOTES:
        rect = pygame.Rect(x, y, button_width, button_height)
        if rect.collidepoint(pos):
            return note
        y += button_height + 10
    return None

# Inizializzazione di Pygame
pygame.init()

# Dimensioni della finestra
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simulatore di Suono di Bicchiere di Cristallo')

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Parametri del cerchio
circle_radius = 100
circle_center = (width // 2, height // 2)
border_width = 30  # Larghezza del bordo dove il suono è attivato (incrementato)

# Frequenza iniziale
selected_note = "La#5"
frequency = NOTES[selected_note]
duration = 1.0

# Genera il tono e carica il suono
tone = generate_tone(frequency, duration)
sound = play_sound(tone)
sound.stop()  # Fermare il suono inizialmente

# Font per i pulsanti
font = pygame.font.Font(None, 36)

running = True
sound_playing = False
while running:
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, circle_center, circle_radius, 2)
    draw_buttons(screen, font, selected_note)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            note = get_note_from_position(event.pos)
            if note:
                selected_note = note
                frequency = NOTES[selected_note]
                tone = generate_tone(frequency, duration)
                sound = play_sound(tone)

    # Ottieni la posizione del mouse
    mouse_pos = pygame.mouse.get_pos()
    distance = np.sqrt((mouse_pos[0] - circle_center[0]) ** 2 + (mouse_pos[1] - circle_center[1]) ** 2)

    # Verifica se il mouse è sul bordo del cerchio
    if circle_radius - border_width <= distance <= circle_radius + border_width:
        if not sound_playing:
            sound.play(-1)
            sound_playing = True
    else:
        if sound_playing:
            sound.stop()
            sound_playing = False

    pygame.display.flip()

pygame.quit()
