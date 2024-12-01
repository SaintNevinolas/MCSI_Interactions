import cv2
import mediapipe as mp

# Initialisation des modules MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Fonction de détection du mouvement (pencher en avant/arrière)
def detect_tilt(landmarks):
    # Récupération des coordonnées des points clés nécessaires (comme les épaules et les hanches)
    shoulder_left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    shoulder_right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    hip_left = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    hip_right = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
    
    # Calcul des positions horizontales (coordonnée x) des épaules et des hanches
    shoulder_x = (shoulder_left.x + shoulder_right.x) / 2
    hip_x = (hip_left.x + hip_right.x) / 2

    # Calcul de la différence entre la position des épaules et des hanches sur l'axe horizontal
    diff = shoulder_x - hip_x

    # Si la différence est positive, l'utilisateur se penche en avant
    if diff > 0.05:
        return "Penche en avant"
    # Si la différence est négative, l'utilisateur se penche en arrière
    elif diff < -0.05:
        return "Penche en arrière"
    # Si la différence est proche de 0, la personne est dans une position neutre
    else:
        return "Position neutre"

# Capture de la vidéo
cap = cv2.VideoCapture(2)  # Changez l'index selon votre caméra (0 pour la webcam, 1 pour une caméra externe, etc.)

# Vérification si la caméra a bien été ouverte
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la caméra")
    exit()

# Initialisation de MediaPipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Conversion de l'image BGR en RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Détection de la pose
        results = pose.process(image)

        # Retour à l'image BGR pour affichage
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Dessiner les landmarks de la pose sur l'image
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Appeler la fonction de détection du mouvement
            pose_status = detect_tilt(results.pose_landmarks.landmark)
            cv2.putText(image, pose_status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Affichage de l'image
        cv2.imshow("Detection de mouvement", image)

        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Libérer la capture et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
