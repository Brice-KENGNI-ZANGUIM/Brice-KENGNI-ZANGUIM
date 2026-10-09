# Mettre ce profil en ligne

GitHub affiche en tête de votre page de profil le fichier `README.md` d'un dépôt **public** qui porte
**exactement** votre nom d'utilisateur. Ici : `Brice-KENGNI-ZANGUIM/Brice-KENGNI-ZANGUIM`.

## 1. Créer le dépôt spécial

Sur github.com : bouton « New repository », nom `Brice-KENGNI-ZANGUIM`, visibilité **Public**, sans
README ni licence (ce dossier les apporte). GitHub signale alors que c'est un dépôt spécial.

## 2. Envoyer ce dossier

Depuis ce dossier (`previews/profil-github/`), qui est déjà un dépôt git avec un premier commit :

    git remote add origin git@github.com:Brice-KENGNI-ZANGUIM/Brice-KENGNI-ZANGUIM.git
    git push -u origin main

Le bandeau, la présentation animée, les badges, les projets, les statistiques et les séries de
contributions s'affichent aussitôt. Les deux images produites par les workflows arrivent à l'étape 4.

## 3. Le jeton des métriques

Le workflow « Métriques du profil » lit votre activité par l'API de GitHub.

1. github.com > Settings > Developer settings > Personal access tokens > Tokens (classic) >
   « Generate new token (classic) ».
2. Nom : `metriques-profil` ; expiration : à votre choix (sans expiration, il ne faudra jamais le
   renouveler) ; cases : `read:user` et `public_repo`. Cochez `repo` en entier si les métriques
   doivent compter aussi vos dépôts privés.
3. Copiez le jeton, puis dans le dépôt `Brice-KENGNI-ZANGUIM` : Settings > Secrets and variables >
   Actions > « New repository secret », nom `METRICS_TOKEN`, valeur : le jeton.

## 4. Lancer les trois workflows une première fois

Dépôt `Brice-KENGNI-ZANGUIM` > onglet Actions :

- « Métriques du profil » > « Run workflow » : écrit `metrics/general.svg` (calendrier de l'année,
  langages, habitudes de travail, distinctions) ;
- « Animation des contributions » > « Run workflow » : crée la branche `output` avec l'animation du
  calendrier, en thème clair et en thème sombre ;
- « Indicateurs du profil » > « Run workflow » : relève vos dépôts (privés compris), vos langages,
  vos années sur GitHub et toutes vos contributions, puis redessine le panneau « In numbers ».

Si un workflow échoue sur un refus d'écriture : Settings > Actions > General > Workflow permissions >
« Read and write permissions ».

Ensuite, les trois se relancent seuls chaque nuit (3 h 17, 3 h 41 et 4 h 05, heure UTC).

## 5. Modifier

- **Le texte** : la section « Profil » et les trois domaines, dans `README.md`.
- **Les lignes animées** : le paramètre `lines=` de l'adresse `readme-typing-svg` ; lignes séparées
  par `;`, espaces écrits `+`, lettres accentuées encodées (`é` = `%C3%A9`, `è` = `%C3%A8`).
- **Les projets** : le tableau « Projets choisis ». Un projet privé ne s'y met pas, le lien
  serait mort pour le visiteur.
- **Les couleurs** : nuit `0B1220`, marine `1E3A8A`, cyan `22D3EE`, texte `E8ECF3`, reprises dans
  toutes les adresses d'images ; en changer une, c'est la remplacer partout.
- **Le courriel** : le badge « Contact » ; retirez la ligne pour ne pas l'exposer.
- **Épingler** : sur votre profil, « Customize your pins », pour mettre en avant six dépôts sous
  le README.

## Les images dessinées pour ce profil

Le bandeau, les titres de section, les icônes des domaines, l'orbite des outils, le panneau des
indicateurs, le séparateur et le pied sortent tous de `outils/dessiner.py`. Pour changer un texte ou
une couleur : modifier ce fichier, lancer `python3 outils/dessiner.py`, commiter `assets/`.

## Ce que chaque image appelle

| Image | Service | Remarque |
| --- | --- | --- |
| Bandeau haut et bas | capsule-render.vercel.app | service public |
| Présentation animée | readme-typing-svg.demolab.com | service public |
| Badges | img.shields.io | service public |
| Visites | komarev.com | compte à chaque affichage |
| Statistiques | github-readme-stats.vercel.app | service public, parfois saturé |
| Séries de contributions | streak-stats.demolab.com | service public |
| Métriques complètes | lowlighter/metrics, dans vos Actions | image hébergée dans le dépôt |
| Animation du calendrier | Platane/snk, dans vos Actions | image hébergée dans le dépôt |

Les deux dernières ne dépendent d'aucun service tiers une fois produites : ce sont les plus sûres.
