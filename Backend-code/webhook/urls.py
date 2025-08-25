from django.urls import path
from .views import ElevenLabsWebhookView
from django.urls import path
from .views import get_latest_conversation, ConversationDataView, get_conversations, get_last_conversation_data

urlpatterns = [
    path("webhook/", ElevenLabsWebhookView.as_view(), name="elevenlabs-webhook"),
    path('conversations/', get_latest_conversation, name='get-conversations'),
    path('api/conversations/', ConversationDataView.as_view(), name='conversation_data'),
    path('get_conversations/', get_conversations, name='retrieve_conversations'),
    path('graph_data/', get_last_conversation_data, name='graph_data'),
]
