# Crea un programa donde diferentes opciones pueden ser aplicadas
# a la edición de un texto.

# SOLUCION: Aplicar el patrón Decorator.

# El patrón Decorator permite agregar funcionalidades a un objeto de 
# forma dinámica, sin modificar su interfaz ni suestructura original. 
# En este caso, podemos crear una clase base para el texto y luego 
# diferentes decoradores para aplicar estilos como negrita, cursiva, 
# mayúsculas, etc.
# 
# El objeto original (Text) se envuelve con decoradores 
# (BoldDecorator, ItalicDecorator, etc.) que agregan funcionalidades adicionales
# para mostrar el mismo texto con diferentes estilos# 
# 
# Pero en python, se puede hacer Duck typing: si todas las clases implicadas
# proporcionan el método esperado (en este caso, .display()), no es necesario 
# que hereden de una clase común.


from abc import ABC, abstractmethod

class TextComponent(ABC):
    @abstractmethod
    def display(self) -> str:
        pass

class Text (TextComponent):
    def __init__(self, content: str):
        self.content = content

    def display(self) -> str:
        return self.content

class Decorator(TextComponent):
    def __init__(self, text: TextComponent):
        self.text = text

    def display(self):
        pass

class BoldDecorator(Decorator):
    def display(self):
        return f"<b>{self.text.display()}</b>"  

class ItalicDecorator(Decorator):
    def display(self):
        return f"<i>{self.text.display()}</i>"
    
class MayusculasDecorator(Decorator):
    def display(self):
        return f"{self.text.display().upper()}"




if __name__ == "__main__":
    text = Text("Hola, mundo!")

    bold_text = BoldDecorator(text)
    italic_text = ItalicDecorator(text)
    may_text=MayusculasDecorator(text)

    print("Texto original:", text.display())
    print("Texto en negrita:", bold_text.display())
    print("Texto en cursiva:", italic_text.display())
    print("Texto en mayuscula:", may_text.display())




    bold_italic = BoldDecorator(ItalicDecorator(text))
    print("Texto en negrita y cursiva:", bold_italic.display())  #permite composicion, uno de los objetivos del patron decorador!!!!


    # ¿por qué no proxy? El objetivo del proxy es representar a 
    # otro objeto y no añadir funcionalidad al objeto per se,
    # aunque a veces se ocupe de otras funciones 
    # (carga diferida, seguridad, etc.), 

    # ¿por qué no adapter? adapter cambia la interfaz, pero no 
    # agrega nuevocomportamiento

    # ¿por qué no composite? Composite define una estructura 
    # jerárquica y tiene un uso mucho más amplio, el decorator 
    # define capas de funcionalidad.

