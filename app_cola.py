"""
Implementa un modelo de red de colas interconectadas.
Diseña un sistema con múltiples nodos y colas distribuidas.
Calcula la probabilidad de que un cliente deba esperar en un nodo determinado antes de ser atendido en otro.
"""

import random
import simpy


# Definición de la clase Cliente
class Cliente:
    def __init__(self, nombre, tiempo_llegada):
        self.nombre = nombre
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_espera = 0


# Función que representa el comportamiento de un cliente en un nodo
def cliente(
    pantalla, env, nombre, nodo_actual, cola_actual, tiempo_servicio, tiempos_espera
):
    # Registro del tiempo de llegada del cliente
    llegada = env.now
    pantalla.value += (
        f"El cliente {nombre} llega al nodo {nodo_actual} en el tiempo {llegada}\n"
    )
    # El cliente solicita ser atendido en el nodo actual
    with cola_actual.request() as req:
        yield req
        # Calculo del tiempo de espera en el nodo actual
        espera = env.now - llegada
        # Registro del tiempo de espera en la lista correspondiente
        tiempos_espera[nodo_actual].append(espera)
        # Inicio del servicio al cliente en el nodo actual
        pantalla.value += f"El cliente {nombre} comienza a ser atendido en el nodo {nodo_actual} en el tiempo {env.now} (espera: {espera})\n"
        yield env.timeout(tiempo_servicio)
        # Fin del servicio al cliente en el nodo actual
        pantalla.value += f"El cliente {nombre} termina de ser atendido en el nodo {nodo_actual} en el tiempo {env.now}\n"


# Función que simula la llegada de clientes a la red de colas
def llegada_clientes(pantalla, env, nodos, colas, tiempos_espera, num_clientes=None):
    cliente_id = 0
    while (num_clientes and cliente_id < num_clientes) or not num_clientes:
        # Generación de un tiempo de llegada exponencial
        tiempo_llegada = random.expovariate(1)
        # Espera hasta que llegue un cliente
        yield env.timeout(tiempo_llegada)
        # Selección aleatoria de un nodo para el cliente
        nodo_actual = random.choice(nodos)
        cola_actual = colas[nodo_actual]
        cliente_id += 1
        # Inicio del proceso del cliente en el nodo actual
        env.process(
            cliente(
                pantalla,
                env,
                f"Cliente {cliente_id}",
                nodo_actual,
                cola_actual,
                tiempo_servicio=1,
                tiempos_espera=tiempos_espera,
            )
        )


def simulacion(pantalla, metodo_seleccionado, nodos, valor):
    # Configuración de la simulación
    env = simpy.Environment()
    # Definición de los nodos en la red de colas
    num_nodos = nodos  # Número de nodos en la red
    nodos = [f"Nodo #{i+1}" for i in range(num_nodos)]
    # Creación de las colas para cada nodo
    colas = {nodo: simpy.Resource(env, capacity=1) for nodo in nodos}
    # Inicialización de la lista para almacenar los tiempos de espera en cada nodo
    tiempos_espera = {nodo: [] for nodo in nodos}

    if metodo_seleccionado == "Por tiempo":
        env.process(llegada_clientes(pantalla, env, nodos, colas, tiempos_espera))
        # Tiempo de simulación
        until = valor
        # Ejecutar la simulación hasta que se atiendan todos los clientes
        env.run(until)

    elif metodo_seleccionado == "Por clientes":
        # Configuración de llegada de clientes
        num_clientes = valor  # Número total de clientes
        env.process(
            llegada_clientes(pantalla, env, nodos, colas, tiempos_espera, num_clientes)
        )
        # Ejecutar la simulación hasta que se atiendan todos los clientes
        env.run()

    # Cálculo de las probabilidades de espera en cada nodo
    for nodo, tiempos in tiempos_espera.items():
        if tiempos:
            probabilidad_espera = len([t for t in tiempos if t > 0]) / len(tiempos)
            """
            tiempos es una lista que contiene los tiempos de espera de todos los clientes que pasaron por un nodo específico.
            [t for t in tiempos if t > 0] filtra los tiempos de espera que son mayores que cero, es decir, aquellos clientes que tuvieron que esperar en el nodo antes de ser atendidos.
            len([t for t in tiempos if t > 0]) calcula la cantidad de clientes que experimentaron algún tiempo de espera en ese nodo.
            len(tiempos) es el total de clientes que pasaron por ese nodo.
            Dividir el número de clientes que esperaron entre el total de clientes da como resultado la probabilidad de que un cliente deba esperar en ese nodo antes de ser atendido en otro.
            """
            pantalla.value += (
                f"Probabilidad de espera en {nodo}: {probabilidad_espera}\n"
            )
            continue

        pantalla.value += f"No hay datos suficientes para calcular la probabilidad de espera en {nodo}\n"
