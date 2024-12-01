from oscpy.server import OSCThreadServer
import time
import pygame
import pyvjoy  # Importation de pyvjoy pour manipuler un périphérique vJoy

# Initialisation de Pygame pour afficher le joystick virtuel
pygame.init()

# Configurer un écran pour afficher le joystick
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulation de Joystick virtuel")

# Paramètres pour l'axe du joystick
center_x = 400  # Position du joystick sur l'écran (centre)
center_y = 300  # Position du joystick sur l'écran (centre)
joystick_radius = 100  # Rayon du "joystick" simulé (plus grand pour plus de mouvement)
dead_zone = 0.2  # Zone morte (20% autour du centre pour réduire la sensibilité)

# Initialisation du périphérique vJoy (assurez-vous que vJoy est bien installé et configuré)
vj = pyvjoy.VJoyDevice(1)  # Choisir le périphérique vJoy (par exemple, périphérique 1)

# Fonction pour afficher les valeurs reçues
def dump(address, *values):
    print(f'{address.decode("utf8")}: {", ".join(str(v) for v in values)}')

# Callback pour l'orientation du téléphone (yaw)
def callback_orientation_yaw(*values):
    yaw = values[0]  # Récupérer la valeur du yaw (rotation horizontale)
    
    # Mapper l'inclinaison yaw en pourcentage de -1 (gauche) à 1 (droite) avec inversion et nouvelle échelle
    joystick_percentage = -yaw / 60  # Valeur entre -1 et 1 avec une plage de ±60°
    joystick_percentage = max(min(joystick_percentage, 1), -1)  # Limiter à la plage [-1, 1]
    
    # Appliquer la zone morte
    if abs(joystick_percentage) < dead_zone:
        joystick_percentage = 0  # Rester au centre si dans la zone morte
    else:
        # Réajuster pour compenser la zone morte
        joystick_percentage = (
            (joystick_percentage - dead_zone) / (1 - dead_zone)
            if joystick_percentage > 0
            else (joystick_percentage + dead_zone) / (1 - dead_zone)
        )

    # Calculer la position du joystick sur l'axe horizontal (gauche/droite)
    joystick_x = center_x + (joystick_percentage * joystick_radius)  # Ajuster l'affichage
    
    # Limiter la position pour qu'elle ne dépasse pas les bords de l'écran
    joystick_x = max(min(joystick_x, center_x + joystick_radius), center_x - joystick_radius)
    
    # Afficher les valeurs pour déboguer
    print(f"Inclinaison yaw : {yaw}° -> Pourcentage du joystick horizontal : {joystick_percentage * 100}% -> Position : {joystick_x}")
    
    # Mettre à jour l'affichage du joystick
    pygame.draw.circle(screen, (255, 0, 0), (int(joystick_x), center_y), joystick_radius)
    pygame.display.update()

    # Simuler le mouvement du joystick avec vJoy
    simulate_joystick_event(joystick_percentage)

def simulate_joystick_event(joystick_percentage):
    """
    Mettre à jour l'axe X du périphérique vJoy en fonction du pourcentage du joystick.
    """
    # Conversion de la valeur en plage vJoy [0, 32767] pour l'axe X
    vjoy_value = int((joystick_percentage + 1) * 16383.5)  # Mapper [-1, 1] à [0, 32767]
    vjoy_value = max(0, min(vjoy_value, 32767))  # Limiter la valeur pour qu'elle reste valide

    # Mettre à jour l'axe X du périphérique vJoy
    vj.set_axis(pyvjoy.HID_USAGE_X, vjoy_value)  # Axe X de vJoy

# Setup OSC
osc = OSCThreadServer(default_handler=dump)
osc.listen(address='0.0.0.0', port=8000, default=True)

# Lier les callbacks aux messages OSC
osc.bind(b'/multisense/orientation/yaw', callback_orientation_yaw)

# Boucle principale pour afficher le joystick et simuler les mouvements
running = True
while running:
    # Gestion des événements Pygame (permet de fermer proprement la fenêtre)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Nettoyer l'écran à chaque itération
    screen.fill((0, 0, 0))

    # Dessiner le joystick virtuel au centre
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), joystick_radius)  # Joystick au centre
    pygame.display.update()

    time.sleep(0.016)  # Pause pour limiter la fréquence d'actualisation

# Arrêter le serveur OSC
osc.stop()
pygame.quit()
