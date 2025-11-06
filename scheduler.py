"""
Scheduler pour les rappels automatiques quotidiens
"""
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from checker import TaskChecker
from config import REMINDER_CONFIG, USER_LIST_MAPPING
import os


class ReminderScheduler:
    def __init__(self, bot, checker: TaskChecker):
        self.bot = bot
        self.checker = checker
        self.scheduler = AsyncIOScheduler()
        self.channel_id = os.getenv("REMINDER_CHANNEL_ID")
    
    async def send_daily_reminder(self):
        """
        Envoie un rappel quotidien pour les colonnes vides
        """
        try:
            # Vérifier les colonnes vides
            users_to_remind = self.checker.check_empty_lists()
            
            if not users_to_remind:
                print("✅ Toutes les colonnes ont des tâches, pas de rappel envoyé.")
                return
            
            # Récupérer le canal Discord
            if not self.channel_id:
                print("❌ Aucun canal de rappel configuré (REMINDER_CHANNEL_ID)")
                return
            
            channel = self.bot.get_channel(int(self.channel_id))
            if not channel:
                print(f"❌ Canal {self.channel_id} introuvable")
                return
            
            # Préparer le message avec les vraies mentions
            message = "⚠️ **Rappel quotidien - Mise à jour des tâches** ⚠️\n\n"
            
            for user_id, list_name in users_to_remind.items():
                message += f"<@{user_id}> Ta colonne **{list_name}** est vide ! N'oublie pas d'ajouter tes tâches ! 📝\n"
            
            message += "\n_Rappel automatique • 18h00_"
            
            # Envoyer le message (sans embed pour que les mentions fonctionnent)
            await channel.send(message)
            print(f"✅ Rappel envoyé à {len(users_to_remind)} utilisateur(s)")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi du rappel: {e}")
    
    def start(self):
        """
        Démarre le scheduler avec le rappel quotidien à 18h
        """
        if not REMINDER_CONFIG["enabled"]:
            print("ℹ️ Rappels automatiques désactivés")
            return
        
        # Créer un trigger cron pour 18h tous les jours
        trigger = CronTrigger(
            hour=REMINDER_CONFIG["hour"],
            minute=REMINDER_CONFIG["minute"],
            timezone="Europe/Paris"  # Ajustez selon votre timezone
        )
        
        # Ajouter la tâche planifiée
        self.scheduler.add_job(
            self.send_daily_reminder,
            trigger=trigger,
            id="daily_reminder",
            name="Rappel quotidien des tâches",
            replace_existing=True
        )
        
        self.scheduler.start()
        print(f"✅ Rappels automatiques activés (tous les jours à {REMINDER_CONFIG['hour']}h{REMINDER_CONFIG['minute']:02d})")
    
    def stop(self):
        """
        Arrête le scheduler
        """
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("❌ Scheduler arrêté")
