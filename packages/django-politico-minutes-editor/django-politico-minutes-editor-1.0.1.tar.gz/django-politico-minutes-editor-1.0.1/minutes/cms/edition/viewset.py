from minutes.utils.serialize_and_save import serialize_and_save
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from minutes.models import (
    Edition,
    Minute,
    MinuteType,
    Interstitial,
    Theme,
    InterstitialInstance,
    Vertical,
    Sponsor,
)
from minutes.tasks import publish_if_ready, unpublish, publish
from .serializers import (
    EditionSerializer,
    EditionContextSerializer,
    InterstitialInstanceSerializer,
    MinuteSerializer,
    MinuteTypeSerializer,
)
from ..common.serializers import (
    ThemeSerializer,
    VerticalSerializer,
    InterstitialSerializer,
    SponsorSerializer,
)
from ..common.viewsets.base import BaseCMSViewset


class EditionViewset(BaseCMSViewset):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer

    def context(self):
        return {
            "theme": ThemeSerializer(Theme.objects.all(), many=True).data,
            "sponsor": SponsorSerializer(
                Sponsor.objects.all(), many=True
            ).data,
            "vertical": VerticalSerializer(
                Vertical.objects.all(), many=True
            ).data,
            "interstitial": InterstitialSerializer(
                Interstitial.objects.all(), many=True
            ).data,
            "meta_types": MinuteTypeSerializer(
                MinuteType.objects.filter(is_meta=True), many=True
            ).data,
        }

    def create(self, request):
        serializer = EditionContextSerializer(data=request.data)
        serialize_and_save(serializer)
        return Response(serializer.data)

    def update(self, request, pk=None):
        data = request.data.copy()

        # Update cards
        cards = data.pop("cards")
        for card in cards:
            sort = card["edition_sort"]
            c_id = card["id"]
            if card["model"] == "Minute":
                m = Minute.objects.get(id=c_id)
                m_serializer = MinuteSerializer(m, data={"edition_sort": sort})
                serialize_and_save(m_serializer)
            elif card["model"] == "Interstitial":
                i = InterstitialInstance.objects.get(id=c_id)
                i_serializer = InterstitialInstanceSerializer(
                    i, data={"edition_sort": sort}
                )
                serialize_and_save(i_serializer)

        # Update other edition data
        instance = self.queryset.get(id=pk)
        serializer = self.serializer_class(instance, data=data)
        serialize_and_save(serializer)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def update_sort(self, request, pk=None):
        data = request.data.copy()

        # Update cards
        cards = data.pop("cards")
        for card in cards:
            sort = card["edition_sort"]
            c_id = card["id"]
            if card["model"] == "Minute":
                m = Minute.objects.get(id=c_id)
                m.edition_sort = sort
                m.save()
            elif card["model"] == "Interstitial":
                i = InterstitialInstance.objects.get(id=c_id)
                i.edition_sort = sort
                i.save()

        return Response("OK")

    @action(detail=True, methods=["post"])
    def update_sponsor(self, request, pk=None):
        data = request.data.copy()

        try:
            sponsor_data = data.get("sponsor")
            if sponsor_data:
                s = Sponsor.objects.get(id=sponsor_data.get("id"))
            else:
                s = None
        except Sponsor.DoesNotExist:
            s = None

        e = self.queryset.get(id=pk)
        e.sponsor = s
        e.save()

        return Response("OK")

    @action(detail=True, methods=["post"])
    def update_context(self, request, pk=None):
        data = request.data.copy()

        # Update other edition data
        instance = self.queryset.get(id=pk)
        currently_is_live = instance.live

        serializer = EditionContextSerializer(instance, data=data)
        serialize_and_save(serializer)

        publish_if_ready.delay(instance.id.hex)
        if currently_is_live and not instance.live:
            unpublish(instance.id.hex)

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def trigger_preview(self, request, pk=None):
        edition = self.get_object()
        r = publish(edition.id, "STAGING")

        if r.status_code == 200:
            return Response("OK")
        else:
            return Response(
                r.text, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=["post"])
    def trigger_publish(self, request, pk=None):
        edition = self.get_object()
        r = publish_if_ready(edition.id)

        if r.status_code == 200:
            return Response("OK")
        else:
            return Response(
                r.text, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
