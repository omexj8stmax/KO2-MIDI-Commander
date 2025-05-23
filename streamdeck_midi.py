import mido
import os
import time
import subprocess
import platform # Importiere das platform Modul, um das OS zu erkennen

def execute_cross_platform_command(command_config):
    """
    Führt einen Befehl plattformübergreifend aus.
    command_config sollte ein Dictionary mit 'windows', 'darwin' (macOS) und 'linux' Schlüsseln sein,
    die jeweils den spezifischen Befehl für das OS enthalten.
    """
    current_os = platform.system()
    command_to_execute = None

    if current_os == "Windows" and "windows" in command_config:
        command_to_execute = command_config["windows"]
    elif current_os == "Darwin" and "darwin" in command_config: # macOS ist "Darwin"
        command_to_execute = command_config["darwin"]
    elif current_os == "Linux" and "linux" in command_config:
        command_to_execute = command_config["linux"]
    else:
        print(f"Kein Befehl für das aktuelle Betriebssystem ({current_os}) definiert.")
        return

    if command_to_execute:
        try:
            print(f"Führe Befehl aus auf {current_os}: {command_to_execute}")
            # subprocess.Popen ist gut für nicht-blockierende Ausführung von GUI-Anwendungen.
            # Für Befehle, die im Terminal ausgeführt werden sollen, können Sie auch subprocess.run() nutzen,
            # aber Popen ist flexibler für verschiedene Anwendungen.
            subprocess.Popen(command_to_execute, shell=True)
        except Exception as e:
            print(f"Fehler bei der Befehlsausführung '{command_to_execute}': {e}")

# Erweitertes Mapping mit plattformspezifischen Befehlen
# Jede Note kann jetzt ein Dictionary mit 'name' und 'command' enthalten.
# 'command' ist selbst ein Dictionary mit OS-spezifischen Befehlen.
mapping = {
    # Reihe A (Noten 36-47)
    36: {"name": "A-.", "command": {
        "windows": "notepad.exe",
        "darwin": "open -a 'TextEdit'",
        "linux": "gedit" # oder 'xed' für Mint, 'mousepad' für XFCE etc.
    }},
    37: {"name": "A-0", "command": {
        "windows": "start chrome www.google.com",
        "darwin": "open -a 'Google Chrome' www.google.com",
        "linux": "xdg-open www.google.com" # Öffnet im Standard-Browser
    }},
    38: {"name": "A-ENTER", "command": {
        "windows": "explorer .", # Aktuellen Ordner öffnen
        "darwin": "open .",
        "linux": "xdg-open ."
    }},
    39: {"name": "A-1", "command": {
        "windows": "calc.exe",
        "darwin": "open -a 'Calculator'",
        "linux": "gnome-calculator" # Oder 'kcalc', 'xcalc'
    }},
    40: {"name": "A-2", "command": {
        "windows": "mspaint.exe",
        "darwin": "open -a 'Preview'", # Öffnet Preview, nicht direkt Paint-Äquivalent
        "linux": "gimp" # Oder 'pinta', 'kolourpaint'
    }},
    41: {"name": "A-3", "command": {
        "windows": "taskmgr", # Task-Manager
        "darwin": "open -a 'Activity Monitor'",
        "linux": "gnome-system-monitor" # Oder 'ksysguard', 'htop'
    }},
    42: {"name": "A-4", "command": {
        "windows": "cmd.exe", # Eingabeaufforderung
        "darwin": "open -a 'Terminal'",
        "linux": "gnome-terminal" # Oder 'konsole', 'xfce4-terminal'
    }},
    43: {"name": "A-5", "command": {
        "windows": "powershell.exe",
        "darwin": "open -a 'iTerm'", # Wenn iTerm installiert ist, sonst Terminal
        "linux": "konsole" # Oder 'xfce4-terminal'
    }},
    44: {"name": "A-6", "command": {
        "windows": "control.exe", # Systemsteuerung
        "darwin": "open /System/Library/PreferencePanes", # Systemeinstellungen öffnen
        "linux": "gnome-control-center" # Oder 'kde-settings', 'xfce4-settings-manager'
    }},
    45: {"name": "A-7", "command": {
        "windows": "explorer shell:AppsFolder\\Microsoft.Windows.Photos_8wekyb3d8bbwe!App", # Fotos-App
        "darwin": "open -a 'Photos'",
        "linux": "shotwell" # Oder 'gthumb', 'eog'
    }},
    46: {"name": "A-8", "command": {
        "windows": "wmplayer.exe", # Windows Media Player (falls vorhanden)
        "darwin": "open -a 'Music'", # Oder 'VLC'
        "linux": "vlc" # Oder 'rhythmbox', ' audacious'
    }},
    47: {"name": "A-9", "command": {
        "windows": "msconfig", # Systemkonfiguration
        "darwin": "open /Applications/Utilities/Disk\\ Utility.app", # Festplattendienstprogramm
        "linux": "gnome-disks" # Oder 'kde-partitionmanager'
    }},

    # Reihe B (Noten 48-59) - Beispiele für Anwendungs-Shortcuts oder URLs
    48: {"name": "B-.", "command": {
        "windows": "start chrome https://chat.openai.com/",
        "darwin": "open -a 'Google Chrome' https://chat.openai.com/",
        "linux": "xdg-open https://chat.openai.com/"
    }},
    49: {"name": "B-0", "command": {
        "windows": "start firefox www.youtube.com",
        "darwin": "open -a 'Firefox' www.youtube.com",
        "linux": "firefox www.youtube.com"
    }},
    50: {"name": "B-ENTER", "command": {
        "windows": "code .", # VS Code im aktuellen Ordner öffnen (wenn im PATH)
        "darwin": "code .",
        "linux": "code ."
    }},
    51: {"name": "B-1", "command": {
        "windows": "start microsoft-edge:https://github.com",
        "darwin": "open -a 'Safari' https://github.com",
        "linux": "xdg-open https://github.com"
    }},
    52: {"name": "B-2", "command": {
        "windows": "start teams", # Microsoft Teams
        "darwin": "open -a 'Microsoft Teams'",
        "linux": "teams"
    }},
    53: {"name": "B-3", "command": {
        "windows": "start zoom", # Zoom Client
        "darwin": "open -a 'Zoom'",
        "linux": "zoom"
    }},
    54: {"name": "B-4", "command": {
        "windows": "start outlook", # Outlook
        "darwin": "open -a 'Microsoft Outlook'",
        "linux": "thunderbird" # Oder 'evolution'
    }},
    55: {"name": "B-5", "command": {
        "windows": "start word", # Microsoft Word
        "darwin": "open -a 'Microsoft Word'",
        "linux": "libreoffice --writer"
    }},
    56: {"name": "B-6", "command": {
        "windows": "start excel", # Microsoft Excel
        "darwin": "open -a 'Microsoft Excel'",
        "linux": "libreoffice --calc"
    }},
    57: {"name": "B-7", "command": {
        "windows": "start powerpnt", # Microsoft PowerPoint
        "darwin": "open -a 'Microsoft PowerPoint'",
        "linux": "libreoffice --impress"
    }},
    58: {"name": "B-8", "command": {
        "windows": "control desk.cpl,,3", # Anzeigeeinstellungen
        "darwin": "open '/System/Library/PreferencePanes/Displays.prefPane'",
        "linux": "gnome-control-center display" # Oder spezifische Befehle für KDE/XFCE
    }},
    59: {"name": "B-9", "command": {
        "windows": "control mmsys.cpl,,1", # Soundeinstellungen
        "darwin": "open '/System/Library/PreferencePanes/Sound.prefPane'",
        "linux": "gnome-control-center sound"
    }},

    # Reihe C (Noten 60-71) - Beispiele für Systemaktionen oder Skripte
    60: {"name": "C-.", "command": {
        "windows": "shutdown /s /t 0", # Herunterfahren (sofort)
        "darwin": "sudo shutdown -h now", # ACHTUNG: Benötigt Passwort! Besser: AppleScript
        "linux": "sudo shutdown -h now" # ACHTUNG: Benötigt Passwort!
        # Für macOS/Linux ohne sudo-Prompt könnte man eigene Shell-Skripte verwenden
    }},
    61: {"name": "C-0", "command": {
        "windows": "shutdown /r /t 0", # Neustarten (sofort)
        "darwin": "sudo shutdown -r now", # ACHTUNG: Benötigt Passwort!
        "linux": "sudo shutdown -r now" # ACHTUNG: Benötigt Passwort!
    }},
    62: {"name": "C-ENTER", "command": {
        "windows": "rundll32.exe user32.dll,LockWorkStation", # PC sperren
        "darwin": "/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend", # Sperren
        "linux": "gnome-screensaver-command --lock" # Oder 'xdg-screensaver lock'
    }},
    63: {"name": "C-1", "command": {
        "windows": "start ms-settings:", # Einstellungen öffnen
        "darwin": "open -a 'System Settings'", # Oder 'System Preferences' für ältere macOS
        "linux": "gnome-control-center"
    }},
    64: {"name": "C-2", "command": {
        "windows": "start ms-settings:network-status", # Netzwerkeinstellungen
        "darwin": "open '/System/Library/PreferencePanes/Network.prefPane'",
        "linux": "gnome-control-center network"
    }},
    65: {"name": "C-3", "command": {
        "windows": "start ms-settings:privacy-webcam", # Kameraeinstellungen
        "darwin": "open '/System/Library/PreferencePanes/Security.prefPane'", # Allgemeinere Sicherheit
        "linux": "xdg-open about:preferences#privacy" # Je nach Browser-Einstellungen
    }},
    66: {"name": "C-4", "command": {
        "windows": "start ms-settings:personalization", # Personalisierung
        "darwin": "open '/System/Library/PreferencePanes/DesktopScreenEffects.prefPane'",
        "linux": "gnome-control-center appearance"
    }},
    67: {"name": "C-5", "command": {
        "windows": "start ms-settings:appsfeatures", # Apps & Features
        "darwin": "open /Applications", # Anwendungen Ordner
        "linux": "gnome-software" # Oder 'synaptic', 'Discover' etc.
    }},
    68: {"name": "C-6", "command": {
        "windows": "start ms-settings:gaming-xboxnetworking", # Gaming-Einstellungen
        "darwin": "open -a 'App Store'", # Gaming ist meist über App Store
        "linux": "steam" # Wenn Steam installiert ist
    }},
    69: {"name": "C-7", "command": {
        "windows": "start ms-settings:windowsupdate", # Windows Update
        "darwin": "open '/System/Library/PreferencePanes/SoftwareUpdate.prefPane'",
        "linux": "gnome-software --updates" # Oder spezifische Update-Manager
    }},
    70: {"name": "C-8", "command": {
        "windows": "start powershell.exe -NoExit -Command \"Get-WmiObject -Class Win32_StartupCommand | Select-Object Name, Command\"", # Autostart-Einträge
        "darwin": "open '/System/Library/PreferencePanes/UsersAndGroups.prefPane'", # Anmeldeobjekte
        "linux": "gnome-session-properties" # Autostart-Anwendungen
    }},
    71: {"name": "C-9", "command": {
        "windows": "start explorer shell:RecycleBinFolder", # Papierkorb öffnen
        "darwin": "open ~/.Trash",
        "linux": "xdg-open trash:///"
    }},

    # Reihe D (Noten 72-83) - Weitere Beispiele oder spezifischere Anwendungen
    72: {"name": "D-.", "command": {
        "windows": "start chrome --incognito", # Inkognito-Modus Chrome
        "darwin": "open -a 'Google Chrome' --args --incognito",
        "linux": "google-chrome --incognito"
    }},
    73: {"name": "D-0", "command": {
        "windows": "start firefox --private-window", # Privater Modus Firefox
        "darwin": "open -a 'Firefox' --private-window",
        "linux": "firefox --private-window"
    }},
    74: {"name": "D-ENTER", "command": {
        "windows": "start brave", # Brave Browser
        "darwin": "open -a 'Brave Browser'",
        "linux": "brave-browser"
    }},
    75: {"name": "D-1", "command": {
        "windows": "start slack", # Slack
        "darwin": "open -a 'Slack'",
        "linux": "slack"
    }},
    76: {"name": "D-2", "command": {
        "windows": "start discord", # Discord
        "darwin": "open -a 'Discord'",
        "linux": "discord"
    }},
    77: {"name": "D-3", "command": {
        "windows": "start spotify", # Spotify
        "darwin": "open -a 'Spotify'",
        "linux": "spotify"
    }},
    78: {"name": "D-4", "command": {
        "windows": "start vlc", # VLC Player
        "darwin": "open -a 'VLC'",
        "linux": "vlc"
    }},
    79: {"name": "D-5", "command": {
        "windows": "start steam://open/games", # Steam Spiele-Bibliothek
        "darwin": "open -a 'Steam'",
        "linux": "steam"
    }},
    80: {"name": "D-6", "command": {
        "windows": "notepad.exe C:\\Users\\Public\\Desktop\\NOTES.txt", # Eine spezifische Datei öffnen
        "darwin": "open /Users/Shared/NOTES.txt",
        "linux": "gedit /tmp/NOTES.txt"
    }},
    81: {"name": "D-7", "command": {
        "windows": "explorer C:\\", # C:\ Laufwerk öffnen
        "darwin": "open /Volumes", # Externe Laufwerke
        "linux": "xdg-open /" # Root-Verzeichnis
    }},
    82: {"name": "D-8", "command": {
        "windows": "start control ncpa.cpl", # Netzwerkverbindungen
        "darwin": "open '/System/Library/PreferencePanes/Network.prefPane'",
        "linux": "nm-connection-editor" # NetworkManager GUI
    }},
    83: {"name": "D-9", "command": {
        "windows": "start devmgmt.msc", # Geräte-Manager
        "darwin": "open /Applications/Utilities/System\\ Information.app",
        "linux": "gnome-system-log" # Oder 'dmesg' im Terminal
    }}
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
                elif msg.type == 'note_off':
                    note_info = mapping.get(msg.note)
                    if note_info:
                        key_name = note_info["name"]
                        print(f"⚪️ losgelassen: {key_name} (Note {msg.note})")
                    else:
                        print(f"⚪️ losgelassen: Unbekannt (Note {msg.note})")
        except KeyboardInterrupt:
            print("\n👋 Beendet.")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()