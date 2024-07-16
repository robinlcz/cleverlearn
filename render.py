import os
import re
file_path= "./LimitesSuites/limitesSuites.tex"

def latex_to_html(latex_str):
    # Dictionnaire des commandes LaTeX et leurs équivalents HTML
    replacements = {
        r'\\textbf{([^}]*)}': r'<strong>\1</strong>',
        r'\\textit{([^}]*)}': r'<em>\1</em>',
        r'\\underline{([^}]*)}': r'<u>\1</u>',
        r'\\section{([^}]*)}': r'<h1>\1</h1>',
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
        r'\\hphtantom{' : r'',
        r'\\end{remark}' : r'',
        r'\\end{theo}' : r'',
        r'\\end{exo}' : r'',
        r'\\end{corr}' : r'',
        r'\\end{prop}' : r'',
        r'\\end{deff}' : r'',
    }

    # Appliquer les remplacements
    html_str = latex_str
    for latex, html in replacements.items():
        html_str = re.sub(latex, html, html_str)

    # Gestion des tableaux
    html_str = convert_tabular_to_html(html_str)


    # Gestion des lignes nouvelles
    html_str = html_str.replace('\n', '<br>')

    return html_str

def convert_tabular_to_html(latex_str):
    tabular_pattern = re.compile(r'\\begin{tabular}{([^}]*)}(.*?)\\end{tabular}', re.DOTALL)
    tabulars = tabular_pattern.findall(latex_str)
    
    for tabular in tabulars:
        column_format, table_content = tabular
        html_table = '<table border="1">\n'

        # Traitement des lignes
        rows = table_content.strip().split(r'\\')
        for row in rows:
            html_table += '  <tr>\n'
            columns = row.split('&')
            for column in columns:
                html_table += f'    <td>{column.strip()}</td>\n'
            html_table += '  </tr>\n'

        html_table += '</table>\n'

        latex_str = latex_str.replace(
            f'\\begin{tabular}{{{column_format}}}{table_content}\\end{tabular}',
            html_table
        )

    return latex_str

def main():
    with open(file_path, 'r') as file:
        src = file.read()
        
        section = src.split('\section')
        
        

    file.close()
     
    for i in range(3): 
        # Créer une page HTML
        html_page = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Chapitre 1 </title>
            <script src="mathjax-config.js" defer></script>
            <script id="MathJax-script" async
                src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
            </script>
        </head>
        <body>
        <p>
            {latex_to_html(section[1])}
        </p>
        </body>
        </html>
        """
    
        html_file_path = 'index.html'
        
        with open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_page)
main()