import pygame, sys, math
from settings import *
from functions import *

# Creamos la ventana
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WITH, WINDOW_HEIGHT))

# Margenes del rectangulo
margen_x = 10
margen_y = 10

# Rectangulo
rectangulo = pygame.Rect(margen_x, margen_y, ladoX, ladoY)

# Texto cambiante
text_var1 = 'NO SELECCIONADO'
text_var2 = 'NO SELECCIONADO'

# Cantidad de monitores
monitor_count = 2

# Flags
monitor1_set = False
monitor2_set = False
productor_seat_set = False
first_reflections_set = False

# Porcion de codigo que calcula los puntos donde se debe evaluar si instalar un panel acustico
panel_vertical_positions_left = []
panel_vertical_positions_right = []
panel_horizontal_positions_down = []
panel_horizontal_positions_up = []
pos_y = 0
pos_x = 0

# Para la verticalidad del rectangulo:
while pos_y < (10 + ladoY):
    panel_vertical_positions_left.append((margen_x, margen_y + pos_y))
    panel_vertical_positions_right.append((margen_x + ladoX, margen_y + pos_y))
    pos_y = pos_y + fraccion_lado

# Para la horizontalidad del rectangulo
while pos_x < (10 + ladoX):
    panel_horizontal_positions_down.append((margen_x + pos_x, margen_y + ladoY))
    panel_horizontal_positions_up.append((margen_x + pos_x, margen_y))
    pos_x = pos_x + fraccion_lado

# Bucle de la aplicacion
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

    # Dibuja los puntos donde deben situarse los monitores si los mismos fueron posicionados
    if monitor1_set:
        pygame.draw.circle(display_surface, 'blue', clicked_position1, radio)
    
    if monitor2_set:
        pygame.draw.circle(display_surface, 'blue', clicked_position2, radio)

    # Calcular coordenadas de intersección, es el punto donde se sentara el productor
    # Para esto usaremos el teorema de pitágoras y SOCATOA
    # Asumiremos que la recta entre Pos1 y Pos2 es la hipotenusa del triángulo
    # Y que entre la interseccion de las dos rectas que generan el punto donde esta el productor hay un ángulo de 90 grados
    # Ademas, ambos catetos del triangulo tienen la misma longitud
    if monitor1_set and monitor2_set and not productor_seat_set:
        x1, y1 = clicked_position1 # Posicion monitor 1
        x2, y2 = clicked_position2 # Posicion monitor 2

        hipotenusa = math.sqrt(((x1 - x2)**2)+(y1 - y2)**2) # Hipotenusa del triangulo
        #cateto_opuesto = math.sin(math.radians(90)) * hipotenusa # Calculamos el cateto opuesto
        cateto_opuesto = math.sqrt((hipotenusa**2) / 2)  # Lado del triángulo

        
        # Calcular el punto de intersección
        x_intersection = (x1 + x2) / 2
        y_intersection = (y1 + y2) / 2 + cateto_opuesto
        productor_seat = (x_intersection, y_intersection)
        long_lado = math.sqrt(((x1 - x_intersection)**2)+(y1 - y_intersection)**2)

        # Flag
        productor_seat_set = True
    
    # Dibuja el asiento del productor si este se ha calculado
    if productor_seat_set:
        pygame.draw.circle(display_surface, 'blue', productor_seat, radio)
        pygame.draw.line(display_surface, 'red', productor_seat, clicked_position1, 2)
        pygame.draw.line(display_surface, 'red', productor_seat, clicked_position2, 2)
    
    # Si se calculo el asiento del productor pero no la posicion de los paneles
    if productor_seat_set and not first_reflections_set:
        # Calcular las posiciones donde se instalarian los paneles acusticos
        # 1. Se trazará una recta hacia cada monitor desde el productor (rectas origen) (ya esta realizado)
        # 2. Iterativamente, se trazaran rectas desde el productor hacia cada posicion del rectangulo (rectas variables)
        # 3. Se calcula el angulo de incidencia entre la recta origen y la recta variable
        # 4. Desde el punto que choca una recta variable y un lado del paralelogramo, se trazará una nueva recta siguiendo el ángulo incidente que calculamos
        # 5. Si esta nueva recta choca en algun punto con uno de los monitores de audio, guardaremos la posicion de dicha recta en un array para luego dibujarlo.
        
        intersecciones_verticales_izquierda = calcular_posiciones_paneles(panel_vertical_positions_left, productor_seat, clicked_position1, clicked_position2, display_surface, margen_y, radio)
        intersecciones_verticales_derecha = calcular_posiciones_paneles(panel_vertical_positions_right, productor_seat, clicked_position1, clicked_position2, display_surface, margen_y, radio)
        intersecciones_horizontal_abajo = calcular_posiciones_paneles(panel_horizontal_positions_down, productor_seat, clicked_position1, clicked_position2, display_surface, margen_y, radio)
        intersecciones_horizontal_arriba = calcular_posiciones_paneles(panel_horizontal_positions_up, productor_seat, clicked_position1, clicked_position2, display_surface, margen_y, radio)
        
        first_reflections_set = True    
                
    # Dibuja las posiciones donde hay primeras reflexiones si estas se han calculado:
    if first_reflections_set:
        if len(intersecciones_verticales_derecha) > 0:
            
            # Este bucle dibuja las primeras reflexiones
            for i in intersecciones_verticales_derecha:
                pygame.draw.circle(display_surface, 'yellow', i, 3)
        
        if len(intersecciones_verticales_izquierda) > 0:
            
            # Este bucle dibuja las primeras reflexiones
            for i in intersecciones_verticales_izquierda:
                pygame.draw.circle(display_surface, 'yellow', i, 3)
            

        if len(intersecciones_horizontal_abajo) > 0:
            
            # Este bucle dibuja las primeras reflexiones
            for i in intersecciones_horizontal_abajo:
                pygame.draw.circle(display_surface, 'yellow', i, 3)
            

        if len(intersecciones_horizontal_arriba) > 0:
            
            # Este bucle dibuja las primeras reflexiones
            for i in intersecciones_horizontal_arriba:
                pygame.draw.circle(display_surface, 'yellow', i, 3)
    

    ''''
    # Posiciones donde se evaluarian los "espejos"  
    for i in panel_vertical_positions_right:
        pygame.draw.circle(display_surface, 'yellow', i, 2)

    for i in panel_vertical_positions_left:
        pygame.draw.circle(display_surface, 'yellow', i, 2)
    
    for i in panel_horizontal_positions_down:
        pygame.draw.circle(display_surface, 'yellow', i, 2)
    
    for i in panel_horizontal_positions_up:
        pygame.draw.circle(display_surface, 'yellow', i, 2)
    '''
        
    # Texto
    text_pos1_surf = font.render('Pos. Monitor 1: '+ text_var1, True, 'white')
    text_pos1_rect = text_pos1_surf.get_rect(topright = (WINDOW_WITH-10, 10))
    text_pos2_surf = font.render('Pos. Monitor 2: '+ text_var2, True, 'white')
    text_pos2_rect = text_pos2_surf.get_rect(topright = (WINDOW_WITH-10, 40))
    display_surface.blit(text_pos1_surf, text_pos1_rect)
    display_surface.blit(text_pos2_surf, text_pos2_rect)

    pygame.display.flip()  # Actualizar la pantalla
    pygame.time.Clock().tick(60)  # Limitar a 60 FPS