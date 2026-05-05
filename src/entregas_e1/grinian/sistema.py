from clases import *
from excepciones import *

class Sistema:
    def __init__(self):
        self.almacenes = []
        self.naves = []
        self.usuarios = []
        self.usuario_activo = None

# getters
    def get_almacenes(self):
        return self.almacenes

    def get_naves(self):
        return self.naves

    def get_usuarios(self):
        return self.usuarios
    
    def get_usuario_activo(self):
        return self.usuario_activo

# metodos
    #metodos de la sesion
    def iniciar_sesion(self,ID:str):
        for usuario in self.usuarios:
            if usuario.ID == ID:
                self.usuario_activo = usuario
                return f"sesion iniciada, {usuario.nombre} , {type(usuario).__name__}"

    def cerrar_sesion(self):
        if self.usuario_activo:
            print("sesion cerrada")
        self.usuario_activo = None

    #metodos para añadir objetos a las listas de elementos 
    def registrar_almacenes(self,almacen:Almacen):
        self.get_almacenes().append(almacen)

    def registrar_naves(self,nave:Nave):
        self.get_naves().append(nave)

    def registrar_usuario(self,usuario):
        self.get_usuarios().append(usuario)

    #metodos de nave-comandante
    def encontrar_repuesto(self,nombre_repuesto:str):
        """
        El metodo encuentra los repuestos en los distintos almacenes
        para devolver los almacenes y las caracteristicas de los repuestos
        en cada almacen del tipo que se busca

        no tiene ninguna accion diferente y se puede usar el metodo siempre que la sesion este iniciada
        """

        if self.get_usuario_activo() is None:
            raise AccesoDenegadoError("Iniciar sesion primero")
        
        resultados = []
        for almacen in self.get_almacenes():
            repuesto = almacen.buscar_repuesto(nombre_repuesto)

            if repuesto != -1:
                resultados.append(f"{repuesto} en el almacen {almacen}")
            else:
                return "el repuesto no se encontro en ningun lugar"
        
        return resultados

    def adquirir_repuesto(self,nombre_repuesto:str,nombre_almacen:str,cantidad : int):

        """
        El metodo requiere de los parametros nombre_repuesto, nombre almacen y cantidad
        para ejecutar la accion de añadir el repuesto a la nave indicada

        el motivo por el que se pide nombre del repuesto y almacen es para que el COMANDANTE
        pueda decidir de donde sacarlo y en las cantidades que quiera

        el porque no pide nave es porque este metodo solo se puede ejecutar siendo COMANDANTE
        y tiene una nave asignada a el por lo que accede a esa informacion directamente no la pide

        esto se entiende con como funciona el metodo anterior buscar_repuesto
        """

        if not isinstance(self.get_usuario_activo(),Comandante):
            raise AccesoDenegadoError("el usuario no es de teipo comandante")
        
        nave_asignada = self.get_usuario_activo().get_nave()

        almacen_origen = None
        for almacen in self.get_almacenes():
            if almacen.get_nombre() == nombre_almacen:
                almacen_origen = almacen
                break
        
        if almacen_origen == None:
            raise ValueError("No se encontró el almacén especificado.")

        repuesto = almacen_origen.buscar_repuesto(nombre_repuesto)
        if repuesto == -1:
            raise ValueError("no se encontro el repuesto en el almacen,\n prueba comprobar el nombre")
        
        if repuesto.get_cantidad() < cantidad:
            raise StockInsuficienteError("no hay stock suficiente en el almacen para suplir las necesidades")

        cantidad2 = repuesto.get_cantidad() - cantidad
        repuesto.set_cantidad(cantidad2)

        nave_asignada.añadir_repuestos(repuesto)
        
        return f"se añadio la cantidad indicada del repuesto indicado del almacen indicado" #decorar esta mierda de salida

    def consultar_nave(self):
            
        """
        Sirve para poder revisar facilmente el numero de repuestos de la nave
        esto funciona por la suma de cadena de texto

        por cada repuesto en la lista de repuestos suma a la cadena original el get_nombre
        y get_cantidad 
        """
        if not isinstance(self.get_usuario_activo(),Comandante):
            raise AccesoDenegadoError("el usuario no es de teipo comandante")
        
        nave_asignada = self.get_usuario_activo().get_nave()
        lista_repuestos = nave_asignada.get_repuestos()


        if len(lista_repuestos) == 0:
            return "No hay repuestos"

        resultado = "--------- Numero de repuestos\n"
            
        for repuesto in lista_repuestos:
            resultado += f"- {repuesto.get_nombre()} - {repuesto.get_cantidad()}\n " 
            

        return resultado
    
    def enviar_mensaje(self, clave_destino: int, mensaje: str):

        """
        el motivo por el que pide la clave destino es para buscar dentro 
        de la pool de naves del sistema cual coincide con ese numero, 
        como si fuera un numero de telefono

        el porque no pide la nave de origen es porque este metodo solo 
        se puede ejecutar siendo COMANDANTE y accede a su nave directamente

        luego formatea el string y lo mete en la nave destino
        """
        if not isinstance(self.get_usuario_activo(),Comandante):
            raise AccesoDenegadoError("el usuario no es de teipo comandante")
        
        nave_origen = self.get_usuario_activo().get_nave()
        nave_destino = None
        

        for nave in self.get_naves():

            if nave.get_clave() == clave_destino:
                nave_destino = nave
                break
                
        if nave_destino is None:
            raise ValueError(f"No hay ninguna nave con clave {clave_destino}.")
            
        texto_final = f"De {nave_origen.get_nombre()} ({nave_origen.get_identificador()}): {mensaje}"
        nave_destino.recibir_mensaje(texto_final)
        
        return "Mensaje transmitido."

    def consultar_mensajes(self):

        """
        El metodo no pide parametros porque solo lee la bandeja
        de entrada de la nave asignada al usuario activo

        primero comprueba que el usuario sea tipo COMANDANTE
        y despues simplemente saca su nave y devuelve la lista cruda 
        de mensajes que tiene guardados usando el metodo de la nave    
        """

        if not isinstance(self.get_usuario_activo(),Comandante):
            raise AccesoDenegadoError("el usuario no es de teipo comandante")
        
        nave_actual = self.get_usuario_activo().get_nave()
        return nave_actual.leer_mensajes()

    #metodos de almacen-operario
    def crear_repuesto(self,nombre:str, proveedor:str, cantidad:int, coste:float):

        """
        El metodo solo puede ser usado por usuarios del tipo OPERARIO
        por eso comprueba que que el tipo sea ese mismo.

        igual que en los anteriores metodos el almacen no hace falta pasarlo
        como parametro el operario solo puede tener un almacen y accede atraves
        de el a este

        El metodo comprueba que no exista un objeto repuesto ya existente en el almacen
        si existe salta una excepcion
        si no existe lo añade segun los parametros pasados por el usuario
        """

        if not isinstance(self.get_usuario_activo(),Operario):
            raise AccesoDenegadoError("el usuario no es de teipo OPERARIO")
        
        almacen_asignado = self.get_usuario_activo().get_almacen()

        if almacen_asignado.buscar_repuesto(nombre) != -1 : #comprueba si ya existe
            raise ValueError("ya existe el repuesto")
        
        nuevo_repuesto = Repuesto(nombre,proveedor,cantidad,coste)
        almacen_asignado.agregar_repuesto(nuevo_repuesto)

        return "repuesto ha sido añadido" #decorar tambien esta salida

    def actualizar_stock(self,nombre_repuesto:str, cantidad_sumar:int):

        """
        el motivo por el que no pide el almacen es porque este metodo solo 
        se puede ejecutar siendo OPERARIO y ya tiene un almacen asignado 
        al que accede directamente

        despues busca el repuesto indicado dentro de su propio almacen,
        saca la cantidad actual, le suma la cantidad nueva y la vuelve a
        guardar modificando el objeto
        """

        if not isinstance(self.get_usuario_activo(),Operario):
            raise AccesoDenegadoError("el usuario no es de teipo OPERARIO")
        
        almacen_asignado = self.get_usuario_activo().get_almacen()
        repuetso = almacen_asignado.buscar_repuesto(nombre_repuesto)

        if repuetso == -1:
            raise ValueError("No existe el repuesto")
        
        stock_actual = repuetso.get_cantidad()
        nueva_cantidad = stock_actual + cantidad_sumar
        repuetso.set_cantidad(nueva_cantidad)

        return "repuesto actualizado" #decorar la salida...
    
    def consultar_almacen(self):

        """
        el motivo por el que no pide de que almacen sacar los datos es 
        porque asume que el usuario es OPERARIO y accede directamente 
        a su lugar de trabajo

        luego saca la lista de piezas y comprueba si esta vacia,
        si no lo esta, hace un bucle para sacar el nombre y la cantidad 
        de cada repuesto y devuelve un string ya formateado para imprimir
        """

        almacen_asignado = self.get_usuario_activo().get_almacen()
        lista_repuestos = almacen_asignado.get_catalogo()


        if len(lista_repuestos) == 0:
            return "No hay repuestos"

        resultado = "---------\n"
            
        for repuesto in lista_repuestos:
            resultado += f"- {repuesto.get_nombre()} - {repuesto.get_cantidad()}\n " 
            

        return resultado