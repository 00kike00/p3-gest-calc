from hand_tracker import HandTracker
import time

class GestureRecognizer:
    def __init__(self, dwell_time=1.5):
        self.dwell_time = dwell_time
        
        self.last_gesture = None
        self.gesture_start_time = 0
        
        self.op_map = {
            0: 'C',   # Puño = Clear / Reset
            1: '+',   # 1 dedo = Suma
            2: '-',   # 2 dedos = Resta
            3: '*',   # 3 dedos = Multiplicación
            4: '/',   # 4 dedos = División
            5: '='    # 5 dedos = Igual
        }

    def is_palma(self, landmarks, hand_label):
        """Determina si la mano (Right o Left) muestra la palma (True) o el revés (False)."""
        if hand_label == "Right":
            return landmarks[5].x < landmarks[17].x
        elif hand_label == "Left":
            return landmarks[5].x > landmarks[17].x
        return True

    def count_fingers(self, landmarks, hand_label,  is_palma=True):
        """Cuenta los dedos levantados según las coordenadas de los landmarks."""
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]
        count = 0

        # Dedos: Índice, Medio, Anular, Meñique
        for tip, pip in zip(tip_ids, pip_ids):
            if landmarks[tip].y < landmarks[pip].y:
                count += 1

        # Pulgar
        thumb_tip = landmarks[4].x
        thumb_ip = landmarks[3].x
        if (hand_label == "Right" and is_palma) or (hand_label == "Left" and not is_palma):
            if thumb_tip < thumb_ip: count += 1
        else:
            if thumb_tip > thumb_ip: count += 1

        return count

    def get_gesture(self, landmarks, hand_label):
        """Devuelve el gesto detectado al instante según la mano."""
        palma = self.is_palma(landmarks, hand_label)

        dedos = self.count_fingers(landmarks, hand_label, is_palma=palma)
        if hand_label == "Right":        
            if palma:
                return str(dedos)  # Palma: '0' a '5'
            else:
                if dedos == 0:
                    return '<'     # Revés + Puño = Borrado
                elif 1 <= dedos <= 4:
                    return str(5 + dedos)  # Revés: '6' a '9'
                elif dedos == 5:
                    return '.'
                    
        elif hand_label == "Left":
            return self.op_map.get(dedos, None)

        return None

    def get_confirmed_gesture(self, landmarks, hand_label):
        """Devuelve el gesto SOLO si se mantiene durante self.dwell_time segundos."""
        raw_gesture = self.get_gesture(landmarks, hand_label)
        
        if raw_gesture is None:
            self.last_gesture = None
            return None

        current_time = time.time()
        
        if raw_gesture == self.last_gesture:
            if current_time - self.gesture_start_time >= self.dwell_time:
                self.gesture_start_time = current_time + 0.4
                return raw_gesture
        else:
            self.last_gesture = raw_gesture
            self.gesture_start_time = current_time

        return None