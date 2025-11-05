"""
Client pour interagir avec l'API Trello
"""
import requests


class TrelloClient:
    def __init__(self, api_key, token, board_id):
        self.api_key = api_key
        self.token = token
        self.board_id = board_id
        self.base_url = "https://api.trello.com/1"
    
    def _build_auth_params(self, additional_params=None):
        """Construit les paramètres d'authentification"""
        params = {
            "key": self.api_key,
            "token": self.token
        }
        if additional_params:
            params.update(additional_params)
        return params
    
    def get_lists(self):
        """Récupère toutes les listes du tableau"""
        url = f"{self.base_url}/boards/{self.board_id}/lists"
        response = requests.get(url, params=self._build_auth_params())
        response.raise_for_status()
        return response.json()
    
    def get_cards_in_list(self, list_id):
        """Récupère toutes les cartes d'une liste"""
        url = f"{self.base_url}/lists/{list_id}/cards"
        response = requests.get(url, params=self._build_auth_params())
        response.raise_for_status()
        return response.json()
    
    def get_all_cards(self):
        """Récupère toutes les cartes du tableau"""
        url = f"{self.base_url}/boards/{self.board_id}/cards"
        response = requests.get(url, params=self._build_auth_params())
        response.raise_for_status()
        return response.json()
    
    def create_card(self, list_id, name, description=""):
        """Crée une nouvelle carte dans une liste"""
        url = f"{self.base_url}/cards"
        params = self._build_auth_params({
            "idList": list_id,
            "name": name,
            "desc": description
        })
        response = requests.post(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def move_card(self, card_id, new_list_id):
        """Déplace une carte vers une autre liste"""
        url = f"{self.base_url}/cards/{card_id}"
        params = self._build_auth_params({
            "idList": new_list_id
        })
        response = requests.put(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def archive_card(self, card_id):
        """Archive une carte (équivalent à 'cocher' une tâche)"""
        url = f"{self.base_url}/cards/{card_id}"
        params = self._build_auth_params({
            "closed": "true"
        })
        response = requests.put(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_board(self):
        """Récupère les informations du tableau"""
        url = f"{self.base_url}/boards/{self.board_id}"
        params = self._build_auth_params({
            "fields": "name,url,desc"
        })
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_full_board(self):
        """Récupère le tableau complet avec toutes les listes et cartes"""
        board = self.get_board()
        lists = self.get_lists()
        
        # Récupère les cartes pour chaque liste
        lists_with_cards = []
        for list_data in lists:
            cards = self.get_cards_in_list(list_data["id"])
            list_data["cards"] = cards
            lists_with_cards.append(list_data)
        
        board["lists"] = lists_with_cards
        return board
