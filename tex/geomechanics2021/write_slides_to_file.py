import os

with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
    'parts',
    '2021_11_11.tex'),
    'a+',
    encoding='utf-8'
) as f:
    f.write('\documentclass[main.tex]{subfiles}\n')
    f.write('\n')
    f.write('\\begin{document}\n')
    f.write('\n')
    f.write('\\section{Лекция 11.11.2021 (Жигульский С.В.)}\n')
    f.write('\n')
    for i in range(1, 52):
        f.write('\\begin{center}\n')
        f.write('\includegraphics[width=.95\\textwidth, page=' + str(i) + ']{Geomechanics_course_1.pdf}\n')
        f.write('\\end{center}\n')
        f.write('\n')
    f.write('\end{document}')
