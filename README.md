# Bagpipe-Dataset
Aquest repositori conté un conjunt de 48 minuts de mostres de l'instrument sac de gemecs d'alta qualitat a 44.1kHz i 16 bits de profunditat. <br>
Permet extraure caracteristiques i obtenir mètriques per entrenar un model DDSP <br><br>

El repositori segueix la següent estructura: <br>

![Diagrama sin título drawio (2)](https://github.com/user-attachments/assets/ead7fad5-427b-48eb-937d-2681e8ccd597) <br>

Els scripts són accesibles per a: <br>
    - extreure dades - [Extracció caracteristiques](https://github.com/JesusPavonGarcia/Bagpipe-Dataset/tree/main/DDSP/Codi) <br>
    - comparar dades - [Evaluació mètriques](https://github.com/JesusPavonGarcia/Bagpipe-Dataset/tree/main/DDSP/Codi) <br>

Els audios test són accesibles a DDSP\Codi\Resintesi on es poden trobar els audios originals i resintetizats <br>
    - original i sintetitzat per diferents models  - [Resintesi](https://github.com/JesusPavonGarcia/Bagpipe-Dataset/tree/main/DDSP/Resintesi) <br>

Si es desitja fer un experiment directament amb DDSP es possible via <br>
     -  [AUDIOS TEST](https://github.com/JesusPavonGarcia/Bagpipe-Dataset/tree/main/DDSP/test)  es troben els audios test en TFRECORD <br>
     - [ENTRENAMENT DDSP](https://github.com/JesusPavonGarcia/Bagpipe-Dataset/tree/main/DDSP/Codi/Train%20DDSP) es troba el notebook per executar localment un entrenament i crear un model <br>
