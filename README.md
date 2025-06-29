# ElectronTransportSim
Interfaz interactiva para simular el transporte colisional de electrones en plasmas de fusión confinados magnéticamente.

Este repositorio contiene un script en Python diseñado para simular la **difusividad transversal de partículas cargadas en un plasma** bajo efectos colisionantes. El enfoque está inspirado en escenarios relevantes para plasmas de fusión como los de tipo tokamak (JET, ITER).

## 🔧 Requisitos

- Python ≥ 3.10
- numpy
- matplotlib
- tkinter (usually included with standard Python distributions)

Para instalar las librerías necesarias, ejecuta en tu terminal (bash, PowerShell o CMD):

pip install numpy
pip install matplotlib
pip install tkinter

## Descripción del script

El script simula la trayectoria de electrones sometidos a colisiones y un campo magnético uniforme, calculando parámetros físicos como la frecuencia de colisión, frecuencia ciclotrón y radio de Larmor. Permite visualizar:

- Trayectorias de partículas con colisiones.

- Distribución inicial de velocidades de las partículas.

- Histograma gaussiano generado mediante el método de transformada inversa.

- Barra de herramientas para ampliar, guardar o moverse por las imágnes que se crean.

## Cómo usarlo

1. Ejecuta el script en tu terminal o entorno Python:

python ElectronTransportSim.py

2. Ingresa los parámetros en la interfaz gráfica:

- Temperatura (K): Temperatura electrónica en kelvin (ej. 1.16e7).

- Número de partículas: Cantidad de partículas a simular (ej. 10000).

- Número de colisiones: Número de colisiones o pasos en la simulación (ej. 100).

- Campo magnético B0 (T): Valor del campo magnético en teslas (ej. 3.4).

3. Utiliza:

- Simular para comenzar la simulación.

- Aparecen por pantalla los parámetros físicos relevantes para el problema y damos a ok.

- Visualizar las trayectorias en pantalla automáticamente

- Visualizar la distribución inicial de velocidades.

- Ver el histograma gaussiano asociado.

## Contacto

Para dudas o sugerencias, puedes abrir un issue en este repositorio.

## Licencia

Este proyecto está bajo licencia MIT. Puedes usarlo y modificarlo libremente siempre que incluyas el aviso de derechos de autor incluido en LICENSE en todas las copias o porciones sustanciales del Software.
