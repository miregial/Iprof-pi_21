from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.serializers import PrizeSer, ResultSer, ParticipantSer, PromoMinSer, PromoSer
from api.models import Promo, Result
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from random import shuffle

class PromoViewSet(ViewSet):
    queryset = Promo.objects.all()

    @extend_schema(request=PromoMinSer,responses={201: int,422: OpenApiResponse(response=dict)})
    def create(self, request):
        serializer = PromoMinSer(data=request.data)
        if serializer.is_valid():
            promo = serializer.save()
            return Response(promo.id, status=201)
        else:
            return Response({"detail": serializer.errors}, status=422)

    @extend_schema(responses={200: PromoSer})
    def retrieve(self, request, pk):
        promo = get_object_or_404(self.queryset, pk=pk)
        serializer = PromoSer(promo)
        return Response(serializer.data)

    def destroy(self, request, pk):
        promo = get_object_or_404(self.queryset, pk=pk)
        promo.delete()
        return Response(status=204)

    @extend_schema(request=PromoMinSer,responses={206: PromoMinSer})
    def update(self, request, pk):
        promo = get_object_or_404(self.queryset, pk=pk)
        serializer = PromoMinSer(promo, data=request.data, partial=True)
        if serializer.is_valid():
            promo = serializer.save()
            return Response(status=206)
        else:
            return Response({"detail": serializer.errors}, status=422)


    @extend_schema(request=ParticipantSer,responses={201: int,422: OpenApiResponse(response=dict)})
    @action(detail=True, methods=['post'], url_path='rafle')
    def rafle(self, request, pk):
        promo = get_object_or_404(self.queryset, pk=pk)
        prizes = promo.prizes.all()
        participants = promo.participants.all()
        if len(prizes) == len(participants):
            shuffle(prizes)
            shuffle(participants)
            results = []
            for prize, participant in zip(prizes, participants):
                result = Result.objects.create(winner=participant, prize=prize)
                results.append(result)
            serializer = ResultSer(results, many=True)
            return Response(serializer.data, status=201)
        else:
            return Response(status=409)

    @action(detail=True, methods=['post'], url_path='participant')
    def add_participant(self, request, pk):
        promo = get_object_or_404(self.queryset, pk=pk)
        
        serializer = ParticipantSer(data=request.data)
        if serializer.is_valid():
            participant = serializer.save()
            print(participant)
            promo.participants.add(participant)
            return Response(participant.id, status=204)
        else:
            return Response({"detail": serializer.errors}, status=422)

    @extend_schema(request=PrizeSer,responses={204: int,422: OpenApiResponse(response=dict)})
    @action(detail=True, methods=['post'], url_path='prize')
    def add_prize(self, request, pk):
        promo = get_object_or_404(self.queryset, pk=pk)
        serializer = PrizeSer(data=request.data)
        if serializer.is_valid():
            prize = serializer.save()
            promo.prizes.add(prize)
            return Response(prize.id, status=204)
        else:
            return Response({"detail": serializer.errors}, status=422)
            
    @action(detail=True, methods=['delete'], url_path='participant/(?P<participant_id>[^/.]+)')
    def remove_participant(self, request, pk, participant_id):
        promo = get_object_or_404(self.queryset, pk=pk)
        participant = get_object_or_404(promo.participants.all(), pk=participant_id)
        promo.participants.remove(participant)
        return Response(status=200)


    @action(detail=True, methods=['delete'], url_path='participant/(?P<prize_pk>[^/.]+)')
    def remove_prize(self, request, pk, prize_pk):
        promo = get_object_or_404(self.queryset, pk=pk)
        promo.prizes.remove(get_object_or_404(promo.prizes.all(), pk=prize_pk))
        return Response(status=200)
    

    @extend_schema(responses={200: PromoMinSer})
    def list(self, request):
        serializer = PromoMinSer(self.queryset, many=True)
        return Response(serializer.data)