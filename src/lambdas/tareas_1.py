"""
Se desea implementar sistema sencillo de gestión de tareas con un estilo de 
programación funcional.

Cada tarea se representará mediante un diccionario con tres entradas:

id: identificador único de la tarea,
description: texto descriptivo de la tarea,
state: estado actual de la tarea.

Los estados posibles de una tarea serán: CREADA, INICIADA y COMPLETADA.

El sistema deberá permitir:

- añadir una nueva tarea a la colección;
- marcar una tarea como iniciada;
- marcar una tarea como completada.
- obtener todas las tareas;
- filtrar tareas por estado;
- agrupar tareas por estado;
- obtener representaciones derivadas de la colección, por ejemplo descripciones
  o resúmenes textuales.

La implementación deberá seguir un estilo funcional, entendiendo por ello que
todas las transformaciones se expresarán mediante funciones que no modificarán 
la colección de tareas original, sino que devolverán una nueva. 

El estilo funcional aporta los siguientes beneficios:
- Inmutabilidad de la colección: al no modificar la colección original, se evitan efectos 
  secundarios y se facilita el razonamiento sobre el código.
- Composición: las funciones pueden combinarse fácilmente para crear nuevas
  funcionalidades a partir de las básicas.
- Separación entre identidad y evolución: la tarea tiene un id y una descripción
  inmutables, pero su estado representa su evolución a través de 
  transformaciones.
- Facilita el testing: al no depender de un estado mutable, las funciones son 
  más fáciles de probar de forma aislada.
- Permite el uso de funciones de orden superior: se pueden utilizar funciones 
  como map, filter y reduce para transformar y procesar la colección de tareas.
"""

from typing import List, Dict, Union
import itertools

from enum import Enum

class TaskState(Enum):
    CREADA = 'CREADA'
    INICIADA = 'INICIADA'
    COMPLETADA = 'COMPLETADA'

class TransitionError(Exception):
    """Excepción personalizada para errores de transición de estado en tareas."""
    pass

# Definición de una tarea como un diccionario
# Las claves son de tipo str y los valores pueden ser int, str o TaskState.
Task = Dict[str, Union[int, str, TaskState]]

# Generador de ids únicos para las tareas.
def generate_task_id() -> itertools.count:
    """Generador de ids únicos para las tareas."""
    id_gen = itertools.count(1)
    def get_next_id():
        return next(id_gen)
    return get_next_id

get_new_id = generate_task_id()


def display_tasks(tasks: List[Task]):
    """Imprimir la lista de tareas por pantalla."""
    for task in tasks:
        print(f"Task [id: {task['id']}, description: {task['description']}, state: {task['state'].value}]")


# Se parte de esta función para crear una nueva tarea.
def add_task(tasks: List[Task], description: str) -> List[Task]:

    """Agrega una nueva tarea a la lista de tareas.
    
    Args:
        tasks: Lista actual de tareas.
        description: Descripción de la nueva tarea a agregar.
    Returns:
        Una nueva lista de tareas con la nueva tarea agregada.
        En lugar de modificar la lista original, se devuelve una nueva 
        lista con la tarea añadida.   
    """

    task_id = get_new_id()
    new_task = {'id': task_id, 
                'description': description, 
                'state': TaskState.CREADA}
    return tasks + [new_task]


def mark_as_initiated(tasks: List[Task], task_id: int) -> List[Task]:
    """Marca una tarea como iniciada según su ID.

    Args:
        tasks: Lista actual de tareas.
        task_id: ID de la tarea a marcar como iniciada.
    Returns:
       Una nueva lista de tareas con la tarea marcada como iniciada.

    Exceptions: 
        ValueError: Si no se encuentra la tarea con el ID proporcionado.
    """

    task = filter(lambda task: task['id'] == task_id, tasks)
    if not task:
        raise ValueError(f"No se encontró la tarea con ID {task_id}")
    task = next(task)
    task['state'] = TaskState.INICIADA
    return tasks


def mark_as_completed(tasks: List[Task], task_id: int) -> List[Task]:
    """Marca una tarea como completada según su ID.

    Args:
        tasks: Lista actual de tareas.
        task_id: ID de la tarea a marcar como completada.
    Returns:
       Una nueva lista de tareas con la tarea marcada como completada.

    Exceptions: 
        ValueError: Si no se encuentra la tarea con el ID proporcionado.
        TransitionError: Si la tarea no está en estado INICIADA.
    """

    task = filter(lambda task: task['id'] == task_id, tasks)
    if not task:
        raise ValueError(f"No se encontró la tarea con ID {task_id}")
    task = next(task)
    if task['state'] != TaskState.INICIADA:
        raise TransitionError(f"La tarea con ID {task_id} no está en estado INICIADA")
    task['state'] = TaskState.COMPLETADA
    return tasks


def filter_completed_tasks(tasks: List[Task]) -> List[Task]:
    """Filtra y devuelve solo las tareas completadas."""
    return list(filter(lambda task: task['state'] == TaskState.COMPLETADA, tasks))

def filter_incomplete_tasks(tasks: List[Task]) -> List[Task]:
    """Filtra y devuelve solo las tareas incompletas."""
    return list(filter(lambda task: task['state'] != TaskState.COMPLETADA, tasks))

def get_first_n_incomplete(tasks: List[Task], n: int) -> List[Task]:
    """Obtiene las primeras N tareas incompletas."""
    incomplete_tasks = filter(lambda task: task['state'] != TaskState.COMPLETADA, tasks)
    return list(itertools.islice(incomplete_tasks, n))

def repeat_task_n_times(task: Task, n: int) -> List[Task]:
    """Repite una tarea N veces en una nueva lista."""
    return [task] * n

def group_tasks_by_status(tasks: List[Task]):
    """Agrupa las tareas en completadas e incompletas usando itertools.groupby."""
    
    tasks.sort(key=lambda task: str(task['state']))  # Necesario ordenar para groupby
    
    # Imprimir directamente el resultado del groupby en esta función.
    for state, group in itertools.groupby(tasks, key=lambda task: task['state']):
        print(f"Estado: {state.value}")
        for task in group:
            print(f"  Task [id: {task['id']}, description: {task['description']}]")

# Ejemplo de uso
if __name__ == "__main__":

   tasks = []

   tasks = add_task(tasks, "Implementar funcionalidad A")
   tasks = add_task(tasks, "Escribir documentación")
   tasks = add_task(tasks, "Realizar pruebas unitarias")
   
   tasks = mark_as_initiated(tasks, 1)
   tasks = mark_as_completed(tasks, 1)
   tasks = mark_as_initiated(tasks, 2)
   completed_tasks = filter_completed_tasks(tasks)
   incomplete_tasks = filter_incomplete_tasks(tasks)

   print("All Tasks:")
   display_tasks(tasks)

   print("\nCompleted Tasks:")
   display_tasks(completed_tasks)

   print("\nIncomplete Tasks:")
   display_tasks(incomplete_tasks)

   print("\nPrimeras 2 tareas incompletas:")
   display_tasks(get_first_n_incomplete(tasks, 2))

   print("\nRepetir tarea 3 veces:")
   display_tasks(repeat_task_n_times(tasks[0], 3))

   print("\nTareas agrupadas por estado:")
   group_tasks_by_status(tasks)
