import json

# Intenta diferentes codificaciones
encodings = ['latin-1', 'cp1252', 'iso-8859-1']

# Usa 'data.json' en lugar de 'data_temp.json'
input_file = 'data.json'
output_file = 'data_clean.json'

for encoding in encodings:
    try:
        print(f"Intentando abrir {input_file} con codificación: {encoding}")
        # Leer el archivo JSON
        with open(input_file, 'r', encoding=encoding) as file:
            data = json.load(file)

        # Guardar el archivo JSON con codificación UTF-8
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        print(f"¡Éxito! Archivo convertido y guardado como {output_file}")
        break
    except Exception as e:
        print(f"Error con {encoding}: {str(e)}")
        continue