# Snips-action-quizz snippet skill 
Petit quizz fonctionnel en francais sur le thème des pays-capitales pour l'assistant vocal snips écrit afin d'étudier python et snips.ai
Code encore très potache et non garanti exempt de bug. 

Le nom des capitales est un slot importé via wikidata.
La réponse "Je ne sais pas" générera un comportement similaire à une fausse réponse.
La commande "Arrête la partie" termine la session.
La liste des pays/capitales est un fichier txt sauvé en format utf-8 ( ! important afin d'éviter toute sorte d'erreurs liées à l'accentuation ). 
Pour l'instant le quizz tourne en boucle une fois que l'on prononce "Hey Snips, démarre une partie".
De nombreux pays et capitales ne sont pas bien prononcés et génère de fausses mauvaises réponses
Certains pays sont reconnus par les slots sans majuscules ce qui entraine aussi de fausses mauvaises réponses.

