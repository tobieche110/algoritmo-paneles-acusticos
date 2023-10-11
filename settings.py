import pygame

pygame.init()

# Longitudes de los lados del cuadrado.
# En algunos casos, para una mejor representación, se recomienda multiplicar los números por un escalar. Sino, darle el valor de 1.
# Para el correcto funcionamiento, el lado X debe ser mayor o igual al lado Y
escalar = 40
ladoX = 3 * escalar # 3 metros, escalando a 40
ladoY = 6 * escalar # 6 metros

# Dimensiones de la ventana
WINDOW_WITH = 800
WINDOW_HEIGHT = 400

# Radio de las circunferencias que representaran al productor y a los monitores
radio = 15

# La siguiente variable representa en cuanto se dividiran los lados para probar las distintas posiciones donde podrian haber primeras reflexiones. Se representa en pixeles.
# Mientras menor sea el numero, mas pruebas de reflexion la aplicacion hara (mas preciso), pero tambien aumentara la fuerza de computo.
fraccion_lado = 1

# Fuente
font = pygame.font.Font(None, 30)