#!/usr/bin/env python3
"""
Directory Fuzzer - Herramienta para fuzzing de directorios web
Autor: Investigación OSINT
Propósito: Descubrir directorios y archivos ocultos en aplicaciones web

ADVERTENCIA: Esta herramienta debe usarse únicamente en sistemas donde tengas
autorización explícita. El uso no autorizado puede ser ilegal.
"""

import requests
import argparse
import threading
import time
from queue import Queue
from urllib.parse import urljoin
from colorama import init, Fore, Style
import sys
from datetime import datetime

# Inicializar colorama para colores en terminal
init(autoreset=True)

class DirectoryFuzzer:
    def __init__(self, target_url, wordlist_file, threads=10, timeout=5, extensions=None):
        """
        Inicializa el fuzzer de directorios
        
        Args:
            target_url: URL objetivo (ej: http://ejemplo.com)
            wordlist_file: Ruta al archivo wordlist
            threads: Número de hilos para paralelización
            timeout: Timeout para cada petición en segundos
            extensions: Lista de extensiones a probar (ej: ['php', 'html'])
        """
        self.target_url = target_url.rstrip('/')
        self.wordlist_file = wordlist_file
        self.threads = threads
        self.timeout = timeout
        self.extensions = extensions or []
        self.queue = Queue()
        self.results = []
        self.total_requests = 0
        self.found_count = 0
        self.lock = threading.Lock()
        self.start_time = None
        
    def load_wordlist(self):
        """Carga la wordlist desde el archivo"""
        try:
            with open(self.wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip()]
            return words
        except FileNotFoundError:
            print(f"{Fore.RED}[!] Error: No se encontró el archivo {self.wordlist_file}{Style.RESET_ALL}")
            sys.exit(1)
            
    def generate_urls(self, words):
        """Genera URLs a partir de la wordlist y extensiones"""
        urls = []
        for word in words:
            # URL base sin extensión
            urls.append(word)
            # URLs con extensiones
            for ext in self.extensions:
                urls.append(f"{word}.{ext}")
        return urls
        
    def check_url(self, path):
        """Realiza la petición HTTP y analiza la respuesta"""
        url = urljoin(self.target_url + '/', path)
        
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                allow_redirects=False,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            status_code = response.status_code
            content_length = len(response.content)
            
            with self.lock:
                self.total_requests += 1
            
            # Códigos de estado interesantes
            if status_code in [200, 201, 202, 203, 204, 301, 302, 307, 308, 401, 403]:
                result = {
                    'url': url,
                    'status': status_code,
                    'size': content_length,
                    'path': path
                }
                
                with self.lock:
                    self.results.append(result)
                    self.found_count += 1
                
                # Colorear según código de estado
                if status_code == 200:
                    color = Fore.GREEN
                    status_text = f"[200 OK]"
                elif status_code in [301, 302, 307, 308]:
                    color = Fore.YELLOW
                    status_text = f"[{status_code} REDIRECT]"
                elif status_code == 403:
                    color = Fore.CYAN
                    status_text = f"[403 FORBIDDEN]"
                elif status_code == 401:
                    color = Fore.MAGENTA
                    status_text = f"[401 UNAUTHORIZED]"
                else:
                    color = Fore.WHITE
                    status_text = f"[{status_code}]"
                
                print(f"{color}{status_text} {url} ({content_length} bytes){Style.RESET_ALL}")
                
        except requests.exceptions.Timeout:
            pass  # Ignorar timeouts silenciosamente
        except requests.exceptions.ConnectionError:
            pass  # Ignorar errores de conexión
        except Exception as e:
            pass  # Ignorar otros errores
            
    def worker(self):
        """Worker thread que procesa URLs de la cola"""
        while True:
            path = self.queue.get()
            if path is None:
                break
            self.check_url(path)
            self.queue.task_done()
            
    def run(self):
        """Ejecuta el fuzzing"""
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"  Directory Fuzzer - Herramienta de Fuzzing de Directorios")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}[*] Objetivo: {self.target_url}")
        print(f"[*] Wordlist: {self.wordlist_file}")
        print(f"[*] Hilos: {self.threads}")
        print(f"[*] Timeout: {self.timeout}s")
        if self.extensions:
            print(f"[*] Extensiones: {', '.join(self.extensions)}")
        print(f"{Style.RESET_ALL}")
        
        # Cargar wordlist
        words = self.load_wordlist()
        urls = self.generate_urls(words)
        total_urls = len(urls)
        
        print(f"{Fore.YELLOW}[*] Total de URLs a probar: {total_urls}{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}[+] Iniciando fuzzing...{Style.RESET_ALL}\n")
        
        self.start_time = time.time()
        
        # Agregar URLs a la cola
        for url in urls:
            self.queue.put(url)
        
        # Iniciar threads
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        
        # Esperar a que termine la cola
        self.queue.join()
        
        # Detener threads
        for _ in range(self.threads):
            self.queue.put(None)
        for t in threads:
            t.join()
            
        self.show_summary()
        
    def show_summary(self):
        """Muestra el resumen de resultados"""
        elapsed_time = time.time() - self.start_time
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"  Resumen de Resultados")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}[*] Total de peticiones: {self.total_requests}")
        print(f"[*] Directorios/archivos encontrados: {self.found_count}")
        print(f"[*] Tiempo total: {elapsed_time:.2f} segundos")
        print(f"[*] Velocidad: {self.total_requests/elapsed_time:.2f} peticiones/segundo{Style.RESET_ALL}\n")
        
        if self.results:
            print(f"{Fore.GREEN}[+] Recursos encontrados:{Style.RESET_ALL}\n")
            
            # Ordenar por código de estado
            self.results.sort(key=lambda x: x['status'])
            
            for result in self.results:
                print(f"  [{result['status']}] {result['url']} ({result['size']} bytes)")
                
    def save_report(self, output_file):
        """Guarda el reporte en un archivo"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Reporte de Fuzzing de Directorios\n")
                f.write(f"{'='*70}\n\n")
                f.write(f"Objetivo: {self.target_url}\n")
                f.write(f"Wordlist: {self.wordlist_file}\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total de peticiones: {self.total_requests}\n")
                f.write(f"Recursos encontrados: {self.found_count}\n\n")
                
                if self.results:
                    f.write(f"Resultados:\n")
                    f.write(f"{'-'*70}\n\n")
                    
                    for result in self.results:
                        f.write(f"[{result['status']}] {result['url']}\n")
                        f.write(f"  Tamaño: {result['size']} bytes\n\n")
                        
            print(f"\n{Fore.GREEN}[+] Reporte guardado en: {output_file}{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error al guardar reporte: {e}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description='Directory Fuzzer - Herramienta para descubrir directorios y archivos ocultos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Fuzzing básico
  python directory_fuzzer.py -u http://ejemplo.com -w wordlist.txt

  # Con extensiones y más hilos
  python directory_fuzzer.py -u http://ejemplo.com -w wordlist.txt -e php,html,txt -t 20

  # Guardar reporte
  python directory_fuzzer.py -u http://ejemplo.com -w wordlist.txt -o reporte.txt

ADVERTENCIA: Use esta herramienta solo en sistemas donde tenga autorización.
        """
    )
    
    parser.add_argument('-u', '--url', required=True, help='URL objetivo (ej: http://ejemplo.com)')
    parser.add_argument('-w', '--wordlist', required=True, help='Ruta al archivo wordlist')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Número de hilos (default: 10)')
    parser.add_argument('-T', '--timeout', type=int, default=5, help='Timeout en segundos (default: 5)')
    parser.add_argument('-e', '--extensions', help='Extensiones separadas por coma (ej: php,html,txt)')
    parser.add_argument('-o', '--output', help='Archivo de salida para el reporte')
    
    args = parser.parse_args()
    
    # Procesar extensiones
    extensions = []
    if args.extensions:
        extensions = [ext.strip() for ext in args.extensions.split(',')]
    
    # Crear y ejecutar fuzzer
    fuzzer = DirectoryFuzzer(
        target_url=args.url,
        wordlist_file=args.wordlist,
        threads=args.threads,
        timeout=args.timeout,
        extensions=extensions
    )
    
    try:
        fuzzer.run()
        
        # Guardar reporte si se especificó
        if args.output:
            fuzzer.save_report(args.output)
            
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Fuzzing interrumpido por el usuario{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == '__main__':
    main()
