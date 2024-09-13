from rest_framework import serializers
from .models import Campaign

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'campaign_name', 'campaign_type', 'campaign_status', 'campaign_date', 'campaign_end_date']
