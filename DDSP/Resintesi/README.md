- **Model A** — Mostra petita d’alta qualitat <br>
Utilitza una única font de gran qualitat: la Jack Lee Bagpipe Music Library. <br>
Aquest model busca determinar si amb una mostra petita, però consistent i clara pot ser suficient per
obtenir resultats satisfactoris. És útil com a punt de partida per establir una línia base. <br> <br>
- **Model B** — Mostra gran i equilibrada <br>
Inclou el màxim nombre de fonts disponibles, amb una selecció de 6 minuts d’àudio per font, assegurant
una distribució equilibrada en duració. <br><br>
L’objectiu és observar el comportament del model amb dades diverses però controlades en proporció. <br> <br>
- **Model C** — Mostra gran, no equilibrada, amb seccionament <br>
Similar al model B pel que fa a volum i diversitat de fonts, però sense equilibrar la duració entre elles. <br>
A més, aquest model incorpora una preparació prèvia en què els arxius d’àudio han estat segmentats en
fragments de 4 segons mitjançant el script proporcionat. <br>

23
Creat amb la finalitat d’analitzar l'afectació aquesta fragmentació i desequilibri a l’entrenament.<br><br>
- **Model D** — Mostra gran, duració recomanada, pocs passos <br>
Selecciona el màxim nombre de fonts possibles, amb una duració de mostres que segueix les
recomanacions de DDSP (10-15 minuts).<br>
No obstant això, aquest model es limita a un nombre reduït de passos d’entrenament, amb l’objectiu de
mesurar l’evolució inicial i la capacitat d’aprenentatge ràpid. <br><br>
- **Model E** — Configuració recomanada (Magenta)<br>
Similar al Model D ofereix una mostra diversa i extensa de fonts, amb una duració de dades recomanada
per Magenta. Aquest model pretén aproximar-se al comportament esperat en condicions òptimes, tant
en termes de duració com de nombre de passos (arribant al màxim permès dins les limitacions d’aquesta
investigació).<br> 
