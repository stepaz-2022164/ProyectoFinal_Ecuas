# Proyecto final de Ecuaciones Diferenciales 1

## Modelación y comparación experimental del avance de un programa SHA-256

Proyecto de aplicación de ecuaciones diferenciales al rendimiento de software. Se mide el avance de un programa que lee un archivo de 512 MiB y calcula su resumen SHA-256. Las mediciones se comparan con un modelo de velocidad constante.

**Curso:** Ecuaciones Diferenciales 1, segundo ciclo de 2026.  
**Área:** Computación y programación.  
**Integrantes:** Zabdi Pelicó, James Sipac y Sergio Tepaz.

## Modelo matemático

Mientras queda trabajo pendiente:

$$\frac{dB}{dt}=v, \qquad B(0)=0.$$

Su solución analítica y el tiempo previsto de finalización son:

$$B(t)=vt, \qquad T=\frac{S}{v}.$$

- $B(t)$: volumen procesado, en MiB.
- $t$: tiempo transcurrido, en segundos.
- $v$: velocidad efectiva de lectura y cálculo, en MiB/s.
- $S$: tamaño del archivo, 512 MiB.

Al incluir la finalización del procesamiento, el avance se expresa como $B(t)=\min(vt,S)$. El modelo aproxima mediante una función continua un conteo que en el programa cambia por bloques.

## Requisitos

- Python 3; el informe documenta mediciones con Python 3.12.14.
- Aproximadamente 512 MiB libres para el archivo temporal, además del espacio para los resultados.
- Git, si se desea clonar el repositorio desde la terminal.

El experimento usa únicamente la biblioteca estándar de Python; no requiere instalar paquetes adicionales.

## Obtener el proyecto

```bash
git clone https://github.com/stepaz-2022164/ProyectoFinal_Ecuas.git
cd ProyectoFinal_Ecuas
```

## Ejecutar el experimento

El código completo aparece en el apéndice B del informe. Para ejecutarlo, debe estar guardado como `experimento.py` en una carpeta exclusiva para el experimento.

```bash
python experimento.py
```

Según la configuración del sistema, el comando puede ser `python3 experimento.py`.

El programa realiza los siguientes pasos:

1. Crea un archivo real de 512 MiB con un patrón determinista.
2. Ejecuta una corrida de calentamiento que se excluye del análisis.
3. Realiza tres corridas de calibración para estimar la velocidad.
4. Realiza cinco corridas de validación sin recalibrar el modelo.
5. Lee bloques de 1 MiB y registra el tiempo acumulado cada 16 MiB.
6. Verifica que las ocho ejecuciones produzcan la misma huella SHA-256.
7. Guarda las mediciones y métricas y elimina el archivo temporal al finalizar correctamente.

El cronometraje mide lectura, cálculo del hash y registro intermedio. La creación del archivo queda fuera del intervalo medido.

## Archivos generados

| Archivo | Contenido |
| --- | --- |
| `mediciones.csv` | Corrida, fase, MiB acumulados y tiempo acumulado en segundos. |
| `resultados.json` | Entorno, huella SHA-256, velocidades, tiempo previsto y métricas por corrida. |
| `archivo_prueba.bin` | Archivo temporal de 512 MiB; se elimina al finalizar correctamente. |

**Cada ejecución sobrescribe los archivos de resultados y el archivo temporal del mismo nombre.** Conservar una copia de los registros que se quieran comparar y usar una carpeta exclusiva para el experimento.

## Análisis de resultados

La velocidad del modelo es el promedio de las velocidades de las tres corridas de calibración. Se compara la predicción fija con las cinco corridas de validación mediante:

- Error absoluto medio del avance (MAE).
- Raíz del error cuadrático medio del avance (RMSE).
- Coeficiente $R^2$ respecto de la predicción calibrada.
- Error porcentual firmado del tiempo de finalización.

El informe también presenta el error porcentual absoluto medio del tiempo y la variabilidad de las velocidades.

### Valores reportados en el informe

| Indicador | Valor |
| --- | --- |
| Velocidad calibrada | 1457.940 MiB/s |
| Tiempo previsto para 512 MiB | 0.351181 s |
| Error porcentual absoluto medio del tiempo en validación | 4.62 % |
| Coeficiente de variación de la velocidad en validación | 4.59 % |

Estos valores corresponden a las mediciones descritas en el informe, realizadas en un entorno remoto. Una nueva ejecución produce sus propios registros; el equipo, la caché y la carga del sistema pueden modificar los resultados.

## Informe y código LaTeX

El informe contiene la introducción, los supuestos del modelo, la solución analítica, el diseño experimental, las tablas, las gráficas, la discusión, las conclusiones y el código Python.

El apéndice A describe los archivos fuente `Anteproyecto_Ecuas.tex` y `Anteproyecto_Ecuas.txt`. Cuando se incorporen al repositorio, el archivo `.tex` puede compilarse con pdfLaTeX o abrirse en Overleaf. Según el informe, las coordenadas de las gráficas y el código están incluidos en el documento y no requieren imágenes externas ni una bibliografía separada.

## Alcance y limitaciones

El estudio evalúa un único tamaño de archivo, contenido, algoritmo y esquema de lectura. Las corridas son breves y consecutivas y pueden beneficiarse de la caché del sistema. La velocidad efectiva incluye tanto lectura como cálculo; no representa exclusivamente el rendimiento del disco o del procesador. Los resultados describen ese montaje y no garantizan el mismo rendimiento en otros equipos.

La implementación documentada mide una ejecución de software y la compara con una solución analítica. No implementa dos métodos numéricos iterativos para resolver ecuaciones diferenciales.

## Referencias

- Strang, G. y Herman, E. J. (2016). *Calculus Volume 2*, sección 4.3: [Separable Equations](https://openstax.org/books/calculus-volume-2/pages/4-3-separable-equations).
- Python Software Foundation. [Documentación de hashlib](https://docs.python.org/3/library/hashlib.html).
- Python Software Foundation. [Documentación de time](https://docs.python.org/3/library/time.html).
