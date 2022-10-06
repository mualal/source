import os

with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'parts',
    '2022_09_28.tex'),
    'a+',
    encoding='utf-8'
) as f:
    f.write('\documentclass[main.tex]{subfiles}\n')
    f.write('\n')
    f.write('\\begin{document}\n')
    f.write('\n')
    f.write('% \\textcolor{red}{Вводная лекция}\n')
    f.write('\n')
    f.write('\\section{Практика 28.09.2022 (Базыров И.Ш.)}\n')
    f.write('\n')
    for i in range(1, 231):
        f.write('\\begin{center}\n')
        f.write('\includegraphics[width=.95\\textwidth, page=' + str(i) + ']{Training_Tempest_7_0_v04.pdf}\n')
        f.write('\\end{center}\n')
        f.write('\n')
    f.write('\end{document}')
