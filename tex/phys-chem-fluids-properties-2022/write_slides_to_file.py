import os

with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'parts',
    '2022_10_25.tex'),
    'a+',
    encoding='utf-8'
) as f:
    f.write('\documentclass[main.tex]{subfiles}\n')
    f.write('\n')
    f.write('\\begin{document}\n')
    f.write('\n')
    f.write('\\section{Лекция 25.10.2022 (Брусиловский А.И.)}\n')
    f.write('\n')
    for i in range(69, 305):
        f.write('\\begin{center}\n')
        f.write('\includegraphics[width=\\textwidth]{jpg_slide'+str(i)+'}'+'\n')
        f.write('\\end{center}\n')
        f.write('\n')
    f.write('\end{document}')
