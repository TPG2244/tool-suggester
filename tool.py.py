import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import socket
import whois
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def display_banner():
    """Display the tool's banner and author information."""
    print("===============================")
    print("        ADVANCE TOOL SUGGESTER      ")
    print("       AUTHOR: RONAK   ")
    print("===============================")
    print("      ONLY FOR EDUCATIONAL PURPOSE")
    print("===============================\n")

def check_url(url):
    try:
        response = requests.head(url, timeout=7, verify=False, allow_redirects=True)
        return response.status_code < 400
    except requests.exceptions.RequestException:
        return False

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def get_whois_info(domain):
    try:
        domain_info = whois.whois(domain)
        return json.dumps(domain_info, indent=4)
    except Exception:
        return "WHOIS lookup failed."

def suggest_tools():
    tools = {
        "Information Gathering": ["Nmap", "Maltego", "Recon-ng", "theHarvester"],
        "Vulnerability Analysis": ["OpenVAS", "Nikto", "Wapiti"],
        "Web Application Analysis": ["Burp Suite", "OWASP ZAP", "Wpscan"],
        "Password Attacks": ["John the Ripper", "Hashcat", "Hydra"],
        "Exploitation Tools": ["Metasploit", "Armitage", "BeEF"]
    }
    return json.dumps(tools, indent=4)

def analyze_url():
    url = url_entry.get().strip()
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    
    if check_url(url):
        result_text.insert(tk.END, "✅ URL is reachable!\n", "success")
    else:
        result_text.insert(tk.END, "❌ URL is not reachable!\n", "error")
    
    domain = url.replace("https://", "").replace("http://", "").split('/')[0]
    ip = get_ip(domain)
    if ip:
        result_text.insert(tk.END, f"🌐 Resolved IP: {ip}\n", "header")
    
    result_text.insert(tk.END, "📜 WHOIS Info:\n" + get_whois_info(domain) + "\n", "info")
    result_text.insert(tk.END, "🛠 Suggested Tools:\n" + suggest_tools() + "\n", "info")
    
    result_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Cyber Recon Dashboard")
root.geometry("1200x700")
root.resizable(False, False)

# Load and set background image
bg_image = Image.open("background.jpg")  # Change to your image path
bg_image = bg_image.resize((1200, 700), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(relwidth=1, relheight=1)

style = ttk.Style()
style.configure("TButton", font=("Consolas", 12), foreground="lime", background="black")

url_entry = tk.Entry(root, width=50, font=("Consolas", 12), bg="black", fg="lime", insertbackground="lime")
url_entry.pack(pady=10)

analyze_button = ttk.Button(root, text="⚡ Start Analysis", command=analyze_url)
analyze_button.pack(pady=10)

result_text = tk.Text(root, wrap=tk.WORD, width=90, height=50, font=("Consolas", 10), bg="black", fg="lime")
result_text.pack(pady=10)
result_text.config(state=tk.DISABLED)

root.mainloop()
