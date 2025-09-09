from tkinter import filedialog
import customtkinter as ctk
from tkinter import messagebox
import math
from scipy.stats import chi2
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración del tema de los gráficos
plt.style.use('dark_background')
theme_bg = '#2B4162'
data_color = '#8B9DAE'
accept_color = '#508D4E'
reject_color = '#A41C34'
text_color = '#F2F4F7'

# --- Funciones de Generación de Números ---

def calcular_cuadrados_medios(entrada_y0, entrada_n, entrada_d):
    """Función para el algoritmo de Cuadrados Medios."""
    try:
        y0_str = entrada_y0
        n_iteraciones = int(entrada_n)
        n_digitos = int(entrada_d)
        if not y0_str.isdigit() or len(y0_str) != n_digitos:
            raise ValueError(f"La semilla debe ser un número entero de exactamente {n_digitos} dígitos.")
        
        numeros_ri = []
        tabla = "N\tY_i\tY_i²\tX_(i+1)\t\tR_i\n"
        y_actual = int(y0_str)
        for i in range(n_iteraciones):
            y_actual_str = str(y_actual).zfill(n_digitos)
            y_cuadrado = str(int(y_actual_str) ** 2)
            if len(y_cuadrado) % 2 != 0:
                y_cuadrado = "0" + y_cuadrado
            mitad = (len(y_cuadrado) - n_digitos) // 2
            x_siguiente = y_cuadrado[mitad:mitad + n_digitos]
            r_i = float("0." + x_siguiente)
            numeros_ri.append(r_i)
            tabla += f"{i+1}\t{y_actual_str}\t{y_cuadrado}\t{x_siguiente}\t\t{r_i}\n"
            y_actual = int(x_siguiente)
        
        return tabla, numeros_ri
    except ValueError as e:
        raise ValueError(f"Error en Cuadrados Medios: {e}")

def calcular_productos_medios(entrada_y0, entrada_y1, entrada_n, entrada_d):
    """Función para el algoritmo de Productos Medios."""
    try:
        y0_str = entrada_y0
        y1_str = entrada_y1
        n_iteraciones = int(entrada_n)
        n_digitos = int(entrada_d)
        if not y0_str.isdigit() or not y1_str.isdigit() or len(y0_str) != n_digitos or len(y1_str) != n_digitos:
            raise ValueError(f"Ambas semillas deben ser números enteros de exactamente {n_digitos} dígitos.")
            
        numeros_ri = []
        tabla = "N\tY_(i-1)\tY_i\tProducto\tX_(i+1)\t\tR_i\n"
        y_anterior = int(y0_str)
        y_actual = int(y1_str)
        for i in range(n_iteraciones):
            producto = str(y_anterior * y_actual).zfill(n_digitos * 2)
            mitad = (len(producto) - n_digitos) // 2
            x_siguiente = producto[mitad:mitad + n_digitos]
            r_siguiente = float("0." + x_siguiente)
            numeros_ri.append(r_siguiente)
            tabla += f"{i+1}\t{str(y_anterior).zfill(n_digitos)}\t{str(y_actual).zfill(n_digitos)}\t{producto}\t{x_siguiente}\t\t{r_siguiente}\n"
            y_anterior = y_actual
            y_actual = int(x_siguiente)
        
        return tabla, numeros_ri
    except ValueError as e:
        raise ValueError(f"Error en Productos Medios: {e}")

def calcular_multiplicador_constante(entrada_a, entrada_y0, entrada_n, entrada_d):
    """Función para el algoritmo de Multiplicador Constante."""
    try:
        a = int(entrada_a)
        y0_str = entrada_y0
        n_iteraciones = int(entrada_n)
        n_digitos_y = int(entrada_d)
        if not y0_str.isdigit() or len(y0_str) != n_digitos_y or len(str(a)) != n_digitos_y:
            raise ValueError(f"La constante y la semilla deben ser números enteros de exactamente {n_digitos_y} dígitos.")
        
        numeros_ri = []
        tabla = "N\ta\t\tY_i\t\tProducto\tY_(i+1)\t\tR_i\n"
        y_actual = int(y0_str)
        for i in range(n_iteraciones):
            y_actual_str = str(y_actual).zfill(n_digitos_y)
            producto = str(a * y_actual).zfill(n_digitos_y * 2)
            mitad = (len(producto) - n_digitos_y) // 2
            y_siguiente = producto[mitad:mitad + n_digitos_y]
            r_i = float("0." + y_siguiente)
            numeros_ri.append(r_i)
            tabla += f"{i+1}\t{a}\t\t{y_actual_str}\t\t{producto}\t{y_siguiente}\t\t{r_i}\n"
            y_actual = int(y_siguiente)
            
        return tabla, numeros_ri
    except ValueError as e:
        raise ValueError(f"Error en Multiplicador Constante: {e}")

# --- Funciones de Pruebas Estadísticas ---

def ejecutar_prueba_medias_con_input(resultados_texto, entrada_z, numeros_ri):
    """Ejecuta la prueba de medias con el valor Z proporcionado por el usuario."""
    if not numeros_ri:
        resultados_texto.delete(1.0, ctk.END)
        resultados_texto.insert(ctk.END, "Error: No se han generado números para ejecutar la prueba.")
        return
    
    try:
        z_alfa_2 = float(entrada_z.replace(',', '.'))
    except ValueError:
        resultados_texto.delete(1.0, ctk.END)
        resultados_texto.insert(ctk.END, "Error: Por favor, ingrese un valor numérico para Z_alpha/2.")
        return
    
    n = len(numeros_ri)
    suma_ri = sum(numeros_ri)
    promedio_r = suma_ri / n
    denominador = math.sqrt(12 * n)
    li_r = 0.5 - z_alfa_2 * (1 / denominador)
    ls_r = 0.5 + z_alfa_2 * (1 / denominador)
    
    resultados_texto.delete(1.0, ctk.END)
    resultados_texto.insert(ctk.END, "Resultados de la Prueba de Medias:\n\n")
    resultados_texto.insert(ctk.END, f"Número de iteraciones (n): {n}\n")
    resultados_texto.insert(ctk.END, f"Promedio calculado (r): {promedio_r:.4f}\n")
    resultados_texto.insert(ctk.END, f"Límite de Aceptación Inferior (LI_r): {li_r:.4f}\n")
    resultados_texto.insert(ctk.END, f"Límite de Aceptación Superior (LS_r): {ls_r:.4f}\n\n")
    
    if li_r <= promedio_r <= ls_r:
        resultados_texto.insert(ctk.END, "Conclusión: El promedio cae dentro del rango de aceptación.\nEl conjunto de números es apto para usarse en un estudio de simulación.")
    else:
        resultados_texto.insert(ctk.END, "Conclusión: El promedio no cae dentro del rango de aceptación.\nEl conjunto de números no es apto para usarse en un estudio de simulación.")

def ejecutar_prueba_varianza_con_confianza(resultados_texto, entrada_confianza, numeros_ri):
    """
    Ejecuta la prueba de varianza con el nivel de confianza como valor decimal.
    Basado en la lógica del código de referencia proporcionado.
    """
    if not numeros_ri or len(numeros_ri) < 2:
        resultados_texto.delete(1.0, ctk.END)
        resultados_texto.insert(ctk.END, "Error: Se requieren al menos 2 números para la prueba de varianza.")
        return
    try:
        nivel_confianza = float(entrada_confianza.replace(',', '.'))
        if not (0 < nivel_confianza < 1):
            raise ValueError
    except ValueError:
        resultados_texto.delete(1.0, ctk.END)
        resultados_texto.insert(ctk.END, "Error: Ingrese un valor numérico válido entre 0 y 1 para el nivel de confianza.")
        return
        
    n = len(numeros_ri)
    grados_libertad = n - 1
    alfa = 1 - nivel_confianza
    
    # Calcular valores de Chi-cuadrada
    chi_li = chi2.ppf(alfa / 2, grados_libertad)
    chi_ls = chi2.ppf(1 - alfa / 2, grados_libertad)
    
    # Calcular varianza de la muestra
    promedio_r = sum(numeros_ri) / n
    sumatoria_varianza = sum([(ri - promedio_r) ** 2 for ri in numeros_ri])
    varianza_r = sumatoria_varianza / grados_libertad
    
    # Calcular los límites de aceptación para la varianza
    li_varianza = chi_li / (12 * grados_libertad)
    ls_varianza = chi_ls / (12 * grados_libertad)
    
    resultados_texto.delete(1.0, ctk.END)
    resultados_texto.insert(ctk.END, "Resultados de la Prueba de Varianza (Modo Automático):\n\n")
    resultados_texto.insert(ctk.END, f"Número de iteraciones (n): {n}\n")
    resultados_texto.insert(ctk.END, f"Grados de libertad: {grados_libertad}\n")
    resultados_texto.insert(ctk.END, f"Nivel de confianza: {nivel_confianza * 100:.0f}%\n")
    resultados_texto.insert(ctk.END, f"Varianza calculada (v(r)): {varianza_r:.4f}\n")
    resultados_texto.insert(ctk.END, f"Valores de Chi-cuadrada calculados: {chi_li:.4f} (LI) y {chi_ls:.4f} (LS)\n")
    resultados_texto.insert(ctk.END, f"Límite de Aceptación Inferior (LI_v(r)): {li_varianza:.4f}\n")
    resultados_texto.insert(ctk.END, f"Límite de Aceptación Superior (LS_v(r)): {ls_varianza:.4f}\n\n")
    
    if li_varianza <= varianza_r <= ls_varianza:
        resultados_texto.insert(ctk.END, "Conclusión: La varianza cae dentro del rango de aceptación. El conjunto de números pasa la prueba de varianza.")
    else:
        resultados_texto.insert(ctk.END, "Conclusión: La varianza no cae dentro del rango de aceptación. El conjunto de números no pasa la prueba de varianza.")

def ejecutar_prueba_uniformidad_chi_cuadrada(resultados_texto, entrada_intervalos, entrada_confianza, numeros_ri):
    """Ejecuta la prueba de uniformidad de Chi-cuadrada con una salida tabulada."""
    if not numeros_ri or len(numeros_ri) < 2:
        resultados_texto.delete(1.0, ctk.END)
        resultados_texto.insert(ctk.END, "Error: Primero debe generar números.")
        return
    try:
        m_intervalos = int(entrada_intervalos)
        nivel_confianza = float(entrada_confianza.replace(',', '.'))
        if m_intervalos <= 1:
            raise ValueError
    except ValueError:
        resultados_texto.delete(1.0, ctk.END)
        resultados_texto.insert(ctk.END, "Error: El número de intervalos (m) debe ser un entero > 1 y la confianza un valor numérico.")
        return
    n = len(numeros_ri)
    intervalo_tamano = 1.0 / m_intervalos
    frecuencias_observadas = [0] * m_intervalos
    for r in numeros_ri:
        for i in range(m_intervalos):
            limite_inferior = i * intervalo_tamano
            limite_superior = (i + 1) * intervalo_tamano
            if r >= limite_inferior and r < limite_superior:
                frecuencias_observadas[i] += 1
                break
    frecuencia_esperada = n / m_intervalos
    
    chi_cuadrado_calculado = 0
    tabla_str = "{:<15} {:<20} {:<20} {:<20}\n".format("Intervalo", "Frec. Observada (Oi)", "Frec. Esperada (Ei)", "(Oi-Ei)^2/Ei")
    tabla_str += "-" * 75 + "\n"
    for i, oi in enumerate(frecuencias_observadas):
        limite_inf = i * intervalo_tamano
        limite_sup = (i + 1) * intervalo_tamano
        contribucion_chi = ((oi - frecuencia_esperada) ** 2) / frecuencia_esperada
        chi_cuadrado_calculado += contribucion_chi
        intervalo_str = f"[{limite_inf:.2f}, {limite_sup:.2f})"
        tabla_str += "{:<15} {:<20} {:<20.2f} {:<20.4f}\n".format(intervalo_str, oi, frecuencia_esperada, contribucion_chi)

    grados_libertad = m_intervalos - 1
    alfa = 1 - nivel_confianza
    chi_cuadrada_tabulada = chi2.ppf(1 - alfa, grados_libertad)
    
    resultados_texto.delete("1.0", ctk.END)
    resultados_texto.insert(ctk.END, "Resultados de la Prueba de Uniformidad:\n\n")
    resultados_texto.insert(ctk.END, tabla_str)
    resultados_texto.insert(ctk.END, f"\nEstadístico de prueba χ² calculado: {chi_cuadrado_calculado:.4f}\n")
    resultados_texto.insert(ctk.END, f"Valor de χ² de la tabla: {chi_cuadrada_tabulada:.4f}\n\n")
    if chi_cuadrado_calculado <= chi_cuadrada_tabulada:
        resultados_texto.insert(ctk.END, "Conclusión: Se acepta la hipótesis nula. Los números están distribuidos uniformemente.")
    else:
        resultados_texto.insert(ctk.END, "Conclusión: Se rechaza la hipótesis nula. Los números no están distribuidos uniformemente.")

def graficar_histograma_uniformidad(numeros_ri, m_intervalos):
    """Genera y muestra un histograma de los números R_i con KDE."""
    if not numeros_ri:
        messagebox.showinfo("Información", "Primero debe generar números para poder graficar.")
        return
    plt.figure(figsize=(10, 7), facecolor=theme_bg)
    ax = plt.gca()
    ax.set_facecolor(theme_bg)
    sns.histplot(numeros_ri, bins=m_intervalos, stat="count", color=data_color, edgecolor=data_color, linewidth=1.5, alpha=0.6)
    sns.kdeplot(numeros_ri, color=accept_color, linewidth=2.5, ax=ax)
    frecuencia_esperada = len(numeros_ri) / m_intervalos
    plt.axhline(y=frecuencia_esperada, color=reject_color, linestyle='--', linewidth=2, label=f'Frecuencia Esperada ({frecuencia_esperada:.2f})')
    plt.title('Histograma de Frecuencias (Prueba de Uniformidad)', color=text_color)
    plt.xlabel('Intervalos [0, 1)', color=text_color)
    plt.ylabel('Frecuencia Observada', color=text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(data_color)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.show()

def exportar_a_txt(resultados_texto):
    """Permite al usuario guardar el contenido del cuadro de texto en un archivo .txt."""
    contenido = resultados_texto.get("1.0", ctk.END)
    if not contenido.strip():
        messagebox.showinfo("Información", "No hay resultados para exportar.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")],
        title="Guardar resultados como..."
    )

    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(contenido)
            messagebox.showinfo("Éxito", "Los resultados se han guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar el archivo: {e}")