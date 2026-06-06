def calcular_tiempo(gb, mbps):
    segundos = (gb * 8192) / mbps
    return segundos

ot = "si"

while ot == "si":
    try:
        tam = float(input("Tamaño del archivo (GB): "))
        velocidad = float(input("Velocidad (Mbps): "))
        
        segundos_totales = calcular_tiempo(tam, velocidad)
        
        print(f"Tiempo estimado: {segundos_totales:.2f} segundos.")
        
    except ValueError:
        print("Error: Ingresa solo números.")
    
    print("-" * 30)
    ot = input("¿Desea calcular otro tiempo? (si/no): ").lower().strip()