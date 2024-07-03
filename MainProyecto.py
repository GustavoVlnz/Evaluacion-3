import math
import customtkinter as ctk
import os
import tkinter
from PIL import Image
from tkinter import filedialog
import pandas as pd
from CTkTable import CTkTable
from CTkTableRowSelector import CTkTableRowSelector
import tkintermapview
import pandas as pd
import sqlite3
import pyproj
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import csv 


# Crear la ventana principal
root = ctk.CTk()
root.title("Proyecto Final progra I 2024")
root.geometry("950x450")

def haversine(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    rad = math.pi / 180
    dlat = (lat2 - lat1) * rad
    dlon = (lon2 - lon1) * rad

    lat1 = lat1 * rad
    lat2 = lat2 * rad

    R = 6371

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    distancia = R * c

    return distancia

lat1, lon1 = 48.8566, 2.3522  # París
lat2, lon2 = 51.5074, -0.1278  # Londres
distancia = haversine(lat1, lon1, lat2, lon2)
print(f"La distancia entre París y Londres es de {distancia:.2f} km")


def csv_a_sqlite(csv_file, database_name, table_name):
    # Leer el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(csv_file)

    conn = sqlite3.connect(database_name)
    # Insertar los datos del DataFrame en una tabla de la base de datos
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    # Cerrar la conexión
    conn.close()


def ejecutar_query_sqlite(database_name, table_name, columns='*', where_column=None, where_value=None):
    
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    # Crear la consulta SQL
    query = f'SELECT {columns} FROM {table_name}'
    if where_column and where_value is not None:
        query += f' WHERE {where_column} = ?'

    # Ejecutar la consulta SQL
    cursor.execute(query, (where_value,) if where_column and where_value is not None else ())
    # Obtener los resultados de la consulta
    resultados = cursor.fetchall()
    indices = [description[0] for description in cursor.description]

    # Impresion de los RUTs
    for rut in resultados:
        print(rut[0])
    conn.close()
    return indices, resultados



def agregar_df_a_sqlite(df, database_name, table_name):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(database_name)
    # Agregar el DataFrame a la tabla SQLite
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    # Cerrar la conexión
    conn.close()


#documentacion=https://github.com/TomSchimansky/TkinterMapView?tab=readme-ov-file#create-path-from-position-list
def get_country_city(lat,long):
    country = tkintermapview.convert_coordinates_to_country(lat, long)
    print(country)
    city = tkintermapview.convert_coordinates_to_city(lat, long)
    return country,city
# Definir la función para convertir UTM a latitud y longitud


def utm_to_latlong(easting, northing, zone_number, zone_letter):
    # Crear el proyector UTM
    utm_proj = pyproj.Proj(proj='utm', zone=zone_number, datum='WGS84')
    
    # Convertir UTM a latitud y longitud
    longitude, latitude = utm_proj(easting, northing, inverse=True)
    return round(latitude,2), round(longitude,2)


def insertar_data(data:list):
    pass
    #necesitamos convertir las coordenadas UTM a lat long


def combo_event2(value):
    try:
        marker_2.delete()
    except NameError:
        pass
    result=ejecutar_query_sqlite('progra2024_final.db', 'personas_coordenadas',columns='Latitude,Longitude,Nombre,Apellido', where_column='RUT', where_value=value)
    nombre_apellido=str(result[0][2])+' '+str(result[0][3])
    marker_2 = map_widget.set_marker(result[0][0], result[0][1], text=nombre_apellido)


def combo_event(value):

    mapas.set_address("moneda, santiago, chile")
    mapas.set_position(48.860381, 2.338594)  # Paris, France
    mapas.set_zoom(15)
    address = tkintermapview.convert_address_to_coordinates("London")
    print(address)


    ruts_list = ("csv_file")
    optionmenu_1.set_values(ruts_list)
    pass
    #mapas.set_address("moneda, santiago, chile")
    #mapas.set_position(48.860381, 2.338594)  # Paris, France
    #mapas.set_zoom(15)
    #address = tkintermapview.convert_address_to_coordinates("London")
    #print(address)

def center_window(window, width, height):
    # Obtener el tamaño de la ventana principal
    root.update_idletasks()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_x()
    root_y = root.winfo_y()

    # Calcular la posición para centrar la ventana secundaria
    x = root_x + (root_width // 2) - (width // 2)
    y = root_y + (root_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

def setup_toplevel(window):
    window.geometry("400x300")
    window.title("Modificar datos")
    center_window(window, 400, 300)  # Centrar la ventana secundaria
    window.lift()  # Levanta la ventana secundaria
    window.focus_force()  # Forzar el enfoque en la ventana secundaria
    window.grab_set()  # Evita la interacción con la ventana principal


    label = ctk.CTkLabel(window, text="ToplevelWindow")
    label.pack(padx=20, pady=20)

def calcular_distancia(RUT1,RUT2):
    
    pass

def guardar_data(row_selector):
    print(row_selector.get())
    print(row_selector.table.values)

def editar_panel(root):
    global toplevel_window
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = ctk.CTkToplevel(root)
        setup_toplevel(toplevel_window)
    else:
        toplevel_window.focus()
# Función para manejar la selección del archivo

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo:
        print(f"Archivo seleccionado: {archivo}")
        tabla(archivo)

def on_scrollbar_move(*args):
    canvas1.yview(*args)
    canvas1.bbox("all")
    
def leer_archivo_csv(ruta_archivo):
    try:
        datos = pd.read_csv(ruta_archivo)
        mostrar_datos(datos)
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")

def abrir_csv(archivo):
    dataframe = pd.read_csv(archivo)
    encabezado = dataframe.columns.tolist()
    data= dataframe.values.tolist()
    data.insert(0,encabezado)
    return data

def tabla(archivo):
    data=abrir_csv(archivo)
    tabla_ordenada=CTkTable(master=scrollable_frame, row=len(data), column=len(data[0]), values=data)
    tabla_ordenada.pack(expand=True, fill= "both", padx=15, pady=15)


# Función para mostrar los datos en la tabla
def mostrar_datos(datos):

    # Botón para imprimir las filas seleccionadas
    boton_imprimir = ctk.CTkButton(
        master=home_frame, text="guardar informacion", command=lambda: guardar_data())
    boton_imprimir.grid(row=2, column=0, pady=(0, 20))
    
    # Botón para imprimir las filas seleccionadas
    boton_imprimir = ctk.CTkButton(
        master=data_panel_superior, text="modificar dato", command=lambda: editar_panel(root))
    boton_imprimir.grid(row=0, column=2, pady=(0, 0))

    # Botón para imprimir las filas seleccionadas
    boton_imprimir = ctk.CTkButton(
        master=data_panel_superior, text="Eliminar dato", command=lambda: editar_panel(root),fg_color='purple',hover_color='red')
    boton_imprimir.grid(row=0, column=3, padx=(10, 0))

    home_frame_cargar_datos = ctk.CTkButton(data_panel_superior, command=mostrar_datos, text="Cargar Archivo", fg_color='green', hover_color='gray')
    home_frame_cargar_datos.grid(row=0, column=1, padx=15, pady=15)
    
    tabla()



def select_frame_by_name(name):
    home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
    frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
    frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

    if name == "home":
        home_frame.grid(row=0, column=1, sticky="nsew")
    else:
        home_frame.grid_forget()
    if name == "frame_2":
        second_frame.grid(row=0, column=1, sticky="nsew")
    else:
        second_frame.grid_forget()
    if name == "frame_3":
        third_frame.grid(row=0, column=1, sticky="nsew")
    else:
        third_frame.grid_forget()

def home_button_event():
    select_frame_by_name("home")

def frame_2_button_event():
    select_frame_by_name("frame_2")

def frame_3_button_event():
    select_frame_by_name("frame_3")


def change_appearance_mode_event(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)


def mapas(panel):
    # create map widget
    map_widget = tkintermapview.TkinterMapView(panel,width=800, height=500, corner_radius=0)
    #map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    map_widget.pack(fill=ctk.BOTH, expand=True)
    return map_widget



# Configurar el diseño de la ventana principal
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Establecer la carpeta donde están las imágenes
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "iconos")
logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "uct.png")), size=(140, 50))
home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "db.png")),
                          dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                          dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
add_user_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                              dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

# Crear el marco de navegación
navigation_frame = ctk.CTkFrame(root, corner_radius=0)
navigation_frame.grid(row=0, column=0, sticky="nsew")
navigation_frame.grid_rowconfigure(4, weight=1)

navigation_frame_label = ctk.CTkLabel(navigation_frame, text="", image=logo_image,
                                      compound="left", font=ctk.CTkFont(size=15, weight="bold"))
navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

home_button = ctk.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                            image=home_image, anchor="w", command=home_button_event)
home_button.grid(row=1, column=0, sticky="ew")

frame_2_button = ctk.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                               image=chat_image, anchor="w", command=frame_2_button_event)
frame_2_button.grid(row=2, column=0, sticky="ew")

frame_3_button = ctk.CTkButton(navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                               image=add_user_image, anchor="w", command=frame_3_button_event)
frame_3_button.grid(row=3, column=0, sticky="ew")

appearance_mode_menu = ctk.CTkOptionMenu(navigation_frame, values=["Light", "Dark", "System"],
                                         command=change_appearance_mode_event)
appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

# Crear el marco principal de inicio



# Crear el marco de navegación
home_frame = ctk.CTkFrame(root, fg_color="transparent")
home_frame.grid_rowconfigure(1, weight=1)
home_frame.grid_columnconfigure(0, weight=1)

data_panel_superior = ctk.CTkFrame(home_frame, corner_radius=0,)
data_panel_superior.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

data_panel_inferior = ctk.CTkFrame(home_frame, corner_radius=0)
data_panel_inferior.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
data_panel_inferior.grid_rowconfigure(0, weight=1)
data_panel_inferior.grid_columnconfigure(0, weight=1)

home_frame_large_image_label = ctk.CTkLabel(data_panel_superior, text="Ingresa el archivo en formato .csv",font=ctk.CTkFont(size=15, weight="bold"))
home_frame_large_image_label.grid(row=0, column=0, padx=15, pady=15)
home_frame_cargar_datos=ctk.CTkButton(data_panel_superior, command=seleccionar_archivo,text="Cargar Archivo",fg_color='green',hover_color='gray')
home_frame_cargar_datos.grid(row=0, column=1, padx=15, pady=15)

scrollable_frame = ctk.CTkScrollableFrame(master=data_panel_inferior)
scrollable_frame.grid(row=0, column=0,sticky="nsew")



# Crear el segundo marco
second_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")
second_frame.grid_rowconfigure(0, weight=1)
second_frame.grid_columnconfigure(0, weight=1)
second_frame.grid_rowconfigure(1, weight=1)
second_frame.grid_columnconfigure(1, weight=1)

# Crear el frame superior para los comboboxes
top_frame = ctk.CTkFrame(second_frame)
top_frame.pack(side=ctk.TOP, fill=ctk.X)

# Crear el frame inferior para los dos gráficos
bottom_frame = ctk.CTkFrame(second_frame)
bottom_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

# Crear los paneles izquierdo y derecho para los gráficos
left_panel = ctk.CTkFrame(bottom_frame)
left_panel.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

right_panel = ctk.CTkFrame(bottom_frame)
right_panel.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

# Crear los paneles superior izquierdo y derecho para los comboboxes
top_left_panel = ctk.CTkFrame(top_frame)
top_left_panel.pack(side=ctk.LEFT, fill=ctk.X, expand=True)

top_right_panel = ctk.CTkFrame(top_frame)
top_right_panel.pack(side=ctk.RIGHT, fill=ctk.X, expand=True)









# Conneccion a la database

conn = sqlite3.connect('data_a_procesar.db')
cursor = conn.cursor()

def combo_evento(selected_value):
    print(f"valor seleccionado: {selected_value}")
    create_bar_chart(selected_value)

paises = [pais[0] for pais in cursor.execute("SELECT DISTINCT Pais FROM Informacion").fetchall()]
combobox_left = ctk.CTkComboBox(top_left_panel, state="readonly", values=paises, command=combo_evento)
combobox_left.pack(pady=20, padx=20)
combobox_left.set("Seleccione el país")

def create_bar_chart(selected_country):
    profesiones = [prof[0] for prof in cursor.execute("SELECT DISTINCT Profesion FROM Informacion WHERE Pais = ?", (selected_country,)) ]
    if not profesiones:
        print(f"No hay profesiones para el país seleccionado: {selected_country}")
        return

    sizes = cursor.execute("SELECT COUNT(Profesion) FROM Informacion WHERE Pais = ? GROUP BY Profesion", (selected_country)).fetchall()
    

    fig1, ax = plt.subplots()
    labels = profesiones
    sizes = sizes

    ax.bar(labels, sizes, color='skyblue')

    ax.set_xlabel("Categorías")
    ax.set_ylabel("Valores")
    fig1.suptitle(f"Grafico de Barras - Profesiones en {selected_country}")
    ax.set_xticks(rotation=45, ha='right')

    canvas1 = FigureCanvasTkAgg(fig1, master=left_panel)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)



#def get_employee_counts_by_profession(selected_country):
  #  prof = "SELECT COUNT(Profesion) AS count, Profesion FROM Informacion WHERE Pais = {selected_country} GROUP BY Profesion"
   # cursor.execute(prof, (selected_country))
    #cant_p=cursor.execute("Select count(Profesion) FROM Informacion WHERE Pais = {selected_country}  GROUP BY Profesion")
    #professions = []  # List to store profession labels
    #counts = []  # List to store corresponding employee counts
    
    #cursor.execute(prof)
 #   results = cursor.fetchall()
  #  for row in results:
   #     professions.append(row[0])
    #    counts.append(row[1])
    #
    #return professions, counts



#def create_bar_chart(professions, counts, fig):
 #   ax = fig.add_subplot(111)  # Create an axis on the figure
  #  ax.bar(professions, counts, color='skyblue')
   # ax.set_xlabel("Profesión")
    #ax.set_ylabel("Cantidad de Empleados")
  #  ax.set_title("Empleados por Profesión en {selected_country}")
   # ax.set_xticks(rotation=45, ha='right')
   # print(professions)




    #canvas1 = FigureCanvasTkAgg(fig, master=left_panel)
    #canvas1.draw()
    #canvas1.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)


#def create_bar_chart(professions, counts):
 #   fig1=plt.figure(figsize=(10, 6))
  # plt.xlabel("Profesión")
   # plt.ylabel("Cantidad de Empleados")
    #plt.title("Empleados por Profesión en {selected_country}")  # Replace with selected country
    #plt.xticks(rotation=45, ha='right')
    #plt.tight_layout()
   # plt.show()
    #canvas1 = FigureCanvasTkAgg(fig1, master=left_panel)
    #canvas1.draw()
    #canvas1.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

#query = """
    #SELECT
    #pais,
    #COUNT(DISTINCT Profesion) AS cantidad_profesiones
    #FROM
   # Informacion
  #  GROUP BY
 #   pais;
#"""

#cursor.execute(query)


# Preparar los datos
#paises = [row[0] for row in data]
#cantidad_profesiones = [row[1] for row in data]
#x = np.arange(len(paises))

# Crear el gráfico
#fig1, ax1 = plt.subplots()
#ax1.bar(fig1, ax1)
#ax1.set_xticks(fig1)
#ax1.set_xticklabels(paises, rotation=45, ha="right")
#ax1.set_xlabel("Profesion")
#ax1.set_ylabel("cantidad de empleados")
#ax1.set_title("Profesiones por Pais")










# Agregar un Combobox al panel superior derecho

emotions = [emocion[0] for emocion in cursor.execute("SELECT DISTINCT Estado_Emocional FROM Informacion").fetchall()]
combobox_right = ctk.CTkComboBox(top_right_panel, state="readonly", values=emotions, command=combo_event2)
combobox_right.set("seleccione estado emocional")
combobox_right.pack(pady=20, padx=20)
#el objetivo principal de cursor.execute()es ejecutar sentencias SQL en la base de datos



def update_pie_chart(selected_emotion):
    

  

    # Borrar los datos existentes del gráfico circular
    ax2.clear()

    #  Obtener datos de la base de datos en funcion de la emocion seleccionada
   
    cursor = conn.cursor()
    query = "SELECT DISTINCT Profesion, COUNT(*) AS Profesionales FROM Informacion WHERE Estado_emocional = ?"
    cursor.execute(query, (selected_emotion,))
    data2 = cursor.fetchall()

    # Extraer etiquetas y recuentos de profesiones
    labels2 = [row[0] for row in data2]
    sizes2 = [row[1] for row in data2]

    if not sizes2:  
        labels2= ["No data found"]
        sizes2 = [1]
        colors = ['gray']
        

    
    ax2.pie(sizes2, labels2=labels2, colors=colors, autopct='%1.1f%%')
    ax2.axis('equal')  # se asegura que sea circular
    ax2.set_title("Estado emocional vs Profesion")

    # Actualiza el canva2 y vuelve a dibujar el gráfico circular
    canvas2.draw()


fig2, ax2 = plt.subplots()
labels2 = []  #
sizes2 = []  #Tamaños inicialmente vacíos
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']




canvas2 = FigureCanvasTkAgg(fig2, master=right_panel)
canvas2.draw()
canvas2.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)


def combo_event2(selected_emotion):
    print(f"la emocion seleccionada es: {selected_emotion}")
    update_pie_chart(selected_emotion) 





# Crear el tercer marco
third_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="transparent")
third_frame.grid_rowconfigure(0, weight=1)
third_frame.grid_columnconfigure(0, weight=1)
third_frame.grid_rowconfigure(1, weight=3)  # Panel inferior 3/4 más grande
# Crear dos bloques dentro del frame principal
third_frame_top =  ctk.CTkFrame(third_frame, fg_color="gray")
third_frame_top.grid(row=0, column=0,  sticky="nsew", padx=5, pady=5)

third_frame_inf =  ctk.CTkFrame(third_frame, fg_color="lightgreen")
third_frame_inf.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

label_rut = ctk.CTkLabel(third_frame_top, text="RUT 1",font=ctk.CTkFont(size=15, weight="bold"))

map_widget=mapas(third_frame_inf)
label_rut = ctk.CTkLabel(third_frame_top, text="RUT",font=ctk.CTkFont(size=15, weight="bold"))

label_rut.grid(row=0, column=0, padx=5, pady=5)

label_rut2 = ctk.CTkLabel(third_frame_top, text="RUT 2",font=ctk.CTkFont(size=15, weight="bold"))
label_rut2.grid(row=10, column=0, padx=5, pady=5)

optionmenu_1 = ctk.CTkOptionMenu(third_frame_top, dynamic_resizing=True,
values=["Value 1", "Value 2", "Value Long Long Long"],command=lambda value:combo_event(value))
optionmenu_1.grid(row=0, column=1, padx=5, pady=(5, 5))

optionmenu_2 = ctk.CTkOptionMenu(third_frame_top, dynamic_resizing=True,
values=["Value 1", "Value 2", "Value Long Long Long"],command=lambda value:combo_event(value))
optionmenu_2.grid(row=10, column=1, padx=5, pady=(5, 5))




# Seleccionar el marco predeterminado
select_frame_by_name("home")
toplevel_window = None
root.protocol("WM_DELETE_WINDOW", root.quit)
# Ejecutar el bucle principal de la interfaz
root.mainloop()
