# Bopytex

Bopytex is a command line tool for producing random math exercises with their correction. It embeds [mapytex](https://git.opytex.org/lafrite/Mapytex) and [python](python.org) into [latex](latex-project.org) through [jinja](jinja.pocoo.org).

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/)

    pip install -U bopytex

## Simple example

Let's say I want an exercise on adding 2 fractions (files are in `examples`).

The *latex* template called `tpl_add_fraction.tex`

``` latex
\documentclass[12pt]{article}

\begin{document}

\section{Ajouts de fractions}

Adding two fractions
%- set e = Expression.random("{a} / {b} + {c} / {k*b}", ["b > 1", "k>1"])
\[
    A = \Var{e}
\]
Solution 
\[
    \Var{e.simplify().explain() | join('=')}
\]
\end{document}
```

Generate latex files and compile those for 2 different subjects.

```
bopytex -t tpl_add_fractions.tex -N 2
```

It produces 2 sources files

- `01_add_fractions.tex`

```latex
\documentclass[12pt]{article}

\begin{document}

\section{Ajouts de fractions}

Adding two fractions
\[
    A = \frac{- 2}{4} + \frac{7}{8}
\]
Solution 
\[
    \frac{- 2}{4} + \frac{7}{8}=\frac{- 2 \times 2}{4 \times 2} + \frac{7}{8}=\frac{- 4}{8} + \frac{7}{8}=\frac{- 4 + 7}{8}=\frac{3}{8}
\]

\end{document}
```

- `02_add_fractions.tex`

```latex
\documentclass[12pt]{article}

\begin{document}

\section{Ajouts de fractions}

Adding two fractions
\[
    A = \frac{8}{9} + \frac{3}{63}
\]
Solution 
\[
    \frac{8}{9} + \frac{3}{63}=\frac{8 \times 7}{9 \times 7} + \frac{3}{63}=\frac{56}{63} + \frac{3}{63}=\frac{56 + 3}{63}=\frac{59}{63}
\]

\end{document}
```

And a ready to print pdf.

- [ all_add_fraction.pdf ]( ./examples/all_add_fraction.pdf )





