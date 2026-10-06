# Hero Caves – Roblox-Prototyp

## Downloads über GitHub

**[Aktuelles Spiel herunterladen](https://github.com/Radorrrr/rador/raw/refs/heads/main/hero-caves/HeroCaves.rbxlx)** · **[Alles als ZIP herunterladen](https://github.com/Radorrrr/rador/raw/refs/heads/main/hero-caves/HeroCaves.zip)**

Lade die Spiel-Datei herunter und öffne sie in Roblox Studio über **Datei → Aus Datei öffnen**. Falls dein Browser die Datei als Text anzeigt, nutze auf der [GitHub-Dateiseite](https://github.com/Radorrrr/rador/blob/main/hero-caves/HeroCaves.rbxlx) oben rechts **Download raw file**.

Diese Links zeigen jeweils auf die zuletzt hier hochgeladene Version. Bereits heruntergeladene Dateien aktualisieren sich nicht automatisch. Sichere eigene Studio-Änderungen separat, bevor du ein Update öffnest.

![Die vier Helden](Charaktere.png)


## Starten (einfachster Weg)
1. Öffne `HeroCaves.rbxlx` in Roblox Studio über **Datei → Aus Datei öffnen**.
2. Klicke **Play**. Die Map entsteht beim Start automatisch.
3. Klicke **Zu meiner Base**. Dein Ritter kämpft bereits automatisch.
4. Sammle Gold, kaufe Upgrades im linken Menü und gehe zum Händler für weitere Helden. Öffne dort mit **E** den Shop (auf Touch-Geräten den Prompt antippen).
5. Mit **Stop** verlässt du den Test. Über **Datei → In Roblox veröffentlichen** kannst du später dein eigenes Erlebnis erstellen.

## Alternativ in deine leere Baseplate einfügen
1. Öffne **Explorer** über die Studio-Suche oder das Fenster-Menü.
2. Füge unter **ServerScriptService** ein **Script** namens `HeroCavesServer` hinzu. Ersetze den gesamten Inhalt durch `Game.server.lua`.
3. Füge unter **StarterPlayer → StarterPlayerScripts** ein **LocalScript** namens `HeroCavesClient` hinzu. Ersetze den gesamten Inhalt durch `Game.client.lua`.
4. Füge unter **ReplicatedStorage** ein **ModuleScript** namens `CharacterDesign` hinzu und ersetze seinen Inhalt durch `CharacterDesign.lua`.
5. Klicke **Play**. Du brauchst keine hochgeladenen Assets oder Animation-IDs.

## Regeln dieser Version
- Eigene Base pro Spieler; kostenlose Startfigur Ritter.
- Helden: Ritter, Berserker, Magier und Paladin; jeder einmal kaufbar.
- Käufe nur nahe dem Händler. Gekaufte Helden laufen mit 16 Studs/s entlang des Weges zur Base. Erst bei Ankunft greifen sie an.
- Feste vier Kampfplätze; Helden blicken zum Gegner. Schwert/Axt schwingen, Magier hebt den Stab und erzeugt ein magisches Projektil. Die Bewegung ist prozedural und benötigt keine hochgeladenen Animationen.
- Der Gegner läuft aus der Höhle in die Mitte und bleibt dort passiv. Schadensberechnung erfolgt auf dem Server unabhängig von Waffenkollisionen.
- Boss bei Welle 5, 10, 15 usw.; exakt 10-fache HP des vorherigen Gegners. 30 Sekunden ab Ankunft im Kampfbereich.
- Bei Zeitablauf wird die vorherige Welle zum wiederholbaren Gold-Farmen. **Boss erneut versuchen** startet den Boss neu mit voller Gesundheit und neuer Zeit.
- Gold wird bei Tod sofort gutgeschrieben. Keine einsammelbaren Münzen in dieser Version.
- Upgrades steigern Schaden, Angriffsgeschwindigkeit bleibt je Held konstant. Levelgrenze 100.
- Schmied und Chronist sind sichtbare Platzhalter ohne Funktion.
- Fortschritt gilt nur für die aktuelle Sitzung. Noch kein DataStore, Offline-Fortschritt, Rebirth oder fertige Grafik.

## Werte ändern
Am Anfang von `Game.server.lua` steht die Heldenliste: `cost` = Kaufpreis, `damage` = Schaden pro Angriff, `speed` = Angriffe pro Sekunde, `weapon` = Sword/Axe/Staff.
`hp(wave)` legt die Gegner-Lebenspunkte fest, `upgradeCost` die Upgrade-Kosten. Bei Änderungen der Scripts die Studio-Script-Inhalte entsprechend ersetzen; die mitgelieferte Place-Datei aktualisiert sich nicht automatisch.

## Spieltest in Studio
- Teste solo Start-Ritter, Gold und Upgrades.
- Kaufe einen Helden und beobachte Weg, Ankunft und Angriffe.
- Lass einen Boss scheitern: Farm-Welle davor muss wiederkehren; mit dem Button erneut versuchen.
- Teste mit zwei Spielern im Studio-Server-Test: getrennte Bases, Gold und Helden.
- Ohne Gold darf ein Kauf/Upgrade den Kontostand nicht ändern.

Die Datei wurde strukturell geprüft. Ein Roblox-Laufzeittest war in dieser Arbeitsumgebung nicht möglich.

## Neue Charaktermodelle
Die vier Helden haben jetzt eigene Gesichter, Kleidung, Rüstung, Gürtel und detaillierte Waffen. Metall, Stoff, Holz und Neon sind eingebaute Roblox-Materialien. Es gibt keine externen Bildtexturen oder erforderlichen Asset-IDs.

Die aktualisierte `HeroCaves.rbxlx` enthält die Designs bereits. Unter **ServerStorage → CharacterModels** findest du zusätzlich die vier statischen Modelle zum Bearbeiten. Für eine Vorschau im Editor kannst du eine Kopie eines Modells nach Workspace ziehen. Die laufenden Spielfiguren werden aus `CharacterDesign.lua` aufgebaut; Änderungen an den statischen Kopien werden deshalb nicht automatisch ins Spiel übernommen.

Die einzelnen `.rbxmx`-Dateien lassen sich in Studio über **Modell einfügen / Aus Datei einfügen** (je nach Studio-Version im Kontextmenü von Workspace) importieren. Sie sind verankerte Part-Modelle, keine Humanoid-Rigs. Im Spiel bewegt das vorhandene Script den rechten Arm und die gesamte Waffe samt Details.

`Charaktere.png` zeigt eine aus derselben Geometrie berechnete Übersicht. Die tatsächlichen Materialien und Beleuchtung in Roblox Studio können anders aussehen.
