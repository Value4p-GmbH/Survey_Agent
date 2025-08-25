from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .ai import process_and_send_translation, process_and_mark_answers
from.models import ConversationLog
from rest_framework.decorators import api_view
from .models import ConversationLog, Conversation, TranscriptionEntry, AnalysisResult, AnalysisData
from .serializers import ConversationLogSerializer, ConversationSerializer, TranscriptionEntrySerializer, AnalysisResultSerializer, AnalysisDataSerializer
from django.shortcuts import get_object_or_404


@method_decorator(csrf_exempt, name='dispatch')
class ElevenLabsWebhookView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data             

        try:
            transcript = data.get('data', {}).get('transcript', [])
            if not transcript:
                return Response(
                    {'status': 'error', 'message': 'No transcript data found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except AttributeError:
            return Response(
                {'status': 'error', 'message': 'Invalid data format'},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = []
        for entry in transcript:
            role = entry.get('role')
            message = entry.get('message')
            if role and message is not None:
                conversation.append({
                    'role': role,
                    'message': message
                })

               
            
        

        translation_str = process_and_send_translation(conversation)

        try:
            translation = json.loads(translation_str) 
        except json.JSONDecodeError:
            return Response(
                {'status': 'error', 'message': 'Invalid JSON returned from translate_json'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        merged_data = {
            "conversation": conversation,
            "translation": translation
        }

        conversation_log  = ConversationLog.objects.create(
            conversation=conversation,
            translation=translation
        )
        analysis_data = data.get('data', {}).get('analysis', {})
        print(f"Analysis data: {analysis_data}")
        serializer = AnalysisDataSerializer(data={
        'conversation': conversation_log.id,
        'analysis': analysis_data
        })
        serializer.is_valid(raise_exception=True)
        serializer.save() 

        return Response(
            {'status': 'success', 'data': merged_data},
            status=status.HTTP_200_OK
        )



@api_view(['GET'])
def get_latest_conversation(request):
    latest = ConversationLog.objects.order_by('-timestamp').first()
    if not latest:
        return Response({"message": "No conversations found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ConversationLogSerializer(latest)
    return Response(serializer.data, status=status.HTTP_200_OK)


# your_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConversationSerializer

class ConversationDataView(APIView):
    def post(self, request, *args, **kwargs):
        
        received_data = request.data.get('data', {})

       
        received_data['event_timestamp'] = request.data.get('event_timestamp')
        
        
        metadata = received_data.get('metadata', {})
        received_data['call_duration_secs'] = metadata.get('call_duration_secs')
        received_data['main_language'] = metadata.get('main_language')
        
       
        serializer = ConversationSerializer(data=received_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
def get_conversations(request, pk=None):
    
    if pk:        
        conversation = get_object_or_404(
            Conversation.objects.select_related('analysis').prefetch_related('transcript'), 
            pk=pk
        )
        serializer = ConversationSerializer(conversation)
    else:        
        conversations = Conversation.objects.all().order_by('-event_timestamp')
        conversations = conversations.select_related('analysis').prefetch_related('transcript')       
        serializer = ConversationSerializer(conversations, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_last_conversation_data(request, *args, **kwargs):
    last_analysis = AnalysisData.objects.order_by('-id').first()
    print(last_analysis)
    if not last_analysis:
        return Response({"message": "No conversations found."}, status=status.HTTP_404_NOT_FOUND)

    # Pass only the JSON field instead of the model
    raw_data = process_and_mark_answers(last_analysis.analysis)  
    
    try:
        data = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
    except json.JSONDecodeError:
        data = raw_data  # fallback if it's already a dict/list
    
    return Response({"processed_results": data}, status=status.HTTP_200_OK)


        
   