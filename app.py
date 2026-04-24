from flask import Flask, jsonify, render_template
import threading
import time
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


# =============================
# EJERCICIO 1: MUTEX
# =============================
@app.route("/mutex")
def mutex():
    N = 5
    M = 100000

    # SECUENCIAL
    contador_seq = 0
    inicio_seq = time.time()

    for _ in range(N):
        for _ in range(M):
            contador_seq += 1

    fin_seq = time.time()

    # CONCURRENTE
    contador_conc = 0
    lock = threading.Lock()

    def tarea():
        nonlocal contador_conc
        for _ in range(M):
            with lock:
                contador_conc += 1

    inicio_conc = time.time()

    hilos = []
    for _ in range(N):
        t = threading.Thread(target=tarea)
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    fin_conc = time.time()

    return jsonify({
        "secuencial": {
            "resultado": contador_seq,
            "tiempo": round(fin_seq - inicio_seq, 4)
        },
        "concurrente": {
            "resultado": contador_conc,
            "tiempo": round(fin_conc - inicio_conc, 4)
        }
    })


# =============================
# EJERCICIO 2: SEMÁFORO
# =============================
@app.route("/semaforo")
def semaforo():

    # -------------------------
    # SECUENCIAL
    # -------------------------
    inicio_seq = time.time()
    en_uso = 0
    max_seq = 0

    for i in range(8):
        en_uso += 1
        max_seq = max(max_seq, en_uso)
        time.sleep(0.1)
        en_uso -= 1

    fin_seq = time.time()

    # -------------------------
    # CONCURRENTE CON LOGS
    # -------------------------
    sem = threading.Semaphore(3)
    en_uso = 0
    max_conc = 0
    lock = threading.Lock()
    logs = []

    def tarea(id):
        nonlocal en_uso, max_conc

        logs.append(f"Atleta {id} intentando acceder")

        sem.acquire()

        with lock:
            en_uso += 1
            max_conc = max(max_conc, en_uso)
            logs.append(f"Atleta {id} ENTRA | en uso: {en_uso}")

        time.sleep(random.uniform(0.3, 0.6))

        with lock:
            en_uso -= 1
            logs.append(f"Atleta {id} SALE | en uso: {en_uso}")

        sem.release()

    inicio_conc = time.time()

    hilos = []
    for i in range(8):
        t = threading.Thread(target=tarea, args=(i+1,))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    fin_conc = time.time()

    logs.append(f"Máximo uso alcanzado: {max_conc}")

    return jsonify({
        "secuencial": {
            "max_uso": max_seq,
            "tiempo": round(fin_seq - inicio_seq, 4)
        },
        "concurrente": {
            "max_uso": max_conc,
            "tiempo": round(fin_conc - inicio_conc, 4),
            "logs": logs
        }
    })



# =============================
# EJERCICIO 3: PRODUCTOR-CONSUMIDOR
# =============================
@app.route("/prodcons")
def prodcons():

    # SECUENCIAL
    inicio_seq = time.time()

    produced_seq = 20
    consumed_seq = 20

    fin_seq = time.time()

    # CONCURRENTE
    buffer = []
    size = 10

    mutex = threading.Lock()
    empty = threading.Semaphore(size)
    full = threading.Semaphore(0)

    produced = 0
    consumed = 0

    def productor():
        nonlocal produced
        for i in range(20):
            empty.acquire()
            with mutex:
                buffer.append(i)
                produced += 1
            full.release()

    def consumidor():
        nonlocal consumed
        for i in range(20):
            full.acquire()
            with mutex:
                buffer.pop(0)
                consumed += 1
            empty.release()

    inicio_conc = time.time()

    t1 = threading.Thread(target=productor)
    t2 = threading.Thread(target=consumidor)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    fin_conc = time.time()

    return jsonify({
        "secuencial": {
            "producidos": produced_seq,
            "consumidos": consumed_seq,
            "tiempo": round(fin_seq - inicio_seq, 4)
        },
        "concurrente": {
            "producidos": produced,
            "consumidos": consumed,
            "tiempo": round(fin_conc - inicio_conc, 4)
        }
    })


# =============================
# EJERCICIO 4: LECTORES-ESCRITORES
# =============================
@app.route("/lectores")
def lectores():

    # -------------------------
    # SECUENCIAL
    # -------------------------
    inicio_seq = time.time()
    log_seq = []

    for i in range(3):
        log_seq.append(f"Lector {i+1} leyendo")

    for i in range(2):
        log_seq.append(f"Escritor {i+1} escribiendo")

    fin_seq = time.time()

    # -------------------------
    # CONCURRENTE CON LOGS
    # -------------------------
    read_count = 0
    mutex_lectores = threading.Lock()
    mutex_escritor = threading.Lock()
    logs = []

    def lector(id):
        nonlocal read_count

        logs.append(f"Lector {id} quiere leer")

        with mutex_lectores:
            read_count += 1
            if read_count == 1:
                logs.append(f"Lector {id} bloquea escritores")
                mutex_escritor.acquire()

        logs.append(f"Lector {id} leyendo")
        time.sleep(random.uniform(0.2, 0.4))

        with mutex_lectores:
            read_count -= 1
            if read_count == 0:
                logs.append(f"Lector {id} libera escritores")
                mutex_escritor.release()

        logs.append(f"Lector {id} termina")

    def escritor(id):
        logs.append(f"Escritor {id} quiere escribir")

        mutex_escritor.acquire()
        logs.append(f"Escritor {id} escribiendo")
        time.sleep(random.uniform(0.3, 0.5))
        mutex_escritor.release()

        logs.append(f"Escritor {id} termina")

    inicio_conc = time.time()

    hilos = []

    for i in range(3):
        hilos.append(threading.Thread(target=lector, args=(i+1,)))

    for i in range(2):
        hilos.append(threading.Thread(target=escritor, args=(i+1,)))

    for h in hilos:
        h.start()

    for h in hilos:
        h.join()

    fin_conc = time.time()

    return jsonify({
        "secuencial": {
            "operaciones": log_seq,
            "tiempo": round(fin_seq - inicio_seq, 4)
        },
        "concurrente": {
            "operaciones": logs,
            "tiempo": round(fin_conc - inicio_conc, 4)
        }
    })



# =============================
# EJERCICIO 5: BARRERA
# =============================
@app.route("/barrera")
def barrera():

    # -------------------------
    # SECUENCIAL
    # -------------------------
    inicio_seq = time.time()
    orden_seq = []

    for i in range(5):
        orden_seq.append(f"Hilo {i+1} Fase 1")

    for i in range(5):
        orden_seq.append(f"Hilo {i+1} Fase 2")

    fin_seq = time.time()

    # -------------------------
    # CONCURRENTE CON LOGS
    # -------------------------
    barrier = threading.Barrier(5)
    logs = []

    def tarea(id):
        logs.append(f"Hilo {id} inicia Fase 1")
        time.sleep(random.uniform(0.2, 0.6))

        logs.append(f"Hilo {id} esperando en barrera")
        barrier.wait()

        logs.append(f"Hilo {id} inicia Fase 2")

    inicio_conc = time.time()

    hilos = []
    for i in range(5):
        t = threading.Thread(target=tarea, args=(i+1,))
        hilos.append(t)
        t.start()

    for t in hilos:
        t.join()

    fin_conc = time.time()

    return jsonify({
        "secuencial": {
            "orden": orden_seq,
            "tiempo": round(fin_seq - inicio_seq, 4)
        },
        "concurrente": {
            "orden": logs,
            "tiempo": round(fin_conc - inicio_conc, 4)
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
