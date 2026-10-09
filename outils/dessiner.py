#!/usr/bin/env python3
"""Les images du profil, engendrees ici et nulle part ailleurs : le bandeau (un reseau de spins dont
la precession dessine une onde de spin, traverse par un reseau de neurones), les cartes des
domaines et le pied de page. SVG animes en CSS, lisibles par GitHub dans une balise img.

    python3 outils/dessiner.py        # ecrit assets/*.svg

Auteur : Brice Kengni Zanguim
"""
import math
import random
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
NUIT, ABYSSE, MARINE, CYAN, TEXTE, DOUX = "#070D1A", "#0B1730", "#1E3A8A", "#22D3EE", "#E8ECF3", "#8FA3C0"
VERT = "#34D399"
POLICE = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"


def fleche(x, y, long, couleur, ep):
    """Un spin : une fleche verticale centree en (x, y)."""
    h = long / 2
    return (f'<line x1="{x:.1f}" y1="{y + h:.1f}" x2="{x:.1f}" y2="{y - h + 3:.1f}" stroke="{couleur}" '
            f'stroke-width="{ep}" stroke-linecap="round"/>'
            f'<path d="M{x - 4:.1f} {y - h + 6:.1f} L{x:.1f} {y - h:.1f} L{x + 4:.1f} {y - h + 6:.1f}" fill="none" '
            f'stroke="{couleur}" stroke-width="{ep}" stroke-linecap="round" stroke-linejoin="round"/>')


def bandeau(cible):
    L, H = 1200, 320
    pas, periode = 40, 7.0
    morceaux = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{H}" viewBox="0 0 {L} {H}" role="img" '
                f'aria-label="Brice Kengni Zanguim">',
                '<defs>',
                f'<linearGradient id="ciel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NUIT}"/>'
                f'<stop offset="0.6" stop-color="{ABYSSE}"/><stop offset="1" stop-color="{MARINE}"/></linearGradient>',
                f'<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{CYAN}" stop-opacity="0.35"/>'
                f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>',
                f'<linearGradient id="voile" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{NUIT}" stop-opacity="0.92"/>'
                f'<stop offset="0.55" stop-color="{NUIT}" stop-opacity="0.55"/><stop offset="1" stop-color="{NUIT}" stop-opacity="0"/></linearGradient>',
                f'<linearGradient id="nom" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{TEXTE}"/>'
                f'<stop offset="1" stop-color="{CYAN}"/></linearGradient>',
                '<clipPath id="cadre"><rect width="1200" height="320" rx="18"/></clipPath>',
                '</defs>',
                '<style>',
                f'.spin{{transform-box:fill-box;transform-origin:center;animation:precession {periode}s linear infinite}}',
                '@keyframes precession{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}',
                '.lien{stroke-dasharray:6 10;animation:flux 3.2s linear infinite}',
                '@keyframes flux{to{stroke-dashoffset:-64}}',
                '.noeud{transform-box:fill-box;transform-origin:center;animation:pouls 2.8s ease-in-out infinite}',
                '@keyframes pouls{0%,100%{opacity:.55;transform:scale(1)}50%{opacity:1;transform:scale(1.35)}}',
                '.entree{opacity:0;animation:entree 1.4s ease-out forwards}',
                '@keyframes entree{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}',
                '.balayage{animation:balayage 9s ease-in-out infinite}',
                '@keyframes balayage{0%{transform:translateX(-300px)}100%{transform:translateX(1500px)}}',
                '@media (prefers-reduced-motion:reduce){.spin,.lien,.noeud,.balayage{animation:none}.entree{opacity:1;animation:none}}',
                '</style>',
                '<g clip-path="url(#cadre)">',
                f'<rect width="{L}" height="{H}" fill="url(#ciel)"/>',
                '<ellipse class="balayage" cx="0" cy="160" rx="260" ry="200" fill="url(#halo)"/>']
    # Le reseau de spins : la phase de chaque spin avance avec l'abscisse, d'ou une onde qui court.
    for j in range(H // pas + 1):
        for i in range(L // pas + 1):
            x, y = i * pas + 20, j * pas + 20
            phase = (i * 0.55 + j * 0.18) % (2 * math.pi)
            retard = -periode * phase / (2 * math.pi)
            proche = abs(j * pas + 20 - H / 2) / (H / 2)
            op = (0.22 + 0.33 * (1 - proche)) * (0.45 if x > 820 else 1.0)
            couleur = CYAN if (i + j) % 7 else VERT
            morceaux.append(f'<g class="spin" style="animation-delay:{retard:.2f}s" opacity="{op:.2f}">'
                            f'{fleche(x, y, 22, couleur, 1.6)}</g>')
    # Le reseau de neurones, a droite : trois couches reliees, l'information qui circule.
    random.seed(7)
    couches = [[(860, 90), (860, 160), (860, 230)], [(970, 70), (970, 135), (970, 200), (970, 265)],
               [(1080, 120), (1080, 200)]]
    for a, b in zip(couches, couches[1:]):
        for p in a:
            for q in b:
                morceaux.append(f'<line class="lien" x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="{CYAN}" '
                                f'stroke-opacity="0.45" stroke-width="1.3" style="animation-delay:-{random.random() * 3:.2f}s"/>')
    for c in couches:
        for p in c:
            morceaux.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="9" fill="{ABYSSE}" stroke="{CYAN}" stroke-width="2"/>')
            morceaux.append(f'<circle class="noeud" cx="{p[0]}" cy="{p[1]}" r="4" fill="{CYAN}" '
                            f'style="animation-delay:-{random.random() * 2.8:.2f}s"/>')
    # Le texte, sur un voile qui l'isole du reseau.
    morceaux += [f'<rect width="760" height="{H}" fill="url(#voile)"/>',
                 f'<g class="entree" style="animation-delay:.2s"><text x="64" y="138" font-family="{POLICE}" font-size="56" '
                 f'font-weight="700" fill="url(#nom)" letter-spacing="1">Brice Kengni Zanguim</text></g>',
                 f'<g class="entree" style="animation-delay:.6s"><rect x="66" y="160" width="96" height="4" rx="2" fill="{CYAN}"/></g>',
                 f'<g class="entree" style="animation-delay:.9s"><text x="64" y="206" font-family="{POLICE}" font-size="24" '
                 f'font-weight="600" fill="{TEXTE}">Theoretical Physics  |  Quantum Magnetism</text></g>',
                 f'<g class="entree" style="animation-delay:1.2s"><text x="64" y="244" font-family="{POLICE}" font-size="24" '
                 f'font-weight="600" fill="{TEXTE}">Machine Learning  |  Software &amp; Applications</text></g>',
                 f'<g class="entree" style="animation-delay:1.5s"><text x="64" y="282" font-family="{POLICE}" font-size="16" '
                 f'fill="{DOUX}">Physique théorique, magnétisme quantique, apprentissage automatique, logiciel</text></g>',
                 '</g>',
                 f'<rect x="0.5" y="0.5" width="1199" height="319" rx="18" fill="none" stroke="{MARINE}"/>',
                 '</svg>']
    cible.write_text("\n".join(morceaux), encoding="utf-8")


def _icone(contenu, style=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">'
            '<defs><radialGradient id="f" cx="0.5" cy="0.35" r="0.75"><stop offset="0" stop-color="' + MARINE + '"/>'
            '<stop offset="1" stop-color="' + NUIT + '"/></radialGradient></defs>'
            '<style>' + style + '@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>'
            '<rect x="2" y="2" width="124" height="124" rx="28" fill="url(#f)" stroke="' + CYAN + '" stroke-opacity="0.5" stroke-width="2"/>'
            + contenu + '</svg>')


def domaines():
    """Quatre icones animees, une par domaine."""
    # Physique theorique : une orbite qui tourne autour d'un noyau, et un paquet d'onde.
    physique = _icone(
        '<g class="o"><ellipse cx="64" cy="64" rx="44" ry="16" fill="none" stroke="' + CYAN + '" stroke-width="3"/>'
        '<circle cx="108" cy="64" r="5" fill="' + VERT + '"/></g>'
        '<g class="o2"><ellipse cx="64" cy="64" rx="44" ry="16" fill="none" stroke="' + CYAN + '" stroke-opacity="0.6" stroke-width="3"/></g>'
        '<circle cx="64" cy="64" r="8" fill="' + TEXTE + '"/>',
        '.o{transform-origin:64px 64px;animation:t 9s linear infinite}.o2{transform-origin:64px 64px;transform:rotate(60deg);animation:t2 12s linear infinite}'
        '@keyframes t{to{transform:rotate(360deg)}}@keyframes t2{from{transform:rotate(60deg)}to{transform:rotate(420deg)}}')
    # Magnetisme quantique : trois spins antiparalleles qui precessent en opposition.
    spins = ""
    for i, x in enumerate((34, 64, 94)):
        sens = "p" if i % 2 == 0 else "q"
        spins += (f'<g class="{sens}" style="transform-origin:{x}px 64px">'
                  f'<line x1="{x}" y1="86" x2="{x}" y2="44" stroke="{CYAN if i % 2 == 0 else VERT}" stroke-width="5" stroke-linecap="round"/>'
                  f'<path d="M{x - 9} 52 L{x} 40 L{x + 9} 52" fill="none" stroke="{CYAN if i % 2 == 0 else VERT}" stroke-width="5" '
                  'stroke-linecap="round" stroke-linejoin="round"/></g>'
                  f'<circle cx="{x}" cy="64" r="4" fill="{TEXTE}"/>')
    magnetisme = _icone(spins, '.p{animation:a 4s ease-in-out infinite}.q{transform:rotate(180deg);animation:b 4s ease-in-out infinite}'
                        '@keyframes a{0%,100%{transform:rotate(-18deg)}50%{transform:rotate(18deg)}}'
                        '@keyframes b{0%,100%{transform:rotate(198deg)}50%{transform:rotate(162deg)}}')
    # Machine learning : un petit reseau dont les liens portent un flux.
    noeuds = [(34, 44), (34, 84), (64, 34), (64, 64), (64, 94), (94, 64)]
    liens = [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (4, 5)]
    ml = "".join(f'<line class="l" x1="{noeuds[a][0]}" y1="{noeuds[a][1]}" x2="{noeuds[b][0]}" y2="{noeuds[b][1]}" stroke="{CYAN}" '
                 f'stroke-width="2.5" style="animation-delay:-{k * 0.35:.2f}s"/>' for k, (a, b) in enumerate(liens))
    ml += "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{NUIT}" stroke="{TEXTE}" stroke-width="3"/>' for x, y in noeuds)
    ml = _icone(ml, '.l{stroke-dasharray:5 7;animation:f 1.6s linear infinite}@keyframes f{to{stroke-dashoffset:-24}}')
    # Logiciel : des chevrons et un curseur qui clignote.
    logiciel = _icone(
        f'<path d="M48 42 L26 64 L48 86" fill="none" stroke="{CYAN}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="M80 42 L102 64 L80 86" fill="none" stroke="{CYAN}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<rect class="c" x="58" y="50" width="12" height="28" rx="2" fill="{VERT}"/>',
        '.c{animation:c 1.1s steps(2,start) infinite}@keyframes c{to{opacity:0}}')
    for nom, svg in (("physique", physique), ("magnetisme", magnetisme), ("ml", ml), ("logiciel", logiciel)):
        (ASSETS / f"domaine-{nom}.svg").write_text(svg, encoding="utf-8")


def separateur(cible, L=1200, H=24):
    """Un filet qui s'allume d'un bout a l'autre."""
    cible.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{H}" viewBox="0 0 {L} {H}">'
        f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient></defs>'
        '<style>.b{animation:b 4.5s ease-in-out infinite}@keyframes b{from{transform:translateX(-400px)}to{transform:translateX(1200px)}}'
        '@media (prefers-reduced-motion:reduce){.b{animation:none}}</style>'
        f'<rect x="0" y="{H / 2 - 0.5}" width="{L}" height="1" fill="{MARINE}"/>'
        f'<rect class="b" x="0" y="{H / 2 - 1}" width="400" height="2" fill="url(#g)"/>'
        f'<circle cx="{L / 2}" cy="{H / 2}" r="4" fill="{NUIT}" stroke="{CYAN}" stroke-width="2"/></svg>', encoding="utf-8")


def pied(cible, L=1200, H=120):
    """Le pied : une onde de spin couchee, qui ondule lentement, et une signature."""
    import math as m
    pts = " ".join(f"{x},{H / 2 + 14 * m.sin(x / 60):.1f}" for x in range(0, L + 1, 10))
    fleches = ""
    for i in range(0, L // 40 + 1):
        x = i * 40 + 20
        a = m.degrees(m.sin(x / 60)) * 0.9
        fleches += (f'<g transform="rotate({a:.1f} {x} {H / 2 + 14 * m.sin(x / 60):.1f})">'
                    + fleche(x, H / 2 + 14 * m.sin(x / 60), 18, CYAN, 1.4) + '</g>')
    cible.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{H}" viewBox="0 0 {L} {H}">'
        '<style>.v{animation:v 6s ease-in-out infinite alternate}@keyframes v{from{transform:translateX(-40px)}to{transform:translateX(40px)}}'
        '@media (prefers-reduced-motion:reduce){.v{animation:none}}</style>'
        f'<rect width="{L}" height="{H}" rx="18" fill="{NUIT}"/>'
        f'<g class="v" opacity="0.55"><polyline points="{pts}" fill="none" stroke="{MARINE}" stroke-width="2"/>{fleches}</g>'
        f'<text x="{L / 2}" y="{H - 16}" text-anchor="middle" font-family="{POLICE}" font-size="14" fill="{DOUX}">'
        'Brice Kengni Zanguim  |  quantum magnetism and machine learning</text></svg>', encoding="utf-8")


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    bandeau(ASSETS / "bandeau.svg")
    domaines()
    separateur(ASSETS / "separateur.svg")
    pied(ASSETS / "pied.svg")
    print("\n".join(sorted(f.name for f in ASSETS.glob("*.svg"))))
