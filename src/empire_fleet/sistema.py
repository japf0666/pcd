from excepciones import DatoInvalidoError
from interfaces import Nave
from dominio import Almacen


class MiImperio:
    def __init__(self) -> None:
        self.naves: list[Nave] = []
        self.almacenes: list[Almacen] = []

    def registrar_nave(self, nave: Nave) -> None:
        if not isinstance(nave, Nave):
            raise DatoInvalidoError("Solo se pueden registrar naves.")
        self.naves.append(nave)

    def registrar_almacen(self, almacen: Almacen) -> None:
        if not isinstance(almacen, Almacen):
            raise DatoInvalidoError("Solo se pueden registrar almacenes.")
        self.almacenes.append(almacen)

    def listar_naves(self) -> list[Nave]:
        return list(self.naves)

    def listar_almacenes(self) -> list[Almacen]:
        return list(self.almacenes)