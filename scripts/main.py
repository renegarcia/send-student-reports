import csv
import argparse
import send_report_email


email_field = "Email"


def leer_csv_a_diccionarios(nombre_archivo):
    # Abre el archivo en modo lectura ('r') y especifica la codificación (utf-8 es común)
    with open(nombre_archivo, mode="r", encoding="utf-8", newline="") as archivo_csv:
        # csv.DictReader usa la primera fila como nombres de columna (keys)
        lector = csv.DictReader(archivo_csv)

        # Convierte el objeto DictReader (que es un iterador) a una lista
        lista_de_diccionarios = list(lector)

        return lista_de_diccionarios


def leer_plantilla(nombre_archivo: str) -> str | None:
    """
    Abre el archivo especificado, lee todo su contenido en una variable
    y retorna esa cadena de texto.

    Args:
        nombre_archivo: El nombre (y ruta) del archivo a leer.

    Returns:
        Una cadena de texto con el contenido del archivo, o None en caso de error.
    """
    contenido = None

    try:
        # Usamos 'with open(...)' para asegurar que el archivo se cierre automáticamente
        # Se abre en modo lectura ('r') y se usa 'utf-8' como codificación estándar.
        with open(nombre_archivo, mode="r", encoding="utf-8") as archivo:
            # .read() lee todo el contenido del archivo de una vez como una cadena de texto.
            contenido = archivo.read()

        print(f"✅ Archivo de plantilla '{nombre_archivo}' leído con éxito.")
        return contenido

    except FileNotFoundError:
        print(f"❌ ERROR: El archivo de plantilla '{nombre_archivo}' no fue encontrado.")
        # Podrías terminar el script aquí si el archivo es esencial
        # sys.exit(1)
        return None
    except Exception as e:
        print(f"❌ ERROR inesperado al leer la plantilla: {e}")
        return None


def main():
    # 1. Configurar el Analizador de Argumentos (ArgumentParser)
    parser = argparse.ArgumentParser(description="Script to send email reports.")

    # 2. Agregar el argumento 'csv'
    # --csv es la versión larga, -c es la abreviatura.
    # required=True asegura que el usuario DEBE proporcionar este argumento.
    parser.add_argument(
        "--csv",
        "-c",
        type=str,
        required=True,
        help="CSV file (eg: 'data.csv').",
    )

    # 3. Agregar el argumento 'template'
    # --template es la versión larga, -t es la abreviatura.
    # required=True asegura que el usuario DEBE proporcionar este argumento.
    parser.add_argument(
        "--template",
        "-t",
        type=str,
        required=True,
        help="Template file (eg: 'template.html').",
    )

    # 3. Leer los argumentos pasados por la consola
    args = parser.parse_args()

    # El nombre del archivo ahora está en args.csv
    nombre_del_archivo = args.csv

    # 4. Llamar a la función principal con el nombre del archivo
    datos = leer_csv_a_diccionarios(nombre_del_archivo)
    print(f"\nImported {len(datos)} rows.")

    # 5. Leer plantilla y mezclar datos
    nombre_plantilla = args.template
    plantilla = leer_plantilla(nombre_plantilla)

    if plantilla is None:
        print(f"Error reading template <{nombre_plantilla}>")
        exit(1)

    # 6. Sustituir los datos en la plantilla
    print("Sending mail")
    for row in datos:
        email = row[email_field]
        subject = "Calificaciones del curso"
        content = plantilla.format(**row)
        token = send_report_email.setup_access_token()
        send_report_email.send_report_email(email, subject, content, token)
        print(f"Email sent to {email}")


if __name__ == "__main__":
    main()
