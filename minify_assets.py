"""
Script de minification des assets CSS et JavaScript
Pour la production, utilisez ce script avant le déploiement
"""

import re
from pathlib import Path


def minify_css(css_content):
    """
    Minifie le contenu CSS
    
    Args:
        css_content: Contenu CSS à minifier
    
    Returns:
        CSS minifié
    """
    # Supprimer les commentaires
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Supprimer les espaces et sauts de ligne
    css_content = re.sub(r'\s+', ' ', css_content)
    # Supprimer les espaces autour des caractères spéciaux
    css_content = re.sub(r'\s*([{}:;,])\s*', r'\1', css_content)
    # Supprimer les points-virgules de fin
    css_content = re.sub(r';}', '}', css_content)
    return css_content.strip()


def minify_js(js_content):
    """
    Minifie le contenu JavaScript
    
    Args:
        js_content: Contenu JavaScript à minifier
    
    Returns:
        JavaScript minifié
    """
    # Supprimer les commentaires sur une ligne
    js_content = re.sub(r'//.*', '', js_content)
    # Supprimer les commentaires multilignes
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    # Supprimer les espaces et sauts de ligne
    js_content = re.sub(r'\s+', ' ', js_content)
    # Supprimer les espaces autour des opérateurs
    js_content = re.sub(r'\s*([=+\-*/%&|^<>!?:;,{}()[\]])\s*', r'\1', js_content)
    return js_content.strip()


def minify_file(input_path, output_path=None, minifier=None):
    """
    Minifie un fichier
    
    Args:
        input_path: Chemin du fichier d'entrée
        output_path: Chemin du fichier de sortie (optionnel)
        minifier: Fonction de minification (minify_css ou minify_js)
    """
    input_path = Path(input_path)
    
    if output_path is None:
        output_path = input_path.with_suffix(input_path.suffix + '.min')
    else:
        output_path = Path(output_path)
    
    # Lire le fichier
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Minifier
    if minifier:
        minified = minifier(content)
    else:
        # Déterminer le type de fichier
        if input_path.suffix == '.css':
            minified = minify_css(content)
        elif input_path.suffix == '.js':
            minified = minify_js(content)
        else:
            raise ValueError(f"Type de fichier non supporté: {input_path.suffix}")
    
    # Écrire le fichier minifié
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    
    original_size = len(content)
    minified_size = len(minified)
    reduction = (1 - minified_size / original_size) * 100
    
    print(f"✓ {input_path.name} → {output_path.name}")
    print(f"  Original: {original_size:,} octets")
    print(f"  Minifié: {minified_size:,} octets")
    print(f"  Réduction: {reduction:.1f}%")
    print()


def minify_all_assets():
    """Minifie tous les assets CSS et JS du projet"""
    project_root = Path(__file__).parent
    
    # Fichiers CSS à minifier
    css_files = [
        project_root / 'style.css',
        project_root / 'static' / 'style.css',
    ]
    
    # Fichiers JS à minifier
    js_files = [
        project_root / 'script.js',
        project_root / 'static' / 'js' / 'script.js',
    ]
    
    print("=== Minification des fichiers CSS ===\n")
    for css_file in css_files:
        if css_file.exists():
            try:
                minify_file(css_file, minifier=minify_css)
            except Exception as e:
                print(f"✗ Erreur avec {css_file}: {e}\n")
    
    print("\n=== Minification des fichiers JavaScript ===\n")
    for js_file in js_files:
        if js_file.exists():
            try:
                minify_file(js_file, minifier=minify_js)
            except Exception as e:
                print(f"✗ Erreur avec {js_file}: {e}\n")
    
    print("\n=== Minification terminée ===")
    print("\nPour utiliser les fichiers minifiés en production:")
    print("1. Remplacez les liens vers les fichiers originaux par les fichiers .min")
    print("2. Ou configurez votre serveur pour servir les fichiers minifiés")


if __name__ == '__main__':
    minify_all_assets()
