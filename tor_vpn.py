#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import signal
import socket
import shutil
import warnings
import subprocess
from datetime import datetime

# =========================================================
# OCULTAR WARNINGS GTK
# =========================================================

os.environ["GTK_THEME"] = "Adwaita"
os.environ["NO_AT_BRIDGE"] = "1"

warnings.filterwarnings("ignore")

# =========================================================
# COLORES
# =========================================================

R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
M = "\033[1;35m"
C = "\033[1;36m"
W = "\033[1;37m"
X = "\033[0m"

# =========================================================
# CONFIG
# =========================================================

TORRC = "/etc/tor/torrc"

PAISES = {
    1: ("Alemania", "{de}"),
    2: ("Estados Unidos", "{us}"),
    3: ("Japón", "{jp}"),
    4: ("Francia", "{fr}"),
    5: ("Canadá", "{ca}"),
    6: ("España", "{es}"),
    7: ("Brasil", "{br}"),
    8: ("México", "{mx}"),
    9: ("Países Bajos", "{nl}")
}

INTERVALOS = {
    1: ("1 minuto", 60),
    2: ("5 minutos", 300),
    3: ("10 minutos", 600),
    4: ("30 minutos", 1800),
    5: ("Estático", 0)
}

# =========================================================
# DETECCIÓN DINÁMICA DE ANCHO
# =========================================================

def obtener_ancho():
    """Devuelve el ancho actual de la terminal para ajustar las cajas."""
    try:
        return os.get_terminal_size().columns - 2
    except:
        return 60  # Ancho por defecto si falla la detección

# =========================================================
# CTRL + C / CTRL + Z
# =========================================================

def salir(signum, frame):
    ancho = obtener_ancho()
    print(f"\n{R}" + "═" * ancho)
    print(" [!] SCRIPT DETENIDO POR EL USUARIO - CERRANDO PROCESOS")
    print("═" * ancho + f"{X}")

    try:
        subprocess.run(
            ["pkill", "-f", "tor"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except:
        pass

    os._exit(0)

signal.signal(signal.SIGINT, salir)
signal.signal(signal.SIGTSTP, salir)

# =========================================================
# LIMPIAR
# =========================================================

def limpiar():
    os.system("clear")

# =========================================================
# BANNER
# =========================================================

def banner():
    ancho = obtener_ancho()
    print(f"{M}╔" + "═" * ancho + "╗")
    
    logo = ["██╗███████╗███████╗ █████╗ ███████╗ ██████╗",
            "██║██╔════╝██╔════╝██╔══██╗╚══███╔╝██╔═══██╗",
            "██║█████╗  █████╗  ███████║  ███╔╝ ██║   ██║",
            "██   ██║██╔══╝  ██╔══╝  ██╔══██║ ███╔╝  ██║   ██║",
            "╚█████╔╝███████╗██║     ██║  ██║███████╗╚██████╔╝",
            " ╚════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝"]
            
    for linea in logo:
        if len(linea) <= ancho:
            print(f"║ {linea.center(ancho - 2)} ║")
        else:
            print(f"║ {linea[:ancho-4]}... ║")
            
    print(f"║ {'-> TOR VPN ANONYMITY <-'.center(ancho)} ║")
    print(f"╚" + "═" * ancho + f"╝{X}")

# =========================================================
# ROOT
# =========================================================

def verificar_root():
    if os.geteuid() != 0:
        print(f"\n{R}[!] Error: Este script requiere privilegios de Administrador.{X}")
        print(f"{Y}[+] Ejecútalo usando: {W}sudo python3 {sys.argv[0]}{X}\n")
        sys.exit(1)

# =========================================================
# DEPENDENCIAS
# =========================================================

def instalar_dependencias():
    deps = ["tor", "curl"]
    faltan = []

    print(f"\n{C}┌─── Verificando dependencias esenciales{X}")

    for d in deps:
        if shutil.which(d):
            print(f"{C}│{X}  [{G}OK{X}] {d}")
        else:
            faltan.append(d)
            print(f"{C}│{X}  [{R}FALTA{X}] {d}")

    if faltan:
        print(f"{C}├─── Instalar dependencias faltantes...{X}\n")
        subprocess.run(["apt", "update"], stdout=subprocess.DEVNULL)
        cmd = ["apt", "install", "-y"] + faltan
        subprocess.run(cmd)
    else:
        print(f"{C}└─── Todo listo para continuar.{X}")

# =========================================================
# PAISES
# =========================================================

def mostrar_paises():
    ancho = obtener_ancho()
    print(f"\n{C}┌" + "─" * (ancho - 1))
    print(f"│ Selecciona el país de salida:{X}")
    for n, d in PAISES.items():
        extra = ""
        if d[0] in ["Estados Unidos", "Francia"]:
            extra = f" {G}(Recomendado para rotación){X}"
        print(f"{C}│{X}  [{Y}{n}{X}] {d[0]}{extra}")
    print(f"{C}└" + "─" * (ancho - 1) + f"{X}")

# =========================================================
# SELECT PAIS
# =========================================================

def seleccionar_pais():
    while True:
        try:
            op = int(input(f"{G}➔ Selecciona una opción:{X} "))
            if op in PAISES:
                return PAISES[op]
        except:
            pass
        print(f"{R}[!] Opción inválida. Intenta de nuevo.{X}")

# =========================================================
# PUERTO
# =========================================================

def seleccionar_puerto():
    ancho = obtener_ancho()
    print(f"\n{C}┌" + "─" * (ancho - 1))
    print(f"│ Configuración de Puerto SOCKS5:{X}")
    print(f"{C}│{X}  [{Y}1{X}] 9050 {G}(Predeterminado / Recomendado){X}")
    print(f"{C}│{X}  [{Y}2{X}] 9150")
    print(f"{C}│{X}  [{Y}3{X}] Puerto Personalizado")
    print(f"{C}└" + "─" * (ancho - 1) + f"{X}")

    while True:
        try:
            op = int(input(f"{G}➔ Selecciona una opción:{X} "))
            if op == 1:
                return 9050
            elif op == 2:
                return 9150
            elif op == 3:
                p = int(input(f"{G}➔ Introduce el puerto (1-65535):{X} "))
                if 1 <= p <= 65535:
                    return p
        except:
            pass
        print(f"{R}[!] Puerto o selección inválidos.{X}")

# =========================================================
# INSTALAR NAVEGADORES
# =========================================================

def instalar_firefox():
    print(f"\n{Y}[+] Instalando Firefox ESR...{X}\n")
    subprocess.run(["apt", "install", "-y", "firefox-esr"])

def instalar_chromium():
    print(f"\n{Y}[+] Instalando Chromium...{X}\n")
    subprocess.run(["apt", "install", "-y", "chromium"])


def instalar_tor_browser():
    print(f"\n{Y}[+] Instalando Tor Browser Launcher...{X}\n")

    subprocess.run([
        "apt",
        "install",
        "-y",
        "torbrowser-launcher"
    ])

    print(f"{G}[+] Descargando Tor Browser...{X}")

    subprocess.run([
        "torbrowser-launcher"
    ])

def buscar_tor_browser():

    posibles = [

        shutil.which("tor-browser"),
        shutil.which("torbrowser-launcher"),
        "/opt/tor-browser/start-tor-browser",
        "/usr/bin/torbrowser-launcher"

    ]

    for p in posibles:

        if p and os.path.isfile(p):

            return p

    return None

# =========================================================
# SELECT NAV
# =========================================================

def seleccionar_navegador():
    ancho = obtener_ancho()
    print(f"\n{C}┌" + "─" * (ancho - 1))
    print(f"│ Selección de Navegador Anónimo:{X}")
    print(f"{C}│{X}  [{Y}1{X}] Firefox")
    print(f"{C}│{X}  [{Y}2{X}] Chromium")
    print(f"{C}│{X}  [{Y}3{X}] Tor Browser")
    print(f"{C}└" + "─" * (ancho - 1) + f"{X}")

    while True:
        try:
            op = int(input(f"{G}➔ Selecciona una opción:{X} "))
            if op == 1:
                firefox = shutil.which("firefox") or shutil.which("firefox-esr")
                if not firefox:
                    r = input(f"{Y}[?] Firefox no está instalado. ¿Instalar ahora? (s/n): {X}").lower()
                    if r == "s":
                        instalar_firefox()
                        firefox = shutil.which("firefox-esr")
                return firefox

            elif op == 2:
                chromium = shutil.which("chromium")
                if not chromium:
                    r = input(f"{Y}[?] Chromium no está instalado. ¿Instalar ahora? (s/n): {X}").lower()
                    if r == "s":
                        instalar_chromium()
                        chromium = shutil.which("chromium")
                return chromium

            elif op == 3:
                torb = buscar_tor_browser()

                if not torb:
                    r = input(f"{Y}[?] Tor Browser no está instalado. ¿Instalar ahora? (s/n): {X}").lower()

                    if r == "s":
                        instalar_tor_browser()
                        torb = buscar_tor_browser()

                return torb
        except:
            pass
        print(f"{R}[!] Opción inválida.{X}")

# =========================================================
# INTERVALOS
# =========================================================

def mostrar_intervalos():
    ancho = obtener_ancho()
    print(f"\n{C}┌" + "─" * (ancho - 1))
    print(f"│ Frecuencia de Rotación de IP:{X}")
    for n, d in INTERVALOS.items():
        print(f"{C}│{X}  [{Y}{n}{X}] {d[0]}")
    print(f"{C}└" + "─" * (ancho - 1) + f"{X}")

# =========================================================
# SELECT INTERVALO
# =========================================================

def seleccionar_intervalo():
    while True:
        try:
            op = int(input(f"{G}➔ Selecciona una opción:{X} "))
            if op in INTERVALOS:
                return INTERVALOS[op]
        except:
            pass
        print(f"{R}[!] Opción inválida.{X}")

# =========================================================
# CONFIG TOR
# =========================================================

def configurar_tor(codigo, puerto):
    config = f"""
SocksPort {puerto}
ControlPort 9051
CookieAuthentication 1

ExitNodes {codigo}
StrictNodes 1
MaxCircuitDirtiness 20
NewCircuitPeriod 15
"""
    with open(TORRC, "w") as f:
        f.write(config)

# =========================================================
# RESTART TOR
# =========================================================

def reiniciar_tor():
    print(f"\n{C}[+] Levantando circuitos de TOR...{X}")
    subprocess.run(["systemctl", "restart", "tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10)

# =========================================================
# IP REAL
# =========================================================

def ip_real():
    try:
        ip = subprocess.check_output("curl -s https://ifconfig.me", shell=True)
        return ip.decode().strip()
    except:
        return "ERROR"

# =========================================================
# IP TOR
# =========================================================

def ip_tor(puerto):
    try:
        cmd = f'curl --socks5-hostname 127.0.0.1:{puerto} -s https://ifconfig.me'
        ip = subprocess.check_output(cmd, shell=True)
        return ip.decode().strip()
    except:
        return "ERROR"

# =========================================================
# ROTAR TOR
# =========================================================

def nueva_identidad(puerto):
    vieja = ip_tor(puerto)
    try:
        s = socket.socket()
        s.connect(("127.0.0.1", 9051))
        s.send(b'AUTHENTICATE\r\n')
        s.recv(1024)
        s.send(b'SIGNAL NEWNYM\r\n')
        s.recv(1024)
        s.close()

        print(f"\n{C}[+] Solicitando cambio de circuito. Esperando nueva IP...{X}")
        for _ in range(15):
            time.sleep(1)

        nueva = ip_tor(puerto)
        if nueva != vieja:
            print(f"{G}[✓] ¡IP ROTADA CON ÉXITO!{X}")
            print(f"{Y}[+] Nueva IP Tor:{X} {nueva}")
        else:
            print(f"{Y}[!] TOR reutilizó el circuito anterior. Se reintentará en el próximo ciclo.{X}")

    except KeyboardInterrupt:
        salir(None, None)
    except Exception as e:
        print(f"{R}[!] Error en rotación:{X} {e}")

# =========================================================
# ABRIR NAVEGADOR
# =========================================================

def abrir_navegador(nav, puerto):

    if not nav:
        print(f"{R}[!] Error: Navegador no asignado.{X}")
        return

    usuario_real = os.getenv("SUDO_USER")
    home = os.path.expanduser(f"~{usuario_real}")
    ancho = obtener_ancho()

    if "firefox" in nav:
        try:

            check_proc = subprocess.run(
                ["pgrep", "-u", usuario_real, "-f", "firefox"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if check_proc.returncode == 0:

                print(f"\n{R}╔" + "═" * ancho + "╗")
                print(" ║  [!] ADVERTENCIA: Firefox ya se está ejecutando.".ljust(ancho + 1) + "║")
                print(" ║  Para aplicar Tor correctamente es necesario cerrarlo.".ljust(ancho + 1) + "║")
                print("╚" + "═" * ancho + f"╝{X}")

        except:
            pass

    print(f"\n{G}[+] Abriendo navegador en modo ultra-privado...{X}\n")

    try:

        # FIREFOX
        if "firefox" in nav:

            perfil_temp = os.path.join(
                home,
                ".mozilla/firefox/jefazo.default"
            )

            os.makedirs(
                perfil_temp,
                exist_ok=True
            )

            prefs = os.path.join(
                perfil_temp,
                "user.js"
            )

            with open(prefs, "w") as f:

                f.write("""
user_pref("media.peerconnection.enabled", false);
user_pref("media.peerconnection.ice.default_address_only", true);
user_pref("network.proxy.socks_remote_dns", true);
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.firstparty.isolate", true);
user_pref("network.trr.mode", 5);
""")

            subprocess.Popen([
                "sudo", "-u", usuario_real,
                nav,
                "--new-instance",
                "--profile", perfil_temp,
                "--private-window"
            ],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL)

        # TOR BROWSER
        elif "torbrowser" in nav or "tor-browser" in nav:

            print(f"{Y}[+] Lanzando Tor Browser...{X}")

            subprocess.Popen([
                "sudo",
                "-u",
                usuario_real,
                nav
            ],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL)

        # CHROMIUM
        else:

            proxy = f"socks5://127.0.0.1:{puerto}"

            subprocess.Popen([
                "sudo", "-u", usuario_real,
                nav,
                f"--proxy-server={proxy}",
                "--incognito",
                "--new-window",
                "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
                "--webrtc-ip-handling-policy=disable_non_proxied_udp",
                "--disable-features=WebRtcHideLocalIpsWithMdns",
                "--host-resolver-rules=MAP * ~NOTFOUND , EXCLUDE localhost",
                "--disable-sync",
                "--disable-background-networking",
                "--disable-default-apps",
                "--log-level=3"
            ],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL)

    except Exception as e:

        print(
            f"{R}[!] Error al lanzar el navegador:{X} {e}"
        ) 
               
      

 
def verificar_fuga(puerto):

    real = ip_real()
    tor = ip_tor(puerto)

    if real == tor:
        print(f"{R}[!] ALERTA: TOR NO ESTÁ FUNCIONANDO{X}")

    else:
        print(f"{G}[✓] Proxy SOCKS operativo{X}")
        print(f"{Y}[!] Verifica WebRTC en browserleaks.com/webrtc{X}")

# =========================================================
# =========================================================
# RESUMEN
# =========================================================

def resumen(pais, puerto, intervalo, nav):
    ancho = obtener_ancho()
    print(f"\n{M}╔" + "═" * ancho + "╗")
    print(f"║{'RESUMEN DE CONFIGURACIÓN'.center(ancho)}║")
    print("╚" + "═" * ancho + f"╝{X}")
    print(f" {G}•{X} Países de salida : {W}{pais}{X}")
    print(f" {G}•{X} Puerto Proxificado: {W}{puerto}{X}")
    print(f" {G}•{X} Tiempo de Rotación: {W}{intervalo}{X}")
    print(f" {G}•{X} Navegador Base    : {W}{os.path.basename(nav)}{X}")
    print(f"{M}" + "═" * (ancho + 2) + f"{X}")

# =========================================================
# LOOP
# =========================================================

def ejecutar(nav, pais, puerto, intervalo):
    abrir_navegador(nav, puerto)
    c = 1

    while True:
        ancho = obtener_ancho()
        
        hora = datetime.now().strftime("%H:%M:%S")
        real = ip_real()
        tor = ip_tor(puerto)

        print(f"\n{B}┌" + "─" * ancho + "┐{X}")
        print(f"  [{M}Métricas del Circuito #{c}{X}] ➔ Hora local: {W}{hora}{X}")
        print(f"  {R}» IP REAL DE TU ISP {X} : {W}{real}{X}")
        print(f"  {C}» IP MÁSCARA (TOR)  {X} : {G}{tor}{X}")
        print(f"  {M}» PAÍS DE SALIDA    {X} : {W}{pais}{X}")
        print(f"  {Y}» PUERTO ASIGNADO   {X} : {W}{puerto}{X}")
        print(f"{B}└" + "─" * ancho + f"┘{X}")

        if intervalo != 0:
            for _ in range(intervalo):
                time.sleep(1)
            nueva_identidad(puerto)
        else:
            time.sleep(20)

        c += 1

# =========================================================
# MAIN
# =========================================================

def main():
    verificar_root()
    limpiar()
    banner()
    instalar_dependencias()
    mostrar_paises()
    
    pais, codigo = seleccionar_pais()
    puerto = seleccionar_puerto()
    nav = seleccionar_navegador()

    if not nav:
        print(f"{R}[!] Error crítico: No hay un navegador disponible para usar.{X}")
        sys.exit(1)

    mostrar_intervalos()
    intervalo_txt, intervalo = seleccionar_intervalo()

    resumen(pais, puerto, intervalo_txt, nav)
    input(f"\n{G}➔ Presiona [ENTER] para desplegar la red anónima...{X}")

    configurar_tor(codigo, puerto)
    reiniciar_tor()
    verificar_fuga(puerto)
    ejecutar(nav, pais, puerto, intervalo)

# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()
