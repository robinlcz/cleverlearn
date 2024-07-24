import os
import re
import sys

# Dictionnaire des commandes LaTeX et leurs équivalents HTML
replacements = {
    r'\\textbf{([^}]*)}': r'<strong>\1</strong>',
    r'\\textit{([^}]*)}': r'<em>\1</em>',
    r'\\underline{([^}]*)}': r'<u>\1</u>',
    r'\\section{([^}]*)}': r'<h1>\1</h1>',
    r'\\section*{([^}]*)}': r'<h1>\1</h1>',
    r'\\subsection{([^}]*)}': r'<h2>\1</h2>',
    r'\\subsubsection{([^}]*)}': r'<h3>\1</h3>',
    r'\\begin{itemize}': r'<ul>',
    r'\\end{itemize}': r'</ul>',
    r'\\begin{enumerate}': r'<ol>',
    r'\\end{enumerate}': r'</ol>',
    r'\\item': r'<li>',
    r'\\begin{quote}': r'<blockquote>',
    r'\\end{quote}': r'</blockquote>',
    r'\\begin{verbatim}': r'<pre>',
    r'\\end{verbatim}': r'</pre>',
    r'\\begin{theo}' : r'<h3><strong><u>Théorème</u></strong></h3>',
    r'\\begin{exo}' : r'<h3><strong><u>Exercice</u></strong></h3>',
    r'\\begin{corr}' : r'<h3><strong><u>Correction</u></strong></h3>',
    r'\\begin{prop}' : r'<h3><strong><u>Proposition</u></strong></h3>',
    r'\\begin{deff}' : r'<h3><strong><u>Définition</u></strong></h3>',
    r'\\begin{remark}' : r'<u><em> Remarque : </em></u>',
    r'\\hphantom{([^}]*)}' : r'',
    r'\\end{remark}' : r'',
    r'\\end{theo}' : r'',
    r'\\end{exo}' : r'',
    r'\\end{corr}' : r'',
    r'\\end{prop}' : r'',
    r'\\end{deff}' : r'',
    r'{Entrainement et exercices}' : r'<h2>Entrainement et exercices</h2>',
    r'{Correction des exercices}' : r'',
    r'{Contenu de cours}' : r'<h2>Contenu de cours</h2>',
    r'\\newpage' : r'',
}

# Ensemble gestion des erreurs de frappes
ensCorr = {"co", "cor", "corr", "corri", "corrig", "correxion"}
ensExo = {}

def latex_to_html(latex_str):

    # Appliquer les remplacements
    html_str = latex_str
    for latex, html in replacements.items():
        html_str = re.sub(latex, html, html_str)

    # Gestion des tableaux, images, matrices
    html_str = convert_tabular_to_html(html_str)
    html_str = convert_images_to_html(html_str)

    # Gestion des lignes nouvelles
    html_str = html_str.replace('\n', '<br>')

    return html_str

def convert_tabular_to_html(latex_str):
    tabular_pattern = re.compile(r'\\begin{tabular}{([^}]*)}(.*?)\\end{tabular}', re.DOTALL)
    matches = tabular_pattern.findall(latex_str)
    for match in matches:
        column_format, table_content = match
        html_table = '<table border="1">\n'
        # Traitement des lignes
        rows = table_content.strip().split(r'\\')
        for row in rows:
            row = row.strip()
            if not row:
                continue
            html_table += '  <tr>'
            columns = row.split('&')
            for column in columns:
                column = column.strip()
                # Ignorer les commandes de mise en forme dans les cellules
                column = re.sub(r'\\text{([^}]*)}', r'\1', column)
                column = re.sub(r'\\textbf{([^}]*)}', r'<strong>$\1$</strong>', column)
                column = re.sub(r'\\textit{([^}]*)}', r'<em>$\1$</em>', column)
                column = re.sub(r'\\underline{([^}]*)}', r'<u>$\1$</u>', column)
                html_table += f'    <td>{column}</td>'
            html_table += '  </tr>'

        html_table += '</table>'
        latex_str = latex_str.replace(
            table_content,
            html_table
        )
    latex_str = re.sub(r'\\begin{tabular}{([^}]*)}', r'', latex_str)
    latex_str = re.sub(r'\\end{tabular}', r'', latex_str)
    latex_str = re.sub(r'\\hline', r'', latex_str)
    return latex_str

def convert_images_to_html(latex_str):
    image_pattern = re.compile(r'\\includegraphics(?:\[.*?\])?{([^}]*)}')
    matches = image_pattern.findall(latex_str)
    for match in matches:
        image_path = match
        alt_text = "Image"  # Vous pouvez définir un texte alternatif par défaut ou l'extraire des options LaTeX
        image_html = f'<img src="{image_path}" alt="{alt_text}">'
        
        latex_str = latex_str.replace(f'\\includegraphics{{{image_path}}}', image_html)
    
    return latex_str

def main(arg, path="./"):
    with open(arg, 'r') as file:
        src = file.read()
        
        section = src.split('\section')
    try:
        section[2] = section[2].split(r'\end{exo}')
        section[3] = section[3].split(r'\end{corr}')
    except IndexError:
        print("Pas d'exercice / pas de correction")
    file.close()
    
    # Ajout des nouveaux théorèmes 
    theorem_pattern = re.compile(r'\\newtheorem{([^}]*)}{([^}]*)}')
    matches = theorem_pattern.findall(section[0])
    for match in matches:
        theorem_label, theorem_name = match
        # Remplacement dans le contenu
        replacements[rf'\\begin{{{theorem_label}}}'] = rf'<h3><strong>{theorem_name}:</strong></h3>'
        replacements[rf'\\end{{{theorem_label}}}'] = rf''
    
    
    # Créer une page HTML
    html_page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chapitre 1 </title>
        <script src="/Users/rlcz/Desktop/cleaverlearn/Fiches/mathjax-config.js" defer></script>
        <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
        </script>
    </head>
    <body>
    <a href="exo.html">Liste d'exercice</a>
    <p>
        {latex_to_html(section[1])}
    </p>
    </body>
    </html>
    """
        
    html_file_path = path + 'index.html'
    html_file_path2 = path + 'exo.html'
    html_page2 = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exercice Chapitre 1 </title>
        <script src="/Users/rlcz/Desktop/cleaverlearn/Fiches/mathjax-config.js" defer></script>
        <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
        </script>
    </head>
    <body>
    <a href="index.html">Cours</a>
    <p>
    """
    try:
        for i in range(len(section[2])):
            html_page2 += f"{latex_to_html(section[2][i])} {latex_to_html(section[3][i])}"
        html_page2 += f"""</p>
                        </body>
                        </html>"""


    except IndexError:
        print("Pas d'exercices pour cette fiche")
        html_page2 += f"""</p>
                        </body>
                        </html>"""
        
        
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_page)
            
        html_file.close()
    with open(html_file_path2, 'w', encoding='utf-8') as html_file:
        html_file.write(html_page2)
        
        html_file.close()

args = sys.argv[1:]
main(args[0],args[1])