#9. Crea un programa donde diferentes opciones de decoración pueden ser aplicadas a un texto.

#SOLUCION: Es necesario usar el patrón Decorator
class Text:
    def __init__(self, content):
        self.content = content

    def display(self):
        return self.content


#en el esquema del patron decorador, decorator y text deberían heredar una interfaz comun (una clase abstracta por ejemplo). Pero se puede hacer Duck typing.
#Mientras todas las clases (como Text, BoldDecorator, etc.) tengan un método .display(), no necesitas herencia.
#Python solo necesita que “parezcan” tener el método esperado.

class Decorator:
    def __init__(self, text):
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


    #por que no proxy? El objetivo del proxy es controlar (carga diferida, seguridad, etc.), no agregar funciones
    #por que no adapter? adapter Cambia la interfaz, no agrega comportamiento
    #por que no composite? Composite estructura jerárquica (árbol), Decorator es en capas

