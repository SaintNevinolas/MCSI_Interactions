import sounddevice as sd
import numpy as np
import math

counter = 0
# Paramètres de l'enregistrement
SAMPLE_RATE = 44100  # Fréquence d'échantillonnage (44.1 kHz)
CHANNELS = 2         # Nombre de canaux (stéréo)
CHUNK_SIZE = 1024    # Taille du bloc (nombre d'échantillons par lecture)

# ID du périphérique (changer selon ton micro)
DEVICE_ID = 2        # L'ID de ton microphone

# Fonction pour convertir le RMS en dB
def rms_to_db(rms):
    """Convertit la valeur RMS (Root Mean Square) en dB"""
    if rms <= 0:
        return -100  # Valeur de dB pour silence
    return 20 * math.log10(rms)

# Fonction de callback qui sera appelée par sounddevice pour traiter les données audio
def audio_callback(indata, frames, time, status):
    """Traitement des données audio"""
    if status:
        print(f"Erreur : {status}")

    # Convertir les données audio en numpy array
    audio_data = np.array(indata)

    # Calculer la valeur RMS pour chaque canal (gauche et droite)
    rms_value_left = np.sqrt(np.mean(np.square(audio_data[:, 0])))  # Canal gauche
    rms_value_right = np.sqrt(np.mean(np.square(audio_data[:, 1])))  # Canal droit

    # Calculer la valeur RMS combinée des deux canaux (moyenne)
    rms_value_combined = np.sqrt(np.mean(np.square(audio_data)))

    # Vérifier que la valeur RMS combinée n'est pas nulle
    if rms_value_combined > 0:
        # Calculer les décibels à partir de la valeur RMS
        db_value = rms_to_db(rms_value_combined)

        if db_value > -30:
            global counter 
            counter = counter + 1
            print(counter)
        # Afficher le niveau sonore pour les deux canaux et la combinaison
        # print(f"Niveau sonore combiné : {db_value:.2f} dB")
        # print(f"Niveau gauche : {rms_to_db(rms_value_left):.2f} dB, Niveau droit : {rms_to_db(rms_value_right):.2f} dB")
    else:
        print("Silence détecté ou problème avec la lecture des données.")

# Ouvrir le flux audio
with sd.InputStream(device=DEVICE_ID, channels=CHANNELS, samplerate=SAMPLE_RATE, blocksize=CHUNK_SIZE, callback=audio_callback):
    print(f"Enregistrement en cours avec le périphérique {DEVICE_ID}...")
    input("Appuyez sur Entrée pour arrêter l'enregistrement.")
