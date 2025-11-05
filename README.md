# 🤖 Bot Discord-Trello

Bot Discord qui permet d'interagir avec un tableau Trello directement depuis Discord.

## 📋 Fonctionnalités

- ✅ Afficher le tableau complet avec toutes les listes et cartes
- ➕ Ajouter de nouvelles tâches à une liste
- ✔️ Cocher/archiver des tâches complétées
- 🔄 Déplacer des tâches entre les listes
- 📝 Lister toutes les listes disponibles

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Un compte Discord
- Un compte Trello

### 1. Cloner le projet

```bash
git clone <votre-repo>
cd trello-discord
```

### 2. Installer les dépendances

```bash
# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration Discord

1. Aller sur https://discord.com/developers/applications
2. Cliquer sur "New Application"
3. Donner un nom au bot
4. Aller dans l'onglet "Bot"
5. Cliquer sur "Add Bot"
6. Activer "MESSAGE CONTENT INTENT" dans les Privileged Gateway Intents
7. Copier le token (Reset Token si nécessaire)

**Inviter le bot sur votre serveur:**

1. Aller dans l'onglet "OAuth2" > "URL Generator"
2. Cocher les scopes:
   - `bot`
   - `applications.commands`
3. Cocher les permissions:
   - View Channels
   - Send Messages
   - Embed Links
   - Read Message History
4. Copier l'URL générée et l'ouvrir dans un navigateur

### 4. Configuration Trello

#### Obtenir l'API Key et le Token

1. **Aller sur le portail Power-Up Admin:**
   - https://trello.com/power-ups/admin

2. **Créer ou sélectionner une Power-Up:**
   - Si vous n'en avez pas, créez-en une nouvelle
   - Donnez-lui un nom (ex: "Discord Bot")
   - Pas besoin de configurer les autres options

3. **Récupérer l'API Key:**
   - Dans votre Power-Up, allez dans l'onglet "API Key"
   - Copiez votre **API Key**

4. **Générer un Token:**
   - Sur la même page, cliquez sur "Generate a new Token"
   - Ou utilisez ce lien en remplaçant `VOTRE_API_KEY` :
   ```
   https://trello.com/1/authorize?expiration=never&name=DiscordBot&scope=read,write&response_type=token&key=VOTRE_API_KEY
   ```
   - Autorisez l'accès
   - Copiez le **Token** généré

5. **Trouver l'ID de votre tableau:**
   - Ouvrir votre tableau Trello
   - L'URL ressemble à: `https://trello.com/b/ABC123/nom-tableau`
   - L'ID du tableau est `ABC123`

### 5. Configuration du bot

1. Copier le fichier d'exemple:
```bash
cp .env.example .env
```

2. Éditer le fichier `.env` avec vos informations:
```env
DISCORD_TOKEN=votre_token_discord
TRELLO_API_KEY=votre_api_key_trello
TRELLO_TOKEN=votre_token_trello
TRELLO_BOARD_ID=votre_board_id
```

### 6. Lancer le bot

```bash
python bot.py
```

Vous devriez voir:
```
✅ Bot connecté en tant que VotreBot#1234
📋 Connecté au tableau Trello
📌 Tableau: Nom de votre tableau
```

## 📚 Commandes disponibles

| Commande | Description | Exemple |
|----------|-------------|---------|
| `!tableau` | Affiche le tableau complet | `!tableau` |
| `!listes` | Liste toutes les listes | `!listes` |
| `!ajouter [liste] [tâche]` | Ajoute une tâche | `!ajouter todo Faire les courses` |
| `!cocher [tâche]` | Coche/archive une tâche | `!cocher courses` |
| `!deplacer [tâche] [liste]` | Déplace une tâche | `!deplacer courses done` |
| `!aide` | Affiche l'aide | `!aide` |

## 💡 Exemples d'utilisation

### Afficher le tableau complet
```
!tableau
```

### Ajouter une tâche
```
!ajouter todo Préparer la présentation
!ajouter "en cours" Développer la feature X
```

### Cocher une tâche terminée
```
!cocher présentation
```

### Déplacer une tâche
```
!deplacer "feature X" done
```

## 🛠️ Structure du projet

```
trello-discord/
├── bot.py              # Point d'entrée du bot Discord
├── trello_client.py    # Client pour l'API Trello
├── requirements.txt    # Dépendances Python
├── .env.example        # Exemple de configuration
├── .env               # Configuration (à créer)
└── README.md          # Ce fichier
```

## ⚠️ Notes importantes

- Le fichier `.env` contient des informations sensibles et ne doit **jamais** être partagé
- Le bot doit avoir les bonnes permissions Discord (voir configuration)
- Les noms de listes et tâches peuvent être partiels (recherche par correspondance)
- Si plusieurs tâches correspondent, le bot vous demandera d'être plus précis
- **Important:** Le Token Trello doit être généré via le lien d'autorisation, pas le Secret de la Power-Up

## 🐛 Dépannage

### Le bot ne se connecte pas
- Vérifiez que le token Discord est correct
- Assurez-vous que "MESSAGE CONTENT INTENT" est activé

### Erreur Trello
- Vérifiez que l'API Key et le Token sont corrects (pas le Secret !)
- Assurez-vous que l'ID du tableau est valide
- Vérifiez que vous avez accès au tableau
- Le Token doit être généré via le lien d'autorisation dans le portail Power-Up Admin

### Commandes qui ne fonctionnent pas
- Vérifiez que le bot a les bonnes permissions sur le serveur
- Le préfixe par défaut est `!`, assurez-vous de l'utiliser

## 📝 Licence

MIT

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.
