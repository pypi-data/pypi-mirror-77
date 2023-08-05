Snippets pour Opytex
####################

On regroupe ici quelques snippets pour centraliser ce qui a déjà été produit avec Opytex.

Fractions
=========


Simplifications de fractions
----------------------------

-  Trouver le numérateur quand le dénominateur augmente

   .. code-block:: latex

      \Block{set a,b,ans,c = random_str("{a},{b},{a*c},{b*c}", conditions = ["{a} != {b}"], val_min = 2, val_max = 10).split(',')}%
      \begin{align*}
            \dfrac{\Var{a}}{\Var{b}} = \dfrac{\ldots}{\Var{c}}
      \end{align*}

      Solution

      \begin{align*}
        \dfrac{\Var{a}}{\Var{b}} = \dfrac{\Var{ans}}{\Var{c}}
      \end{align*}

  Ce qui produira

  .. code-block:: latex

        \begin{align*}
            \dfrac{2}{6} = \dfrac{\ldots}{48}
        \end{align*}
        Solution
        \begin{align*}
            \dfrac{2}{6} = \dfrac{16}{48}
        \end{align*}

  Et ce qui donne

  .. math::

    \begin{aligned}
        \dfrac{2}{6} = \dfrac{\ldots}{48}
    \end{aligned}

    Solution

    \begin{aligned}
        \dfrac{2}{6} = \dfrac{16}{48}
    \end{aligned}

-  Trouver le numérateur quand le dénominateur diminue

   .. code-block:: latex

      \Block{set a,b,ans,c = random_str("{a*c},{b*c},{a},{b}", conditions = ["{a} != {b}"], val_min = 2, val_max = 10).split(',')}%
      \begin{align*}
            \dfrac{\Var{a}}{\Var{b}} = \dfrac{\cdots}{\Var{c}}
      \end{align*}

    Solution

    \begin{align*}
        \dfrac{\Var{a}}{\Var{b}} = \dfrac{\Var{ans}}{\Var{c}}
    \end{align*}

    Explications

    \begin{align*}
    \Var{f.simplify().explain()|join('=')} 
    \end{align*}

  Ce qui produira

  .. code-block:: latex

        \begin{align*}
            \dfrac{12}{9} = \dfrac{\cdots}{3}
        \end{align*}
        Solution
        \begin{align*}
            \dfrac{12}{9} = \dfrac{4}{3}
        \end{align*}
        Explications
        
        \begin{align*}
            \frac{ 12 }{ 9 }=\frac{ 4 \times 3 }{ 3 \times 3 }=\frac{ 4 }{ 3 } 
        \end{align*}

  Et ce qui donne

  .. math::

        \begin{align*}
            \dfrac{12}{9} = \dfrac{\cdots}{3}
        \end{align*}

        Solution

        \begin{align*}
            \dfrac{12}{9} = \dfrac{4}{3}
        \end{align*}

        Explications
        
        \begin{align*}
            \frac{ 12 }{ 9 }=\frac{ 4 \times 3 }{ 3 \times 3 }=\frac{ 4 }{ 3 } 
        \end{align*}


Ajouts de fractions
-------------------

-  Fraction avec le même dénominateur

   .. code-block:: latex

      \Block{set e = Expression.random("{a} / {b} + {c} / {b}", ["{b} > 1"], val_min = 1)}
      \begin{align*}
                  A = \Var{e}
        \end{align*}

      Solution

      \begin{align*}
                  \Var{e.simplify().explain() | join('=')}
      \end{align*}

-  Fraction avec un denominateur multiple de l’autre

   .. code-block:: latex

      \Block{set e = Expression.random("{a} / {b} + {c} / {b*d}", ["{b} > 1","{d} > 1"], val_min = 1)}
      \begin{align*}
        A = \Var{e}
      \end{align*}

      Solution

      \begin{align*}
        \Var{e.simplify().explain() | join('=')}
      \end{align*}

-  Fraction avec des dénominateurs premiers entre eux

   .. code-block:: latex

      \Block{set e = Expression.random("{a} / {b} + {c} / {d}", ["{b} > 1","{d} > 1", "gcd({b},{d}) == 1"], val_min = 1)}
      \begin{align*}
        A = \Var{e}
      \end{align*}

      Solution

      \begin{align*}
        \Var{e.simplify().explain() | join('=')}
      \end{align*}

-  Une fraction et un entier

   .. code-block:: latex

      \Block{set e = Expression.random("{a} / {b} + {c}", ["{b} > 1"], val_min = 1)}
      \begin{align*}
        A = \Var{e}
      \end{align*}

      Solution

      \begin{align*}
        \Var{e.simplify().explain() | join('=')}
      \end{align*}

-  Un entier et une fraction

   .. code-block:: latex

      \Block{set e = Expression.random("{c} + {a} / {b}", ["{b} > 1"], val_min = 1)}
      \begin{align*}
        A = \Var{e}
      \end{align*}

      Solution

      \begin{align*}
        \Var{e.simplify().explain() | join('=')}
      \end{align*}

Multiplications de fractions
----------------------------

-  Une fraction et un entier

   .. code-block:: latex

      \Block{set e = Expression.random("{c} * {a} / {b}", ["{b} > 1"], val_min = 1)}
      \begin{align*}
        A = \Var{e}
      \end{align*}

      Solution

      \begin{align*}
        \Var{e.simplify().explain() | join('=')}
      \end{align*}

-  Fraction avec des dénominateurs quelconques

   .. code-block:: latex

      \Block{set e = Expression.random("{a} / {b} * {c} / {d}", ["{b} > 1","{d} > 1"], val_min = 1)}
      \begin{align*}
        A = \Var{e}
      \end{align*}

      Solution


      \begin{align*}
        \Var{e.simplify().explain() | join('=')}
      \end{align*}
