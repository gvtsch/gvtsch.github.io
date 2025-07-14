---
tags: ["python", "windows"]
---

# Das `keyring`-Modul in Python

Das `keyring`-Modul in Python ist eine Bibliothek, die einen sicheren und einfachen Zugang zu den **systemeigenen Schlüsselbunddiensten** (Keyring Services) des Betriebssystems bietet. Stell es dir vor wie einen digitalen "Schlüsselbund" für Passwörter und andere sensible Informationen.

## Warum ist `keyring` wichtig?
Wenn du in deinen Python-Anwendungen Passwörter, API-Schlüssel oder andere vertrauliche Daten speichern musst, ist es nicht die beste Idee, diese direkt in den Quellcode zu schreiben oder in unverschlüsselten Dateien zu speichern. Das ist ein erhebliches Sicherheitsrisiko.

Und hier kommt `keyring` ins Spiel. Es ermöglicht dir, diese sensiblen Daten sicher zu speichern, indem es die **nativen Mechanismen des Betriebssystems** nutzt. Das bedeutet:

- **Plattformunabhängig:** `keyring` versucht automatisch, den am besten geeigneten Keyring-Backend für deine Umgebung zu verwenden. Je nach Betriebssystem könnten das z.B. sein:
	- **macOS Keychain** auf macOS
	- **Windows Credential Locker** auf Windows
	- **GNOME Keyring** oder **KDE Wallet** auf Linux
- **Sicherheit:** Die Passwörter werden nicht von deiner Anwendung selbst verwaltet, sondern vom Betriebssystem, das in der Regel robustere Sicherheitsmaßnahmen bietet (z.B. Verschlüsselung, Zugriffskontrolle).
- **Benutzerfreundlichkeit:** Für den Endbenutzer bedeutet das oft, dass er nur einmal das Master-Passwort des System-Keyrings (also zum Beispiel beim Windows Login) eingeben muss, um den Zugriff für alle Anwendungen zu ermöglichen, die den Keyring nutzen.

## Wie funktioniert `keyring`?
Die grundlegende Verwendung von `keyring` ist sehr einfach:

1. **Installation:**
    ```bash
    pip install keyring
    ```
2. **Passwort speichern:** Du gibst einen `service`-Namen (z.B. den Namen deiner Anwendung oder des Dienstes, für den das Passwort ist), einen `username` und das `password` an.
    ```python
    import keyring  
    keyring.set_password(
	    "my_awesome_app", 
	    "my_user", 
	    "my_secret_password123")```    
3. **Passwort abrufen:** Du gibst den `service`-Namen und den `username` an.
    ```python
    import keyring  
    password = keyring.get_password("my_awesome_app", "my_user") 
    if password:     
	    print(f"Das Passwort ist: {password}") 
	else:   
		print("Passwort nicht gefunden.")
		```
4. **Passwort löschen:**
    ```python
    import keyring  
    try:     
	    keyring.delete_password("my_awesome_app", "my_user")     
	    print("Passwort gelöscht.") 
	except keyring.errors.PasswordDeleteError:     
		print("Passwort nicht gefunden oder konnte nicht gelöscht werden.")```

## Anwendungsbeispiele:
- **API-Zugangsdaten:** Deine Python-Anwendung muss auf eine externe API zugreifen, die eine Authentifizierung erfordert. Anstatt den API-Schlüssel direkt im Code zu speichern, legst du ihn im Keyring ab. Das kann z.B. dein OpenAI API Key sein, mit dem du GPT und Co zugreifst.
- **Datenbankzugang:** Wenn deine Anwendung mit einer Datenbank kommuniziert, können die Datenbank-Anmeldeinformationen sicher im Keyring gespeichert werden. Um in der Welt der Sprachverarbeitung zu bleiben, könnte das beispielsweise Pinecone sein.
- **E-Mail-Zugangsdaten:** Für Anwendungen, die E-Mails versenden oder empfangen. An dieser Stelle spare ich mir ein Beispiel :)

## Vorteile von `keyring`:
- **Verbesserte Sicherheit:** Reduziert das Risiko, dass sensible Daten offengelegt werden.
- **Bessere Benutzerfreundlichkeit:** Benutzer müssen Passwörter nicht bei jeder Anwendungseingabe neu eingeben, wenn sie bereits im System-Keyring gespeichert sind.
- **Einfache Integration:** Die API ist sehr intuitiv und leicht zu verwenden.
- **Automatisches Backend-Management:** `keyring` kümmert sich darum, das richtige Backend für das jeweilige Betriebssystem zu finden.

## Anlegen eines Keys in Windows
Es gibt verschiedene Möglichkeiten seine Keys z.B. im **Windows Credential Locker** abzulegen.

### Key mit `keyring` ablegen
Man kann seinen Key z.B. unter Verwendung von `keyring` ablegen. D.h. natürlich, dass der für diesen Vorgang einmal im Klartext in einem Python Skript steht. Dieses Skript gehört also nicht veröffentlicht ;) 

```python
import keyring

SERVICE_NAME = "openai_api_key" 
USERNAME = "default_user"

openai_api_key = "sk-..." # Diesen Wert durch den API Key ersetzen

try:
	keyring.set_password(SERVICE_NAME, USERNAME, openai_api_key) 
	print(f"OpenAI API Key für Dienst '{SERVICE_NAME}' und Benutzer '{USERNAME}' erfolgreich gespeichert.") 
except Exception as e: 
	print(f"Fehler beim Speichern des API Keys: {e}")
```

Wenn man das Skript nun ausführt, sollte man die Bestätigung erhalten, dass der Schlüssel erfolgreich gespeichert wurde. Es könnte sein, dass Windows dich in einem Pop-up-Fenstre bittet, den Zugriff zu erlauben oder zu authentifizieren. Das ist im Grunde nur ein Zeichen dafür, dass der **Credential Locker** funktioniert.

### Key manuell ablegen
Man kann den Eintrag, den Key, auch manuell anlegen oder den Eintrag überprüfen:

![Anmeldeinformations-Manager in Windows](https://support.microsoft.com/images/de-de/7a91c53e-f719-4762-830c-af9d7723de3a)
_Quelle: [Microsoft Support](https://support.microsoft.com/de-de/windows/anmeldeinformations-manager-in-windows-1b5c916a-6a16-889f-8581-fc16e8165ac0)_

1. Drücke die Tasten `Win + R` und tippe `control` ein. Wenn du die Eingabe mit `Enter` bestätigst, öffnet sich die Systemsteuerung.
2. In der Systemsteuerung kannst du dann nach `Anmeldeinformationsverwaltung` suchen (oder im englischen nach `Credential Manager`) und es dann durch klicken öffnen.
3. Nun kannst du oben rechts `Windows-Anmeldeinformationen` auswählen.
4. Unter `Generische Anmeldeinformationen` solltest du entweder deinen erzeugten Eintrag finden, oder du kannst einen neuen anlegen, indem du auf den Dialog zum Hinzufügen klickst.


## Zusammenfassung
Das `keyring`-Modul ist eine wertvolle Ergänzung, für jede Python-Anwendung, die sicher mit sensiblen Daten wie bspw. Passwörtern umgehen muss. Darüber hinaus ist es nicht besonders kompliziert in der Anwendung.

