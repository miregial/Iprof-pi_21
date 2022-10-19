from rest_framework.serializers import ModelSerializer
from api.models import Promo, Prize, User, Result
class PrizeSer(ModelSerializer):
    class Meta:
        model = Prize
        fields = ('id', 'description')
        read_only = ('id', )
class ParticipantSer(ModelSerializer):
    class Meta:
        model = User
        read_only = ('id', )
        fields = ('id', 'name')

class PromoSer(ModelSerializer):
    prizes = PrizeSer(many=True)
    participants = ParticipantSer(many=True)
    class Meta:
        model = Promo
        fields = ('id', 'name', 'description', 'prizes', 'participants')
        read_only = ('id', 'prizes', 'participants')



class ResultSer(ModelSerializer):
    winner = ParticipantSer()
    prize = PrizeSer()
    
    class Meta: 
        model = Result
        fields = ('winner', 'prize')

class PromoMinSer(ModelSerializer):
    class Meta:
        model = Promo
        fields = ('id', 'name', 'description')
        read_only = ('id', )
        optional_fields = ('description', )