# Directory Fuzzer - Herramienta de Fuzzing de Directorios Web

## 📋 Descripción

Esta herramienta implementa fuzzing de directorios para descubrir rutas ocultas o no documentadas en aplicaciones web. Es útil para pruebas de seguridad, auditorías y reconocimiento dentro de OSINT técnico.

## ⚠️ ADVERTENCIA LEGAL

**Esta herramienta debe usarse ÚNICAMENTE en sistemas donde tengas autorización explícita del propietario.** El uso no autorizado puede ser ilegal y conllevar consecuencias legales graves.

- ✅ Usar en tus propios sistemas
- ✅ Usar con autorización escrita del propietario
- ✅ Usar en entornos de prueba autorizados
- ❌ **NO usar sin permiso**
- ❌ **NO usar contra sitios de terceros sin autorización**

## 🚀 Instalación

### 1. Requisitos previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install requests colorama
```

## 📖 Uso

### Sintaxis básica

```bash
python directory_fuzzer.py -u <URL_OBJETIVO> -w <ARCHIVO_WORDLIST> [OPCIONES]
```

### Parámetros

| Parámetro | Descripción | Obligatorio |
|-----------|-------------|-------------|
| `-u, --url` | URL objetivo (ej: http://ejemplo.com) | ✅ Sí |
| `-w, --wordlist` | Ruta al archivo wordlist | ✅ Sí |
| `-t, --threads` | Número de hilos paralelos (default: 10) | ❌ No |
| `-T, --timeout` | Timeout en segundos (default: 5) | ❌ No |
| `-e, --extensions` | Extensiones separadas por coma (ej: php,html,txt) | ❌ No |
| `-o, --output` | Archivo de salida para guardar el reporte | ❌ No |

### Ejemplos de uso

#### Ejemplo 1: Fuzzing básico

```bash
python directory_fuzzer.py -u http://ejemplo.com -w wordlist.txt
```

#### Ejemplo 2: Con extensiones específicas

```bash
python directory_fuzzer.py -u http://ejemplo.com -w wordlist.txt -e php,html,txt
```

#### Ejemplo 3: Con más hilos para mayor velocidad

```bash
python directory_fuzzer.py -u http://ejemplo.com -w wordlist.txt -t 20
```

#### Ejemplo 4: Guardar reporte en archivo

```bash
python directory_fuzzer.py -u http://ejemplo.com -w wordlist.txt -o reporte_fuzzing.txt
```

#### Ejemplo 5: Configuración completa

```bash
python directory_fuzzer.py -u https://ejemplo.com -w wordlist.txt -e php,html,asp,aspx -t 15 -T 10 -o resultados.txt
```

## 🎯 Códigos de respuesta HTTP

La herramienta muestra diferentes colores según el código de respuesta:

| Código | Color | Significado |
|--------|-------|-------------|
| 200 | 🟢 Verde | Recurso encontrado y accesible |
| 301/302/307/308 | 🟡 Amarillo | Redirección (puede ser interesante) |
| 401 | 🟣 Magenta | No autorizado (recurso existe pero requiere autenticación) |
| 403 | 🔵 Cyan | Prohibido (recurso existe pero acceso denegado) |
| 404 | ⚪ (Oculto) | No encontrado (no se muestra) |

## 📊 Interpretación de resultados

### Resultados interesantes para investigar:

1. **200 OK**: Directorios o archivos totalmente accesibles
2. **403 Forbidden**: Recursos que existen pero están protegidos (posible mala configuración)
3. **401 Unauthorized**: Recursos que requieren autenticación (paneles admin, etc.)
4. **301/302 Redirect**: Pueden indicar recursos movidos o configuraciones interesantes

## 🔍 Wordlists

El repositorio incluye una wordlist básica (`wordlist.txt`) con aproximadamente 200 entradas comunes. Para análisis más exhaustivos, puedes usar wordlists más completas:

### Wordlists populares:

- **SecLists** (GitHub): Colección enorme de wordlists
  - `directory-list-2.3-medium.txt` (~220,000 palabras)
  - `common.txt` (~4,600 palabras)
  
- **DirBuster wordlists**: Incluidas en Kali Linux
  - `/usr/share/wordlists/dirb/common.txt`
  - `/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`

## 💡 Mejores prácticas

### Para realizar fuzzing responsable:

1. **Obtén autorización** siempre antes de escanear
2. **Limita la velocidad** usando menos hilos si el servidor es lento
3. **Respeta robots.txt** del sitio objetivo
4. **Documenta todo** en tu reporte de auditoría
5. **Reporta vulnerabilidades** de forma responsable al propietario

### Optimización de rendimiento:

- Para sitios lentos: usa `-t 5` (menos hilos)
- Para sitios rápidos: usa `-t 20` o más (más hilos)
- Ajusta timeout según latencia: `-T 10` para sitios lentos
- Usa wordlists específicas según el objetivo (PHP, ASP.NET, etc.)

## 📝 Ejemplo de reporte generado

```
Reporte de Fuzzing de Directorios
======================================================================

Objetivo: http://ejemplo.com
Wordlist: wordlist.txt
Fecha: 2025-12-03 07:14:31
Total de peticiones: 450
Recursos encontrados: 12

Resultados:
----------------------------------------------------------------------

[200] http://ejemplo.com/admin
  Tamaño: 1024 bytes

[200] http://ejemplo.com/login
  Tamaño: 2048 bytes

[403] http://ejemplo.com/backup
  Tamaño: 512 bytes
  
...
```

## 🛠️ Características técnicas

- ✅ **Multithreading**: Paralelización para mayor velocidad
- ✅ **Extensiones personalizadas**: Prueba archivos con diferentes extensiones
- ✅ **Códigos coloreados**: Visualización clara de resultados
- ✅ **Generación de reportes**: Exporta resultados a archivo de texto
- ✅ **Manejo de errores**: Ignora timeouts y errores de conexión
- ✅ **User-Agent personalizado**: Simula navegador real
- ✅ **Control de velocidad**: Configurable mediante hilos

## 🎓 Contexto educativo

### ¿Qué es el fuzzing de directorios?

El fuzzing de directorios es una técnica automatizada que consiste en:

1. Probar cientos o miles de nombres de carpetas y archivos en una web
2. Usar una lista de palabras (wordlist) con nombres típicos
3. Analizar las respuestas del servidor para identificar recursos existentes

### Aplicaciones en seguridad:

- 🔍 **Reconocimiento**: Descubrir la estructura de la aplicación
- 🛡️ **Auditoría**: Encontrar archivos expuestos que no deberían estarlo
- 🔐 **Pentesting**: Identificar paneles de administración ocultos
- 📊 **OSINT técnico**: Recopilar información técnica del objetivo

### Herramientas similares:

- **Dirsearch**: Escáner rápido en Python
- **Gobuster**: Escáner en Go, muy rápido
- **FFUF**: Fuzzer flexible y potente
- **DirBuster**: Herramienta clásica de OWASP (Java)
- **Feroxbuster**: Escáner recursivo en Rust

## 📚 Recursos adicionales

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [SecLists Wordlists](https://github.com/danielmiessler/SecLists)
- [Bug Bounty Methodology](https://github.com/jhaddix/tbhm)

## 📄 Licencia

Este script es educativo y debe usarse de forma responsable y legal.

## 👤 Autor

Investigación OSINT - Herramienta educativa para pruebas de seguridad autorizadas

---

**Recuerda**: La seguridad informática requiere ética. Usa estas herramientas solo donde tengas permiso explícito.
