# absichtlich problematischer code fuer uebung 11
# damit bandit und ruff im bericht etwas anzeigen
import os
import subprocess
import pickle

passwort = "geheim123"  # hardcodiertes passwort -> bandit B105

def rechne(ausdruck):
    # eval ist unsicher -> bandit B307
    return eval(ausdruck)

def befehl_ausfuehren(cmd):
    # shell=True ist unsicher -> bandit B602
    return subprocess.call(cmd, shell=True)

def lade_daten(datei):
    # pickle.load ist unsicher -> bandit B301
    with open(datei, "rb") as f:
        return pickle.load(f)

x = None
if x == None:  # sollte 'is None' sein -> findet ruff (E711)
    pass
