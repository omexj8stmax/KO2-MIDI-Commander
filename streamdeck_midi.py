import mido
import os
import time
import subprocess
import platform

def execute_cross_platform_command(command_config):
    current_os = platform.system()
    command_to_execute = None

    if current_os == "Windows" and "windows" in command_config:
        command_to_execute = command_config["windows"]
    elif current_os == "Darwin" and "darwin" in command_config:
        command_to_execute = command_config["darwin"]
    elif current_os == "Linux" and "linux" in command_config:
        command_to_execute = command_config["linux"]
    elif "default" in command_config: # Fallback für nicht-spezifische OS
        command_to_execute = command_config["default"]
    else:
        print(f"Kein Befehl für das aktuelle Betriebssystem ({current_os}) oder Standardbefehl definiert.")
        return

    if command_to_execute:
        try:
            print(f"Führe Befehl aus auf {current_os}: {command_to_execute}")
            subprocess.Popen(command_to_execute, shell=True)
        except Exception as e:
            print(f"Fehler bei der Befehlsausführung '{command_to_execute}': {e}")

mapping = {
    # =====================================================================
    # BANK A (Notes 36-51) - Alltagsanwendungen & System-Utilities
    # =====================================================================
    36: {"name": "A-01: Notizblock/Texteditor", "command": {
        "windows": "notepad.exe",
        "darwin": "open -a 'TextEdit'",
        "linux": "gedit"
    }},
    37: {"name": "A-02: Webbrowser (Standard) öffnen", "command": {
        "windows": "start chrome", # oder "msedge", "firefox"
        "darwin": "open -a 'Google Chrome'", # oder "Firefox", "Safari"
        "linux": "xdg-open https://www.google.com" # Öffnet Standardbrowser
    }},
    38: {"name": "A-03: Rechner", "command": {
        "windows": "calc.exe",
        "darwin": "open -a 'Calculator'",
        "linux": "gnome-calculator"
    }},
    39: {"name": "A-04: Dateiexplorer/Finder (Home/User)", "command": {
        "windows": "explorer %USERPROFILE%",
        "darwin": "open ~",
        "linux": "xdg-open ~"
    }},
    40: {"name": "A-05: Task-Manager/Systemüberwachung", "command": {
        "windows": "taskmgr",
        "darwin": "open -a 'Activity Monitor'",
        "linux": "gnome-system-monitor"
    }},
    41: {"name": "A-06: Terminal/Eingabeaufforderung", "command": {
        "windows": "cmd.exe",
        "darwin": "open -a 'Terminal'",
        "linux": "gnome-terminal"
    }},
    42: {"name": "A-07: Zwischenablageverlauf (Win/macOS)", "command": {
        "windows": "start ms-settings:clipboard", # Öffnet Einstellungen für Clipboard
        "darwin": "open -a 'Clipboard Viewer'", # macOS hat keinen nativen "Clipboard Viewer", aber Third-Party Tools
        "linux": "echo 'Clipboard History: Use specific tool'" # Linux benötigt auch ein Tool
    }},
    43: {"name": "A-08: Screenshot-Tool", "command": {
        "windows": "snippingtool.exe",
        "darwin": "open -a 'Screenshot'",
        "linux": "gnome-screenshot"
    }},
    44: {"name": "A-09: Discord öffnen", "command": {
        "windows": "start discord",
        "darwin": "open -a 'Discord'",
        "linux": "discord"
    }},
    45: {"name": "A-10: Spotify öffnen", "command": {
        "windows": "start spotify:", # Spotify URI
        "darwin": "open -a 'Spotify'",
        "linux": "spotify"
    }},
    46: {"name": "A-11: E-Mail Client öffnen (Standard)", "command": {
        "windows": "start outlookmail:", # Öffnet Outlook Mail App
        "darwin": "open -a 'Mail'",
        "linux": "thunderbird"
    }},
    47: {"name": "A-12: Kamera-App öffnen", "command": {
        "windows": "microsoft.windows.camera:", # Windows Camera App URI
        "darwin": "open -a 'Photo Booth'",
        "linux": "cheese"
    }},
    48: {"name": "A-13: Einstellungen öffnen (Allgemein)", "command": {
        "windows": "start ms-settings:",
        "darwin": "open -a 'System Settings'",
        "linux": "gnome-control-center"
    }},
    49: {"name": "A-14: Browser im Inkognito/Privat-Modus", "command": {
        "windows": "start chrome --incognito",
        "darwin": "open -a 'Google Chrome' --args --incognito",
        "linux": "google-chrome --incognito"
    }},
    50: {"name": "A-15: VS Code öffnen (aktueller Ordner)", "command": {
        "windows": "code .",
        "darwin": "code .",
        "linux": "code ."
    }},
    51: {"name": "A-16: Slack öffnen", "command": {
        "windows": "start slack",
        "darwin": "open -a 'Slack'",
        "linux": "slack"
    }},

    # =====================================================================
    # BANK B (Notes 52-67) - Produktivität & System-Aktionen
    # =====================================================================
    52: {"name": "B-01: Word öffnen", "command": {
        "windows": "start winword",
        "darwin": "open -a 'Microsoft Word'",
        "linux": "libreoffice --writer"
    }},
    53: {"name": "B-02: Excel öffnen", "command": {
        "windows": "start excel",
        "darwin": "open -a 'Microsoft Excel'",
        "linux": "libreoffice --calc"
    }},
    54: {"name": "B-03: PowerPoint öffnen", "command": {
        "windows": "start powerpnt",
        "darwin": "open -a 'Microsoft PowerPoint'",
        "linux": "libreoffice --impress"
    }},
    55: {"name": "B-04: Outlook öffnen", "command": {
        "windows": "start outlook",
        "darwin": "open -a 'Microsoft Outlook'",
        "linux": "thunderbird" # Oder Evolution
    }},
    56: {"name": "B-05: Zoom starten", "command": {
        "windows": "start zoom",
        "darwin": "open -a 'Zoom'",
        "linux": "zoom"
    }},
    57: {"name": "B-06: PC Sperren", "command": {
        "windows": "rundll32.exe user32.dll,LockWorkStation",
        "darwin": "/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend",
        "linux": "gnome-screensaver-command --lock"
    }},
    58: {"name": "B-07: PC Herunterfahren (sofort)", "command": {
        "windows": "shutdown /s /t 0",
        "darwin": "osascript -e 'tell app \"System Events\" to shut down'", # Weniger invasiv als sudo shutdown
        "linux": "systemctl poweroff" # Alternativ: "sudo shutdown -h now"
    }},
    59: {"name": "B-08: PC Neustarten (sofort)", "command": {
        "windows": "shutdown /r /t 0",
        "darwin": "osascript -e 'tell app \"System Events\" to restart'",
        "linux": "systemctl reboot" # Alternativ: "sudo reboot"
    }},
    60: {"name": "B-09: Soundeinstellungen", "command": {
        "windows": "control mmsys.cpl,,1",
        "darwin": "open '/System/Library/PreferencePanes/Sound.prefPane'",
        "linux": "gnome-control-center sound"
    }},
    61: {"name": "B-10: Anzeigeeinstellungen", "command": {
        "windows": "control desk.cpl,,3",
        "darwin": "open '/System/Library/PreferencePanes/Displays.prefPane'",
        "linux": "gnome-control-center display"
    }},
    62: {"name": "B-11: Standard-Browser öffnen (Google)", "command": {
        "windows": "start https://www.google.com",
        "darwin": "open https://www.google.com",
        "linux": "xdg-open https://www.google.com"
    }},
    63: {"name": "B-12: Standard-Browser öffnen (YouTube)", "command": {
        "windows": "start https://www.youtube.com",
        "darwin": "open https://www.youtube.com",
        "linux": "xdg-open https://www.youtube.com"
    }},
    64: {"name": "B-13: Taschenrechner", "command": { # Duplikat, aber für 16er-Blöcke
        "windows": "calc.exe",
        "darwin": "open -a 'Calculator'",
        "linux": "gnome-calculator"
    }},
    65: {"name": "B-14: Steam öffnen", "command": {
        "windows": "start steam://open/games", # Öffnet Steam Spiele-Bibliothek
        "darwin": "open -a 'Steam'",
        "linux": "steam"
    }},
    66: {"name": "B-15: OBS Studio starten", "command": {
        "windows": "start obs64", # Exe-Name kann variieren
        "darwin": "open -a 'OBS'",
        "linux": "obs"
    }},
    67: {"name": "B-16: VLC Media Player starten", "command": {
        "windows": "start vlc",
        "darwin": "open -a 'VLC'",
        "linux": "vlc"
    }},

    # =====================================================================
    # BANK C (Notes 68-83) - System- & Netzwerk-Tools, spezifische URLs
    # =====================================================================
    68: {"name": "C-01: CMD/PowerShell als Admin (Windows)", "command": {
        "windows": "powershell -Command \"Start-Process cmd -Verb RunAs\"",
        "darwin": "echo 'N/A: Terminal als Admin'", # Keine direkte Entsprechung ohne sudo/GUI
        "linux": "echo 'N/A: Terminal als Admin'"
    }},
    69: {"name": "C-02: Netzwerk- und Freigabecenter", "command": {
        "windows": "control netconnections",
        "darwin": "open '/System/Library/PreferencePanes/Network.prefPane'",
        "linux": "gnome-control-center network"
    }},
    70: {"name": "C-03: Windows Defender Security Center", "command": {
        "windows": "start windowsdefender:",
        "darwin": "open -a 'System Settings' --args PrivacySecurity",
        "linux": "echo 'Antivirus/Firewall: Use specific tool'"
    }},
    71: {"name": "C-04: Geräte-Manager (Windows)", "command": {
        "windows": "devmgmt.msc",
        "darwin": "open /Applications/Utilities/System\\ Information.app",
        "linux": "lshw -short" # Zeigt Hardware im Terminal an, keine GUI
    }},
    72: {"name": "C-05: Bluetooth-Einstellungen", "command": {
        "windows": "start ms-settings:bluetooth",
        "darwin": "open '/System/Library/PreferencePanes/Bluetooth.prefPane'",
        "linux": "gnome-control-center bluetooth"
    }},
    73: {"name": "C-06: Drucker & Scanner", "command": {
        "windows": "start ms-settings:printers",
        "darwin": "open '/System/Library/PreferencePanes/Printers.prefPane'",
        "linux": "gnome-control-center printers"
    }},
    74: {"name": "C-07: Datum & Uhrzeit Einstellungen", "command": {
        "windows": "start ms-settings:dateandtime",
        "darwin": "open '/System/Library/PreferencePanes/DateAndTime.prefPane'",
        "linux": "gnome-control-center datetime"
    }},
    75: {"name": "C-08: Benutzerkonten-Einstellungen", "command": {
        "windows": "start ms-settings:accounts",
        "darwin": "open '/System/Library/PreferencePanes/UsersAndGroups.prefPane'",
        "linux": "gnome-control-center user-accounts"
    }},
    76: {"name": "C-09: Update-Einstellungen", "command": {
        "windows": "start ms-settings:windowsupdate",
        "darwin": "open '/System/Library/PreferencePanes/SoftwareUpdate.prefPane'",
        "linux": "gnome-software --updates"
    }},
    77: {"name": "C-10: Papierkorb leeren (Windows/macOS)", "command": {
        "windows": "PowerShell.exe -NoProfile -Command \"Clear-RecycleBin -Force\"",
        "darwin": "osascript -e 'tell application \"Finder\" to empty trash'",
        "linux": "rm -rf ~/.local/share/Trash/*" # ACHTUNG: Löscht dauerhaft, nur mit Bedacht nutzen!
    }},
    78: {"name": "C-11: Spezifischer Website (z.B. GitHub)", "command": {
        "windows": "start https://github.com",
        "darwin": "open https://github.com",
        "linux": "xdg-open https://github.com"
    }},
    79: {"name": "C-12: Spezifischer Website (z.B. Reddit)", "command": {
        "windows": "start https://www.reddit.com",
        "darwin": "open https://www.reddit.com",
        "linux": "xdg-open https://www.reddit.com"
    }},
    80: {"name": "C-13: Spezifischer Website (z.B. Twitch)", "command": {
        "windows": "start https://www.twitch.tv",
        "darwin": "open https://www.twitch.tv",
        "linux": "xdg-open https://www.twitch.tv"
    }},
    81: {"name": "C-14: Spezifischer Website (z.B. Netflix)", "command": {
        "windows": "start https://www.netflix.com",
        "darwin": "open https://www.netflix.com",
        "linux": "xdg-open https://www.netflix.com"
    }},
    82: {"name": "C-15: Google Docs", "command": {
        "windows": "start https://docs.google.com/",
        "darwin": "open https://docs.google.com/",
        "linux": "xdg-open https://docs.google.com/"
    }},
    83: {"name": "C-16: Google Sheets", "command": {
        "windows": "start https://sheets.google.com/",
        "darwin": "open https://sheets.google.com/",
        "linux": "xdg-open https://sheets.google.com/"
    }},

    # =====================================================================
    # BANK D (Notes 84-99) - Entwicklungstools, Medien & Mehr
    # =====================================================================
    84: {"name": "D-01: GitHub Desktop öffnen", "command": {
        "windows": "start github-desktop",
        "darwin": "open -a 'GitHub Desktop'",
        "linux": "github-desktop" # Wenn als AppImage/Snap/Flatpak installiert
    }},
    85: {"name": "D-02: Docker Desktop starten", "command": {
        "windows": "start \"\" \"C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe\"",
        "darwin": "open -a 'Docker'",
        "linux": "systemctl start docker" # Oder `sudo systemctl start docker`
    }},
    86: {"name": "D-03: Postman öffnen", "command": {
        "windows": "start postman",
        "darwin": "open -a 'Postman'",
        "linux": "postman"
    }},
    87: {"name": "D-04: Browser-Entwickler-Tools (Chrome)", "command": {
        "windows": "start chrome --auto-open-devtools-for-tabs",
        "darwin": "open -a 'Google Chrome' --args --auto-open-devtools-for-tabs",
        "linux": "google-chrome --auto-open-devtools-for-tabs"
    }},
    88: {"name": "D-05: Spotify Song überspringen (Simulieren)", "command": {
        "windows": "(New-Object -ComObject WScript.Shell).SendKeys(\"^%{RIGHT}\")", # Strg+Alt+Rechts
        "darwin": "osascript -e 'tell application \"Spotify\" to next track'",
        "linux": "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next"
    }},
    89: {"name": "D-06: Spotify Play/Pause (Simulieren)", "command": {
        "windows": "(New-Object -ComObject WScript.Shell).SendKeys(\"{MEDIA_PLAY_PAUSE}\")",
        "darwin": "osascript -e 'tell application \"Spotify\" to playpause'",
        "linux": "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause"
    }},
    90: {"name": "D-07: Bildschirmaufnahme starten", "command": {
        "windows": "start ms-screenclip:", # Windows Game Bar Screen Recorder
        "darwin": "open -a 'QuickTime Player'", # Dann manuell Aufnahme starten
        "linux": "gnome-screenshot --interactive" # Interaktives Screenshot-Tool, kann Video aufnehmen
    }},
    91: {"name": "D-08: Webcam aktivieren/deaktivieren (simulieren)", "command": {
        "windows": "echo 'Webcam: Specific software/hotkey needed'", # Kein direkter Systembefehl
        "darwin": "echo 'Webcam: Specific software/hotkey needed'",
        "linux": "echo 'Webcam: Specific software/hotkey needed'"
    }},
    92: {"name": "D-09: Mikrofon stummschalten (simulieren)", "command": {
        "windows": "echo 'Microphone: Specific software/hotkey needed'", # Kein direkter Systembefehl
        "darwin": "osascript -e 'set volume input volume 0'", # Setzt Input-Lautstärke auf 0
        "linux": "amixer set Capture toggle" # Toggle Mic Mute
    }},
    93: {"name": "D-10: Medienlautstärke erhöhen", "command": {
        "windows": "(New-Object -ComObject WScript.Shell).SendKeys(\"{VK_VOLUME_UP}\")",
        "darwin": "osascript -e 'set volume output volume ((get volume settings)'s output volume) + 5'",
        "linux": "amixer -D pulse set Master 5%+"
    }},
    94: {"name": "D-11: Medienlautstärke verringern", "command": {
        "windows": "(New-Object -ComObject WScript.Shell).SendKeys(\"{VK_VOLUME_DOWN}\")",
        "darwin": "osascript -e 'set volume output volume ((get volume settings)'s output volume) - 5'",
        "linux": "amixer -D pulse set Master 5%-"
    }},
    95: {"name": "D-12: Medienlautstärke stummschalten", "command": {
        "windows": "(New-Object -ComObject WScript.Shell).SendKeys(\"{VK_MUTE}\")",
        "darwin": "osascript -e 'set volume with output muted'",
        "linux": "amixer -D pulse set Master toggle"
    }},
    96: {"name": "D-13: YouTube öffnen (ohne Verlauf)", "command": {
        "windows": "start chrome --incognito www.youtube.com",
        "darwin": "open -a 'Google Chrome' --args --incognito www.youtube.com",
        "linux": "google-chrome --incognito www.youtube.com"
    }},
    97: {"name": "D-14: Wikipedia öffnen", "command": {
        "windows": "start https://de.wikipedia.org/",
        "darwin": "open https://de.wikipedia.org/",
        "linux": "xdg-open https://de.wikipedia.org/"
    }},
    98: {"name": "D-15: Google Maps", "command": {
        "windows": "start https://www.google.com/maps",
        "darwin": "open https://www.google.com/maps",
        "linux": "xdg-open https://www.google.com/maps"
    }},
    99: {"name": "D-16: Google Translate", "command": {
        "windows": "start https://translate.google.com/",
        "darwin": "open https://translate.google.com/",
        "linux": "xdg-open https://translate.google.com/"
    }},
    # Falls Sie weitere Noten verwenden wollen (z.B. für Noten-Events außerhalb des
    # KO II Standardbereichs oder wenn Sie Note Off mit Befehlen belegen wollen):
    # E-01 (Beispiel für Note 100)
    # 100: {"name": "E-01: Beispiel Weiterer Befehl", "command": {
    #     "windows": "echo 'Hello from Windows E-01'",
    #     "darwin": "echo 'Hello from macOS E-01'",
    #     "linux": "echo 'Hello from Linux E-01'"
    # }},
    # ... und so weiter bis Note 143 für insgesamt 144 Befehle, falls benötigt.
    # Beachten Sie, dass das KO II nur 64 MIDI Noten als Pads sendet.
}

def clear_terminal():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    print("="*40)
    print(" 🎛️  KO2 MIDI Commander")
    print("="*40)

def main():
    input_names = mido.get_input_names()
    if not input_names:
        print("Keine MIDI-Inputs gefunden. Stelle sicher, dass der KO2 angeschlossen und erkannt wird.")
        print("Möglicherweise müssen Sie `python-rtmidi` installieren, wenn Sie dies noch nicht getan haben.")
        print("Versuchen Sie: `pip install python-rtmidi`")
        return

    print("Verfügbare MIDI-Inputs:")
    for i, name in enumerate(input_names):
        print(f"[{i}] {name}")
    
    try:
        index = int(input("Wähle Port-Index: "))
        port_name = input_names[index]
    except (ValueError, IndexError):
        print("Ungültige Auswahl. Beende.")
        return

    with mido.open_input(port_name) as inport:
        clear_terminal()
        print_header()
        print(f"🎹 Verbunden mit: {port_name}\n")
        print("Drücke eine Taste am KO2...\n")
        print("Hinweis: Befehle sind OS-spezifisch und müssen ggf. angepasst werden.")
        try:
            for msg in inport:
                if msg.type == 'note_on' and msg.velocity > 0:
                    note_info = mapping.get(msg.note)
                    if note_info:
                        key_name = note_info["name"]
                        print(f"🟢 gedrückt: {key_name} (Note {msg.note})")
                        execute_cross_platform_command(note_info["command"])
                    else:
                        print(f"🟢 gedrückt: Unbekannt (Note {msg.note})")
                # Optional: Befehle auch für Note Off-Events
                # elif msg.type == 'note_off':
                #     note_info = mapping.get(msg.note)
                #     if note_info:
                #         key_name = note_info["name"]
                #         print(f"⚪️ losgelassen: {key_name} (Note {msg.note})")
                #         # Hier könnte ein "Beim Loslassen"-Befehl stehen
                #     else:
                #         print(f"⚪️ losgelassen: Unbekannt (Note {msg.note})")
        except KeyboardInterrupt:
            print("\n👋 Beendet.")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()
