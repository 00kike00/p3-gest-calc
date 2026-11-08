import cv2
from hand_tracker import HandTracker
from gestures import GestureRecognizer
from calc import Calculator

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img, is_active=False):
        s = self.height / 100
        color_fill = (180, 230, 180) if is_active else (225, 225, 225)
        
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      color_fill, cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)

        text_x = self.pos[0] + self.width // 2 - int(15 * s)
        text_y = self.pos[1] + self.height // 2 + int(15 * s)

        cv2.putText(img, self.value, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN,
                    3 * s, (50, 50, 50), max(1, round(3 * s)))


def main():
    cap = cv2.VideoCapture(0)

    WIDTH = 1920
    HEIGHT = 1080
    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)

    success, img = cap.read()
    if not success:
        print("Failed to read frame")
        exit(1)

    HEIGHT, WIDTH = img.shape[:2]
    scale = HEIGHT / 1080
    size = int(100 * scale)

    buttonListValues = [['C', '<'],
                        ['7', '8', '9', '/'],
                        ['4', '5', '6', '*'],
                        ['1', '2', '3', '-'],
                        ['0', '.', '=', '+']]

    buttonlist = []
    for y in range(5):
        for x in range(4):
            if y == 0 and x >= 2:
                break

            xpos = int(WIDTH - 5 * size + x * size)
            ypos = int(HEIGHT * 0.15 + y * size)

            if y == 0 and x == 1:
                xpos += size

            if y == 0:
                width = 2 * size
                buttonlist.append(Button((xpos, ypos), width, size, buttonListValues[y][x]))
            else:
                buttonlist.append(Button((xpos, ypos), size, size, buttonListValues[y][x]))

    tracker = HandTracker(detection_con=0.7, track_con=0.7)
    recognizer = GestureRecognizer(dwell_time=0.8)
    calc = Calculator()

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read frame")
            break

        # Volteo horizontal
        img = cv2.flip(img, 1)

        # Detección de manos con MediaPipe
        results = tracker.find_hands(img, draw=True)

        active_symbol = None

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # hand_label indica "Right" o "Left" devuelto por MediaPipe
                hand_label = handedness.classification[0].label

                # Confirmación del gesto por tiempo (dwell_time)
                symbol = recognizer.get_confirmed_gesture(hand_landmarks.landmark, hand_label)
                if symbol:
                    active_symbol = symbol
                    calc.modify_state(symbol)
                    break

        # Dibujar cuadro de texto de la calculadora
        operation_x = int(WIDTH - 5 * size)
        operation_y = int(HEIGHT * 0.05)

        cv2.rectangle(img, (operation_x, operation_y), (operation_x + 4 * size, operation_y + int(1.2 * size)),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, (operation_x, operation_y), (operation_x + 4 * size, operation_y + int(1.2 * size)),
                      (50, 50, 50), 3)

        # Dibujar botones
        for button in buttonlist:
            is_active = (button.value == active_symbol)
            button.draw(img, is_active=is_active)

        # Mostrar el estado actual procesado por la clase Calculator
        cv2.putText(img, calc.state, (operation_x + int(0.1 * size), operation_y + int(0.75 * size)),
                    cv2.FONT_HERSHEY_PLAIN, 3 * scale, (50, 50, 50), max(1, round(3 * scale)))

        cv2.imshow('Calculator', img)

        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()