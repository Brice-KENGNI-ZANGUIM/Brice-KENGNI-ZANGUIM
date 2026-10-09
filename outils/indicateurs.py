#!/usr/bin/env python3
"""Releve les indicateurs du profil sur GitHub et les ecrit dans metrics/kpi.json, que
outils/dessiner.py lit pour dessiner assets/kpi.svg. Lance chaque nuit par le workflow
"Indicateurs du profil" ; a la main : METRICS_TOKEN=... python3 outils/indicateurs.py

Sans jeton, seuls les depots publics se voient et les contributions gardent leur derniere valeur.

Auteur : Brice Kengni Zanguim
"""
import datetime as dt
import json
import os
import urllib.request
from pathlib import Path

UTILISATEUR = "Brice-KENGNI-ZANGUIM"
SORTIE = Path(__file__).resolve().parent.parent / "metrics" / "kpi.json"
JETON = os.environ.get("METRICS_TOKEN", "")


def appeler(url, corps=None):
    entetes = {"Accept": "application/vnd.github+json", "User-Agent": UTILISATEUR}
    if JETON:
        entetes["Authorization"] = f"Bearer {JETON}"
    donnees = json.dumps(corps).encode() if corps is not None else None
    with urllib.request.urlopen(urllib.request.Request(url, data=donnees, headers=entetes), timeout=30) as r:
        return json.load(r)


def depots():
    url = ("https://api.github.com/user/repos?affiliation=owner&per_page=100&page={}" if JETON
           else f"https://api.github.com/users/{UTILISATEUR}/repos?per_page=100&page={{}}")
    tous, page = [], 1
    while True:
        lot = appeler(url.format(page))
        tous += lot
        if len(lot) < 100:
            return [d for d in tous if not d["fork"]]
        page += 1


def contributions(depuis):
    """Toutes les contributions depuis la creation du compte, annee par annee (l'API les borne a un an)."""
    total, debut = 0, depuis
    maintenant = dt.datetime.now(dt.timezone.utc)
    while debut < maintenant:
        fin = min(debut + dt.timedelta(days=365), maintenant)
        q = ('query($u:String!,$a:DateTime!,$b:DateTime!){user(login:$u){contributionsCollection(from:$a,to:$b)'
             '{contributionCalendar{totalContributions}}}}')
        r = appeler("https://api.github.com/graphql", {"query": q, "variables": {
            "u": UTILISATEUR, "a": debut.isoformat(), "b": fin.isoformat()}})
        total += r["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        debut = fin
    return total


def main():
    ancien = json.loads(SORTIE.read_text(encoding="utf-8")) if SORTIE.exists() else {}
    profil = appeler(f"https://api.github.com/users/{UTILISATEUR}")
    cree = dt.datetime.fromisoformat(profil["created_at"].replace("Z", "+00:00"))
    liste = depots()
    kpi = {
        "depots": len(liste) if JETON or "depots" not in ancien else max(len(liste), ancien["depots"]),
        "langages": len({d["language"] for d in liste if d["language"]}) if JETON or "langages" not in ancien
                    else max(len({d["language"] for d in liste if d["language"]}), ancien["langages"]),
        "annees": (dt.datetime.now(dt.timezone.utc) - cree).days // 365,
        "contributions": contributions(cree) if JETON else ancien.get("contributions", 0),
        "releve": dt.date.today().isoformat(),
    }
    SORTIE.write_text(json.dumps(kpi, indent=1) + "\n", encoding="utf-8")
    print(kpi)


if __name__ == "__main__":
    main()
