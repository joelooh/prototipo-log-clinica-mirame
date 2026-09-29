import uuid
from datetime import datetime

def obtener_nombre_archivo(fecha_simulada=None):
    """
    Puntos 1, 1.1 y 2.4:
    Genera el nombre del archivo físico con el formato Log_Exepciones_yyyyMMdd.txt.
    Si el error ocurre en un día diferente, la fecha cambia y se crea un nuevo archivo.
    """
    fecha_actual = fecha_simulada if fecha_simulada else datetime.now()
    formato_fecha = fecha_actual.strftime("%Y%m%d")
    return f"Log_Exepciones_{formato_fecha}.txt"

def escribir_log(nivel, mensaje_error, codigo_error="", fecha_simulada=None):
    """
    Puntos 2.1, 2.2 y 2.3:
    Escribe en el archivo plano (TXT) la hora exacta del error y el detalle de la excepción.
    Usa el modo 'a' (append) para escribir cada nuevo error con diferente hora en el mismo archivo.
    """
    ahora = fecha_simulada if fecha_simulada else datetime.now()
    nombre_archivo = obtener_nombre_archivo(ahora)
    
    # Formato de hora con milisegundos para evidenciar distintas horas de ejecución
    hora_error = ahora.strftime("%H:%M:%S.%f")[:-3]
    fecha_legible = ahora.strftime("%Y-%m-%d")

    linea_log = (
        f"[{fecha_legible} {hora_error}] | "
        f"NIVEL: {nivel} | "
        f"CODIGO: {codigo_error} | "
        f"ERROR: {mensaje_error}\n"
    )

    # Apertura en modo 'a' (append): crea el archivo físico si no existe o agrega líneas al final
    with open(nombre_archivo, mode="a", encoding="utf-8") as archivo:
        archivo.write(linea_log)

    return nombre_archivo

def registrar_paciente():
    """
    Punto 2:
    Ejecuta el flujo de la aplicación dentro de un bloque try-except (try-catch en Python),
    validando entradas y capturando cualquier excepción para escribirla en el LOG.
    """
    try:
        print("\n--- REGISTRO DE PACIENTE Y PRESUPUESTO OFTALMOLÓGICO ---")
        nombre = input("Ingrese nombre del paciente: ").strip()
        
        # Validación de campo vacío
        if not nombre:
            raise ValueError("El usuario ingresó un nombre de paciente vacío.")

        entrada_edad = input("Ingrese edad del paciente: ").strip()
        # Si el usuario ingresa texto en vez de número, int() lanza ValueError automáticamente
        edad = int(entrada_edad)
        
        # Validación de rango de edad
        if edad < 1 or edad > 120:
            raise OverflowError(f"La edad ingresada ({edad}) está fuera del rango permitido (1 a 120 años).")

        entrada_cuotas = input("Ingrese cantidad de cuotas para dividir el copago ($100.000): ").strip()
        cuotas = int(entrada_cuotas)
        
        # Si el usuario ingresa 0 cuotas, se lanza ZeroDivisionError automáticamente
        valor_cuota = 100000 / cuotas

        # Si todo es válido, se registra el evento informativo
        codigo_ok = str(uuid.uuid4())[:8]
        archivo = escribir_log("INFO", "Paciente y presupuesto registrados correctamente.", codigo_ok)
        
        print("\n[OK] Registro realizado correctamente.")
        print(f"     Paciente: {nombre} | Edad: {edad} años | Valor por cuota: ${valor_cuota:,.0f} CLP")
        print(f"     Evento registrado en: {archivo}")

    except Exception as ex:
        # Captura de la excepción (bloque catch) y escritura en el archivo TXT
        codigo_incidente = str(uuid.uuid4())
        detalle_excepcion = f"{type(ex).__name__}: {str(ex)}"
        
        archivo_generado = escribir_log("ERROR", detalle_excepcion, codigo_incidente)

        # Mensaje genérico seguro para el usuario (Estándar OWASP ASVS 4.0.3 / NIST 800-63)
        print("\n[!] Ocurrió un error inesperado al procesar la solicitud.")
        print(f"    Código de error para soporte técnico: {codigo_incidente}")
        print(f"    (Excepción registrada en el archivo físico: {archivo_generado})")

def simular_errores_demostracion():
    """
    Función automatizada para demostrar en el video:
    - Múltiples errores en diferente hora dentro del mismo archivo (Punto 2.3).
    - Creación de un nuevo archivo cuando el error ocurre en un día diferente (Punto 2.4).
    """
    print("\n--- EJECUTANDO PRUEBA AUTOMÁTICA DE EXCEPCIONES ---")

    # Error 1: División por cero (Día actual)
    try:
        print("1. Generando error de división por cero en cálculo de lentes...")
        resultado = 85000 / 0
    except Exception as ex:
        codigo = str(uuid.uuid4())
        detalle = f"{type(ex).__name__}: {str(ex)} (Módulo de Presupuesto)"
        archivo = escribir_log("ERROR", detalle, codigo)
        print(f"   -> Guardado en {archivo} | Código: {codigo}")

    # Error 2: Índice fuera de rango en diferente hora (Mismo día)
    try:
        print("2. Generando error de índice fuera de rango al buscar ficha médica...")
        historial_clinico = ["Ficha_101", "Ficha_102"]
        ficha = historial_clinico[99]
    except Exception as ex:
        codigo = str(uuid.uuid4())
        detalle = f"{type(ex).__name__}: {str(ex)} (Módulo de Fichas Clínicas)"
        archivo = escribir_log("ERROR", detalle, codigo)
        print(f"   -> Guardado en {archivo} | Código: {codigo}")

    # Error 3: Excepción ocurrida en un día diferente (Punto 2.4)
    try:
        print("3. Simulando excepción en un día diferente (29/09/2026)...")
        # Se fija la fecha para mañana: 29 de septiembre de 2026
        fecha_dia_siguiente = datetime(2026, 9, 29, 10, 15, 42, 512000)
        int("id_cita_invalido")
    except Exception as ex:
        codigo = str(uuid.uuid4())
        detalle = f"{type(ex).__name__}: {str(ex)} (Conversión de ID en Base de Datos)"
        archivo_nuevo = escribir_log("ERROR", detalle, codigo, fecha_simulada=fecha_dia_siguiente)
        print(f"   -> Nuevo archivo creado por cambio de día: {archivo_nuevo} | Código: {codigo}")

def main():
    escribir_log("INFO", "Aplicación iniciada - Prototipo Clínica Oftalmológica Mírame.", "INIT-001")
    
    while True:
        print("\n========================================================")
        print("   CLÍNICA OFTALMOLÓGICA 'MÍRAME' - SISTEMA DE REGISTRO ")
        print("========================================================")
        print("1. Registrar atención de paciente (Probar errores manualmente)")
        print("2. Ejecutar simulación automática de errores (Mismo día y día distinto)")
        print("3. Salir")
        
        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            registrar_paciente()
        elif opcion == "2":
            simular_errores_demostracion()
        elif opcion == "3":
            escribir_log("INFO", "Aplicación finalizada correctamente.", "EXIT-001")
            print("Cerrando aplicación...")
            break
        else:
            print("Opción no válida. Por favor seleccione 1, 2 o 3.")

if __name__ == "__main__":
    main()