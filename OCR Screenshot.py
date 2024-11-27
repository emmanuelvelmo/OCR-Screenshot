import threading
import pytesseract
import tkinter
from PIL import ImageGrab

# Variables para coordenadas
x_ini, y_ini, x_fin, y_fin = None, None, None, None

# Variable para texto extraído
tmp_txt = ""

# Función para capturar pantalla y extraer texto
def capt_pant():
    global tmp_txt
    
    # Definir límites de la captura
    x1 = min(x_ini, x_fin)
    y1 = min(y_ini, y_fin)
    x2 = max(x_ini, x_fin)
    y2 = max(y_ini, y_fin)
    
    # Capturar la pantalla en el área seleccionada
    tmp_capt = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    # Extraer texto de la imagen
    tmp_txt = pytesseract.image_to_string(tmp_capt)

# Función para ejecutar la ventana secundaria
def f_vent_selec():
    # Ocultar ventana principal
    vent_princ.instancia_princ.after(0, vent_princ.f_ocu_vent_princ)
    
    # Instancia de la ventana secundaria
    vent_secu = vent_selecc()
    
    # Inicia el bucle de eventos para la ventana secundaria
    vent_secu.instancia_secu.mainloop()
    
    # Cerrar bucle de la ventana secundaria al terminar la selección
    vent_secu.instancia_secu.destroy()
    
    # Capturar pantalla después de selección
    capt_pant()
    
    # Mostrar ventana principal
    vent_princ.instancia_princ.after(0, vent_princ.f_most_vent_princ)
    
    # Actualizar la caja de texto con el texto extraído
    vent_princ.instancia_princ.after(0, vent_princ.f_act_caja_text, tmp_txt)

# Función para iniciar ventana secundaria
def f_vent_selec_hilo():
    # Iniciar la ventana secundaria en un hilo independiente
    threading.Thread(target=f_vent_selec).start()

# Ventana secundaria (para la selección rectangular)
class vent_selecc:
    # Constructor
    def __init__(self):
        self.instancia_secu = tkinter.Tk()
        
        # Ventana en pantalla completa y sin bordes
        self.instancia_secu.attributes("-fullscreen", True)
        self.instancia_secu.configure(bg="black")
        self.instancia_secu.overrideredirect(True)
        
        # Transparencia de la ventana
        self.instancia_secu.attributes("-alpha", 0.4)
        
        # Canvas donde se dibujará el rectángulo
        self.canvas = tkinter.Canvas(self.instancia_secu, bg="black", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Variable para las coordenadas del rectángulo
        self.rectxy = None
        
        # Eventos de mouse en la ventana
        self.canvas.bind("<ButtonPress-1>", self.mouse_izq_pres)
        self.canvas.bind("<B1-Motion>", self.mouse_arr)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_izq_solt)
    
    # Función para selección de rectángulo con clic izquierdo
    def mouse_izq_pres(self, event):
        global x_ini, y_ini
        
        # Captura de coordenadas
        x_ini = event.x
        y_ini = event.y
        
        # Dibujar un rectángulo
        self.rectxy = self.canvas.create_rectangle(x_ini, y_ini, x_ini, y_ini, outline="white", width=1, fill="grey")
    
    # Función para actualizar el rectángulo de selección mientras se arrastra el mouse
    def mouse_arr(self, event):
        cur_x, cur_y = event.x, event.y
        self.canvas.coords(self.rectxy, x_ini, y_ini, cur_x, cur_y)
    
    # Función para al soltar clic izquierdo, terminar la selección
    def mouse_izq_solt(self, event):
        global x_fin, y_fin
        
        # Guardar las coordenadas del borde inferior derecho del rectángulo
        x_fin, y_fin = event.x, event.y
        
        # Cerrar ventana secundaria después de la selección
        self.instancia_secu.quit()

# Ventana principal
class vent_princ:
    # Constructor
    def __init__(self):
        self.instancia_princ = tkinter.Tk()
        
        # Propiedades de la ventana principal
        self.instancia_princ.title("OCR tmp_capt")
        self.instancia_princ.geometry("450x300")
        self.instancia_princ.configure(bg="white")
        
        # Botón para iniciar la selección
        self.select_button = tkinter.Button(self.instancia_princ, text="New", command=self.f_click_vent_selec, height=2, width=20)
        # Agregar el botón con un margen
        self.select_button.pack(fill=tkinter.BOTH, expand=True, padx=10)
        
        # Caja de texto
        self.caja_texto = tkinter.Text(self.instancia_princ, font=("Arial", 11), bg="white", fg="black", bd=1)
        self.caja_texto.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
    
    # Función para iniciar ventana secundaria
    def f_click_vent_selec(self):
        # Ocultar la ventana principal antes de iniciar la selección
        self.instancia_princ.withdraw()
        
        # Realizar selección de área en un hilo independiente
        f_vent_selec_hilo()
    
    # Función para iniciar la ventana principal
    def f_ini_vent_princ(self):
        self.instancia_princ.mainloop()
    
    # Función para ocultar la ventana principal
    def f_ocu_vent_princ(self):
        self.instancia_princ.withdraw()
    
    # Función para mostrar la ventana principal
    def f_most_vent_princ(self):
        self.instancia_princ.deiconify()
    
    # Función para actualizar caja de texto con texto extraído
    def f_act_caja_text(self, text):
        # Insertar el texto nuevo al final del contenido actual
        self.caja_texto.insert(tkinter.END, text + "\n")

# Crear la instancia de la ventana principal
vent_princ = vent_princ()

# Iniciar la aplicación
vent_princ.f_ini_vent_princ()
