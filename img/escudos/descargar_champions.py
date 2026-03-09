import requests
import os

# Configuración
# API_URL = "https://site.api.espn.com/apis/v2/sports/soccer/esp.1/standings"
API_URL = "https://site.api.espn.com/apis/v2/sports/soccer/uefa.champions/standings"

FOLDER = "." # Se descarga donde ejecutes el script

def descargar_escudos():
    print("--- Iniciando descarga de escudos de LaLiga (Búnker Mode) ---")
    
    try:
        response = requests.get(API_URL)
        data = response.json()
        
        # Entramos en la estructura del JSON de ESPN para llegar a los equipos
        equipos = data['children'][0]['standings']['entries']
        
        for entrada in equipos:
            team = entrada['team']
            team_id = team['id']
            team_name = team['shortDisplayName']
            
            # Buscamos la URL del logo (normalmente la primera es la mejor)
            if 'logos' in team and len(team['logos']) > 0:
                logo_url = team['logos'][0]['href']
                
                # Nombre del archivo basado en el ID para que coincida con nuestro código JS
                filename = f"{team_id}.png"
                
                print(f"Descargando {team_name} (ID: {team_id})...")
                
                img_data = requests.get(logo_url).content
                with open(os.path.join(FOLDER, filename), 'wb') as handler:
                    handler.write(img_data)
            else:
                print(f"!!! No se encontró logo para {team_name}")

        print("\n--- ¡Proceso completado! Escudos guardados en local ---")

    except Exception as e:
        print(f"Error fatal: {e}")

if __name__ == "__main__":
    descargar_escudos()