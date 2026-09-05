from datetime import timedelta
from django.db.models import Avg, Count, F
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.disposals.models import Disposal, DisposalCategory


class DashboardStatisticsView(APIView):
    PERIOD_DAYS = {"month": 30, "3months": 90, "6months": 180, "year": 365}

    def get(self, request):
        period = request.query_params.get("period", "6months")
        queryset = Disposal.objects.all()
        if period in self.PERIOD_DAYS:
            queryset = queryset.filter(created_at__gte=timezone.now() - timedelta(days=self.PERIOD_DAYS[period]))

        monthly = queryset.annotate(month=TruncMonth("created_at")).values("month").annotate(count=Count("id")).order_by("month")
        categories = DisposalCategory.objects.filter(disposal__in=queryset).values(name=F("category__name")).annotate(value=Count("id")).order_by("-value")
        total = sum(row["value"] for row in categories) or 1
        return Response({
            "disposals": [{"month": row["month"].strftime("%b"), "count": row["count"]} for row in monthly],
            "categories": [{"name": row["name"], "value": round(row["value"] * 100 / total, 1)} for row in categories],
            "totals": {"disposals": queryset.count(), "averageQuantity": queryset.aggregate(value=Avg("quantity"))["value"] or 0},
        })
