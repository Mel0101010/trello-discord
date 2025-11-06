# 🤖 Bot Discord-Trello

Bot Discord qui permet d'interagir avec un tableau Trello directement depuis Discord.

## 📋 Fonctionnalités

- ✅ Afficher le tableau complet avec toutes les listes et cartes
- ➕ Ajouter de nouvelles tâches à une liste
- ✔️ Cocher/archiver des tâches complétées
- 🔄 Déplacer des tâches entre les listes
- 📝 Lister toutes les listes disponibles
- ⏰ **Rappels automatiques quotidiens à 18h** pour les colonnes vides
- 👥 **Mentions automatiques** des utilisateurs qui n'ont pas mis à jour leurs tâches

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

# ID du canal Discord pour les rappels automatiques (optionnel)
# Activez le mode développeur Discord, clic droit sur le canal > Copier l'ID
REMINDER_CHANNEL_ID=votre_channel_id_ici
```

### 6. Configurer les utilisateurs (optionnel)

Pour personnaliser les rappels automatiques, éditez le fichier `config.py`:

```python
USER_LIST_MAPPING = {
    "323086194500173844": "crypter",    # ID Discord: Nom de la colonne Trello
    "410782067853623320": "flush",
    "430773066554146826": "PtitBob"
}
```

**Comment trouver les IDs Discord:**
1. Activer le mode développeur: Paramètres Discord > Avancés > Mode développeur
2. Clic droit sur un utilisateur > Copier l'ID

### 7. Lancer le bot

```bash
python bot.py
```

Vous devriez voir:
```
✅ Bot connecté en tant que VotreBot#1234
📋 Connecté au tableau Trello
📌 Tableau: Nom de votre tableau
✅ Rappels automatiques activés (tous les jours à 18h00)
```

## 📚 Commandes disponibles

| Commande | Description | Exemple |
|----------|-------------|---------|
| `!tableau` | Affiche le tableau complet | `!tableau` |
| `!listes` | Liste toutes les listes | `!listes` |
| `!ajouter [liste] [tâche]` | Ajoute une tâche | `!ajouter todo Faire les courses` |
| `!cocher [tâche]` | Coche/archive une tâche | `!cocher courses` |
| `!deplacer [tâche] [liste]` | Déplace une tâche | `!deplacer courses done` |
| `!verifier` | Vérifie manuellement les colonnes vides | `!verifier` |
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

### Vérifier les colonnes vides
```
!verifier
```

## ⏰ Rappels Automatiques

Le bot vérifie automatiquement **tous les jours à 18h** si des colonnes sont vides. Si c'est le cas, il envoie un rappel dans le canal configuré avec mention des utilisateurs concernés.

**Configuration:**
1. Définir `REMINDER_CHANNEL_ID` dans le fichier `.env`
2. Configurer le mapping utilisateurs/colonnes dans `config.py`
3. Le bot enverra automatiquement un embed avec les colonnes vides

**Pour tester sans attendre 18h:**
- Utilisez la commande `!verifier` pour vérifier manuellement

## 🛠️ Structure du projet

```
trello-discord/
├── bot.py              # Point d'entrée du bot Discord
├── trello_client.py    # Client pour l'API Trello
├── checker.py          # Vérification des colonnes vides
├── scheduler.py        # Gestion des rappels automatiques
├── config.py           # Configuration (mapping utilisateurs/colonnes)
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
- **Rappels automatiques:** Configurez `REMINDER_CHANNEL_ID` dans `.env` pour activer les rappels quotidiens
- **Timezone:** Les rappels sont configurés pour Europe/Paris, modifiez dans `scheduler.py` si nécessaire

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
