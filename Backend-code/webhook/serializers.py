from rest_framework import serializers
from .models import ConversationLog, TranscriptionEntry, AnalysisResult, Conversation, AnalysisData

class ConversationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationLog
        fields = ['id', 'timestamp', 'conversation', 'translation']
        read_only_fields = ['id', 'timestamp']



class TranscriptionEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionEntry
        fields = ['role', 'message', 'time_in_call_secs']

class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = ['call_successful', 'transcript_summary', 'call_summary_title', 'evaluation_criteria_results']

class ConversationSerializer(serializers.ModelSerializer):
    transcript = TranscriptionEntrySerializer(many=True)
    analysis = AnalysisResultSerializer()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'user_id', 'agent_id', 'event_timestamp', 'call_duration_secs', 'main_language', 'transcript', 'analysis']

    def create(self, validated_data):
        # Pop nested data for transcript and analysis
        transcript_data = validated_data.pop('transcript')
        analysis_data = validated_data.pop('analysis')

        # Create the Conversation object
        conversation = Conversation.objects.create(**validated_data)

        # Create TranscriptionEntry objects
        for entry_data in transcript_data:
            TranscriptionEntry.objects.create(conversation=conversation, **entry_data)
        
        # Create the AnalysisResult object using the popped analysis_data
        AnalysisResult.objects.create(conversation=conversation, **analysis_data)
        
        return conversation
    

    

class AnalysisDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisData
        fields = ['id', 'conversation', 'analysis']