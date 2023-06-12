from pypdf import PdfReader
from docx import Document
# 'para crear un archivo word nuevo
import openai
import os


# 'función que entrega una cadena sin saltos de línea:
def sin_espacios(cadena):
    simbolo = '\n'
    for i in range(len(simbolo)):
        cadena = cadena.replace(simbolo[i], ' ')
        # 'va contando caracter por caracter y si encuentra espacios
        # 'los reemplaza por un espacio en blanco
        return cadena


# 'función que entrega el contenido en texto de un PDF Sin saltos de línea (o muy pocos):
def impresion(lectura):
    paginas = len(lectura.pages)
    pagina_actual = ''
    texto_final = ''
    for elemento in range(0, paginas):
        pagina_actual = lectura.pages[elemento]
        #print(pagina_actual.extract_text())
        texto_pre = pagina_actual.extract_text()
        texto_pre = sin_espacios(texto_pre)
        # utilizo mi función para quitarle los saltos de línea
        texto_final = texto_final+texto_pre
    return texto_final


# 'Función que genera texto de chat GPT
def chat_gpt(cadena_final):
    openai.api_key = "aqui deben insertar su api key"
    openai.Model.list()
    response1 = openai.Completion.create(
        # 'engine='text-davinci-003',  # el modelo de lenguaje a utilizar
        engine='text-davinci-003',
        prompt=f'podrías redactar el texto siguiente en tiempo futuro? (no olvides omitir marcas, precios, modelos y sitios web del textoi final): {cadena_final}',
        # la pregunta o el prompt que se enviará al modelo
        temperature=0,
        # controla la "creatividad" del modelo. Un valor de 0 genera respuestas más precisas y predecibles,
        # pero menos variadas.
        max_tokens=2048,  # la longitud máxima en tokens de la respuesta
        top_p=1.0,  # controla la cantidad de opciones de respuesta generadas por el modelo
        frequency_penalty=0.0,  # penalización por usar la misma palabra varias veces en la respuesta
        presence_penalty=0.0,  # penalización por no incluir palabras importantes en la respuesta
        )
    # 'Analizamos la respuesta...
    response1 = (response1['choices'][0]['text']).strip() # 'resultado a la primer pregunta
    return response1


# 'Función que cambia las diagonales de una dirección windows a una que es leída por python
def cambiando_diagonales(cadena):
    simbolo = "\\"
    for i in range(len(simbolo)):
        cadena = cadena.replace(simbolo[i], '/')
        # 'va contando caracter por caracter y si encuentra espacios
        # 'los reemplaza por un espacio en blanco
        return cadena


# 'Función que crea el documento nuevo de word
def crear_word(cadena_de_chatgpt):
    crear_doctumento_nuevo = Document()
    crear_doctumento_nuevo.add_paragraph(cadena_de_chatgpt)
    crear_doctumento_nuevo.save(f'{archivo}.docx')
    print("Descripción de licitación creada exitosamente...")


ubicacion = str(input("Copia y pega la ubicación del archivo PDF del cual desea generar una descripción de licitacion: "))
ubicacion = cambiando_diagonales(ubicacion)
os.chdir(ubicacion)
print(ubicacion)
archivo = str(input("Copie y pegue el nombre del archivo que desea (no olvide colocar la extensión .pdf): "))
lectura = PdfReader(archivo)
descripcion = impresion(lectura)
# 'Cadena final extraida del pdf...

print(descripcion)
# 'Desde aquí da el primer resultado que requiere mi archivo word
texto_chat = chat_gpt(descripcion)
print(texto_chat)
crear_word(texto_chat)