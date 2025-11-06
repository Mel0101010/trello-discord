"""
Module pour vérifier les colonnes vides et identifier les utilisateurs à rappeler
"""
from trello_client import TrelloClient
from config import USER_LIST_MAPPING


class TaskChecker:
    def __init__(self, trello_client: TrelloClient):
        self.trello = trello_client
    
    def check_empty_lists(self):
        """
        Vérifie quelles colonnes sont vides et retourne les utilisateurs à rappeler
        
        Returns:
            dict: Dictionnaire avec user_id comme clé et nom de la liste comme valeur
                  Ex: {"323086194500173844": "crypter"}
        """
        try:
            # Récupérer toutes les listes du tableau
            lists = self.trello.get_lists()
            
            # Dictionnaire pour stocker les utilisateurs avec colonnes vides
            users_to_remind = {}
            
            # Pour chaque utilisateur configuré
            for user_id, list_name in USER_LIST_MAPPING.items():
                # Trouver la liste correspondante
                matching_list = None
                for trello_list in lists:
                    if list_name.lower() in trello_list['name'].lower():
                        matching_list = trello_list
                        break
                
                if matching_list:
                    # Récupérer les cartes de cette liste
                    cards = self.trello.get_cards_in_list(matching_list['id'])
                    
                    # Si la liste est vide, ajouter l'utilisateur
                    if len(cards) == 0:
                        users_to_remind[user_id] = matching_list['name']
            
            return users_to_remind
        
        except Exception as e:
            print(f"❌ Erreur lors de la vérification des listes: {e}")
            return {}
    
    def get_empty_lists_report(self):
        """
        Génère un rapport détaillé des colonnes vides
        
        Returns:
            str: Rapport formaté
        """
        users_to_remind = self.check_empty_lists()
        
        if not users_to_remind:
            return "✅ Toutes les colonnes ont des tâches !"
        
        report = "📋 **Colonnes vides:**\n\n"
        for user_id, list_name in users_to_remind.items():
            # Récupérer le nom depuis le mapping
            user_name = USER_LIST_MAPPING.get(user_id, "Utilisateur inconnu")
            report += f"• **{list_name}** (<@{user_id}>)\n"
        
        return report
