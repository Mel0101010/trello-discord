"""
Bot Discord pour interagir avec Trello
"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from trello_client import TrelloClient
from checker import TaskChecker
from scheduler import ReminderScheduler

# Charger les variables d'environnement
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")

# Initialiser le bot Discord avec les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialiser le client Trello
trello = TrelloClient(TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID)

# Initialiser le checker et le scheduler
checker = TaskChecker(trello)
scheduler = ReminderScheduler(bot, checker)


@bot.event
async def on_ready():
    """Événement déclenché quand le bot est prêt"""
    print(f"✅ Bot connecté en tant que {bot.user}")
    print(f"📋 Connecté au tableau Trello")
    
    # Vérifier la connexion à Trello
    try:
        board = trello.get_board()
        print(f"📌 Tableau: {board['name']}")
    except Exception as e:
        print(f"❌ Erreur de connexion à Trello: {e}")
    
    # Démarrer le scheduler pour les rappels automatiques
    scheduler.start()


@bot.command(name="tableau", help="Affiche le tableau Trello complet")
async def show_board(ctx):
    """Affiche toutes les listes et cartes du tableau"""
    try:
        await ctx.send("🔄 Récupération du tableau...")
        
        board = trello.get_full_board()
        
        # Créer un embed pour affichage
        embed = discord.Embed(
            title=f"📋 {board['name']}",
            url=board['url'],
            description=board.get('desc', 'Pas de description'),
            color=discord.Color.blue()
        )
        
        # Ajouter chaque liste comme un champ
        for list_data in board['lists']:
            cards_text = ""
            if list_data['cards']:
                for i, card in enumerate(list_data['cards'], 1):
                    cards_text += f"{i}. {card['name']}\n"
            else:
                cards_text = "*Aucune carte*"
            
            # Discord limite à 1024 caractères par champ
            if len(cards_text) > 1024:
                cards_text = cards_text[:1021] + "..."
            
            embed.add_field(
                name=f"📝 {list_data['name']} ({len(list_data['cards'])})",
                value=cards_text,
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command(name="listes", help="Affiche toutes les listes du tableau")
async def show_lists(ctx):
    """Affiche toutes les listes disponibles"""
    try:
        lists = trello.get_lists()
        
        embed = discord.Embed(
            title="📝 Listes disponibles",
            color=discord.Color.green()
        )
        
        for i, list_data in enumerate(lists, 1):
            embed.add_field(
                name=f"{i}. {list_data['name']}",
                value=f"ID: `{list_data['id']}`",
                inline=False
            )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command(name="ajouter", help="Ajoute une tâche à une liste\nUsage: !ajouter [nom_liste] [nom_tâche]")
async def add_task(ctx, list_name: str, *, task_name: str):
    """Ajoute une nouvelle carte/tâche à une liste"""
    try:
        # Trouver la liste correspondante
        lists = trello.get_lists()
        matching_list = None
        
        for list_data in lists:
            if list_name.lower() in list_data['name'].lower():
                matching_list = list_data
                break
        
        if not matching_list:
            await ctx.send(f"❌ Liste '{list_name}' introuvable. Utilisez `!listes` pour voir les listes disponibles.")
            return
        
        # Créer la carte
        card = trello.create_card(matching_list['id'], task_name)
        
        embed = discord.Embed(
            title="✅ Tâche ajoutée",
            description=f"**{card['name']}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Liste", value=matching_list['name'])
        embed.add_field(name="Lien", value=f"[Voir sur Trello]({card['url']})")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command(name="cocher", help="Archive/coche une tâche\nUsage: !cocher [nom_partiel_de_la_tâche]")
async def check_task(ctx, *, task_name: str):
    """Archive une carte (marque comme complétée)"""
    try:
        # Rechercher la carte
        cards = trello.get_all_cards()
        matching_cards = [card for card in cards if task_name.lower() in card['name'].lower()]
        
        if not matching_cards:
            await ctx.send(f"❌ Aucune tâche trouvée contenant '{task_name}'")
            return
        
        if len(matching_cards) > 1:
            # Plusieurs correspondances
            embed = discord.Embed(
                title="⚠️ Plusieurs tâches trouvées",
                description="Soyez plus précis:",
                color=discord.Color.orange()
            )
            for card in matching_cards[:5]:  # Limiter à 5 résultats
                embed.add_field(
                    name=card['name'],
                    value=f"ID: `{card['id']}`",
                    inline=False
                )
            await ctx.send(embed=embed)
            return
        
        # Une seule correspondance, archiver
        card = matching_cards[0]
        trello.archive_card(card['id'])
        
        await ctx.send(f"✅ Tâche cochée/archivée: **{card['name']}**")
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command(name="deplacer", help="Déplace une tâche vers une autre liste\nUsage: !deplacer [nom_tâche] [nom_nouvelle_liste]")
async def move_task(ctx, task_name: str, *, new_list_name: str):
    """Déplace une carte vers une autre liste"""
    try:
        # Trouver la carte
        cards = trello.get_all_cards()
        matching_card = None
        
        for card in cards:
            if task_name.lower() in card['name'].lower():
                matching_card = card
                break
        
        if not matching_card:
            await ctx.send(f"❌ Tâche '{task_name}' introuvable")
            return
        
        # Trouver la nouvelle liste
        lists = trello.get_lists()
        matching_list = None
        
        for list_data in lists:
            if new_list_name.lower() in list_data['name'].lower():
                matching_list = list_data
                break
        
        if not matching_list:
            await ctx.send(f"❌ Liste '{new_list_name}' introuvable")
            return
        
        # Déplacer la carte
        trello.move_card(matching_card['id'], matching_list['id'])
        
        await ctx.send(f"✅ **{matching_card['name']}** déplacée vers **{matching_list['name']}**")
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


@bot.command(name="aide", help="Affiche la liste des commandes disponibles")
async def help_command(ctx):
    """Affiche l'aide"""
    embed = discord.Embed(
        title="🤖 Commandes du Bot Trello",
        description="Voici toutes les commandes disponibles:",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="!tableau",
        value="Affiche le tableau complet avec toutes les listes et tâches",
        inline=False
    )
    
    embed.add_field(
        name="!listes",
        value="Affiche toutes les listes disponibles",
        inline=False
    )
    
    embed.add_field(
        name="!ajouter [liste] [tâche]",
        value="Ajoute une nouvelle tâche\nExemple: `!ajouter todo Faire les courses`",
        inline=False
    )
    
    embed.add_field(
        name="!cocher [tâche]",
        value="Coche/archive une tâche\nExemple: `!cocher courses`",
        inline=False
    )
    
    embed.add_field(
        name="!deplacer [tâche] [nouvelle_liste]",
        value="Déplace une tâche vers une autre liste\nExemple: `!deplacer courses done`",
        inline=False
    )
    
    embed.add_field(
        name="!aide",
        value="Affiche ce message d'aide",
        inline=False
    )
    
    embed.add_field(
        name="!verifier",
        value="Vérifie manuellement les colonnes vides",
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.command(name="verifier", help="Vérifie quelles colonnes sont vides")
async def check_empty(ctx):
    """Vérifie manuellement les colonnes vides et affiche un rapport"""
    try:
        await ctx.send("🔍 Vérification des colonnes en cours...")
        
        users_to_remind = checker.check_empty_lists()
        
        if not users_to_remind:
            await ctx.send("✅ **Tout est à jour !** Toutes les colonnes ont des tâches.")
        else:
            # Message avec vraies mentions (pas embed)
            message = "⚠️ **Colonnes vides détectées** ⚠️\n\n"
            
            for user_id, list_name in users_to_remind.items():
                message += f"<@{user_id}> Ta colonne **{list_name}** est vide ! 📝\n"
            
            await ctx.send(message)
        
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")


# Lancer le bot
if __name__ == "__main__":
    if not all([DISCORD_TOKEN, TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_BOARD_ID]):
        print("❌ Erreur: Variables d'environnement manquantes!")
        print("Assurez-vous d'avoir créé un fichier .env avec toutes les variables requises.")
        exit(1)
    
    try:
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt du bot...")
        scheduler.stop()
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        scheduler.stop()
