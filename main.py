import pygame, sys, math
from settings import *

# Creamos la ventana
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WITH, WINDOW_HEIGHT))

# Rectangulo
rectangulo = pygame.Rect(10, 10, ladoX, ladoY)

# Texto cambiante
text_var1 = 'NO SELECCIONADO'
text_var2 = 'NO SELECCIONADO'

# Cantidad de monitores
monitor_count = 2
monitor1_set = False
monitor2_set = False

while True:
    for event in pygame.event.get():
        # Al tocar la cruz se cierra la ventana
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Evento que al clickear en algun lugar, devuelva la posicion
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rectangulo.collidepoint(event.pos) and monitor_count == 2:  # Verificar si el clic está dentro del rectángulo
                    clicked_position1 = event.pos  # Guardar las coordenadas del click
                    text_var1 = str(clicked_position1)
                    monitor_count -= 1
                    monitor1_set = True
                    
                elif rectangulo.collidepoint(event.pos) and monitor_count == 1:
                    clicked_position2 = (event.pos[0], clicked_position1[1])  # Guardar las coordenadas del click, haciendo que las coordenadas Y sean iguales
                    text_var2 = str(clicked_position2)
                    monitor_count -= 1
                    monitor2_set = True

    display_surface.fill('black') # Fondo
    pygame.draw.rect(display_surface, 'white', rectangulo, 2) # Rectangulo con las dimensiones

    # Dibuja los puntos donde deben situarse los monitores si los mismos fueron seteados
    if monitor1_set:
        pygame.draw.circle(display_surface, 'blue', clicked_position1, 10)
    
    if monitor2_set:
        pygame.draw.circle(display_surface, 'blue', clicked_position2, 10)

    # Calcular coordenadas de intersección, es el punto donde se sentara el productor
    # Para esto usaremos el teorema de pitágoras y SOCATOA
    # Asumiremos que la recta entre Pos1 y Pos2 es la hipotenusa del triángulo
    # Y que entre la interseccion de las dos rectas que generan el punto donde esta el productor hay un ángulo de 90 grados
    # Ademas, ambos catetos del triangulo tienen la misma longitud
    if monitor1_set and monitor2_set:
        x1, y1 = clicked_position1
        x2, y2 = clicked_position2

        hipotenusa = math.sqrt(((x1 - x2)**2)+(y1 - y2)**2) # Hipotenusa del triangulo
        #cateto_opuesto = math.sin(math.radians(90)) * hipotenusa # Calculamos el cateto opuesto
        cateto_opuesto = math.sqrt((hipotenusa**2) / 3)  # Lado del triángulo

        
        # Calcular el punto de intersección
        x_intersection = (x1 + x2) / 2
        y_intersection = (y1 + y2) / 2 + hipotenusa
        long_lado = math.sqrt(((x1 - x_intersection)**2)+(y1 - y_intersection)**2)

        print(hipotenusa)
        print(long_lado)
        # Dibujar líneas desde cada punto al punto de intersección
        #pygame.draw.line(display_surface, 'red', clicked_position1, clicked_position2, 2)
        #pygame.draw.line(display_surface, 'red', clicked_position1, (x_intersection, y_intersection), 2)
        #pygame.draw.line(display_surface, 'red', clicked_position2, (x_intersection, y_intersection), 2)
        pygame.draw.circle(display_surface, 'blue', (x_intersection, y_intersection), 10)

        

    # Texto
    text_pos1_surf = font.render('Pos. Monitor 1: '+ text_var1, True, 'white')
    text_pos1_rect = text_pos1_surf.get_rect(topright = (WINDOW_WITH-10, 10))
    text_pos2_surf = font.render('Pos. Monitor 2: '+ text_var2, True, 'white')
    text_pos2_rect = text_pos2_surf.get_rect(topright = (WINDOW_WITH-10, 40))
    display_surface.blit(text_pos1_surf, text_pos1_rect)
    display_surface.blit(text_pos2_surf, text_pos2_rect)

    pygame.display.flip()  # Actualizar la pantalla
    pygame.time.Clock().tick(60)  # Limitar a 60 FPS