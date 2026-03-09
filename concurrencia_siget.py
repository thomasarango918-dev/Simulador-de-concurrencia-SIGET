import threading
import time
import random

# --- CONFIGURACIÓN DEL ESCENARIO ---
CAPACIDAD_BUFFER = 5
buffer = []

# Semáforos para el control de concurrencia
# 'empty' cuenta los espacios libres, 'full' cuenta los mensajes listos
empty = threading.Semaphore(CAPACIDAD_BUFFER)
full = threading.Semaphore(0)
mutex = threading.Lock() # Para exclusión mutua al modificar la lista

class SensorTrafico(threading.Thread):
    """PRODUCTOR: Simula sensores en San Pedro enviando datos al SIGET"""
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        while True:
            dato = random.randint(1, 100) # Simula un conteo de vehículos
            
            print(f"📡 {self.nombre} intentando enviar dato: {dato}...")
            empty.acquire() # Espera si el buffer está lleno
            mutex.acquire() # Bloquea el acceso al buffer
            
            buffer.append(dato)
            print(f"✅ {self.nombre} almacenó: {dato}. Buffer: {len(buffer)}/{CAPACIDAD_BUFFER}")
            
            mutex.release()
            full.release() # Avisa que hay un dato nuevo listo
            
            time.sleep(random.uniform(1, 3)) # Espera aleatoria para el siguiente dato

class ModuloAnalisis(threading.Thread):
    """CONSUMIDOR: Procesa los datos para ajustar semáforos"""
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre

    def run(self):
        while True:
            full.acquire() # Espera si el buffer está vacío
            mutex.acquire()
            
            dato_procesado = buffer.pop(0)
            print(f"⚙️  {self.nombre} PROCESANDO DATO: {dato_procesado}. Quedan: {len(buffer)}")
            
            mutex.release()
            empty.release() # Avisa que hay un espacio libre
            
            # Simula el tiempo de análisis del SIGET
            time.sleep(random.uniform(2, 4))

# --- INICIO DE LA SIMULACIÓN ---
if __name__ == "__main__":
    print("--- INICIANDO MÓDULO DE CONCURRENCIA SIGET ---")
    
    # Creamos 3 hilos (mínimo solicitado)
    s1 = SensorTrafico("Sensor Calle 50")
    s2 = SensorTrafico("Sensor Parque Principal")
    analizador = ModuloAnalisis("Motor Central SIGET")

    s1.start()
    s2.start()
    analizador.start()