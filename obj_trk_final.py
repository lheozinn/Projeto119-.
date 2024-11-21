import cv2
import time
import math

p1 = 530
p2 = 300

xs = []
ys = []

video = cv2.VideoCapture("footvolleyball.mp4")
# Carregue o rastreador
tracker = cv2.TrackerCSRT_create()

# Leia o primeiro quadro do vídeo
success, img = video.read()

# Selecione a caixa delimitadora na imagem
bbox = cv2.selectROI("tracking", img, False)

# Inicialize o rastreador em img e na caixa delimitadora
tracker.init(img, bbox)

def goal_track(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    c1 = x + int(w / 2)
    c2 = y + int(h / 2)
    cv2.circle(img, (c1, c2), 2, (0, 0, 255), 5)

    cv2.circle(img, (int(p1), int(p2)), 2, (0, 255, 0), 3)
    dist = math.sqrt(((c1 - p1) ** 2) + (c2 - p2) ** 2)
    print(dist)

    if dist <= 20:
        cv2.putText(img, "Ponto", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    xs.append(c1)
    ys.append(c2)

    for i in range(len(xs) - 1):
        cv2.circle(img, (xs[i], ys[i]), 2, (0, 0, 255), 5)

# Função drawBox para desenhar a caixa
def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    # Desenhar o retângulo
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
    # Adicionar texto "Rastreando"
    cv2.putText(img, "Rastreando", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Loop para processar o vídeo
while True:
    # Ler os quadros do vídeo
    check, img = video.read()
    if not check:
        print("Fim do vídeo ou erro ao carregar.")
        break

    # Atualizar o rastreador
    success, bbox = tracker.update(img)

    # Verificar se o rastreamento foi bem-sucedido
    if success:
        # Desenhar a caixa no objeto rastreado
        drawBox(img, bbox)
        # Chamar a função goal_track para cálculos adicionais
        goal_track(img, bbox)
    else:
        # Mostrar mensagem de erro
        cv2.putText(img, "Errou", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Exibir o vídeo
    cv2.imshow("Rastreamento", img)

    # Parar se "q" for pressionado
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar os recursos
video.release()
cv2.destroyAllWindows()
