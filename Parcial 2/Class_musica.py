import pygame
import threading
import time

class ReproductorMusica:
    def __init__(self, ruta_musica):
        self.ruta_musica = ruta_musica
        self.reproduciendo = False
        self.evento_pausa = threading.Event()

    def iniciar_musica(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.ruta_musica)
        pygame.mixer.music.play()
        self.reproduciendo = True

        while pygame.mixer.music.get_busy():
            if self.evento_pausa.is_set():
                pygame.mixer.music.pause()
                while self.evento_pausa.is_set():
                    time.sleep(0.1)
                pygame.mixer.music.unpause()

    def pausar_musica(self):
        self.evento_pausa.set()

    def reanudar_musica(self):
        self.evento_pausa.clear()