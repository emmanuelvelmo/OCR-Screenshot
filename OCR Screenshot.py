import threading
import pytesseract
import tkinter
from PIL import ImageGrab

# Variables para almacenar las coordenadas globales
start_x, start_y, end_x, end_y = None, None, None, None

# Variable global para guardar el texto extraído
extracted_text = ""

# Configuración de pytesseract para que apunte al ejecutable de Tesseract en tu sistema
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Cambia según tu ruta

# Función para capturar pantalla y extraer texto
def capture_screen():
    global extracted_text
    
    # Ajustar las coordenadas
    x1 = min(start_x, end_x)
    y1 = min(start_y, end_y)
    x2 = max(start_x, end_x)
    y2 = max(start_y, end_y)
    
    # Capturar la pantalla en el área seleccionada
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    
    # Usar pytesseract para extraer texto de la imagen
    extracted_text = pytesseract.image_to_string(screenshot)

# Función para iniciar ventana secundaria
def start_selection7():
    # Iniciar la ventana secundaria en un hilo independiente
    threading.Thread(target=run_selection_window).start()

# Función para ejecutar la ventana secundaria
def run_selection_window():
    # Ocultar ventana principal usando after() para ejecutarlo en el hilo principal
    main_window.root.after(0, main_window.withdraw)
    
    # Instancia de la ventana secundaria
    app = RectangularSelector()
    
    # Inicia el bucle de eventos para la ventana secundaria
    app.root.mainloop()
    
    # Cerrar bucle de la ventana secundaria al terminar la selección
    app.root.destroy()
    
    # Realiza la captura de pantalla después de cerrar la ventana de selección
    capture_screen()
    
    # Mostrar ventana principal usando after() para ejecutarlo en el hilo principal
    main_window.root.after(0, main_window.deiconify)
    
    # Actualizar la caja de texto con el texto extraído
    main_window.root.after(0, main_window.update_text_box, extracted_text)

# Ventana secundaria (para la selección rectangular)
class RectangularSelector:
    def __init__(self):
        self.root = tkinter.Tk()
        
        # Poner la ventana en pantalla completa y sin bordes
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.root.overrideredirect(True)
        
        # Configurar la transparencia de la ventana
        self.root.attributes("-alpha", 0.4)
        
        # Canvas donde se dibujará el rectángulo
        self.canvas = tkinter.Canvas(self.root, bg="black", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Variables para las coordenadas del rectángulo
        self.rect = None
        
        # Detecta los eventos de mouse en la ventana
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
    
    # Cuando el usuario hace clic, se inicia la selección del rectángulo
    def on_mouse_down(self, event):
        global start_x, start_y
        
        start_x = event.x
        start_y = event.y
        
        # Dibuja un rectángulo
        self.rect = self.canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="white", width=1, fill="grey")
    
    # Mientras el usuario arrastra, actualizar el rectángulo de selección
    def on_mouse_drag(self, event):
        cur_x, cur_y = event.x, event.y
        self.canvas.coords(self.rect, start_x, start_y, cur_x, cur_y)
    
    # Cuando el usuario suelta el ratón, termina la selección
    def on_mouse_up(self, event):
        global end_x, end_y
        
        # Guarda las coordenadas del borde inferior derecho del rectángulo
        end_x, end_y = event.x, event.y
        
        # Cierra la ventana secundaria después de la selección
        self.root.quit()

# Ventana principal
class MainWindow:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("OCR Screenshot")
        self.root.geometry("450x300")
        self.root.configure(bg="white")
        
        # Botón para iniciar la selección
        self.select_button = tkinter.Button(self.root, text="New", command=self.start_selectionx, height=2, width=20)
        # Agregar el botón con un margen
        self.select_button.pack(fill=tkinter.BOTH, expand=True, padx=10)
        
        # Caja de texto
        self.text_box = tkinter.Text(self.root, font=("Arial", 11), bg="white", fg="black", bd=1)
        self.text_box.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
    
    # Iniciar ventana secundaria
    def start_selectionx(self):
        # Ocultar la ventana principal antes de iniciar la selección
        self.root.withdraw()
        
        # Realizar selección de área en un hilo independiente
        start_selection7()
    
    # Iniciar la ventana principal
    def run(self):
        self.root.mainloop()
    
    # Ocultar la ventana principal
    def withdraw(self):
        self.root.withdraw()
    
    # Mostrar la ventana principal
    def deiconify(self):
        self.root.deiconify()
    
    # Función para actualizar caja de texto con texto extraído
    def update_text_box(self, text):
        # Insertar el texto nuevo al final del contenido actual
        self.text_box.insert(tkinter.END, text + "\n")

# Crear la instancia de la ventana principal
main_window = MainWindow()

# Iniciar la aplicación
main_window.run()
