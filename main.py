import customtkinter as ctk
from tkinter import messagebox
import logica as log

class App(ctk.CTk):
    """
    Clase principal de la aplicación.
    Maneja la interfaz de usuario y la navegación.
    """
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Simulador de Números Pseudoaleatorios")
        self.geometry("900x700")
        self.configure(fg_color="#2B4162")  # Azul oscuro
        
        self.numeros_ri = [] # Almacena los números generados

        # Frame principal para contener todas las vistas
        self.main_frame = ctk.CTkFrame(self, fg_color="#2B4162")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.mostrar_generador()
        
    def limpiar_frame(self):
        """Limpia el contenido del frame principal."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_generador(self):
        """Muestra la interfaz para la generación de números."""
        self.limpiar_frame()
        
        # Título
        titulo = ctk.CTkLabel(self.main_frame, text="GENERADOR DE NÚMEROS PSEUDOALEATORIOS", font=("Arial", 24, "bold"), text_color="#F2F4F7")
        titulo.pack(pady=(20, 10))
        
        # Frame para los botones de algoritmos
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        btn_cuadrados = ctk.CTkButton(btn_frame, text="Cuadrados Medios",
                                      command=lambda: self.crear_panel_generador(log.calcular_cuadrados_medios, [("Y_0 (Semilla):", "entrada_y0"), ("Número de Iteraciones (n):", "entrada_n")], "cuadrados_medios"),
                                      width=200, height=50, fg_color="#8B9DAE", text_color="black", hover_color="#B3C4D5", font=("Arial", 14, "bold"))
        btn_cuadrados.grid(row=0, column=0, padx=10, pady=10)
        
        btn_productos = ctk.CTkButton(btn_frame, text="Productos Medios",
                                      command=lambda: self.crear_panel_generador(log.calcular_productos_medios, [("Y_0 (Semilla 1):", "entrada_y0"), ("Y_1 (Semilla 2):", "entrada_y1"), ("Número de Iteraciones (n):", "entrada_n")], "productos_medios"),
                                      width=200, height=50, fg_color="#8B9DAE", text_color="black", hover_color="#B3C4D5", font=("Arial", 14, "bold"))
        btn_productos.grid(row=0, column=1, padx=10, pady=10)
        
        btn_multiplicador = ctk.CTkButton(btn_frame, text="Multiplicador Constante",
                                          command=lambda: self.crear_panel_generador(log.calcular_multiplicador_constante, [("Constante (a):", "entrada_a"), ("Y_0 (Semilla):", "entrada_y0"), ("Número de Iteraciones (n):", "entrada_n")], "multiplicador_constante"),
                                          width=200, height=50, fg_color="#8B9DAE", text_color="black", hover_color="#B3C4D5", font=("Arial", 14, "bold"))
        btn_multiplicador.grid(row=0, column=2, padx=10, pady=10)
        
        btn_salir = ctk.CTkButton(self.main_frame, text="Salir", command=self.destroy,
                                  width=150, height=40, fg_color="#A41C34", text_color="#F2F4F7",
                                  hover_color="#CC2936",
                                  border_color="#F2F4F7", border_width=2,
                                  font=("Arial", 14, "bold"))
        btn_salir.pack(pady=20)
        
    def crear_panel_generador(self, funcion_calculo, inputs, algoritmo):
        """Muestra la interfaz para el algoritmo seleccionado."""
        self.limpiar_frame()
        
        # Título del algoritmo
        titulo = ctk.CTkLabel(self.main_frame, text=f"ALGORITMO DE {algoritmo.replace('_', ' ').upper()}", font=("Arial", 20, "bold"), text_color="#F2F4F7")
        titulo.pack(pady=(20, 10))
        
        # Frame de entradas
        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(pady=10)
        
        # Campo de entrada para el número de dígitos
        ctk.CTkLabel(input_frame, text="Cantidad de dígitos (d):", text_color="#F2F4F7").grid(row=0, column=0, padx=5, pady=5)
        entrada_d = ctk.CTkEntry(input_frame)
        entrada_d.grid(row=0, column=1, padx=5, pady=5)
        entrada_d.insert(0, "4")
        
        # Campos de entrada dinámicos
        entrada_widgets = {}
        for i, (label_text, entry_key) in enumerate(inputs, start=1):
            ctk.CTkLabel(input_frame, text=label_text, text_color="#F2F4F7").grid(row=i, column=0, padx=5, pady=5)
            entrada = ctk.CTkEntry(input_frame)
            entrada.grid(row=i, column=1, padx=5, pady=5)
            entrada_widgets[entry_key] = entrada
            
        # Botón para generar y mostrar la tabla de resultados
        btn_generar = ctk.CTkButton(input_frame, text="Generar Números",
                                    command=lambda: self.generar_y_mostrar_resultados(funcion_calculo, entrada_widgets, entrada_d),
                                    fg_color="#8B9DAE", text_color="black", hover_color="#B3C4D5")
        btn_generar.grid(row=len(inputs) + 1, column=0, columnspan=2, pady=10)
        
        # Frame de resultados y pruebas
        self.resultados_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.resultados_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botón para volver
        btn_volver = ctk.CTkButton(self.main_frame, text="← Volver", command=self.mostrar_generador,
                                   fg_color="transparent", border_color="#D5D9E0", border_width=2, text_color="#D5D9E0", hover_color="#5D737E")
        btn_volver.pack(pady=10)

    def generar_y_mostrar_resultados(self, funcion_calculo, entrada_widgets, entrada_d):
        """Ejecuta el cálculo y muestra la tabla y los botones de pruebas."""
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()

        try:
            # Reorganizar los argumentos para la función de lógica
            args = [v.get() for v in entrada_widgets.values()]
            args.append(entrada_d.get())

            # La función de lógica devuelve la tabla y los números
            tabla, self.numeros_ri = funcion_calculo(*args)
            
            # Mostrar la tabla de resultados
            resultados_texto = ctk.CTkTextbox(self.resultados_frame, width=800, height=200, bg_color="#1a1a1a", fg_color="#2B4162", text_color="#F2F4F7", border_color="#8B9DAE", border_width=2)
            resultados_texto.insert("end", tabla)
            resultados_texto.configure(state="disabled") # El usuario no puede editar el texto
            resultados_texto.pack(pady=10, padx=10)
            
            # Botones para las pruebas y exportar
            pruebas_frame = ctk.CTkFrame(self.resultados_frame, fg_color="transparent")
            pruebas_frame.pack(pady=10)
            
            btn_pruebas_generales = ctk.CTkButton(pruebas_frame, text="Pruebas Estadísticas",
                                                  command=self.mostrar_pruebas,
                                                  fg_color="#508D4E", text_color="#F2F4F7", hover_color="#6A9955")
            btn_pruebas_generales.pack(side="left", padx=10)
            
            btn_exportar = ctk.CTkButton(pruebas_frame, text="Exportar a .txt",
                                         command=lambda: log.exportar_a_txt(resultados_texto),
                                         fg_color="#D49A00", text_color="black", hover_color="#E0A71E")
            btn_exportar.pack(side="left", padx=10)
            
        except ValueError as e:
            ctk.CTkLabel(self.resultados_frame, text=f"Error: {e}", text_color="#A41C34").pack(pady=10)

    def mostrar_pruebas(self):
        """Muestra la interfaz para las pruebas estadísticas."""
        self.limpiar_frame()
        
        # Título
        titulo = ctk.CTkLabel(self.main_frame, text="PRUEBAS ESTADÍSTICAS", font=("Arial", 24, "bold"), text_color="#F2F4F7")
        titulo.pack(pady=(20, 10))

        # Frame de los botones de prueba
        pruebas_btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pruebas_btn_frame.pack(pady=10)
        
        btn_medias = ctk.CTkButton(pruebas_btn_frame, text="Prueba de Medias",
                                   command=self.mostrar_panel_medias,
                                   width=180, height=50, fg_color="#508D4E", text_color="#F2F4F7", hover_color="#6A9955", font=("Arial", 14, "bold"))
        btn_medias.grid(row=0, column=0, padx=10, pady=10)
        
        btn_varianza = ctk.CTkButton(pruebas_btn_frame, text="Prueba de Varianza",
                                     command=self.mostrar_panel_varianza,
                                     width=180, height=50, fg_color="#508D4E", text_color="#F2F4F7", hover_color="#6A9955", font=("Arial", 14, "bold"))
        btn_varianza.grid(row=0, column=1, padx=10, pady=10)
        
        btn_uniformidad = ctk.CTkButton(pruebas_btn_frame, text="Prueba de Uniformidad",
                                        command=self.mostrar_panel_uniformidad,
                                        width=180, height=50, fg_color="#508D4E", text_color="#F2F4F7", hover_color="#6A9955", font=("Arial", 14, "bold"))
        btn_uniformidad.grid(row=0, column=2, padx=10, pady=10)
        
        # Botón para volver al generador
        btn_volver = ctk.CTkButton(self.main_frame, text="← Volver al Generador", command=self.mostrar_generador,
                                   fg_color="transparent", border_color="#D5D9E0", border_width=2, text_color="#D5D9E0", hover_color="#5D737E")
        btn_volver.pack(pady=20)

    def mostrar_panel_medias(self):
        self.limpiar_frame()
        
        # Título
        titulo = ctk.CTkLabel(self.main_frame, text="PRUEBA DE MEDIAS", font=("Arial", 20, "bold"), text_color="#F2F4F7")
        titulo.pack(pady=(20, 10))
        
        # Controles
        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(pady=10)
        ctk.CTkLabel(input_frame, text="Valor de Z_alpha/2:", text_color="#F2F4F7").pack(side="left")
        entrada_z = ctk.CTkEntry(input_frame)
        entrada_z.pack(side="left", padx=5)
        entrada_z.insert(0, "1.96")
        
        btn_ejecutar = ctk.CTkButton(input_frame, text="Ejecutar", command=lambda: self.mostrar_resultados_prueba("medias", entrada_z=entrada_z),
                                     fg_color="#8B9DAE", text_color="black", hover_color="#B3C4D5")
        btn_ejecutar.pack(side="left", padx=5)
        
        # Botones de navegación
        btn_volver_pruebas = ctk.CTkButton(self.main_frame, text="← Volver a Pruebas", command=self.mostrar_pruebas,
                                           fg_color="transparent", border_color="#D5D9E0", border_width=2, text_color="#D5D9E0", hover_color="#5D737E")
        btn_volver_pruebas.pack(side="bottom", pady=10)
        
        self.resultados_pruebas_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.resultados_pruebas_frame.pack(fill="both", expand=True)

    def mostrar_panel_varianza(self):
        self.limpiar_frame()
        
        titulo = ctk.CTkLabel(self.main_frame, text="PRUEBA DE VARIANZA", font=("Arial", 20, "bold"), text_color="#F2F4F7")
        titulo.pack(pady=(20, 10))
        
        # Controles para la prueba
        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(pady=10)

        ctk.CTkLabel(input_frame, text="Nivel de Confianza:", text_color="#F2F4F7").pack(side="left")
        entrada_confianza = ctk.CTkEntry(input_frame)
        entrada_confianza.insert(0, "0.95")
        entrada_confianza.pack(side="left", padx=5)
        
        btn_ejecutar = ctk.CTkButton(input_frame, text="Ejecutar", command=lambda: self.mostrar_resultados_prueba("varianza", entrada_confianza=entrada_confianza),
                                     fg_color="#8B9DAE", text_color="black", hover_color="#B3C4D5")
        btn_ejecutar.pack(side="left", padx=5)
        
        btn_volver_pruebas = ctk.CTkButton(self.main_frame, text="← Volver a Pruebas", command=self.mostrar_pruebas,
                                           fg_color="transparent", border_color="#D5D9E0", border_width=2, text_color="#D5D9E0", hover_color="#5D737E")
        btn_volver_pruebas.pack(side="bottom", pady=10)
        
        self.resultados_pruebas_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.resultados_pruebas_frame.pack(fill="both", expand=True)
    
    def mostrar_panel_uniformidad(self):
        self.limpiar_frame()
        
        # Título
        titulo = ctk.CTkLabel(self.main_frame, text="PRUEBA DE UNIFORMIDAD", font=("Arial", 20, "bold"), text_color="#F2F4F7")
        titulo.pack(pady=(20, 10))
        
        # Controles
        input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        input_frame.pack(pady=10)
        
        ctk.CTkLabel(input_frame, text="Número de intervalos (m):", text_color="#F2F4F7").grid(row=0, column=0)
        entrada_m = ctk.CTkEntry(input_frame)
        entrada_m.grid(row=0, column=1, padx=5)
        entrada_m.insert(0, "10")
        
        ctk.CTkLabel(input_frame, text="Nivel de Confianza:", text_color="#F2F4F7").grid(row=1, column=0)
        entrada_confianza = ctk.CTkEntry(input_frame)
        entrada_confianza.grid(row=1, column=1, padx=5)
        entrada_confianza.insert(0, "0.95")
        
        btn_ejecutar = ctk.CTkButton(input_frame, text="Ejecutar", command=lambda: self.mostrar_resultados_uniformidad(entrada_m, entrada_confianza),
                                     fg_color="#8B9DAE", text_color="black", hover_color="#B3C4D5")
        btn_ejecutar.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Botones de navegación
        btn_volver_pruebas = ctk.CTkButton(self.main_frame, text="← Volver a Pruebas", command=self.mostrar_pruebas,
                                           fg_color="transparent", border_color="#D5D9E0", border_width=2, text_color="#D5D9E0", hover_color="#5D737E")
        btn_volver_pruebas.pack(side="bottom", pady=10)
        
        self.resultados_pruebas_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.resultados_pruebas_frame.pack(fill="both", expand=True)

    def mostrar_resultados_uniformidad(self, entrada_m, entrada_confianza):
        """Muestra los resultados de la prueba de uniformidad y el botón del histograma y exportar."""
        for widget in self.resultados_pruebas_frame.winfo_children():
            widget.destroy()

        if not self.numeros_ri:
            ctk.CTkLabel(self.resultados_pruebas_frame, text="Error: No se han generado números aún.", text_color="#A41C34").pack(pady=10)
            return

        resultados_texto = ctk.CTkTextbox(self.resultados_pruebas_frame, width=800, height=300, bg_color="#1a1a1a", fg_color="#2B4162", text_color="#F2F4F7", border_color="#8B9DAE", border_width=2)
        resultados_texto.pack(pady=10)
        
        try:
            m_intervalos = int(entrada_m.get())
            if m_intervalos <= 1:
                raise ValueError("El número de intervalos (m) debe ser un entero > 1.")
            
            log.ejecutar_prueba_uniformidad_chi_cuadrada(resultados_texto, entrada_m.get(), entrada_confianza.get(), self.numeros_ri)
            
            # Botones para exportar y graficar
            btn_frame = ctk.CTkFrame(self.resultados_pruebas_frame, fg_color="transparent")
            btn_frame.pack(pady=10)
            
            btn_histograma = ctk.CTkButton(btn_frame, text="Ver Histograma", 
                                          command=lambda: log.graficar_histograma_uniformidad(self.numeros_ri, m_intervalos),
                                          fg_color="#508D4E", text_color="#F2F4F7", hover_color="#6A9955")
            btn_histograma.pack(side="left", padx=10)
            
            btn_exportar = ctk.CTkButton(btn_frame, text="Exportar a .txt",
                                         command=lambda: log.exportar_a_txt(resultados_texto),
                                         fg_color="#D49A00", text_color="black", hover_color="#E0A71E")
            btn_exportar.pack(side="left", padx=10)

        except (ValueError, IndexError) as e:
            resultados_texto.delete(1.0, ctk.END)
            resultados_texto.insert(ctk.END, f"Error: {e}")
            
    def mostrar_resultados_prueba(self, tipo_prueba, **kwargs):
        """Muestra los resultados de una prueba específica en un panel de texto con botón de exportar."""
        for widget in self.resultados_pruebas_frame.winfo_children():
            widget.destroy()

        if not self.numeros_ri:
            ctk.CTkLabel(self.resultados_pruebas_frame, text="Error: No se han generado números aún.", text_color="#A41C34").pack(pady=10)
            return

        resultados_texto = ctk.CTkTextbox(self.resultados_pruebas_frame, width=800, height=300, bg_color="#1a1a1a", fg_color="#2B4162", text_color="#F2F4F7", border_color="#8B9DAE", border_width=2)
        resultados_texto.pack(pady=10)

        try:
            if tipo_prueba == "medias":
                entrada_z = kwargs["entrada_z"].get()
                log.ejecutar_prueba_medias_con_input(resultados_texto, entrada_z, self.numeros_ri)
            elif tipo_prueba == "varianza":
                entrada_confianza = kwargs["entrada_confianza"].get()
                log.ejecutar_prueba_varianza_con_confianza(resultados_texto, entrada_confianza, self.numeros_ri)

            # Botón para exportar
            btn_exportar = ctk.CTkButton(self.resultados_pruebas_frame, text="Exportar a .txt",
                                         command=lambda: log.exportar_a_txt(resultados_texto),
                                         fg_color="#D49A00", text_color="black", hover_color="#E0A71E")
            btn_exportar.pack(pady=10)

        except (ValueError, IndexError) as e:
            resultados_texto.delete(1.0, ctk.END)
            resultados_texto.insert(ctk.END, f"Error: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()