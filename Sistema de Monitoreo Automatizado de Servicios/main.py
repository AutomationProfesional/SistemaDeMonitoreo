import json
import requests
import time
from datetime import datetime
from utils.monitor import check_service
from database.database import guardar_en_database, create_database

def load_services():
    """Carga los servicios desde services.json"""
    try:
        with open("services.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("❌ Archivo de servicios no encontrado")
        return []
    except Exception as error:
        print(f"❌ Error cargando servicios: {error}")
        return []
    
def save_log(log):
    """Guarda los logs en logs.json"""
    try:
        with open("logs.json", "r") as file:
            logs = json.load(file)
    except FileNotFoundError:
        logs = []

    logs.append(log)

    with open("logs.json", "w") as file:
        json.dump(logs, file, indent=4)
    
def enviar_a_n8n(url, data):
    """Envía datos a n8n (webhook opcional)"""
    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"✓ Enviado a n8n: {response.status_code}")
    except Exception as e:
        print(f"⚠ Error enviando a n8n: {e}")

def ejecutar_monitoreo():
    """Ejecuta una ronda de monitoreo"""
    print(f"\n{'='*50}")
    print(f"🔍 Verificando servicios - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}\n")
    
    services = load_services()
    
    if not services:
        print("❌ No hay servicios para monitorear")
        return

    for service in services:
        result = check_service(service["url"])
        log = {
            "service": service["name"],
            "url": service["url"],
            "status": result["status"],
            "date": datetime.now().strftime("%y-%m-%d %H:%M:%S")
        }
        
        if "code" in result:
            log["code"] = result["code"]
        if "message" in result:
            log["message"] = result["message"]
        
        # Guardar en JSON
        save_log(log)
        
        # Guardar en BD SQLite
        guardar_en_database(log)
        
        # Enviar a n8n (descomenta si tienes n8n corriendo)
        # enviar_a_n8n("http://localhost:5678/webhook-test/monitor-alert", log)

        # Mostrar resultado
        status_icon = "✓" if result["status"] == "UP" else "✗"
        print(f"{status_icon} {service['name']}: {result['status']}")
        if "code" in result:
            print(f"   Código HTTP: {result['code']}")
        if "message" in result:
            print(f"   Error: {result['message']}")

def main():
    """Función principal con ejecución en intervalos"""
    create_database()
    
    # Intervalo en segundos (300 = 5 minutos)
    INTERVALO = 300
    
    print("\n" + "="*50)
    print("🚀 MONITOR DE SERVICIOS INICIADO")
    print("="*50)
    print(f"Intervalo de verificación: {INTERVALO // 60} minutos")
    print(f"Inicia: {datetime.now().strftime('%H:%M:%S')}")
    print("="*50)
    
    try:
        while True:
            ejecutar_monitoreo()
            print(f"\n⏳ Próxima verificación en {INTERVALO // 60} minutos...")
            time.sleep(INTERVALO)
    except KeyboardInterrupt:
        print("\n\n⛔ Monitor detenido por el usuario")

if __name__ == "__main__":
    main()