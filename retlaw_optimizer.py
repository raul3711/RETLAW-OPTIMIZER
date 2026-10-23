"""RETLAW OPTIMIZER - Optimizador seguro para jugadores competitivos (Windows 10/11 x64)."""
import os, sys, json, time, shutil, ctypes, tempfile, threading, subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
try:
    import psutil
except ImportError:
    psutil = None
try:
    import winreg
except ImportError:
    winreg = None

APP, VERSION = "RETLAW OPTIMIZER", "1.0"
BG, PANEL, CARD, BLUE, BLUE_DIM, BLUE_HOT = "#070b12", "#0d1420", "#121c2c", "#1e90ff", "#0f4f8f", "#5db3ff"
FG, DIM, OK, WARN, ERR = "#e8f2ff", "#7d8fa8", "#2ecc71", "#f1c40f", "#ff5c5c"
NO_WIN = 0x08000000
DATA_DIR = os.path.join(os.getenv("APPDATA", tempfile.gettempdir()), "RetlawOptimizer")
os.makedirs(DATA_DIR, exist_ok=True)
LOG_FILE = os.path.join(DATA_DIR, "cambios.json")

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception: return False

def sh(cmd, timeout=180):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, creationflags=NO_WIN, timeout=timeout, encoding="utf-8", errors="ignore")
        return (r.stdout or "") + (r.stderr or ""), r.returncode
    except Exception as e:
        return str(e), 1

def ps(script, timeout=180):
    return sh('powershell -NoProfile -ExecutionPolicy Bypass -Command "' + script.replace('"', '\\"') + '"', timeout)

def human(n):
    n = float(n)
    for u in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024: return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} PB"

PROTECTED_PROCS = {"system", "registry", "smss.exe", "csrss.exe", "wininit.exe", "winlogon.exe", "services.exe", "lsass.exe", "svchost.exe", "dwm.exe",
    "explorer.exe", "fontdrvhost.exe", "sihost.exe", "ctfmon.exe", "taskhostw.exe", "runtimebroker.exe", "msmpeng.exe", "nissrv.exe", "securityhealthservice.exe",
    "securityhealthsystray.exe", "mpdefendercoreservice.exe", "easyanticheat.exe", "easyanticheat_eos.exe", "easyanticheat_launcher.exe", "beservice.exe",
    "fortniteclient-win64-shipping.exe", "fortniteclient-win64-shipping_eac.exe", "fortniteclient-win64-shipping_eac_eos.exe", "fortnitelauncher.exe",
    "epicgameslauncher.exe", "epicwebhelper.exe", "audiodg.exe", "spoolsv.exe", "searchindexer.exe", "nvcontainer.exe", "nvdisplay.container.exe", "nvidia share.exe",
    "amdrsserv.exe", "radeonsoftware.exe", "igfxem.exe", "conhost.exe", "wmiprvse.exe", "dllhost.exe", "python.exe", "pythonw.exe", "retlaw_optimizer.exe",
    "applicationframehost.exe", "startmenuexperiencehost.exe", "shellexperiencehost.exe", "textinputhost.exe", "lockapp.exe", "wudfhost.exe", "dashost.exe",
    "memory compression", "idle", "system idle process"}
OPTIONAL_HINTS = {"discord.exe": "Discord", "spotify.exe": "Spotify", "chrome.exe": "Google Chrome", "msedge.exe": "Microsoft Edge", "firefox.exe": "Firefox",
    "opera.exe": "Opera", "brave.exe": "Brave", "onedrive.exe": "OneDrive", "teams.exe": "Teams", "ms-teams.exe": "Teams", "steam.exe": "Steam",
    "steamwebhelper.exe": "Steam Web Helper", "skype.exe": "Skype", "whatsapp.exe": "WhatsApp", "telegram.exe": "Telegram", "slack.exe": "Slack", "zoom.exe": "Zoom",
    "obs64.exe": "OBS Studio", "wallpaper64.exe": "Wallpaper Engine", "wallpaper32.exe": "Wallpaper Engine", "itunes.exe": "iTunes", "ccxprocess.exe": "Adobe Creative Cloud",
    "creative cloud.exe": "Adobe Creative Cloud", "galaxyclient.exe": "GOG Galaxy", "battle.net.exe": "Battle.net", "riotclientservices.exe": "Riot Client",
    "upc.exe": "Ubisoft Connect", "origin.exe": "Origin", "eadesktop.exe": "EA App", "msedgewebview2.exe": "Edge WebView", "widgets.exe": "Widgets de Windows",
    "phoneexperiencehost.exe": "Enlace Movil", "yourphone.exe": "Tu Telefono", "cortana.exe": "Cortana", "searchapp.exe": "Busqueda de Windows (UI)",
    "gamebar.exe": "Xbox Game Bar", "gamebarftserver.exe": "Xbox Game Bar", "xboxpcapp.exe": "Xbox App", "vlc.exe": "VLC", "winrar.exe": "WinRAR",
    "utorrent.exe": "uTorrent", "qbittorrent.exe": "qBittorrent", "logioptionsplus_agent.exe": "Logitech Options+"}
BLOAT_OPTIONAL = {"Microsoft.549981C3F5F10": "Cortana", "Microsoft.BingNews": "Noticias", "Microsoft.BingWeather": "El Tiempo", "Microsoft.BingSearch": "Busqueda Bing",
    "Microsoft.GetHelp": "Obtener ayuda", "Microsoft.Getstarted": "Sugerencias", "Microsoft.MicrosoftOfficeHub": "Office Hub", "Microsoft.MicrosoftSolitaireCollection": "Solitaire",
    "Microsoft.People": "Contactos", "Microsoft.SkypeApp": "Skype", "Microsoft.WindowsFeedbackHub": "Centro de opiniones", "Microsoft.WindowsMaps": "Mapas",
    "Microsoft.ZuneMusic": "Reproductor multimedia", "Microsoft.ZuneVideo": "Peliculas y TV", "Microsoft.YourPhone": "Enlace Movil", "Microsoft.MixedReality.Portal": "Realidad mixta",
    "Microsoft.Microsoft3DViewer": "Visor 3D", "Microsoft.XboxApp": "Xbox (antigua)", "Clipchamp.Clipchamp": "Clipchamp", "Microsoft.Todos": "To Do",
    "Microsoft.PowerAutomateDesktop": "Power Automate", "MicrosoftTeams": "Teams (personal)", "MSTeams": "Teams", "Microsoft.WindowsAlarms": "Alarmas",
    "Microsoft.WindowsSoundRecorder": "Grabadora", "Microsoft.OutlookForWindows": "Outlook (nuevo)", "Microsoft.Windows.DevHome": "Dev Home", "Microsoft.MicrosoftStickyNotes": "Notas rapidas",
    "Microsoft.WindowsCamera": "Camara", "Microsoft.Paint": "Paint", "Microsoft.ScreenSketch": "Recortes", "Microsoft.Windows.Photos": "Fotos", "Microsoft.WindowsCalculator": "Calculadora",
    "Microsoft.Xbox.TCUI": "Xbox TCUI", "Microsoft.XboxGamingOverlay": "Xbox Game Bar", "Microsoft.XboxSpeechToTextOverlay": "Xbox Speech", "Microsoft.GamingApp": "Xbox App",
    "SpotifyAB.SpotifyMusic": "Spotify", "Disney.37853FC22B2CE": "Disney+", "AmazonVideo.PrimeVideo": "Prime Video", "Facebook.Facebook": "Facebook", "Facebook.InstagramBeta": "Instagram",
    "BytedancePte.Ltd.TikTok": "TikTok", "king.com.CandyCrushSaga": "Candy Crush", "king.com.CandyCrushFriends": "Candy Crush Friends", "Microsoft.LinkedIn": "LinkedIn",
    "7EE7776C.LinkedInforWindows": "LinkedIn", "Microsoft.Copilot": "Copilot", "Microsoft.MicrosoftJournal": "Journal", "Microsoft.Whiteboard": "Whiteboard",
    "Microsoft.PowerBI": "Power BI", "Microsoft.Office.OneNote": "OneNote (Store)", "Microsoft.MSPaint": "Paint 3D", "Microsoft.Print3D": "Print 3D", "Microsoft.News": "Noticias",
    "Microsoft.Wallet": "Wallet", "Microsoft.Messaging": "Mensajes", "Microsoft.OneConnect": "Planes moviles", "Microsoft.Office.Sway": "Sway", "Microsoft.RemoteDesktop": "Escritorio remoto",
    "Microsoft.WindowsCommunicationsApps": "Correo y Calendario", "Microsoft.BingFinance": "Finanzas", "Microsoft.BingSports": "Deportes"}
ESSENTIAL_PREFIX = ("Microsoft.VCLibs", "Microsoft.NET", "Microsoft.UI.Xaml", "Microsoft.WindowsStore", "Microsoft.StorePurchaseApp", "Microsoft.DesktopAppInstaller",
    "Microsoft.WindowsTerminal", "Microsoft.SecHealthUI", "Microsoft.Windows.", "Windows.", "Microsoft.AAD", "Microsoft.AccountsControl", "Microsoft.LockApp",
    "Microsoft.Win32WebViewHost", "Microsoft.MicrosoftEdge", "Microsoft.WebMediaExtensions", "Microsoft.HEIFImageExtension", "Microsoft.VP9VideoExtensions",
    "Microsoft.WebpImageExtension", "Microsoft.HEVCVideoExtension", "Microsoft.RawImageExtension", "Microsoft.AV1VideoExtension", "Microsoft.Services.Store.Engagement",
    "Microsoft.WindowsNotepad", "Microsoft.XboxGameCallableUI", "Microsoft.XboxIdentityProvider", "Microsoft.ECApp", "Microsoft.CredDialogHost", "Microsoft.BioEnrollment",
    "Microsoft.AsyncTextService", "NVIDIACorp", "AdvancedMicroDevicesInc", "RealtekSemiconductorCorp", "DolbyLaboratories", "MicrosoftWindows.Client",
    "Microsoft.ApplicationCompatibilityEnhancements", "Microsoft.WidgetsPlatformRuntime", "Microsoft.StartExperiencesApp")
ESSENTIAL_WIN32 = ["visual c++", "redistributable", ".net", "directx", "nvidia", "amd ", "radeon", "intel", "realtek", "driver", "windows sdk", "edge", "webview",
    "easy anti", "battleye", "epic games launcher", "update for windows", "defender", "security"]
OPTIONAL_WIN32 = ["mcafee", "norton", "trial", "toolbar", "candy", "booking", "wildtangent", "wild tangent", "avast", "avg ", "ccleaner", "driver booster", "pc accelerate",
    "web companion", "bytefence", "express vpn", "lenovo vantage", "hp jumpstart", "dell digital delivery", "asus giftbox", "acer collection"]
CRITICAL_STARTUP = ("securityhealth", "defender", "msmpeng", "nvidia", "amd", "realtek", "intel", "rtkaudio", "synaptics", "elan", "igfx", "audio", "ctfmon")

class ChangeLog:
    def __init__(self):
        self.items = []
        try:
            if os.path.exists(LOG_FILE): self.items = json.load(open(LOG_FILE, encoding="utf-8"))
        except Exception: self.items = []
    def add(self, kind, desc, restore):
        self.items.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "kind": kind, "desc": desc, "restore": restore, "restored": False}); self.save()
    def save(self):
        try: json.dump(self.items, open(LOG_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        except Exception: pass

class HoverButton(tk.Button):
    def __init__(self, master, accent=False, **kw):
        base = BLUE if accent else CARD
        super().__init__(master, bg=base, fg="#03101f" if accent else FG, activebackground=BLUE_HOT if accent else BLUE_DIM, activeforeground="#03101f" if accent else "white",
                         relief="flat", bd=0, cursor="hand2", font=("Segoe UI Semibold", 10), padx=16, pady=9, highlightthickness=1, highlightbackground=BLUE if accent else "#1e2d44", **kw)
        self._base, self._hover = base, (BLUE_HOT if accent else "#1a2a42")
        self.bind("<Enter>", lambda e: self._fade(self._hover)); self.bind("<Leave>", lambda e: self._fade(self._base))
    def _fade(self, target, step=0):
        if step > 4: self.config(bg=target); return
        try:
            cur, tgt = self.winfo_rgb(self["bg"]), self.winfo_rgb(target)
            mix = tuple(int(c + (t - c) * 0.45) // 256 for c, t in zip(cur, tgt))
            self.config(bg="#%02x%02x%02x" % mix); self.after(15, lambda: self._fade(target, step + 1))
        except Exception: pass

class Gauge(tk.Canvas):
    def __init__(self, master, title, size=120):
        super().__init__(master, width=size, height=size + 26, bg=BG, highlightthickness=0)
        self.size, self.title, self.val, self.shown, self.text = size, title, 0.0, 0.0, ""
        self.draw()
    def set(self, v, text=""):
        self.val, self.text = max(0, min(100, v)), text; self.animate()
    def animate(self):
        if abs(self.shown - self.val) < 0.6: self.shown = self.val
        else: self.shown += (self.val - self.shown) * 0.3; self.after(30, self.animate)
        self.draw()
    def draw(self):
        self.delete("all"); s, m = self.size, 10
        self.create_oval(m, m, s - m, s - m, outline="#15223a", width=10)
        col = BLUE if self.shown < 70 else WARN if self.shown < 90 else ERR
        self.create_arc(m, m, s - m, s - m, start=90, extent=-3.6 * self.shown, style="arc", outline=col, width=10)
        self.create_text(s / 2, s / 2 - 6, text=f"{self.shown:.0f}%", fill=FG, font=("Segoe UI Black", 18))
        self.create_text(s / 2, s / 2 + 16, text=self.text, fill=DIM, font=("Segoe UI", 8))
        self.create_text(s / 2, s + 10, text=self.title, fill=BLUE, font=("Segoe UI Semibold", 10))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP); self.configure(bg=BG); self.geometry("1120x700"); self.minsize(940, 620)
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1); self.tk.call("tk", "scaling", self.winfo_fpixels("1i") / 72.0)
        except Exception: pass
        self.changelog = ChangeLog(); self.scan = {}; self.bloat_rows = []; self.proc_rows = []; self.startup_rows = []; self.running = True
        self._style(); self._build()
        if psutil: threading.Thread(target=self._monitor_loop, daemon=True).start()
        self.protocol("WM_DELETE_WINDOW", self._quit)
        self.after(600, lambda: self.toast("Bienvenido a RETLAW OPTIMIZER" if is_admin() else "Sin permisos de administrador: algunas funciones estaran limitadas", OK if is_admin() else WARN))

    def _quit(self): self.running = False; self.destroy()

    def _style(self):
        s = ttk.Style(self); s.theme_use("clam")
        s.configure("TProgressbar", troughcolor="#15223a", background=BLUE, bordercolor="#15223a", lightcolor=BLUE, darkcolor=BLUE, thickness=10)
        s.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=FG, rowheight=26, font=("Segoe UI", 10), borderwidth=0)
        s.configure("Treeview.Heading", background=PANEL, foreground=BLUE, font=("Segoe UI Semibold", 10), relief="flat")
        s.map("Treeview", background=[("selected", BLUE_DIM)], foreground=[("selected", "white")])
        s.configure("Card.TCheckbutton", background=CARD, foreground=FG, font=("Segoe UI", 10)); s.map("Card.TCheckbutton", background=[("active", CARD)])
        s.configure("Vertical.TScrollbar", background=CARD, troughcolor=BG, arrowcolor=BLUE, bordercolor=BG)

    def _build(self):
        side = tk.Frame(self, bg=PANEL, width=232); side.pack(side="left", fill="y"); side.pack_propagate(False)
        head = tk.Frame(side, bg=PANEL); head.pack(fill="x", pady=(18, 6), padx=14)
        self.logo_lbl = tk.Label(head, text="⬢", bg=PANEL, fg=BLUE, font=("Segoe UI", 34), cursor="hand2"); self.logo_lbl.pack(side="left")
        self.logo_lbl.bind("<Button-1>", lambda e: self.pick_logo())
        tt = tk.Frame(head, bg=PANEL); tt.pack(side="left", padx=8)
        tk.Label(tt, text="RETLAW", bg=PANEL, fg=FG, font=("Impact", 20)).pack(anchor="w")
        tk.Label(tt, text="OPTIMIZER", bg=PANEL, fg=BLUE, font=("Impact", 13)).pack(anchor="w")
        tk.Label(side, text="clic en el logo para cambiarlo", bg=PANEL, fg=DIM, font=("Segoe UI", 8)).pack()
        self._load_logo()
        tk.Frame(side, bg=BLUE, height=2).pack(fill="x", padx=18, pady=12)
        self.pages, self.navs = {}, {}
        for icon, name in [("⌂", "Inicio"), ("🧹", "Limpieza"), ("📦", "Bloatware"), ("🎮", "Modo Competitivo"), ("📊", "Monitor"), ("🚀", "Inicio de Windows"), ("↩", "Restauracion")]:
            b = tk.Button(side, text=f"  {icon}   {name}", anchor="w", command=lambda n=name: self.show(n), bg=PANEL, fg=FG, activebackground=BLUE_DIM,
                          activeforeground="white", relief="flat", bd=0, font=("Segoe UI", 11), padx=16, pady=10, cursor="hand2")
            b.pack(fill="x"); self.navs[name] = b
            b.bind("<Enter>", lambda e, b=b: b.config(bg="#15213a") if b["bg"] != BLUE_DIM else None)
            b.bind("<Leave>", lambda e, b=b: b.config(bg=PANEL) if b["bg"] != BLUE_DIM else None)
        tk.Label(side, text=f"v{VERSION} - Windows 10/11 x64\n{'Administrador' if is_admin() else 'Usuario estandar'}", bg=PANEL, fg=DIM, font=("Segoe UI", 8), justify="center").pack(side="bottom", pady=12)
        main = tk.Frame(self, bg=BG); main.pack(side="left", fill="both", expand=True)
        self.content = tk.Frame(main, bg=BG); self.content.pack(fill="both", expand=True, padx=22, pady=(18, 4))
        self.toast_lbl = tk.Label(main, text="", bg=BG, fg=FG, font=("Segoe UI Semibold", 10), anchor="w", padx=12, pady=6); self.toast_lbl.pack(fill="x", padx=22)
        logf = tk.Frame(main, bg=PANEL); logf.pack(fill="x", padx=22, pady=(4, 14))
        tk.Label(logf, text="ACTIVIDAD", bg=PANEL, fg=BLUE, font=("Segoe UI Semibold", 8)).pack(anchor="w", padx=10, pady=(5, 0))
        self.logbox = tk.Text(logf, height=5, bg="#05080e", fg="#9cd2ff", relief="flat", font=("Consolas", 9), state="disabled"); self.logbox.pack(fill="x", padx=10, pady=(2, 8))
        self._home(); self._clean(); self._bloat(); self._game(); self._monitor(); self._startup(); self._restore()
        self.show("Inicio")

    def page(self, name, title, sub):
        f = tk.Frame(self.content, bg=BG); self.pages[name] = f
        tk.Label(f, text=title, bg=BG, fg=FG, font=("Segoe UI Black", 20)).pack(anchor="w")
        tk.Label(f, text=sub, bg=BG, fg=DIM, font=("Segoe UI", 10), wraplength=820, justify="left").pack(anchor="w", pady=(0, 12))
        return f

    def show(self, name):
        for n, f in self.pages.items(): f.pack_forget(); self.navs[n].config(bg=PANEL, fg=FG)
        self.navs[name].config(bg=BLUE_DIM, fg="white"); self.pages[name].pack(fill="both", expand=True)
        if name == "Inicio de Windows" and not self.startup_rows: self.task(self.scan_startup)
        if name == "Restauracion": self.refresh_restore()

    def tree(self, parent, cols, widths, height=12, mode="extended"):
        wrap = tk.Frame(parent, bg=BG); wrap.pack(fill="both", expand=True)
        t = ttk.Treeview(wrap, columns=cols, show="headings", height=height, selectmode=mode)
        for c, w in zip(cols, widths): t.heading(c, text=c); t.column(c, width=w, anchor="w", stretch=True)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=t.yview); t.configure(yscrollcommand=sb.set)
        t.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        for tag, col in [("ok", OK), ("warn", WARN), ("err", ERR), ("dim", DIM)]: t.tag_configure(tag, foreground=col)
        return t

    def log(self, msg):
        def _():
            self.logbox.config(state="normal"); self.logbox.insert("end", time.strftime("[%H:%M:%S] ") + msg + "\n"); self.logbox.see("end"); self.logbox.config(state="disabled")
        self.after(0, _)
    def toast(self, msg, color=BLUE):
        def _():
            self.toast_lbl.config(text="●  " + msg, fg=color, bg="#0c1a2b"); self.after(4500, lambda: self.toast_lbl.config(text="", bg=BG))
        self.after(0, _)
    def task(self, fn, *a): threading.Thread(target=fn, args=a, daemon=True).start()
    def ask(self, title, msg): return messagebox.askyesno(title, msg, icon="warning", parent=self)
    def need_admin(self):
        if is_admin(): return True
        self.toast("Esta accion necesita ejecutar la app como administrador (clic derecho > Ejecutar como administrador).", ERR); return False

    def _load_logo(self):
        base = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
        for p in [os.path.join(DATA_DIR, "logo.png"), os.path.join(base, "logo.png")]:
            if os.path.exists(p):
                try:
                    img = tk.PhotoImage(file=p); w = img.width()
                    if w > 64: img = img.subsample(max(1, round(w / 56)))
                    self._logo = img; self.logo_lbl.config(image=img, text=""); return
                except Exception: pass
    def pick_logo(self):
        p = filedialog.askopenfilename(title="Elige tu logo (PNG)", filetypes=[("PNG", "*.png")])
        if p: shutil.copy(p, os.path.join(DATA_DIR, "logo.png")); self._load_logo(); self.toast("Logo actualizado", OK)

    # ---------------- INICIO ----------------
    def _home(self):
        f = self.page("Inicio", "Panel principal", "Optimizacion segura, reversible y con confirmacion en cada cambio")
        g = tk.Frame(f, bg=BG); g.pack(fill="x")
        self.g_cpu, self.g_ram, self.g_disk = Gauge(g, "CPU"), Gauge(g, "RAM"), Gauge(g, "DISCO")
        for i, w in enumerate([self.g_cpu, self.g_ram, self.g_disk]): w.grid(row=0, column=i, padx=14)
        info = tk.Frame(g, bg=CARD, highlightthickness=1, highlightbackground="#1e2d44"); info.grid(row=0, column=3, sticky="nsew", padx=14); g.columnconfigure(3, weight=1)
        self.sys_lbl = tk.Label(info, text="Leyendo informacion del sistema...", bg=CARD, fg=FG, font=("Consolas", 9), justify="left", anchor="nw"); self.sys_lbl.pack(fill="both", expand=True, padx=12, pady=10)
        self.task(self._sysinfo)
        cards = tk.Frame(f, bg=BG); cards.pack(fill="both", expand=True, pady=16)
        for i, (t, s, name) in enumerate([("🧹  Analizar limpieza", "Calcula cuanto espacio puedes recuperar", "Limpieza"), ("📦  Revisar bloatware", "Apps opcionales vs componentes esenciales", "Bloatware"),
                                           ("🎮  Preparar Fortnite", "Cierra lo que elijas y aplica el perfil seguro", "Modo Competitivo"), ("🚀  Inicio de Windows", "Controla que arranca con el PC", "Inicio de Windows")]):
            c = tk.Frame(cards, bg=CARD, highlightthickness=1, highlightbackground="#1e2d44"); c.grid(row=i // 2, column=i % 2, sticky="nsew", padx=6, pady=6)
            cards.columnconfigure(i % 2, weight=1); cards.rowconfigure(i // 2, weight=1)
            tk.Label(c, text=t, bg=CARD, fg=FG, font=("Segoe UI Semibold", 12)).pack(anchor="w", padx=14, pady=(12, 0))
            tk.Label(c, text=s, bg=CARD, fg=DIM, font=("Segoe UI", 9)).pack(anchor="w", padx=14)
            HoverButton(c, text="ABRIR", command=lambda n=name: self.show(n), accent=True).pack(anchor="e", padx=14, pady=10)

    def _sysinfo(self):
        out, _ = ps("(Get-CimInstance Win32_Processor).Name; (Get-CimInstance Win32_VideoController | Select -First 1).Name; (Get-CimInstance Win32_OperatingSystem).Caption")
        parts = [l.strip() for l in out.splitlines() if l.strip()]; lines = []
        if len(parts) >= 3: lines += ["CPU : " + parts[0], "GPU : " + parts[1], "SO  : " + parts[2]]
        if psutil: lines.append("RAM : " + human(psutil.virtual_memory().total))
        lines.append("Perm: " + ("Administrador" if is_admin() else "Usuario estandar"))
        self.after(0, lambda: self.sys_lbl.config(text="\n".join(lines)))

    # ---------------- LIMPIEZA ----------------
    def _clean(self):
        f = self.page("Limpieza", "Limpieza de archivos temporales", "Primero analiza, luego elige que limpiar. Nunca toca documentos personales ni archivos en uso.")
        local = os.getenv("LOCALAPPDATA", ""); win = os.getenv("WINDIR", "C:/Windows"); pdata = os.getenv("PROGRAMDATA", "C:/ProgramData")
        j = os.path.join
        self.clean_cats = {
            "Temporales de usuario (%TEMP%)": [tempfile.gettempdir()],
            "Temporales de Windows": [j(win, "Temp")],
            "Cache de Windows Update (descargas ya instaladas)": [j(win, "SoftwareDistribution", "Download")],
            "Prefetch (se regenera solo)": [j(win, "Prefetch")],
            "Cache de miniaturas del Explorador": [j(local, "Microsoft", "Windows", "Explorer")],
            "Cache de shaders DirectX / NVIDIA / AMD": [j(local, "D3DSCache"), j(local, "NVIDIA", "DXCache"), j(local, "NVIDIA", "GLCache"), j(local, "AMD", "DxCache"), j(local, "AMD", "GLCache")],
            "Logs y cache web de Fortnite / Epic": [j(local, "FortniteGame", "Saved", "Logs"), j(local, "FortniteGame", "Saved", "webcache"), j(local, "FortniteGame", "Saved", "webcache_4430"), j(local, "EpicGamesLauncher", "Saved", "Logs"), j(local, "EpicGamesLauncher", "Saved", "webcache")],
            "Informes de errores de Windows (WER)": [j(local, "Microsoft", "Windows", "WER"), j(pdata, "Microsoft", "Windows", "WER")],
            "Papelera de reciclaje": ["<recycle>"], "Cache DNS": ["<dns>"]}
        self.clean_tree = self.tree(f, ("Categoria", "Archivos", "Espacio recuperable", "Estado"), (380, 90, 150, 220), height=10)
        for k in self.clean_cats: self.clean_tree.insert("", "end", iid=k, values=(k, "-", "-", "sin analizar"))
        r = tk.Frame(f, bg=BG); r.pack(fill="x", pady=10)
        HoverButton(r, text="🔍  ANALIZAR", command=lambda: self.task(self.analyze_clean)).pack(side="left")
        HoverButton(r, text="🧹  LIMPIAR SELECCIONADOS", command=self.confirm_clean, accent=True).pack(side="left", padx=8)
        self.clean_total = tk.Label(r, text="", bg=BG, fg=BLUE, font=("Segoe UI Semibold", 11)); self.clean_total.pack(side="left", padx=12)
        self.clean_bar = ttk.Progressbar(f, mode="determinate"); self.clean_bar.pack(fill="x")
        tk.Label(f, text="Selecciona filas con clic (Ctrl para varias). Solo se eliminan temporales con mas de 1 hora; los archivos en uso se omiten.", bg=BG, fg=DIM, font=("Segoe UI", 8)).pack(anchor="w", pady=4)

    def _iter_files(self, path):
        now = time.time()
        for root, dirs, files in os.walk(path):
            for n in files:
                p = os.path.join(root, n)
                try:
                    st = os.stat(p)
                    if "Explorer" in root and not n.lower().startswith(("thumbcache", "iconcache")): continue
                    if now - st.st_mtime < 3600: continue
                    yield p, st.st_size
                except Exception: continue

    def analyze_clean(self):
        self.scan = {}; total = 0; n = len(self.clean_cats)
        for i, (k, paths) in enumerate(self.clean_cats.items()):
            files, size = [], 0
            if paths == ["<recycle>"]:
                out, _ = ps("(New-Object -ComObject Shell.Application).NameSpace(10).Items() | Measure-Object -Property Size -Sum | Select -Expand Sum")
                try: size = int(float(out.strip() or 0))
                except Exception: size = 0
                files = ["<recycle>"] if size else []
            elif paths == ["<dns>"]: files = ["<dns>"]
            else:
                for p in paths:
                    if os.path.isdir(p):
                        for fp, s in self._iter_files(p): files.append(fp); size += s
            self.scan[k] = (files, size); total += size
            special = bool(files) and files[0].startswith("<")
            self.after(0, lambda k=k, f=files, s=size, sp=special, i=i: (self.clean_tree.item(k, values=(k, "-" if sp or not f else len(f), human(s) if s else "-", "listo" if f else "nada que limpiar"), tags=("ok" if f else "dim",)), self.clean_bar.config(value=(i + 1) * 100 / n)))
        self.after(0, lambda: self.clean_total.config(text="Recuperable: " + human(total)))
        self.after(0, lambda: [self.clean_tree.selection_add(k) for k, (f, s) in self.scan.items() if f])
        self.toast("Analisis completo: " + human(total) + " recuperables", OK); self.log("Analisis de limpieza: " + human(total) + " recuperables.")

    def confirm_clean(self):
        if not self.scan: self.toast("Primero pulsa ANALIZAR", WARN); return
        sel = [k for k in self.clean_tree.selection() if self.scan.get(k, ([], 0))[0]]
        if not sel: self.toast("No hay categorias seleccionadas con contenido", WARN); return
        size = sum(self.scan[k][1] for k in sel)
        if self.ask("Confirmar limpieza", f"Se eliminaran archivos temporales de {len(sel)} categorias ({human(size)}).\n\nNo se tocan documentos personales. Continuar?"):
            self.task(self.do_clean, sel)

    def do_clean(self, sel):
        freed, errors, n = 0, 0, len(sel)
        for i, k in enumerate(sel):
            files, size = self.scan[k]; done = err = 0
            if files == ["<recycle>"]:
                _, rc = ps("Clear-RecycleBin -Force -ErrorAction Stop")
                if rc == 0: done, freed = 1, freed + size
                else: err = 1
            elif files == ["<dns>"]: sh("ipconfig /flushdns"); done = 1
            else:
                for fp in files:
                    try: s = os.path.getsize(fp); os.remove(fp); freed += s; done += 1
                    except Exception: err += 1
                for p in self.clean_cats[k]:
                    for root, dirs, _f in os.walk(p, topdown=False):
                        for d in dirs:
                            try: os.rmdir(os.path.join(root, d))
                            except Exception: pass
            errors += err
            self.after(0, lambda k=k, d=done, e=err, i=i: (self.clean_tree.item(k, values=(k, "-", "-", f"limpiado ({d})" + (f" - {e} en uso/omitidos" if e else "")), tags=("warn" if e else "ok",)), self.clean_bar.config(value=(i + 1) * 100 / n)))
        self.scan = {}
        self.changelog.add("limpieza", f"Limpieza de {n} categorias, {human(freed)} liberados", None)
        self.after(0, lambda: self.clean_total.config(text="Liberado: " + human(freed)))
        self.toast("Limpieza terminada: " + human(freed) + " liberados" + (f", {errors} archivos omitidos por estar en uso" if errors else ""), OK)

    # ---------------- BLOATWARE ----------------
    def _bloat(self):
        f = self.page("Bloatware", "Analisis de bloatware", "Las apps marcadas como ESENCIAL no se pueden desinstalar desde aqui. Nada se desinstala sin tu confirmacion.")
        r = tk.Frame(f, bg=BG); r.pack(fill="x", pady=(0, 8))
        HoverButton(r, text="🔍  ANALIZAR APPS", command=lambda: self.task(self.scan_bloat)).pack(side="left")
        HoverButton(r, text="🗑  DESINSTALAR SELECCIONADAS", command=self.confirm_bloat, accent=True).pack(side="left", padx=8)
        self.bloat_filter = tk.StringVar(value="opcional")
        for v, t in [("opcional", "Solo opcionales"), ("todas", "Todas")]:
            tk.Radiobutton(r, text=t, variable=self.bloat_filter, value=v, command=self.render_bloat, bg=BG, fg=FG, selectcolor=CARD, activebackground=BG, activeforeground=FG, font=("Segoe UI", 9)).pack(side="left", padx=6)
        self.bloat_tree = self.tree(f, ("Aplicacion", "Paquete / Editor", "Tipo", "Clasificacion"), (240, 330, 90, 160), height=14)

    def scan_bloat(self):
        self.toast("Analizando aplicaciones instaladas..."); rows = []
        out, _ = ps("Get-AppxPackage | Where-Object {-not $_.IsFramework} | Select-Object Name | ConvertTo-Json -Compress")
        try: data = json.loads(out.strip() or "[]"); data = data if isinstance(data, list) else [data]
        except Exception: data = []
        for d in data:
            name = d.get("Name", "")
            if name in BLOAT_OPTIONAL: rows.append((BLOAT_OPTIONAL[name], name, "Store", "OPCIONAL", name))
            elif name.startswith(ESSENTIAL_PREFIX): rows.append((name.split(".")[-1], name, "Store", "ESENCIAL", ""))
            else: rows.append((name.split(".")[-1], name, "Store", "REVISAR (terceros)", name))
        out, _ = ps("Get-ItemProperty HKLM:/Software/Microsoft/Windows/CurrentVersion/Uninstall/*, HKLM:/Software/Wow6432Node/Microsoft/Windows/CurrentVersion/Uninstall/*, HKCU:/Software/Microsoft/Windows/CurrentVersion/Uninstall/* -ErrorAction SilentlyContinue | Where-Object {$_.DisplayName -and -not $_.SystemComponent -and $_.UninstallString} | Select-Object DisplayName,Publisher,UninstallString | ConvertTo-Json -Compress")
        try: data = json.loads(out.strip() or "[]"); data = data if isinstance(data, list) else [data]
        except Exception: data = []
        for d in data:
            dn = d.get("DisplayName") or ""; pub = d.get("Publisher") or ""; low = (dn + " " + pub).lower()
            cls = "ESENCIAL" if any(x in low for x in ESSENTIAL_WIN32) else ("OPCIONAL" if any(x in low for x in OPTIONAL_WIN32) else "REVISAR (instalado)")
            rows.append((dn, pub[:40], "Win32", cls, d.get("UninstallString") or ""))
        self.bloat_rows = sorted(rows, key=lambda r: (r[3] != "OPCIONAL", r[3], r[0].lower()))
        self.after(0, self.render_bloat)
        self.log(f"Bloatware: {sum(1 for r in rows if r[3] == 'OPCIONAL')} opcionales, {sum(1 for r in rows if r[3] == 'ESENCIAL')} esenciales, {len(rows)} en total.")
        self.toast("Analisis de apps completado", OK)

    def render_bloat(self):
        self.bloat_tree.delete(*self.bloat_tree.get_children())
        for i, r in enumerate(self.bloat_rows):
            if self.bloat_filter.get() == "opcional" and r[3] != "OPCIONAL": continue
            self.bloat_tree.insert("", "end", iid=str(i), values=r[:4], tags=("ok" if r[3] == "OPCIONAL" else "err" if r[3] == "ESENCIAL" else "warn",))

    def confirm_bloat(self):
        sel = [self.bloat_rows[int(i)] for i in self.bloat_tree.selection()]
        if not sel: self.toast("Selecciona al menos una aplicacion", WARN); return
        if any(r[3] == "ESENCIAL" for r in sel): self.toast("Hay elementos ESENCIALES seleccionados; no se pueden desinstalar desde aqui.", ERR); return
        names = "\n".join("- " + r[0] for r in sel[:15]) + ("\n..." if len(sel) > 15 else "")
        if self.ask("Confirmar desinstalacion", f"Vas a desinstalar {len(sel)} aplicaciones:\n\n{names}\n\nLas apps Win32 abriran su propio desinstalador. Continuar?"):
            self.task(self.do_bloat, sel)

    def do_bloat(self, sel):
        for r in sel:
            if r[2] == "Store":
                out, rc = ps("Get-AppxPackage -Name '" + r[4] + "' | Remove-AppxPackage -ErrorAction Stop")
                self.log(("Desinstalado: " if rc == 0 else "Error al desinstalar: ") + r[0] + ("" if rc == 0 else " - " + out.strip()[:120]))
            else:
                cmd = r[4]
                if cmd.lower().startswith("msiexec"): cmd = cmd.replace("/I", "/X").replace("/i", "/x") + " /passive"
                try: subprocess.Popen(cmd, shell=True); self.log("Desinstalador abierto: " + r[0])
                except Exception as e: self.log(f"No se pudo abrir el desinstalador de {r[0]}: {e}")
            self.changelog.add("bloatware", f"Desinstalado {r[0]} ({r[1]})", None)
        self.toast("Desinstalacion finalizada. Vuelve a analizar para actualizar la lista.", OK)

    # ---------------- MODO COMPETITIVO ----------------
    def _game(self):
        f = self.page("Modo Competitivo", "Modo Competitivo Fortnite", "Cierra solo lo que tu elijas y aplica un perfil seguro y reversible. Defender, drivers, Easy Anti-Cheat y Fortnite nunca se tocan.")
        top = tk.Frame(f, bg=BG); top.pack(fill="both", expand=True)
        left = tk.Frame(top, bg=BG); left.pack(side="left", fill="both", expand=True)
        tk.Label(left, text="Aplicaciones opcionales en ejecucion (consumo actual)", bg=BG, fg=BLUE, font=("Segoe UI Semibold", 10)).pack(anchor="w")
        self.proc_tree = self.tree(left, ("Aplicacion", "Proceso", "RAM", "CPU %", "Instancias"), (170, 180, 90, 70, 70), height=11)
        r = tk.Frame(left, bg=BG); r.pack(fill="x", pady=8)
        HoverButton(r, text="🔍  ANALIZAR CONSUMO", command=lambda: self.task(self.scan_procs)).pack(side="left")
        HoverButton(r, text="✖  CERRAR SELECCIONADAS", command=self.confirm_close, accent=True).pack(side="left", padx=8)
        right = tk.Frame(top, bg=CARD, highlightthickness=1, highlightbackground="#1e2d44", width=330); right.pack(side="left", fill="y", padx=(16, 0)); right.pack_propagate(False)
        tk.Label(right, text="PERFIL DE PREPARACION", bg=CARD, fg=BLUE, font=("Segoe UI Semibold", 11)).pack(anchor="w", padx=14, pady=(12, 4))
        tk.Label(right, text="Cambios seguros, registrados y reversibles desde Restauracion:", bg=CARD, fg=DIM, font=("Segoe UI", 9), wraplength=290, justify="left").pack(anchor="w", padx=14)
        self.game_opts = {}
        for k, t in [("power", "Plan de energia: Alto rendimiento"), ("gamemode", "Activar Modo Juego de Windows"), ("dvr", "Desactivar grabacion en segundo plano (Game DVR)"),
                     ("mouse", "Desactivar aceleracion del raton"), ("notif", "Silenciar notificaciones"), ("visual", "Efectos visuales: mejor rendimiento")]:
            v = tk.BooleanVar(value=True); self.game_opts[k] = v
            ttk.Checkbutton(right, text=t, variable=v, style="Card.TCheckbutton").pack(anchor="w", padx=14, pady=2)
        HoverButton(right, text="🎮  APLICAR PERFIL", command=self.confirm_profile, accent=True).pack(fill="x", padx=14, pady=(12, 6))
        HoverButton(right, text="↩  REVERTIR PERFIL", command=lambda: self.task(self.revert_profile)).pack(fill="x", padx=14)
        tk.Label(right, text="Nota honesta: estos ajustes reducen interferencias y estabilizan el rendimiento, pero no garantizan menos ping ni menos input lag. El ping depende de tu conexion.", bg=CARD, fg=DIM, font=("Segoe UI", 8), wraplength=290, justify="left").pack(anchor="w", padx=14, pady=12)

    def scan_procs(self):
        if not psutil: return
        agg = {}
        for p in psutil.process_iter(["pid", "name", "memory_info"]):
            try:
                n = (p.info["name"] or "").lower()
                if not n or n in PROTECTED_PROCS: continue
                p.cpu_percent(None)
                a = agg.setdefault(n, {"pids": [], "ram": 0, "p": []}); a["pids"].append(p.info["pid"]); a["ram"] += p.info["memory_info"].rss if p.info["memory_info"] else 0; a["p"].append(p)
            except Exception: pass
        time.sleep(1.0); rows = []
        for n, d in agg.items():
            cpu = 0.0
            for p in d["p"]:
                try: cpu += p.cpu_percent(None)
                except Exception: pass
            label = OPTIONAL_HINTS.get(n)
            if label or d["ram"] > 150 * 1024 * 1024 or cpu > 5:
                rows.append((label or n.replace(".exe", "").title(), n, d["ram"], cpu, len(d["pids"]), d["pids"], bool(label)))
        rows.sort(key=lambda r: (not r[6], -r[2])); self.proc_rows = rows
        def _():
            self.proc_tree.delete(*self.proc_tree.get_children())
            for i, r in enumerate(rows): self.proc_tree.insert("", "end", iid=str(i), values=(r[0], r[1], human(r[2]), f"{r[3]:.0f}", r[4]), tags=("ok" if r[6] else "warn",))
        self.after(0, _); self.toast(f"{len(rows)} aplicaciones opcionales detectadas (verde = conocidas, amarillo = alto consumo, revisa antes de cerrar)", OK)

    def confirm_close(self):
        sel = [self.proc_rows[int(i)] for i in self.proc_tree.selection()]
        if not sel: self.toast("Selecciona las aplicaciones que quieres cerrar", WARN); return
        if self.ask("Cerrar aplicaciones", "Se cerraran:\n\n" + "\n".join("- " + r[0] for r in sel) + "\n\nGuarda tu trabajo en ellas antes. Continuar?"):
            self.task(self.do_close, sel)

    def do_close(self, sel):
        for r in sel:
            for pid in r[5]:
                try: psutil.Process(pid).terminate()
                except Exception: pass
            self.log("Cerrado: " + r[0])
        self.changelog.add("procesos", f"Cerradas {len(sel)} apps opcionales", None)
        time.sleep(1); self.scan_procs()

    def confirm_profile(self):
        if not any(v.get() for v in self.game_opts.values()): self.toast("No hay opciones marcadas", WARN); return
        if self.ask("Aplicar perfil de preparacion", "Se aplicaran los ajustes marcados. Se guarda el estado anterior para poder revertirlo.\n\nContinuar?"):
            self.task(self.apply_profile)

    def _reg_get(self, root, path, name):
        try:
            with winreg.OpenKey(root, path) as k: return winreg.QueryValueEx(k, name)[0]
        except Exception: return None
    def _reg_set(self, root, path, name, val, typ):
        with winreg.CreateKey(root, path) as k: winreg.SetValueEx(k, name, 0, typ, val)
    def _reg_change(self, label, path, name, val, typ=None):
        root = winreg.HKEY_CURRENT_USER; typ = typ or (winreg.REG_DWORD if isinstance(val, int) else winreg.REG_SZ)
        old = self._reg_get(root, path, name)
        try:
            self._reg_set(root, path, name, val, typ)
            self.changelog.add("registro", label, {"type": "reg", "path": path, "name": name, "old": old, "typ": typ}); self.log("Aplicado: " + label)
        except Exception as e: self.log(f"No se pudo aplicar {label}: {e}")

    def apply_profile(self):
        o = {k: v.get() for k, v in self.game_opts.items()}
        if o["power"]:
            out, _ = sh("powercfg /getactivescheme"); old = out.split(":")[1].split("(")[0].strip() if ":" in out else None
            _, rc = sh("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
            if rc == 0: self.changelog.add("energia", "Plan de energia -> Alto rendimiento", {"type": "power", "old": old}); self.log("Plan de energia: Alto rendimiento.")
            else: self.log("No se pudo cambiar el plan de energia.")
        if o["gamemode"]:
            self._reg_change("Modo Juego activado", r"Software\Microsoft\GameBar", "AutoGameModeEnabled", 1)
            self._reg_change("Modo Juego permitido", r"Software\Microsoft\GameBar", "AllowAutoGameMode", 1)
        if o["dvr"]:
            self._reg_change("Game DVR desactivado", r"System\GameConfigStore", "GameDVR_Enabled", 0)
            self._reg_change("Captura en segundo plano desactivada", r"Software\Microsoft\Windows\CurrentVersion\GameDVR", "AppCaptureEnabled", 0)
        if o["mouse"]:
            for n in ["MouseSpeed", "MouseThreshold1", "MouseThreshold2"]: self._reg_change("Raton " + n + "=0", r"Control Panel\Mouse", n, "0", winreg.REG_SZ)
            try: ctypes.windll.user32.SystemParametersInfoW(0x0071, 0, (ctypes.c_int * 3)(0, 0, 0), 2)
            except Exception: pass
        if o["notif"]: self._reg_change("Notificaciones silenciadas", r"Software\Microsoft\Windows\CurrentVersion\PushNotifications", "ToastEnabled", 0)
        if o["visual"]: self._reg_change("Efectos visuales: rendimiento", r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting", 2)
        self.toast("Perfil de preparacion aplicado. Todo queda registrado en Restauracion.", OK)

    def revert_profile(self):
        n = sum(1 for it in reversed(self.changelog.items) if it["kind"] in ("registro", "energia") and not it["restored"] and self._restore_item(it))
        self.changelog.save(); self.toast(f"Perfil revertido ({n} cambios restaurados)", OK)

    # ---------------- MONITOR ----------------
    def _monitor(self):
        f = self.page("Monitor", "Monitor del PC", "CPU, RAM, disco, red y procesos en tiempo real, sin congelar la interfaz")
        g = tk.Frame(f, bg=BG); g.pack(fill="x")
        self.m_cpu, self.m_ram, self.m_disk = Gauge(g, "CPU", 110), Gauge(g, "RAM", 110), Gauge(g, "DISCO", 110)
        for i, w in enumerate([self.m_cpu, self.m_ram, self.m_disk]): w.grid(row=0, column=i, padx=10)
        self.m_info = tk.Label(g, text="", bg=BG, fg=DIM, font=("Consolas", 9), justify="left"); self.m_info.grid(row=0, column=3, sticky="w", padx=16)
        tk.Label(f, text="Procesos con mayor consumo (rojo = excesivo, gris = protegido)", bg=BG, fg=BLUE, font=("Segoe UI Semibold", 10)).pack(anchor="w", pady=(10, 2))
        self.mon_tree = self.tree(f, ("Proceso", "PID", "RAM", "CPU %", "Estado"), (260, 70, 100, 70, 200), height=10, mode="browse")
        HoverButton(f, text="✖  Finalizar proceso seleccionado", command=self.kill_selected).pack(anchor="w", pady=8)

    def kill_selected(self):
        s = self.mon_tree.selection()
        if not s: return
        v = self.mon_tree.item(s[0])["values"]; name, pid = str(v[0]), int(v[1])
        if name.lower() in PROTECTED_PROCS: self.toast(name + " es un proceso protegido (sistema/seguridad/anti-cheat); no se cierra.", ERR); return
        if self.ask("Finalizar proceso", f"Cerrar {name} (PID {pid})? Perderas los datos no guardados de esa aplicacion."):
            try: psutil.Process(pid).terminate(); self.log("Proceso finalizado: " + name)
            except Exception as e: self.toast(f"No se pudo cerrar: {e}", ERR)

    def _monitor_loop(self):
        for p in psutil.process_iter():
            try: p.cpu_percent(None)
            except Exception: pass
        n_cpu = psutil.cpu_count() or 1; last_net = psutil.net_io_counters(); last_t = time.time()
        while self.running:
            time.sleep(1.5)
            try:
                cpu = psutil.cpu_percent(None); vm = psutil.virtual_memory()
                try: du = psutil.disk_usage(os.getenv("SystemDrive", "C:") + "/")
                except Exception: du = None
                net = psutil.net_io_counters(); dt = max(0.1, time.time() - last_t)
                down, up = (net.bytes_recv - last_net.bytes_recv) / dt, (net.bytes_sent - last_net.bytes_sent) / dt; last_net, last_t = net, time.time()
                procs = []
                for p in psutil.process_iter(["pid", "name", "memory_info"]):
                    try: procs.append((p.info["name"] or "?", p.info["pid"], p.info["memory_info"].rss if p.info["memory_info"] else 0, p.cpu_percent(None) / n_cpu))
                    except Exception: pass
                procs.sort(key=lambda r: r[2] + r[3] * 50 * 1024 * 1024, reverse=True); top = procs[:14]
                def _():
                    for g in (self.g_cpu, self.m_cpu): g.set(cpu, f"{n_cpu} hilos")
                    for g in (self.g_ram, self.m_ram): g.set(vm.percent, human(vm.used) + " / " + human(vm.total))
                    if du:
                        for g in (self.g_disk, self.m_disk): g.set(du.percent, "libre " + human(du.free))
                    self.m_info.config(text=f"Red: {human(down)}/s bajada, {human(up)}/s subida\nProcesos: {len(procs)}\nRAM disponible: {human(vm.available)}")
                    sel = self.mon_tree.selection(); selpid = self.mon_tree.item(sel[0])["values"][1] if sel else None
                    self.mon_tree.delete(*self.mon_tree.get_children())
                    for name, pid, rss, c in top:
                        prot = name.lower() in PROTECTED_PROCS; heavy = rss > 1.5 * 1024 ** 3 or c > 25
                        st = "protegido" if prot else ("consumo excesivo" if heavy else "normal")
                        iid = self.mon_tree.insert("", "end", values=(name, pid, human(rss), f"{c:.0f}", st), tags=("dim" if prot else "err" if heavy else "ok",))
                        if pid == selpid: self.mon_tree.selection_set(iid)
                self.after(0, _)
            except Exception: pass

    # ---------------- INICIO DE WINDOWS ----------------
    def _startup(self):
        f = self.page("Inicio de Windows", "Aplicaciones de inicio", "Desactivar = igual que en el Administrador de tareas. Reversible. Seguridad y drivers se marcan como CRITICO y no se desactivan.")
        self.startup_tree = self.tree(f, ("Aplicacion", "Comando", "Ubicacion", "Estado", "Clasificacion"), (180, 330, 120, 90, 120), height=13)
        r = tk.Frame(f, bg=BG); r.pack(fill="x", pady=8)
        HoverButton(r, text="🔄  ACTUALIZAR", command=lambda: self.task(self.scan_startup)).pack(side="left")
        HoverButton(r, text="⏸  DESACTIVAR SELECCIONADAS", command=lambda: self.confirm_startup(False), accent=True).pack(side="left", padx=8)
        HoverButton(r, text="▶  ACTIVAR SELECCIONADAS", command=lambda: self.confirm_startup(True)).pack(side="left")

    def _sources(self):
        RUN = r"Software\Microsoft\Windows\CurrentVersion\Run"; APPR = r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run"
        return [("HKCU Run", "HKCU", RUN, APPR), ("HKLM Run", "HKLM", RUN, APPR), ("HKLM Run (32)", "HKLM", r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run", APPR + "32")]

    def _hive(self, name): return winreg.HKEY_CURRENT_USER if name == "HKCU" else winreg.HKEY_LOCAL_MACHINE

    def scan_startup(self):
        rows = []
        for label, rootname, runp, appr in self._sources():
            root = self._hive(rootname)
            try:
                with winreg.OpenKey(root, runp) as k:
                    i = 0
                    while True:
                        try: name, val, _ = winreg.EnumValue(k, i); i += 1
                        except OSError: break
                        enabled = True
                        try:
                            with winreg.OpenKey(root, appr) as a:
                                data = winreg.QueryValueEx(a, name)[0]
                                if isinstance(data, bytes) and data: enabled = data[0] % 2 == 0
                        except OSError: pass
                        crit = any(c in (name + " " + str(val)).lower() for c in CRITICAL_STARTUP)
                        rows.append((name, str(val)[:110], label, "activado" if enabled else "desactivado", "CRITICO" if crit else "opcional", rootname, appr))
            except OSError: pass
        for label, folder in [("Carpeta Inicio (usuario)", os.path.join(os.getenv("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")),
                              ("Carpeta Inicio (todos)", os.path.join(os.getenv("PROGRAMDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs", "StartUp"))]:
            if os.path.isdir(folder):
                for n in os.listdir(folder):
                    if n.lower() == "desktop.ini": continue
                    rows.append((n, os.path.join(folder, n), label, "desactivado" if n.lower().endswith(".disabled") else "activado", "opcional", None, folder))
        self.startup_rows = rows
        def _():
            self.startup_tree.delete(*self.startup_tree.get_children())
            for i, r in enumerate(rows): self.startup_tree.insert("", "end", iid=str(i), values=r[:5], tags=("err" if r[4] == "CRITICO" else "ok" if r[3] == "activado" else "dim",))
        self.after(0, _); self.log(f"Inicio de Windows: {len(rows)} entradas.")

    def confirm_startup(self, enable):
        sel = [self.startup_rows[int(i)] for i in self.startup_tree.selection()]
        if not sel: self.toast("Selecciona entradas primero", WARN); return
        if not enable and any(r[4] == "CRITICO" for r in sel): self.toast("Hay entradas CRITICAS seleccionadas (seguridad/drivers); no se desactivan.", ERR); return
        verb = "activar" if enable else "desactivar"
        if self.ask("Confirmar " + verb, verb.capitalize() + " en el inicio de Windows?\n\n" + "\n".join("- " + r[0] for r in sel)):
            self.task(self.do_startup, sel, enable)

    def do_startup(self, sel, enable):
        for r in sel:
            name, rootname, appr = r[0], r[5], r[6]
            try:
                if rootname:
                    if rootname == "HKLM" and not is_admin(): self.log(name + ": requiere administrador."); continue
                    with winreg.CreateKey(self._hive(rootname), appr) as a: winreg.SetValueEx(a, name, 0, winreg.REG_BINARY, bytes([2 if enable else 3]) + bytes(11))
                else:
                    p = r[1]; newp = p[:-9] if (enable and p.lower().endswith(".disabled")) else (p if enable else p + ".disabled")
                    if newp != p: os.rename(p, newp)
                self.changelog.add("inicio", ("Activado" if enable else "Desactivado") + " en inicio: " + name, {"type": "startup", "name": name, "root": rootname, "appr": appr, "was_enabled": not enable, "path": None if rootname else r[1]})
                self.log(("Activado: " if enable else "Desactivado: ") + name)
            except Exception as e: self.log(f"Error con {name}: {e}")
        self.scan_startup(); self.toast("Cambios de inicio aplicados", OK)

    # ---------------- RESTAURACION ----------------
    def _restore(self):
        f = self.page("Restauracion", "Registro de cambios y restauracion", "Todo lo que RETLAW modifica queda aqui. Puedes revertir cada cambio cuando sea tecnicamente posible.")
        r = tk.Frame(f, bg=BG); r.pack(fill="x", pady=(0, 8))
        HoverButton(r, text="🛡  CREAR PUNTO DE RESTAURACION", command=self.confirm_restore_point, accent=True).pack(side="left")
        HoverButton(r, text="↩  REVERTIR SELECCIONADOS", command=self.confirm_revert).pack(side="left", padx=8)
        HoverButton(r, text="↩↩  REVERTIR TODO", command=lambda: self.confirm_revert(True)).pack(side="left")
        HoverButton(r, text="Abrir Restaurar sistema", command=lambda: subprocess.Popen("rstrui.exe", shell=True)).pack(side="left", padx=8)
        self.rest_tree = self.tree(f, ("Fecha", "Tipo", "Cambio", "Reversible", "Estado"), (140, 90, 420, 90, 110), height=14)

    def refresh_restore(self):
        self.rest_tree.delete(*self.rest_tree.get_children())
        for idx in range(len(self.changelog.items) - 1, -1, -1):
            it = self.changelog.items[idx]
            self.rest_tree.insert("", "end", iid=str(idx), values=(it["t"], it["kind"], it["desc"], "si" if it["restore"] else "no", "restaurado" if it["restored"] else "aplicado"), tags=("dim" if it["restored"] or not it["restore"] else "ok",))

    def confirm_restore_point(self):
        if not self.need_admin(): return
        if self.ask("Punto de restauracion", "Se creara un punto de restauracion de Windows llamado 'RETLAW OPTIMIZER'. Puede tardar un minuto. Continuar?"):
            self.task(self.create_restore_point)
    def create_restore_point(self):
        self.toast("Creando punto de restauracion...")
        out, rc = ps("Enable-ComputerRestore -Drive $env:SystemDrive -ErrorAction SilentlyContinue; Checkpoint-Computer -Description 'RETLAW OPTIMIZER' -RestorePointType MODIFY_SETTINGS -ErrorAction Stop", 300)
        if rc == 0 and "error" not in out.lower(): self.log("Punto de restauracion creado."); self.toast("Punto de restauracion creado correctamente", OK)
        else: self.log("Punto de restauracion: " + out.strip()[:200]); self.toast("Windows no permitio crear el punto (Proteccion del sistema desactivada o ya existe uno de hace menos de 24 h)", WARN)

    def _restore_item(self, it):
        r = it.get("restore")
        if not r: return False
        try:
            if r["type"] == "reg":
                root = winreg.HKEY_CURRENT_USER
                if r["old"] is None:
                    with winreg.OpenKey(root, r["path"], 0, winreg.KEY_SET_VALUE) as k: winreg.DeleteValue(k, r["name"])
                else: self._reg_set(root, r["path"], r["name"], r["old"], r["typ"])
            elif r["type"] == "power":
                sh("powercfg /setactive " + (r["old"] or "381b4222-f694-41f0-9685-ff5bb260df2e"))
            elif r["type"] == "startup":
                if r["root"]:
                    with winreg.CreateKey(self._hive(r["root"]), r["appr"]) as a: winreg.SetValueEx(a, r["name"], 0, winreg.REG_BINARY, bytes([2 if r["was_enabled"] else 3]) + bytes(11))
                else:
                    p = r["path"]; cur = p if os.path.exists(p) else p + ".disabled"
                    target = p if r["was_enabled"] else p + ".disabled"
                    if cur != target and os.path.exists(cur): os.rename(cur, target)
            it["restored"] = True; self.log("Restaurado: " + it["desc"]); return True
        except Exception as e: self.log(f"No se pudo restaurar '{it['desc']}': {e}"); return False

    def confirm_revert(self, all_=False):
        items = self.changelog.items if all_ else [self.changelog.items[int(i)] for i in self.rest_tree.selection()]
        items = [it for it in items if it["restore"] and not it["restored"]]
        if not items: self.toast("No hay cambios reversibles seleccionados", WARN); return
        if self.ask("Revertir cambios", f"Se revertiran {len(items)} cambios. Continuar?"):
            def _():
                n = sum(1 for it in reversed(items) if self._restore_item(it)); self.changelog.save(); self.after(0, self.refresh_restore); self.toast(f"{n} cambios revertidos", OK)
            self.task(_)

def main():
    if os.name != "nt":
        print("RETLAW OPTIMIZER es una aplicacion para Windows."); return
    if winreg is None or psutil is None:
        ctypes.windll.user32.MessageBoxW(0, "Faltan componentes internos (psutil/winreg).", APP, 0x10); return
    App().mainloop()

if __name__ == "__main__":
    main()
