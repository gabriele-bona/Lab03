import csv
from strumento import Strumento
from prestito import Prestito
from operator import attrgetter

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = [] #lista per memorizzare gli oggetti di tipo Strumento
        self.prestiti = [] #lista per memorizzare gli oggetti di tipo Prestito attivi

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        self._responsabile = nuovo_responsabile

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for riga in reader:
                    # creo un nuovo oggetto di tipo Strumento
                    s = Strumento(riga[0].strip(), riga[1].strip(), riga[2].strip(), riga[3].strip(), riga[4].strip()) # riga[0]=codice, riga[1]=tipo, riga[2]=marca, riga[3]=anno, riga[4]=valore
                    self.strumenti.append(s)
        except FileNotFoundError:
            # Se il file non esiste, sollevo l'eccezione
            raise FileNotFoundError(f"Il file '{file_path}' non è stato trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        max_id = 0
        # Ciclo su tutti gli strumenti presenti per trovare il numero ID più alto
        for s in self.strumenti:
            try:
                # s.codice[1:] estrae la parte numerica dopo la 'S'
                numero = int(s.codice[1:])
                if numero > max_id:
                    max_id = numero
            except ValueError:
                # Se un codice non rispetta il formato standard lo ignoro
                pass
        # Genero il nuovo codice incrementando di 1 il valore massimo trovato
        nuovo_codice = f'S{max_id + 1}'
        # Creo il nuovo oggetto Strumento e lo aggiungo al deposito
        nuovo_strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_strumento)
        # Restituisco l'oggetto appena creato
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti, key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # CONTROLLO 1: Verifico se lo strumento esiste nel sistema
        strumento_trovato = False
        for s in self.strumenti:
            if s.codice == id_strumento:
                strumento_trovato = True
                break
        if not strumento_trovato:
            raise Exception(f"Errore: Lo strumento '{id_strumento}' non esiste nel deposito.")
        # CONTROLLO 2: Verifico se lo strumento è già attualmente in prestito
        for p in self.prestiti:
            if p.id_strumento == id_strumento:
                raise Exception(f"Errore: Lo strumento '{id_strumento}' è già stato dato in prestito.")
        # GENERAZIONE ID PRESTITO: Calcolo il numero progressivo più alto per i prestiti
        max_id = 0
        for p in self.prestiti:
            try:
                numero = int(p.id_prestito[1:])
                if numero > max_id:
                    max_id = numero
            except ValueError:
                pass
        id_prestito = f"P{max_id + 1}"
        # Creo l'oggetto Prestito, lo salvo nella lista e lo restituisco
        p = Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestiti.append(p)
        return p

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        for p in self.prestiti:
            if p.id_prestito == id_prestito:
                self.prestiti.remove(p) # Rimuovo l'oggetto dalla lista
                return # Esco subito dal metodo a rimozione avvenuta
        # Se il ciclo finisce senza trovare l'ID, scateno l'errore
        raise Exception(f"Errore: Nessun prestito attivo trovato con ID '{id_prestito}'.")
