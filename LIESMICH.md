# Material für Python Kurse

Notebooks und Code für die Kurse "Einführung in Python", "Python für Programmierer",
"Fortgeschrittenenkurs Python" und Python als Skriptsprache der Coding Akademie München.

## Installation (nur einmal erforderlich)

Verwenden Sie bitte den Befehl

```shell
git clone --recursive https://github.com/hoelzl/python-programmierer.git
cd python-course
```

zum Clonen des Repositories (Beachten Sie das Argument `--recursive`).


Falls Sie mit Anaconda arbeiten müssen Sie typischerweise eine PowerShell aus der Anaconda Installation verwenden; per Default ist Anaconda aus der System-PowerShell nicht verfügbar.

Wenn Sie eine Anaconda PowerShell geöffnet haben können Sie ein Anaconda
Environment, das alle für die Kurse benötigten Pakete enthält, mit den Befehlen

```shell
conda env create --file cam-basic.yaml
```

installieren. Mit dem Befehl

```shell
conda activate cam-basic
```

können Sie dieses Environment aktivieren. Falls Sie die Beispiele zum maschinellen
Lernen ausführen wollen, verwenden Sie stattdessen

```shell
conda env create --file cam.yaml
```

und aktivieren Sie mit

```shell
conda activate cam
```

Das `cam` Environment enthält zusätzlich Bibliotheken zur Datenanalyse und
-visualisierung, sowie zum maschinellen Lernen, benötigt deswegen aber auch erheblich
mehr Speicherplatz auf der Festplatte.

Wenn Sie pip verwenden können Sie die Requirements mit

```shell
pip install -r requirements.txt
```

installieren.

## Start des Notebook Servers

Viele der Folien und Workshops werden als Jupyter Notebooks zur Verfügung
gestellt. Zum Starten des Notebook Servers wechseln Sie in das `python-course`
Verzeichnis und geben das folgende Kommando ein

```shell
jupyter notebook
```

## Verzeichnisstruktur

- Die Kursmaterialien sind in Deutsch und Englisch verfügbar.
  - Die englischen Materialien befinden sich im Ordner `En`.
  - Die deutschen Materialien befinden sich im Ordner `De`.
- Die Folien befinden sich im Unterordner `Slides`.
- Wenn Sie beim Live-Coding mitmachen wollen, können Sie die Notizbücher im
  Ordner `Codealong` verwenden. Dies sind die gleichen Notizbücher wie im Ordner
  `Slides`, aber mit meist leeren Codezellen.
- Die Workshops befinden sich im Unterordner `Workshops`.
- Die Lösungen für alle Workshops befinden sich im Ordner `Solutions`.

## Verwenden der Kursmaterialien mit VS Code oder PyCharm

VS Code oder PyCharm können direkt mit jupyter notebooks arbeiten, falls Sie
lieber eine dieser Entwicklungsumgebungen verwenden, müssen Sie keinen Jupyter
Server starten; Sie können die Notebooks direkt in Ihrer IDE öffnen.

## Lizenz

![](https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png) [Dr. Matthias
Hölzl](https://github.com/hoelzl)

Dieses Werk von [Dr. Matthias Hölzl](https://github.com/hoelzl) ist lizenziert unter
einer [Creative Commons Namensnennung - Nicht kommerziell - Keine Bearbeitungen 4.0
International Lizenz](http://creativecommons.org/licenses/by-nc-nd/4.0/).

