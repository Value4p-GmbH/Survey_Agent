from django.db import models
from django.db.models import JSONField 

class ConversationLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.JSONField()
    translation = models.JSONField()

    def __str__(self):
        return f"Conversation at {self.timestamp}"



class Conversation(models.Model):
    conversation_id = models.CharField(max_length=255, unique=True)
    user_id = models.CharField(max_length=255)
    agent_id = models.CharField(max_length=255)
    event_timestamp = models.IntegerField()
    call_duration_secs = models.IntegerField()
    main_language = models.CharField(max_length=10)

   

class TranscriptionEntry(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='transcript')
    role = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)
    time_in_call_secs = models.IntegerField()

    

class AnalysisResult(models.Model):
    conversation = models.OneToOneField(Conversation, on_delete=models.CASCADE, related_name='analysis')
    call_successful = models.CharField(max_length=50)
    transcript_summary = models.TextField()
    call_summary_title = models.CharField(max_length=255)
    evaluation_criteria_results = JSONField(default=dict) # New field to store the detailed results

    def __str__(self):
        return f"Analysis for {self.conversation}"
    

class AnalysisData(models.Model):
    conversation = models.ForeignKey(ConversationLog, on_delete=models.CASCADE, related_name='analysis_data')
    analysis = JSONField()

    def __str__(self):
        return f"Analysis data for {self.analysis}"

 