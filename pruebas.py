import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600

# Creación de la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Guardar Coordenadas al Clic Dentro del Rectángulo")

# Inicialización de la fuente
font = pygame.font.Font(None, 36)

# Posición y dimensiones del rectángulo
rect_x = 200
rect_y = 150
rect_width = 150
rect_height = 100
rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

# Variable para almacenar las coordenadas del clic
clicked_position = None

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Detectar clic del mouse
            if event.button == 1:  # Botón izquierdo del mouse
                if rect.collidepoint(event.pos):  # Verificar si el clic está dentro del rectángulo
                    clicked_position = event.pos  # Guardar las coordenadas del clic
                else:
                    clicked_position = None  # Resetear las coordenadas si el clic está fuera del rectángulo

    # Resto del código de tu juego aquí

    # Dibujar el rectángulo en la pantalla
    screen.fill((0, 0, 0))  # Llenar la pantalla con negro
    pygame.draw.rect(screen, (255, 0, 0), rect)  # Dibujar el rectángulo en rojo
    if clicked_position:
        clicked_position_str = f'({clicked_position[0]}, {clicked_position[1]})'
        text = font.render(f'Clic en: {clicked_position_str}', True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()  # Actualizar la pantalla
    pygame.time.Clock().tick(60)  # Limitar a 60 FPS

# Salir de Pygame
pygame.quit()
sys.exit()

