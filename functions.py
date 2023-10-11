import math, pygame

# Funcion que calcula si hay una interseccion entre una recta y una circunferencia
def interseccion_con_circunferencia(m, b, c1, c2, r):
    # Coeficientes de la funcion cuadratica
    # Estos coeficientes se encontraron al resolver el sistema de ecuaciones de una circunferencia y una recta
    # Es decir, se despejo la x de la sgte ecuacion: (x - c1)**2 + (mx - c2)**2 = r**2
    # Eso trae como resultado la sgte funcion cuadratica: x**2 * (1 + m**2) + x * (2 * (m * (b - c2) - c1)) + (c1**2 + (b - c2)**2 - r**2) = 0
    a = 1 + m**2
    b2 = 2 * (m * (b - c2) - c1)
    c = c1**2 + (b - c2)**2 - r**2

    # Calculamos el discriminante
    discriminante = b2**2 - 4 * a * c

    # Si el discriminante es negativo, no hay interseccion
    if discriminante < 0:
        return False

    return True

# Funcion que devuelve un array de todas las posiciones donde hay una interseccion entre una recta variable y un monitor
def calcular_posiciones_paneles(panel_positions, productor_seat, monitor1, monitor2, display_surface, margen_y, radio):

    panel_array = []
    x_productor, y_productor = productor_seat
    x_monitor1, y_monitor1 = monitor1
    x_monitor2, y_monitor2 = monitor2

    for possible_panel_pos in panel_positions:
        # PASO 2
        #pygame.draw.line(display_surface, 'yellow', productor_seat, possible_panel_pos)

        x_panel, y_panel = possible_panel_pos

        # PASO 3, m significa pendiente
        # El angulo incidente se calcula para ambos monitores, es decir, se calcularan dos rectas origen por punto
        # Primero calculamos las pendientes de todas las rectas
        if x_productor != x_panel:
            m_variable = (y_productor - y_panel) / (x_productor - x_panel)
        else:
            continue
        
        m_monitor1 = (y_productor - y_monitor1) / (x_productor - x_monitor1)
        m_monitor2 = (y_productor - y_monitor2) / (x_productor - x_monitor2)

        # Segundo, calculamos los angulos incidentes. Formula: angulo = arctan((m1 - m2)/(1 + m1*m2))
        angulo1 = math.atan((m_variable - m_monitor1) / (1 + m_variable*m_monitor1))
        angulo2 = math.atan((m_variable - m_monitor2) / (1 + m_variable*m_monitor2))
        
        # PASO 4
        # Primero, calculamos las pendientes de las nuevas rectas. Formula: m = tan(angulo)
        m1 = math.tan(angulo1)
        m2 = math.tan(angulo2)

        # Segundo, calculamos la ecuacion de las rectas variables para encontrar un punto por donde pasa. Para eso buscamos la ordenada de cada recta.
        # Con esto seria suficiente para buscar la interseccion entre las rectas y las circunferencias que representan los monitores
        b1 = -(m1*x_panel - y_panel)
        b2 = -(m2*x_panel - y_panel)

        
        # Tercero, calculamos un punto cualquiera para cada recta. Usare los margenes del rectangulo para asegurarme que la longitud de ellas corten si o si un monitor.
        x_recta1 = (margen_y - b1) / m1
        x_recta2 = (margen_y - b2) / m2

        punto_recta1 = (x_recta1, margen_y)
        punto_recta2 = (x_recta2, margen_y)
        
        # Cuarto, dibujamos las rectas.
        pygame.draw.line(display_surface, 'yellow', (x_panel, y_panel), punto_recta1)
        pygame.draw.line(display_surface, 'green', possible_panel_pos, punto_recta2)
        

        if interseccion_con_circunferencia(m1, b1, x_monitor1, y_monitor1, radio) or interseccion_con_circunferencia(m2, b2, x_monitor2, y_monitor2, radio) or interseccion_con_circunferencia(m2, b2, x_monitor1, y_monitor1, radio) or interseccion_con_circunferencia(m1, b1, x_monitor2, y_monitor2, radio):
            panel_array.append((x_panel, y_panel))
    
    return panel_array
