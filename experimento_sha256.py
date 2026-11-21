"""Experimento real SHA-256. Ejecutar: python experimento.py"""
import csv
import hashlib
import json
import platform
import ssl
import statistics as st
import time
from pathlib import Path

MIB = 2 ** 20
TOTAL = 512
PASO = 16
DESTINO = Path(__file__).resolve().parent
ARCHIVO = DESTINO / "archivo_prueba.bin"

def corrida(numero, fase):
    puntos = []
    h = hashlib.sha256()
    with ARCHIVO.open("rb") as f:
        inicio = time.perf_counter_ns()
        for bloque in range(1, TOTAL + 1):
            datos = f.read(MIB)
            if len(datos) != MIB:
                raise RuntimeError("Archivo incompleto")
            h.update(datos)
            if bloque % PASO == 0:
                segundos = (time.perf_counter_ns() - inicio) / 1e9
                puntos.append(dict(corrida=numero, fase=fase,
                                   mib=bloque, segundos=segundos))
    return puntos, h.hexdigest()

def main():
    # Archivo materializado; su escritura queda fuera del cronometraje.
    patron = bytes(range(256)) * 4096
    with ARCHIVO.open("wb") as f:
        for _ in range(TOTAL):
            f.write(patron)
    corrida(0, "calentamiento")
    filas, resumen, hashes = [], [], []
    for numero in range(1, 9):
        fase = "calibracion" if numero <= 3 else "validacion"
        puntos, digest = corrida(numero, fase)
        filas.extend(puntos)
        duracion = puntos[-1]["segundos"]
        resumen.append(dict(corrida=numero, fase=fase,
                            segundos=duracion, velocidad=TOTAL/duracion))
        hashes.append(digest)
    assert len(set(hashes)) == 1, "Los hashes no coinciden"
    with (DESTINO / "mediciones.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    cal = [x["velocidad"] for x in resumen[:3]]
    v = st.mean(cal)
    estimado = TOTAL / v
    metricas = []
    for corrida_v in resumen[3:]:
        pp = [x for x in filas if x["corrida"] == corrida_v["corrida"]]
        y = [p["mib"] for p in pp]
        errores = [p["mib"] - v*p["segundos"] for p in pp]
        sse = sum(e*e for e in errores)
        sst = sum((b-st.mean(y))**2 for b in y)
        metricas.append(dict(corrida=corrida_v["corrida"],
            rmse=(sse/len(pp))**0.5, mae=st.mean(map(abs, errores)),
            r2=1-sse/sst,
            error_t=100*(estimado-corrida_v["segundos"])
                         /corrida_v["segundos"]))
    cpu = platform.processor() or "No reportado"
    try:
        cpu = next(line.split(":", 1)[1].strip()
                   for line in Path("/proc/cpuinfo").read_text().splitlines()
                   if line.startswith("model name"))
    except (OSError, StopIteration):
        pass
    resultado = dict(python=platform.python_version(), sistema=platform.system(),
        arquitectura=platform.machine(), cpu=cpu, openssl=ssl.OPENSSL_VERSION,
        reloj=time.get_clock_info("perf_counter")._asdict()
              if hasattr(time.get_clock_info("perf_counter"), "_asdict")
              else vars(time.get_clock_info("perf_counter")),
        total_mib=TOTAL, paso_mib=PASO, sha256=hashes[0],
        resumen=resumen, v=v, tiempo_estimado=estimado,
        sd_calibracion=st.stdev(cal), metricas=metricas)
    (DESTINO / "resultados.json").write_text(
        json.dumps(resultado, indent=2), encoding="utf-8")
    ARCHIVO.unlink()
    print(json.dumps(resultado, indent=2))

if __name__ == "__main__":
    main()

