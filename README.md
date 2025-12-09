# PlantUML Generator

Un wrapper GUI moderne pour générer des diagrammes PlantUML (.puml) en local, sans dépendre d'un serveur externe Web.

## Prérequis

*   **Java Runtime Environment (JRE)** installé et accessible via la commande `java`.
*   **Python 3.10+** (pour le développement/build).

## Installation (Développement)

1.  **Cloner le projet** ou télécharger les sources.
2.  **Créer un environnement virtuel** :
    ```bash
    python -m venv .venv
    ```
3.  **Activer l'environnement** :
    *   Windows : `.venv\Scripts\activate`
    *   Linux/Mac : `source .venv/bin/activate`
4.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

Lancer l'application :
```bash
python main.py
```

## Construction de l'Exécutable (.exe)

Pour générer un fichier `.exe` autonome (dossier `dist/`) :

1.  Assurez-vous d'être dans l'environnement virtuel.
2.  Lancez le script de build :
    ```cmd
    build.bat
    ```

L'exécutable final se trouvera dans `dist/PlantUMLGenerator.exe`.
