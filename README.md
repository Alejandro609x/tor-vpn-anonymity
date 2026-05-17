# TOR VPN ANONYMITY

Herramienta avanzada en Python para automatizar conexiones anónimas mediante TOR, rotación automática de IPs y lanzamiento de navegadores privados usando SOCKS5.

---

# Características

- Rotación automática de IP TOR
- Selección de país de salida
- Compatibilidad con Firefox y Chromium
- Configuración automática de TOR
- Detección de IP real y IP TOR
- Interfaz visual en terminal
- Soporte para múltiples puertos SOCKS5
- Modo privado/incógnito automático
- Reinicio automático de circuitos TOR
- Compatible con Linux/Kali/Debian/Ubuntu

---

# Requisitos

- Python 3
- TOR
- curl
- Firefox ESR o Chromium

---

# Instalación

## Clonar el repositorio

```bash
git clone https://github.com/Alejandro609x/tor-vpn-anonymity.git
```

## Entrar al directorio

```bash
cd tor-vpn-anonymity
```

## Dar permisos

```bash
chmod +x tor_anonymity.py
```
No es muy necesario, ya que se tiene que ejecutar con sudo

---

# Uso

## Ejecutar como ROOT

```bash
sudo python3 tor_anonymity.py
```

o:

```bash
sudo ./tor_anonymity.py
```

---

# Funcionamiento

1. Selecciona el país de salida TOR
2. Selecciona el puerto SOCKS5
3. Selecciona navegador
4. Configura intervalo de rotación
5. El script reinicia TOR automáticamente
6. Se abre el navegador en modo privado
7. TOR rota la IP automáticamente

---

# Países disponibles

- Alemania
- Estados Unidos
- Japón
- Francia
- Canadá
- España
- Brasil
- México
- Países Bajos

Nota: Si quieres rotar IP cada cierto tiempo hay paises mejores que otros. 

---

# Puertos compatibles

- 9050
- 9150
- Personalizado (Puede darte error ya que depende de tus puertos)

---

# Rotación de IP

El script puede rotar automáticamente:

- Cada 1 minuto
- Cada 5 minutos
- Cada 10 minutos
- Cada 30 minutos
- Estático

---

# Compatibilidad

Probado en:

- Kali Linux
- Debian
- Ubuntu
- Parrot OS

---

# Capturas

![menu](Imágenes/menu.png)


![menu](Imágenes/menudos.png)


![menu](Imágenes/menutres.png)


![menu](Imágenes/ipcambio.png)


---

# Advertencia

Esta herramienta fue desarrollada únicamente con fines educativos, privacidad y pruebas de anonimato.

El usuario es responsable del uso que le dé al software.

---
Flujo de Operación Interna

El script opera de manera modular siguiendo estrictamente el siguiente esquema de seguridad:

[Inicio] -> [Verificación de Root] -> [Comprobación de Dependencias (Tor/Curl)]
   │
   ▼
[Menús Interactivos: Selección de País, Puerto Socks5, Navegador e Intervalo]
   │
   ▼
[Modificación en caliente de /etc/tor/torrc] -> [Reinicio Seguro del Servicio Tor]
   │
   ▼
[Limpieza de candados (.parentlock) y Forzado de Cierre de Instancias Previas]
   │
   ▼
[Lanzamiento del Navegador Aislado (Como Usuario No-Root / Desvío de Errores)]
   │
   ▼
[Bucle de Monitoreo Dinámico: Impresión de Métricas Adaptativas y Rotación de IP]

# Arquitectura Técnica y Métodos Críticos

1. Desescalado de Privilegios Seguro (abrir_navegador)

Ejecutar interfaces gráficas o navegadores web como el usuario root rompe las reglas básicas de la seguridad informática. El script soluciona esto detectando el entorno real mediante os.getenv("SUDO_USER"). Al invocar el subproceso, el navegador se aísla por completo:
Python

subprocess.Popen(["sudo", "-u", usuario_real, nav, ...])

2. Rompimiento de Candados de Perfil (.parentlock)

Cuando Firefox se cierra bruscamente, deja un archivo de bloqueo en la carpeta del perfil temporal. La próxima vez que intentes abrirlo, arrojará el error "Firefox is already running". El script previene esto de raíz limpiando este archivo antes de inicializar la ventana:
Python

lock_file = os.path.join(perfil_temp, ".parentlock")
if os.path.exists(lock_file):
    os.remove(lock_file)

3. Rotación de Circuitos mediante Sockets (nueva_identidad)

En lugar de reiniciar el demonio de TOR completo (lo que causaría pérdidas de conexión de más de 10 segundos), el script interactúa directamente por sockets TCP con el puerto de control seguro (9051) inyectando la instrucción de red en caliente SIGNAL NEWNYM. Esto invalida los nodos previos y construye rutas limpias instantáneamente.
4. Supresión de Logs de D-Bus y GTK

---
