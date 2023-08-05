Utilisation de Opytex
#####################

Écriture des documents - surcharge sur latex
============================================

Opytex ajoute deux commandes "latex" pour inclure du code Python interprété dans les documents.

Commande *\Var*
---------------

Cette commande va exécuter du code python qui sera ensuite inclut dans le document tex produit.

    .. code-block:: latex

        Je peux afficher des nombres \Var{2}, \Var{2+3} ...
        Et si j'ai enregistré une variable \Block{set a = 1}, je peux ensuite l'afficher \Var{a}.

Ce qui produira le document suivant

    .. code-block:: latex

        Je peux afficher des nombres 2, 5 ...
        Et si j'ai enregistré une variable, je peux ensuite l'afficher 1.

Commande *\Block*
-----------------

Cette commande permet d'exécuter du code python qui ne sera pas afficher dans le document tex produit.

    .. code-block:: latex

        Je peux déclarer des variables
        \Block{set a = 1}
        \Block{set b = 2}
        Et même faire des calculs
        \Block{set c = a + b}
        Mais rien ne sera affiché.

Ce qui produira le document suivant

    .. code-block:: latex

        Je peux déclarer des variables
        Et même faire des calculs
        Mais rien ne sera affiché.

La commande *Block* donne accès tag de jinja2.

- Les boucles

    .. code-Block:: latex

        On peut faire des boucles et parcourir des listes
        \Block{set l = [1,2,3,4]}
        \Block{for i in l}
        i vaut \Var{i}
        \Block{endfor}

Ce qui produira

    .. code-block:: latex

        On peut faire des boucles et parcourir des listes
        i vaut 1
        i vaut 2
        i vaut 3
        i vaut 4

        
Quelques commandes supplémentaires
==================================

Comme Opytex utilise le moteur de template Jinja2, la notion de filtre peut être utilisée.

Filtres qui marchenet bien avec Mapytex
---------------------------------------

- "join": Mettre en forme un calcul sur une seule ligne

    .. code-block:: latex

        On commence par définir une expression,
        \Block{set e = Expression("1 + 2*3")}
        et on veut détailler sa simplification
        \begin{align*}
            \Var{e.simplify().explain()|join('=')} 
        \end{align*}


  Ce qui produira le document suivant

    .. code-block:: latex

        On commence par définir une expression,
        et on veut détailler sa simplification
        \begin{align*}
            1 + 2 \times 3 =  1 + 6 = 7 
        \end{align*}



- *calculus*: Mettre en forme un calcul sur plusieurs lignes

    .. code-block:: latex

        On commence par définir une expression,
        \Block{set e = Expression("1 + 2*3")}
        et on veut détailler sa simplification
        \begin{eqnarray*}
            \Var{e.simplify().explain()|calculus(name = 'e')} 
        \end{eqnarray*}


  Ce qui produira le document suivant

    .. code-block:: latex

        On commence par définir une expression,
        et on veut détailler sa simplification
        \begin{eqnarray*}
            e & = & 1 + 2 \times 3 \\
            e & = & 1 + 6 \\
            e & = & 7 
        \end{eqnarray*}

    
Compilation des documents
=========================

Pour créer ce DM on commence par rédiger le fichier :download:`template <_downloads/tpl_DM.tex>`.

Puis on génère et compile les 3 sujets avec la commande

    .. code-block:: bash

        opytex -t tpl_DM.tex -N 3

Ce qui a crée les fichiers sources: 

- :download:`01_DM.tex <_downloads/01_DM.tex>`
- :download:`02_DM.tex <_downloads/02_DM.tex>`
- :download:`03_DM.tex <_downloads/03_DM.tex>`

et les fichiers compilés ont été concaténés dans le fichier :download:`all_DM.pdf <_downloads/all_DM.pdf>`.


Pour obtenir la correction, on le demande poliement à Opytex

    .. code-block:: bash

        opytex -t tpl_DM.tex --only-corr

Ce qui a pour effet de décommenter la ligne avec *\printanswers*, de recompiler les documents puis de les concatener dans :download:`corr_DM.pdf <_downloads/corr_DM.pdf>` sans regénérer de nouveaux sujets.

Il est possible aussi de créer les sujets et les corrections en même temps avec

    .. code-block:: bash

        opytex -t tpl_DM.tex -c -N 60


    
