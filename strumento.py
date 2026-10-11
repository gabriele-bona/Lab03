class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f'Strumento n.{self.codice}: {self.tipo} di marca {self.marca}, acquistato nel {self.anno_acquisto} a {self.valore} euro'

    def __repr__(self):
        return f'Strumento({self.codice}, {self.tipo}, {self.marca}, {self.anno_acquisto}, {self.valore})'
