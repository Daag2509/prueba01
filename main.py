import dearpygui.dearpygui as dpg
import pyttsx3
import os

engine = pyttsx3.init()

def texto_convertir(sender, app_dat, user_data):
    texto = dpg.get_value("texto_input")

def file_callback(sender, app_data):
    # Verificar si se seleccionó un archivo
    if 'file_path_name' in app_data:
        file_path = app_data['file_path_name']
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                dpg.set_value("text_display", content)
                update_text_stats(content)  # Actualizar estadísticas de texto
        except FileNotFoundError:
            print(f"Error: El archivo no se encontró en la ruta: {file_path}")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("No se seleccionó ningún archivo.")

def update_text_stats(text):
    # Contar palabras y letras
    word_count = len(text.split())
    letter_count = len(text)
    dpg.set_value("word_count_display", f"Palabras: {word_count}")
    dpg.set_value("letter_count_display", f"Letras: {letter_count}")

def start_conversion(sender, app_data):
    # Obtener el texto a convertir
    texto = dpg.get_value("text_display")
    
    # Obtener configuración de velocidad y volumen
    rate = dpg.get_value("slider_rate")
    volume = dpg.get_value("slider_volume")
    
    # Configurar el motor de texto a voz
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    # Convertir el texto a voz
    engine.save_to_file(texto, "audio_nuevo.mp3")
    engine.runAndWait()

    # Mostrar popup de confirmación
    dpg.configure_item("popup_id", show=True)

def test_voice(sender, app_data):
    # Obtener el texto a probar
    texto = dpg.get_value("text_display")
    
    # Obtener configuración de velocidad y volumen
    rate = dpg.get_value("slider_rate")
    volume = dpg.get_value("slider_volume")
    
    # Configurar el motor de texto a voz
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    # Probar la voz
    engine.say(texto)
    engine.runAndWait()

def get_voices():
    voices = engine.getProperty('voices')
    return voices

dpg.create_context()
with dpg.window(label="Conversor de Texto a Voz", width=600, height=600):

    # Botón para cargar el archivo de texto
    dpg.add_button(label="Cargar archivo de texto", callback=lambda: dpg.show_item("file_dialog_id"))
    
    # Mostrar el contenido del archivo cargado
    dpg.add_text("Contenido del texto:")
    dpg.add_input_text(tag="text_display", multiline=True, readonly=True, width=500, height=200)

    # Contadores de palabras y letras
    dpg.add_text(tag="word_count_display", default_value="Palabras: 0")
    dpg.add_text(tag="letter_count_display", default_value="Letras: 0")

    # Controles para ajustar la velocidad y volumen de la voz
    dpg.add_text("Configuraciones de voz")
    dpg.add_text("Seleccionar voz:")
    voices = get_voices()
    voice_names = [voice.name for voice in voices]
    dpg.add_combo(label="Voces", items=voice_names, tag="voice_selector")
    dpg.add_slider_int(tag="slider_rate", label="Velocidad", default_value=150, min_value=100, max_value=300)
    dpg.add_slider_float(tag="slider_volume", label="Volumen", default_value=0.8, min_value=0.0, max_value=1.0)

    # Botón para probar la voz
    dpg.add_button(label="Probar voz", callback=test_voice)

    # Botón para iniciar la conversión
    dpg.add_button(label="Convertir texto a voz", callback=start_conversion)

# Cuadro de diálogo para seleccionar el archivo
with dpg.file_dialog(directory_selector=False, show=False, callback=file_callback, tag="file_dialog_id"):
    dpg.add_file_extension(".txt", color=(0, 255 , 0, 255))  # Filtra solo archivos .txt

# Popup de confirmación
with dpg.window(label="Confirmación", modal=True, show=False, tag="popup_id"):
    dpg.add_text("La conversión se ha completado con éxito.")
    dpg.add_button(label="Cerrar", callback=lambda: dpg.configure_item("popup_id", show=False))

# Configurar y mostrar la ventana principal
dpg.create_viewport(title="Conversor de Texto a Voz", width=600, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()