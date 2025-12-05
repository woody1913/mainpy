import mysql.connector

#  1. FUNCIÓN DE CONEXIÓN REUTILIZABLE
def conectar():
    """Establece y devuelve la conexión a la base de datos 'AccionClimaDB'."""
    try:
        # Intentamos conectar a la base de datos específica
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1234",
            database="AccionClimaDB"  # <--- CAMBIO AQUÍ
        )
        return mydb
    except mysql.connector.Error as err:
        # No mostramos el error 1049 (Unknown database) si la configuracion_inicial() se encarga
        if err.errno != 1049: 
             print(f"Error al conectar a la base de datos: {err}")
        return None

# --- 2. CONFIGURACIÓN INICIAL (Creación de DB y Tabla) ---
def configuracion_inicial():
    """Asegura que la DB y la tabla Voluntarios existan.""" # <--- CAMBIO AQUÍ
    
    # Conexión temporal, SÓLO para crear la DB (sin especificar una base de datos)
    try:
        temp_db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1234"
        )
        temp_cursor = temp_db.cursor()
        
        # 2.1 CREAR LA BASE DE DATOS si no existe
        temp_cursor.execute("CREATE DATABASE IF NOT EXISTS AccionClimaDB") # <--- CAMBIO AQUÍ
        temp_db.commit()
        temp_cursor.close()
        temp_db.close()
        print("Base de datos 'AccionClimaDB' verificada/creada.") # <--- CAMBIO AQUÍ
        
    except mysql.connector.Error as err:
        print(f"Error al conectar para crear la DB: {err}")
        return False
        
    # Conexión a la DB recién creada para asegurar la tabla
    mydb = conectar()
    if mydb is None:
        print("No se pudo conectar a la DB para crear la tabla.")
        return False

    mycursor = mydb.cursor()
    
    # 2.2 CREACIÓN DE LA TABLA si no existe
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Voluntarios (  # <--- CAMBIO AQUÍ
        id INT AUTO_INCREMENT PRIMARY KEY,
        Nombre VARCHAR(255),
        Contraseña VARCHAR(255),
        Edad INT,
        Peso FLOAT,  # Mantenemos las columnas originales por no alterar el código base, aunque 'Peso' y 'Alturacm' ya no son tan relevantes para "acción climática".
        Alturacm INT 
    )
    """)
    print("Tabla 'Voluntarios' verificada/creada.") # <--- CAMBIO AQUÍ

    # 2.3 Inserción de datos de PRUEBA (SOLO si no existen)
    sql = "INSERT INTO Voluntarios (Nombre, Contraseña, Edad, Peso, Alturacm) VALUES (%s, %s, %s, %s, %s)" # <--- CAMBIO AQUÍ
    val = [
        ( "Eluney Naz", "123", 16, 90.0, 173),
        ("Andrés Bianchi", "123", 31, 67.0, 167),
        ("Máximo Férnandez", "123", 16, 70.0, 174),
        ("Máximo Oliva", "123", 15, 66.0, 180),
        ("Arturo Prat", "123", 61, 78.0, 176),
        ("Benjamín Acosta", "123", 16, 58.0, 172),
        ("Gabriela Ocaño", "123", 51, 137.0, 165)
    ]
    try:
        mycursor.executemany(sql, val)
        mydb.commit()
        print(f"{mycursor.rowcount} registros de prueba insertados.")
    except mysql.connector.Error as err:
        if err.errno == 1062: # Clave duplicada (si ya existen los registros de prueba)
             pass
        else:
             print(f"Error al insertar datos de prueba: {err}")

    # Cierre de conexión de configuración
    mycursor.close()
    mydb.close()
    
    return True

# --- 3. FUNCIONES DEL MENÚ ---

def Registrar_usuario(): 
    print("\nCrear cuenta de Voluntario") # <--- CAMBIO AQUÍ
    
    Nombre = input("Nombre: ")
    Contraseña = input("Contraseña: ")
    try:
        Edad = int(input("Edad: "))
        Peso = float(input("Peso (kg): ")) # Texto actualizado
        Alturacm = int(input("Altura (cm): ")) # Texto actualizado
    except ValueError:
        print("Error: Edad y Altura deben ser números enteros, Peso debe ser un número decimal.") # Texto actualizado
        return
    
    conexion = conectar()
    if conexion is None:
        return
    
    cursor = conexion.cursor()
    
    query = """
        INSERT INTO Voluntarios (Nombre, Contraseña, Edad, Peso, Alturacm) # <--- CAMBIO AQUÍ
        VALUES (%s, %s, %s, %s, %s)
    """
    datos = (Nombre, Contraseña, Edad, Peso, Alturacm)
    
    try:
        cursor.execute(query, datos)
        conexion.commit() 
        print("\n¡Te has registrado como Voluntario con éxito!\n") # <--- CAMBIO AQUÍ
    except mysql.connector.Error as err:
        print(f"Error al registrar voluntario: {err}") # <--- CAMBIO AQUÍ
    
    cursor.close()
    conexion.close()

def iniciar_sesion():
    print("\nInicio de sesión de Voluntario") # <--- CAMBIO AQUÍ
    Nombre = input("Nombre: ")
    Contraseña = input("Contraseña: ")

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    query = "SELECT id, Nombre, Alturacm FROM Voluntarios WHERE Nombre = %s AND Contraseña = %s" # <--- CAMBIO AQUÍ
    cursor.execute(query, (Nombre, Contraseña))
    resultado = cursor.fetchone() 

    if resultado:
        print(f"\n¡Bienvenido a la Acción Climática! {resultado[1]} (ID: {resultado[0]}, Altura: {resultado[2]}cm)\n") # <--- CAMBIO AQUÍ
    else:
        print("\nDatos no encontrados, intenta de nuevo o crea una cuenta de Voluntario.\n") # <--- CAMBIO AQUÍ

    cursor.close()
    conexion.close()

def consultar_usuario():
    print("\nConsulta de Voluntario") # <--- CAMBIO AQUÍ
    user_id = input("ID de voluntario: ") # <--- CAMBIO AQUÍ

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT id, Nombre, Edad, Peso, Alturacm FROM Voluntarios WHERE id = %s", (user_id,)) # <--- CAMBIO AQUÍ
        resultado = cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error al consultar: {err}")
        resultado = None

    if resultado:
        print("\nDatos del Voluntario:") # <--- CAMBIO AQUÍ
        print(f"ID: {resultado[0]}, Nombre: {resultado[1]}, Edad: {resultado[2]}, Peso: {resultado[3]}kg, Altura: {resultado[4]}cm")
    else:
        print("\nNo existe un voluntario con ese ID.") # <--- CAMBIO AQUÍ

    cursor.close()
    conexion.close()

def modificar_usuario():
    print("\nActualizar datos de Voluntario") # <--- CAMBIO AQUÍ
    user_id = input("ID del voluntario a modificar: ") # <--- CAMBIO AQUÍ

    try:
        nueva_edad = int(input("Edad Nueva: "))
        nuevo_peso = float(input("Nuevo Peso (kg): ")) # Texto actualizado
        nueva_altura = int(input("Nueva Altura en cm: ")) # Texto actualizado
    except ValueError:
        print("Error: Edad y Altura deben ser números enteros, Peso debe ser un número.") # Texto actualizado
        return

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    query = """
        UPDATE Voluntarios # <--- CAMBIO AQUÍ
        SET Edad = %s, Peso = %s, Alturacm = %s
        WHERE id = %s
    """
    datos = (nueva_edad, nuevo_peso, nueva_altura, user_id)

    try:
        cursor.execute(query, datos)
        conexion.commit()
        if cursor.rowcount > 0:
            print("\nDatos del Voluntario modificados correctamente!\n") # <--- CAMBIO AQUÍ
        else:
            print("\nNo se encontró un voluntario con ese ID o no se hicieron cambios.") # <--- CAMBIO AQUÍ
    except mysql.connector.Error as err:
        print(f"Error al modificar datos: {err}")

    cursor.close()
    conexion.close()

def modificar_contraseña():
    print("\nModificar contraseña de Voluntario") # <--- CAMBIO AQUÍ
    user_id = input("ID del voluntario: ") # <--- CAMBIO AQUÍ
    nueva_contr = input("Nueva contraseña: ")

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    query = "UPDATE Voluntarios SET Contraseña = %s WHERE id = %s" # <--- CAMBIO AQUÍ
    
    try:
        cursor.execute(query, (nueva_contr, user_id))
        conexion.commit()
        if cursor.rowcount > 0:
            print("\nContraseña actualizada.\n")
        else:
            print("\nNo se encontró un voluntario con ese ID.") # <--- CAMBIO AQUÍ
    except mysql.connector.Error as err:
        print(f"Error al modificar contraseña: {err}")

    cursor.close()
    conexion.close()

def eliminar_cuenta():
    print("\nEliminar cuenta de Voluntario") # <--- CAMBIO AQUÍ
    user_id = input("ID del voluntario a eliminar: ") # <--- CAMBIO AQUÍ
    confirmacion = input("Está seguro de que desea eliminar la cuenta de voluntario? (s/n): ").lower() # <--- CAMBIO AQUÍ
    
    if confirmacion != 's':
        print("\nOperación cancelada.")
        return

    conexion = conectar()
    if conexion is None:
        return

    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM Voluntarios WHERE id = %s", (user_id,)) # <--- CAMBIO AQUÍ
        conexion.commit()
        
        if cursor.rowcount > 0:
            print("\nCuenta de Voluntario borrada correctamente.\n") # <--- CAMBIO AQUÍ
        else:
            print("\nNo se encontró un voluntario con ese ID.") # <--- CAMBIO AQUÍ
            
    except mysql.connector.Error as err:
        print(f"Error al eliminar cuenta: {err}")

    cursor.close()
    conexion.close()

# --- 4. FUNCIÓN DEL MENÚ Y EJECUCIÓN PRINCIPAL ---

def menu():
    while True:
        print("\n--- ¡Bienvenido al Portal de Voluntarios por el Clima! ---") # <--- CAMBIO AQUÍ
        print("1. Registrar nuevo voluntario") # <--- CAMBIO AQUÍ
        print("2. Iniciar sesión de voluntario") # <--- CAMBIO AQUÍ
        print("3. Consultar datos de voluntario") # <--- CAMBIO AQUÍ
        print("4. Modificar mis datos")
        print("5. Modificar mi contraseña")
        print("6. Eliminar mi cuenta de voluntario") # <--- CAMBIO AQUÍ
        print("7. Salir")
        print("------------------------------------------")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            Registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            consultar_usuario()
        elif opcion == "4":
            modificar_usuario()
        elif opcion == "5":
            modificar_contraseña()
        elif opcion == "6":
            eliminar_cuenta()
        elif opcion == "7":
            print("¡Gracias por tu acción por el clima! Vuelve pronto!") # <--- CAMBIO AQUÍ
            break
        else:
            print("Opción inválida. Pruebe otra vez.\n")

if __name__ == "__main__":
    print("Iniciando configuración de base de datos para la Acción Climática...") # <--- CAMBIO AQUÍ
    if configuracion_inicial():
        print("\nConfiguración lista. Iniciando menú de Voluntarios.") # <--- CAMBIO AQUÍ
        menu()
    else:
        print("\nNo se pudo iniciar la aplicación debido a un error de conexión o configuración con MySQL.")
