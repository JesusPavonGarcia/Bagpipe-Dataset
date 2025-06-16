# Bagpipe-Dataset
Aquest repositori conté un conjunt de 48 minuts de mostres de l'instrument sac de gemecs d'alta qualitat a 44.1kHz i 16 bits de profunditat.
Permet extraure caracteristiques i obtenir mètriques per entrenar un model DDSP

El repositori segueix la següent estructura

![Diagrama sin título drawio (2)](https://github.com/user-attachments/assets/ead7fad5-427b-48eb-937d-2681e8ccd597)

Els scripts són accesibles per a:
    - extreure dades - DDSP\Codi\Extract_features
    - coparar dades - DDSP\Codi\Comparatives_audio

Els audios test són accesibles a DDSP\Codi\Resintesi on es poden trobar els audios originals i resintetizats
    - original - DDSP\Codi\Resintesi
    - coparar dades - DDSP\Codi\Comparatives_audio

Si es desitja fer un experiment directament amb DDSP es possible via la carpeta DDSP\Codi\test on es troben els audios test en TFRECORD i el script per executar
