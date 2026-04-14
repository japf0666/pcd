
"""
Diseña un sistema de gestión de lista de tareas utilizando un enfoque de 
programación funcional en Python. El sistema debe permitir 
- agregar tareas, 
- marcar tareas como completas y 
- filtrar tareas según su estado.

Enfoque de Programación Funcional: utiliza funciones y estructuras de datos 
inmutables para implementar el sistema de gestión de tareas. 
Evita el uso de estado mutable y enfatiza el uso de funciones de 
orden superior, como map, filter y reduce.
"""

from typing import List, Dict, Union
import itertools

# Definición de una tarea como un diccionario
# Las claves son de tipo str y los valores pueden ser int, str o bool.
Task = Dict[str, Union[int, str, bool]]


# Se parte de esta función para crear una nueva tarea.
def add_task(tasks: List[Task], description: str) -> List[Task]:

    """Agrega una nueva tarea a la lista de tareas.
    
    Args:
        tasks: Lista actual de tareas.
        description: Descripción de la nueva tarea a agregar.
    Returns:
        Una nueva lista de tareas con la nueva tarea agregada.
        En lugar de modificar la lista original, se devuelve una nueva 
        lista con la tarea añadida (inmutable).   
    """

    task_id = len(tasks) + 1
    new_task = {'id': task_id, 'description': description, 'completed': False}
    return tasks + [new_task]


def mark_as_complete(tasks: List[Task], task_id: int):
    """Marca una tarea como completa según su ID.
       En este caso 
    
    """
    task = filter(lambda task: task['id'] == task_id, tasks)
    if not task:
        raise ValueError(f"No se encontró la tarea con ID {task_id}")
    task = next(task)
    task['completed'] = True


def filter_completed_tasks(tasks: List[Task]) -> List[Task]:
    """Filtra y devuelve solo las tareas completadas."""


def filter_incomplete_tasks(tasks: List[Task]) -> List[Task]:
    """Filtra y devuelve solo las tareas incompletas."""


def display_tasks(tasks: List[Task]):
    """Imprimir la lista de tareas por pantalla."""
    for task in tasks:
        print(f"Task {task['id']}: {task['description']} {'(Completed)' if task['completed'] else '(Incomplete)'}")


"""
A continuación resuelve las siguientes funciones utilizando la librería itertools de Python.
"""

def generate_task_id() -> itertools.count:
    """Generador de IDs únicos para nuevas tareas."""
    


def get_first_n_incomplete(tasks: List[Task], n: int) -> List[Task]:
    """Obtiene las primeras N tareas incompletas."""


def repeat_task_n_times(task: Task, n: int) -> List[Task]:
    """Repite una tarea N veces en una nueva lista."""


def group_tasks_by_status(tasks: List[Task]):
    """Agrupa las tareas en completadas e incompletas usando itertools.groupby."""
    
    tasks.sort(key=lambda task: task['completed'])  # Necesario ordenar para groupby
    
    # Imprimir directamente el resultado del groupby en esta función.


# Example usage:
tasks = []

tasks = add_task(tasks, "Implementar funcionalidad A")
tasks = add_task(tasks, "Escribir documentación")
tasks = add_task(tasks, "Realizar pruebas unitarias")



tasks = mark_as_complete(tasks, 2)
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

