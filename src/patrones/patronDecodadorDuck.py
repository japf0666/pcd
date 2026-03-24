# Crea un programa donde diferentes opciones pueden ser aplicadas
# a la edición de un texto.

# SOLUCION: Aplicar el patrón Decorator.

class Text:
    def __init__(self, content):
        self.content = content

    def display(self):
        return self.content


# En el esquema del patron decorador, decorator y text 
# deben  heredar una interfaz comun (por ejemplo, una clase abstracta).

# Pero en Python se puede hacer Duck typing: si todas las clases implicadas
# proporcionan el método esperado (en este caso, .display()), no es necesario
# que hereden de una clase común.

class Decorator:
    def __init__(self, text: str):
        self.text = text

    def display(self) -> str:
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


