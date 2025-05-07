# Relazione Tecnica - Web Server Statico in Python

## 1. Introduzione

### Obiettivo del progetto
L'obiettivo di questo progetto è la creazione di un semplice **web server HTTP** utilizzando **Python**, in grado di servire un sito web statico. Il server è progettato per rispondere a richieste HTTP di tipo `GET`, restituendo file come HTML, CSS e immagini dal file system.

Sono stati implementati alcuni aspetti opzionali, tra cui:
- La gestione dei MIME types per garantire che i file siano inviati con l'intestazione `Content-Type` corretta.
- Il logging delle richieste HTTP in un file di log.
- Aggiunta di animazioni tramite il file css

### Tecnologie utilizzate
- **Python**: per l'implementazione del server.
- **Socket programming**: per la gestione delle connessioni di rete.
- **HTML/CSS**: per la realizzazione del sito web statico.
- **Threading**: per gestire più richieste in parallelo.
- **File I/O**: per la lettura dei file richiesti e il logging.

## 2. Progettazione del Web Server

### Descrizione generale
Il server HTTP è realizzato in Python e utilizza **socket TCP** per ricevere richieste dai browser web. Gestisce richieste `GET` e restituisce il contenuto richiesto o una pagina di errore 404 se il file non esiste.

### Struttura del server
- Crea un socket TCP che ascolta su `localhost:8080`.
- Accetta connessioni entranti e gestisce ogni richiesta in un thread separato.
- Analizza la richiesta HTTP per determinare il metodo e il percorso.
- Serve i file statici presenti nella directory `www/`.
- Invia la risposta HTTP con codice `200 OK` o `404 Not Found`.

### Gestione degli errori
Quando il file richiesto non esiste, il server:
- Genera una semplice pagina HTML di errore.
- Restituisce una risposta HTTP con codice di stato `404 Not Found`.

## 3. Implementazione del Server

### Struttura del codice
Il codice è organizzato nei seguenti blocchi principali:
- **Creazione e configurazione del socket**:
  - Uso di `socket.socket()` e `bind()` su `localhost:8080`.
  - `listen(10)` per accettare un massimo di 10 connessioni in coda.
- **Parsing della richiesta**:
  - Si legge la prima riga della richiesta HTTP e si estrae il metodo e il percorso.
- **Risposta HTTP**:
  - Se il file esiste, viene letto in binario e inviato con intestazioni appropriate.
  - In caso contrario, viene restituita una pagina di errore.
- **Gestione dei file statici**:
  - I file vengono cercati nella directory `www/`, mantenendo la struttura delle sottocartelle.
- **Gestione dei MIME types**:
  - Un dizionario associa estensioni come `.html`, `.css` e `.jpg` ai rispettivi MIME type.
- **Logging delle richieste**:
  - Ogni richiesta viene registrata in un file `log.txt`, includendo timestamp, metodo, percorso e codice di risposta.

## 4. Sito Web Statico

### Descrizione del sito
Il sito web statico è composto da **quattro pagine HTML**, collegate tra loro, che mostrano contenuti informativi. Lo stile è stato definito tramite file CSS, e vengono caricate immagini nella pagina dedicata ai trofei.

### Struttura delle pagine HTML
- **Home page**: una panoramica introduttiva con le info sulle prossime partite.
- **Pagina "Chi siamo"**: breve descrizione della storia della squadra ed elenco dei giocatori con numero, nazionalità, età, ruolo.
- **Pagina "Trofei"**: mostra i trofei vinti dalla squadra con aggiunta di immagini(`.jpg`).

### Design e responsive layout
Il sito è stato stilizzato con **CSS**, e include un layout flessibile con aggiunta di "animazioni"

## 5. Prove e Risultati

### Test del server
Il server è stato testato in locale su `http://localhost:8080`:
- ✅ Le pagine HTML sono servite correttamente (risposta 200 OK).
- ✅ Le immagini e il CSS vengono caricati correttamente.
- ✅ In caso di richieste a file non esistenti, viene restituito correttamente un errore `404`.

## 6. Conclusioni

### Risultati ottenuti
Il progetto ha raggiunto l’obiettivo di realizzare un **web server HTTP semplice ma funzionale**, in grado di:
- Servire file statici da una directory locale.
- Gestire correttamente i MIME types.
- Rispondere con codici HTTP adeguati.
- Registrare le richieste in un file di log.
- Gestire più richieste simultaneamente grazie all’uso di thread.


**Giuseppe Fusco, Ingegneria e Scienze Informatiche (Università di Bologna) A.A 2024/25**
