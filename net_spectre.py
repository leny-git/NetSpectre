import socket
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import pyfiglet

console = Console()

def show_banner():
    ascii_banner = pyfiglet.figlet_format("NetSpectre", font="slant")
    console.print(f"[bold cyan]{ascii_banner}[/bold cyan]")
    console.print(Panel.fit("[bold green]NETSPECTRE CORE // Operatör: Leny | Advanced Recon Framework[/bold green]", border_style="cyan"))

def grab_banner(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((target_ip, port))
        banner_data = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        if banner_data:
            return banner_data
    except:
        pass
    return "Servis Kimliği Gizli / Yanıt Yok"

def scan_port(target_ip, port, open_ports):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.8)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        s.close()
    except:
        pass

def main():
    show_banner()
    
    while True:
        console.print("\n[bold red]>>> NETSPECTRE SİSTEMİ AKTİF <<<[/bold red]")
        target_input = console.input("[bold yellow][NETSPECTRE // ?][/bold yellow] Hedef IP gir (Çıkış için 'q'): ").strip()
        
        if target_input.lower() == 'q':
            console.print("[bold cyan]NetSpectre kapatıldı. Görüşürüz Leny![/bold cyan]")
            break
            
        if not target_input:
            continue

        try:
            target_ip = socket.gethostbyname(target_input)
        except socket.gaierror:
            console.print("[bold red][NETSPECTRE // !] Hedef çözümlenemedi Leny![/bold red]")
            continue

        console.print(f"\n[bold blue][NETSPECTRE // *][/bold blue] Hedef kilitlenildi: [bold white]{target_ip}[/bold white]")
        console.print(f"[bold blue][NETSPECTRE // *][/bold blue] Vektör taraması başlatılıyor...\n")

        open_ports = []
        
        with console.status("[bold green]NetSpectre portları yokluyor Leny...", spinner="dots"):
            with ThreadPoolExecutor(max_workers=30) as executor:
                for port in range(1, 1025):
                    executor.submit(scan_port, target_ip, port, open_ports)

        table = Table(title=f"NetSpectre Raporu — {target_ip}")
        table.add_column("Port", style="cyan", justify="center")
        table.add_column("Durum", style="green", justify="center")
        table.add_column("Servis Fingerprint & Banner", style="magenta")

        if open_ports:
            console.print("[bold yellow][NETSPECTRE // *] Açık portlar yakalandı Leny! Banner çekiliyor...[/bold yellow]\n")
            for p in sorted(open_ports):
                service_banner = grab_banner(target_ip, p)
                table.add_row(str(p), "AÇIK", service_banner)
            console.print(table)
        else:
            console.print("[bold red][NETSPECTRE // !] Açık port bulunamadı Leny.[/bold red]")

        console.print("\n[bold cyan]" + "="*40 + "[/bold cyan]")

if __name__ == "__main__":
    main()
