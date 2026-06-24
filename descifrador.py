import subprocess

def ejecutar_comando_git(comando):
    """Función auxiliar para enviar comandos a la terminal y recibir el texto."""
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, text=True, shell=True)
    return resultado.stdout.strip()

def main():
    # Obtener el historial de hashes ordenados desde el más antiguo al más reciente
    historial_raw = ejecutar_comando_git("git log --reverse --format=%H")
    commits = historial_raw.splitlines()
    
    # Inicializar la cadena vacía llamada Llave
    Llave = ""
    
    for commit_hash in commits:
        if not commit_hash:
            continue
            
        # 1. EXTRAER EL CONTENIDO DE NUCLEO.TXT EN ESTE COMMIT EXACTO
        contenido = ejecutar_comando_git(f"git show {commit_hash}:nucleo.txt")
        
        # Si el archivo está vacío por alguna razón, pasamos al siguiente
        if not contenido:
            continue
            
        # 2. EVALUACIÓN DE ESTADO: Convertir los primeros 6 caracteres del hash a decimal
        primeros_6 = commit_hash[:6]
        valor_decimal = int(primeros_6, 16)
        
        # 3. MÁQUINA DE ESTADOS (EL CIFRADO)
        if valor_decimal % 2 == 0:
            # --- CASO PAR ---
            # Tomar el primer carácter del contenido
            caracter = contenido[0]
            
            # Contar la cantidad de números (0-9) en el hash completo
            conteo_numeros = 0
            for digito in commit_hash:
                if digito.isdigit():
                    conteo_numeros += 1
            
            # Aplicar Cifrado César (Desplazamiento)
            if caracter.isupper():
                nueva_letra = chr((ord(caracter) - ord('A') + conteo_numeros) % 26 + ord('A'))
            elif caracter.islower():
                nueva_letra = chr((ord(caracter) - ord('a') + conteo_numeros) % 26 + ord('a'))
            else:
                nueva_letra = caracter  # Mantiene espacios o símbolos iguales
                
        else:
            # --- CASO IMPAR ---
            # Tomar el último carácter del contenido
            caracter = contenido[-1]
            
            # Contar la cantidad de letras (a-f) en el hash completo
            conteo_letras = 0
            for letra in commit_hash.lower():
                if letra in "abcdef":
                    conteo_letras += 1
            
            # Convertir a ASCII, sumar el conteo de letras y volver a transformar en carácter
            codigo_ascii = ord(caracter)
            nuevo_codigo = codigo_ascii + conteo_letras
            nueva_letra = chr(nuevo_codigo)
            
        # Concatenar el resultado a la variable Llave
        Llave = Llave + nueva_letra
        
        # 4. MUTACIÓN FINAL: Si es un commit de Merge, la Llave se invierte
        # Revisamos si el commit tiene más de un padre (lo que delata un Merge)
        padres = ejecutar_comando_git(f"git log -1 --format=%P {commit_hash}")
        es_merge = len(padres.split()) > 1
        
        if es_merge:
            Llave = Llave[::-1]  # Truco sencillo de Python para voltear un texto
            
    # Imprimir por consola únicamente la cadena final Llave
    print(Llave)

if __name__ == "__main__":
    main()