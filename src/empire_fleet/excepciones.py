class MiImperioError(Exception):
    pass


class StockInsuficienteError(MiImperioError):
    pass


class RepuestoNoEncontradoError(MiImperioError):
    pass


class RepuestoNoAutorizadoError(MiImperioError):
    pass


class DatoInvalidoError(MiImperioError):
    pass

class UsuarioNoAutorizadoError(MiImperioError):
    pass