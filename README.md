# Calculadora Basada en Gestos
**Asignatura:** Sistemas Interactivos Inteligentes (UIE)
**Autor:** Enrique Posada

## Sistema Operativo y Entorno
Este proyecto ha sido desarrollado y probado en Windows utilizando uv como gestor de paquetes y entornos virtuales, tal y como se indica en los requisitos de la práctica

# Creación del entorno virtual
uv venv

# Instalación de dependencias
uv pip install -r requirements.txt

# Probar la cámara
uv run python src/gest-calc/webcam_test.py

# Ejecutar la calculadora
uv run python src/gest-calc/main.py

# Gestos y su equivalencia

## Mano Derecha
Se usa para poner los números, el punto decimal y borrar el último caracter.
Su funcionamiento varía según si muestra la palma de la mano o el revés de la mano.

Cuando se muestra la palma de la mano, se pueden introducir números del 0 al 5, según el número de dedos levantados, para los números restantes (6-9) sigue la misma lógica pero mostrando el revés de la mano. Para introducir el número 6 se levanta un dedo de 
la mano, para el 7 se levantan dos y así hasta el 9. Además, si el usuario cierra la mano borra el último caracter introducido y
si levanta todos pone el punto decimal.

## Mano Izquierda
0 dedos levantados = Borrar todo (Reset)
1 dedo levantado = Sumar
2 dedos levantados = Restar
3 dedos levantados = Multiplicar 
4 dedos levantados = Dividir
5 dedos levantados = Resultado

