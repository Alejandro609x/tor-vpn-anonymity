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

```markdown
![menu](screenshots/menu.png)
```

---

# Advertencia

Esta herramienta fue desarrollada únicamente con fines educativos, privacidad y pruebas de anonimato.

El usuario es responsable del uso que le dé al software.

---

# Mejoras recomendadas

- Validación de conexión TOR
- Detección de fugas DNS
- Verificación automática de servicio TOR
- Configuración separada usando:
  
```bash
/etc/tor/torrc.d/custom.conf
```

- Soporte para proxies encadenados
- Verificación de fingerprint del navegador

---
