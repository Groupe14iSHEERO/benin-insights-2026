"""
Traducteur de fichier TXT à deux colonnes (Anglais → Français)
Utilise l'API googletrans (gratuite) ou deep-translator comme alternative.

Installation :
    pip install deep-translator

Usage :
    python traduire_colonnes.py input.txt output.txt

Format du fichier d'entrée (séparateur = tabulation ou virgule) :
    hello	world
    good morning	have a nice day
"""

import sys
import time
import argparse

# ─── Détection automatique du séparateur ─────────────────────────────────────

def detecter_separateur(ligne: str) -> str:
    """Devine le séparateur : tabulation, virgule, point-virgule ou pipe."""
    for sep in ("\t", ",", ";", "|"):
        if sep in ligne:
            return sep
    return "\t"  # défaut

# ─── Traduction ───────────────────────────────────────────────────────────────

def traduire_texte(texte: str, traducteur) -> str:
    """Traduit un texte en français, retourne l'original en cas d'échec."""
    if not texte.strip():
        return texte
    try:
        return traducteur.translate(texte)
    except Exception as e:
        print(f"  ⚠️  Erreur de traduction pour '{texte}': {e}", file=sys.stderr)
        return texte

# ─── Traitement du fichier ────────────────────────────────────────────────────

def traduire_fichier(
    chemin_entree: str,
    chemin_sortie: str,
    encodage: str = "utf-8",
    delai: float = 0.5,
    colonne: int = 0,          # 0 = toutes les colonnes, 1 = col 1 seulement, 2 = col 2 seulement
):
    """
    Lit le fichier d'entrée, traduit les colonnes demandées et écrit le résultat.

    Args:
        chemin_entree : chemin du fichier source
        chemin_sortie : chemin du fichier de destination
        encodage      : encodage du fichier (défaut utf-8)
        delai         : pause entre chaque ligne (évite le blocage API)
        colonne       : 0=toutes, 1=première colonne, 2=deuxième colonne
    """
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("Module 'deep-translator' non installé.")
        print("Exécutez : pip install deep-translator")
        sys.exit(1)

    traducteur = GoogleTranslator(source="en", target="fr")

    with open(chemin_entree, "r", encoding=encodage) as f_in:
        lignes = f_in.readlines()

    if not lignes:
        print("Fichier vide.")
        return

    sep = detecter_separateur(lignes[0])
    print(f"Fichier : {chemin_entree}")
    print(f"Séparateur détecté : {repr(sep)}")
    print(f"Traduction EN → FR  ({len(lignes)} lignes)\n")

    resultats = []
    for i, ligne in enumerate(lignes, start=1):
        ligne = ligne.rstrip("\n")
        parties = ligne.split(sep, maxsplit=1)  # max 2 colonnes

        if len(parties) == 2:
            col1, col2 = parties

            if colonne == 0:          # toutes les colonnes
                col1_fr = traduire_texte(col1.strip(), traducteur)
                col2_fr = traduire_texte(col2.strip(), traducteur)
            elif colonne == 1:        # première colonne seulement
                col1_fr = traduire_texte(col1.strip(), traducteur)
                col2_fr = col2
            else:                     # deuxième colonne seulement
                col1_fr = col1
                col2_fr = traduire_texte(col2.strip(), traducteur)

            nouvelle_ligne = f"{col1_fr}{sep}{col2_fr}"
        else:
            # Ligne à une seule colonne ou vide
            nouvelle_ligne = traduire_texte(ligne, traducteur) if ligne.strip() else ligne

        resultats.append(nouvelle_ligne)
        print(f"  [{i:>4}/{len(lignes)}] {ligne[:50]:<50} →  {nouvelle_ligne[:50]}")
        time.sleep(delai)

    with open(chemin_sortie, "w", encoding=encodage) as f_out:
        f_out.write("\n".join(resultats))

    print(f"\n✅  Traduction terminée → {chemin_sortie}")

# ─── Interface en ligne de commande ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Traduit un fichier TXT à deux colonnes (anglais → français)."
    )
    parser.add_argument("entree",  help="Fichier TXT source (anglais)")
    parser.add_argument("sortie",  help="Fichier TXT de destination (français)")
    parser.add_argument(
        "--encodage", default="utf-8",
        help="Encodage du fichier (défaut : utf-8)"
    )
    parser.add_argument(
        "--delai", type=float, default=0.05,
        help="Délai en secondes entre chaque requête (défaut : 0.5)"
    )
    parser.add_argument(
        "--colonne", type=int, choices=[0, 1, 2], default=2,
        help="0 = toutes les colonnes (défaut), 1 = colonne 1, 2 = colonne 2"
    )

    args = parser.parse_args()
    traduire_fichier(
        args.entree,
        args.sortie,
        encodage=args.encodage,
        delai=args.delai,
        colonne=args.colonne,
    )

if __name__ == "__main__":
    main()
