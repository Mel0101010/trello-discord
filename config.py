"""
Configuration du bot Discord-Trello
"""

# Mapping des utilisateurs Discord et leurs colonnes Trello associées
USER_LIST_MAPPING = {
    "323086194500173844": "crypter",  # ID Discord de crypter
    "410782067853623320": "flush",    # ID Discord de flush
    "430773066554146826": "PtitBob",   # ID Discord de PtitBob
    "381421024765280265": "situzy",
    "400657314547367936": "bara"
}

# Configuration des rappels
REMINDER_CONFIG = {
    "enabled": True,
    "hour": 18,  # Heure du rappel (18h)
    "minute": 00,  # Minute du rappel
    "channel_id": 1436072032746864701,  # ID du canal Discord où envoyer les rappels (à configurer dans .env)
    "message_template": "⚠️ Rappel quotidien : {mentions}\nVotre colonne **{list_name}** est vide ! N'oubliez pas d'ajouter vos tâches de la journée."
}

# Messages personnalisables
MESSAGES = {
    "no_tasks_reminder": "📝 N'oubliez pas de mettre à jour vos tâches !",
    "all_good": "✅ Tout le monde a mis à jour ses tâches aujourd'hui !",
    "empty_column": "La colonne **{list_name}** est vide."
}
