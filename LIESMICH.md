# Material für Python Kurse

Notebooks und Code für die Kurse "Einführung in Python", "Python für Programmierer",
"Fortgeschrittenenkurs Python" und Python als Skriptsprache der Coding Akademie München.

Verwenden Sie bitte den Befehl

```shell
$ git clone --recursive https://github.com/hoelzl/python-programmierer.git
```

zum Clonen des Repositories (Beachten Sie das Argument `--recursive`).

Ein Anaconda Environment können Sie mit den Befehlen

```shell
cd python-programmierer
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

Zum Starten des Notebook Servers verwenden Sie das Kommando

```shell
jupyter notebook
```

## Lizenz

![](https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png) [Dr. Matthias
Hölzl](https://github.com/hoelzl)

Dieses Werk von [Dr. Matthias Hölzl](https://github.com/hoelzl) ist lizenziert unter
einer [Creative Commons Namensnennung - Nicht kommerziell - Keine Bearbeitungen 4.0
International Lizenz](http://creativecommons.org/licenses/by-nc-nd/4.0/).

