"""Dashboard API — single endpoint for all dashboard data."""
import datetime
from decimal import Decimal

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import IsAdminOrMasterOrOwner


class DashboardView(APIView):
    permission_classes = [IsAdminOrMasterOrOwner]

    def get(self, request):
        today = timezone.now().date()
        current_month_start = today.replace(day=1)
        prev_month_end = current_month_start - datetime.timedelta(days=1)
        prev_month_start = prev_month_end.replace(day=1)
        year_start = today.replace(month=1, day=1)

        from apps.machines.models import Machine, MaintenanceSchedule, MaintenanceHistory
        from apps.warehouse.models import SparePart
        from django.db.models import Sum

        # ── Machines ──
        total_machines = Machine.objects.filter(deleted_at__isnull=True).count()

        # ── Schedules with alert levels ──
        schedules = list(
            MaintenanceSchedule.objects.filter(machine__deleted_at__isnull=True)
            .select_related('machine', 'machine__workshop')
        )
        levels = {'in_repair': 0, 'overdue': 0, 'near': 0, 'ok': 0}
        for s in schedules:
            lv = s.alert_level
            if lv in levels:
                levels[lv] += 1
        no_schedule = total_machines - len(schedules)

        # ── Expenses ──
        def month_expense(start, end=None):
            qs = MaintenanceHistory.objects.filter(completed_at__date__gte=start)
            if end:
                qs = qs.filter(completed_at__date__lte=end)
            return qs.aggregate(t=Sum('total_cost'))['t'] or Decimal('0')

        curr_exp = month_expense(current_month_start)
        prev_exp = month_expense(prev_month_start, prev_month_end)

        def pct_change(curr, prev):
            if not prev:
                return None
            return round((float(curr) - float(prev)) / float(prev) * 100, 1)

        # ── Warehouse value ──
        parts = list(SparePart.objects.select_related('unit').all())
        warehouse_val = sum(
            float(sp.unit_price or 0) * float(sp.quantity or 0) for sp in parts
        )

        # ── Workshop expenses ──
        from apps.workshops.models import Workshop
        ws_data = []
        for ws in Workshop.objects.all():
            mids = list(
                Machine.objects.filter(workshop=ws, deleted_at__isnull=True)
                .values_list('id', flat=True)
            )
            if not mids:
                continue
            c_exp = float(
                MaintenanceHistory.objects.filter(
                    machine_id__in=mids, completed_at__date__gte=current_month_start
                ).aggregate(t=Sum('total_cost'))['t'] or 0
            )
            y_exp = float(
                MaintenanceHistory.objects.filter(
                    machine_id__in=mids, completed_at__date__gte=year_start
                ).aggregate(t=Sum('total_cost'))['t'] or 0
            )
            ws_data.append({
                'workshop_id': ws.id,
                'workshop_name': ws.name,
                'machines_count': len(mids),
                'current_month_cost': c_exp,
                'yearly_cost': y_exp,
            })
        ws_data.sort(key=lambda x: x['yearly_cost'], reverse=True)

        # ── Top 10 machines by expense ──
        from django.db.models import Sum as S
        raw = (
            MaintenanceHistory.objects.values(
                'machine_id', 'machine__name', 'machine__inventory_number',
                'machine__workshop__name'
            ).annotate(total_expense=S('total_cost')).order_by('-total_expense')[:10]
        )
        max_exp = max((float(r['total_expense']) for r in raw), default=1) or 1
        top_machines = []
        for r in raw:
            last = (
                MaintenanceHistory.objects.filter(machine_id=r['machine_id'])
                .order_by('-completed_at').values('completed_at').first()
            )
            top_machines.append({
                'machine_id': r['machine_id'],
                'machine_name': r['machine__name'],
                'inventory_number': r['machine__inventory_number'],
                'workshop_name': r['machine__workshop__name'] or '—',
                'total_expense': round(float(r['total_expense']), 2),
                'last_to_date': last['completed_at'].date().isoformat() if last else None,
                'percentage': round(float(r['total_expense']) / max_exp * 100),
            })

        # ── 6-month chart ──
        monthly_chart = []
        for i in range(5, -1, -1):
            m = today.month - i
            y = today.year
            while m <= 0:
                m += 12
                y -= 1
            ms = today.replace(year=y, month=m, day=1)
            if m == 12:
                me = today.replace(year=y + 1, month=1, day=1) - datetime.timedelta(days=1)
            else:
                me = today.replace(year=y, month=m + 1, day=1) - datetime.timedelta(days=1)
            cost = float(
                MaintenanceHistory.objects.filter(
                    completed_at__date__gte=ms, completed_at__date__lte=me
                ).aggregate(t=S('total_cost'))['t'] or 0
            )
            monthly_chart.append({
                'month': f"{y}-{m:02d}",
                'month_label': ms.strftime('%b'),
                'total_cost': round(cost, 2),
            })

        # ── Recent 5 TO ──
        recent = list(
            MaintenanceHistory.objects.select_related('machine', 'completed_by')
            .order_by('-completed_at')[:5]
        )
        recent_to = [
            {
                'machine_name': r.machine.name,
                'inventory_number': r.machine.inventory_number,
                'completed_by_name': r.completed_by.get_full_name() if r.completed_by else '—',
                'completed_at': r.completed_at.isoformat(),
                'total_cost': round(float(r.total_cost), 2),
            }
            for r in recent
        ]

        # ── Low stock ──
        low_sp = list(
            SparePart.objects.filter(quantity__isnull=False, quantity__gte=0)
            .select_related('unit').prefetch_related('machines')
            .order_by('quantity')[:5]
        )
        low_stock = [
            {
                'id': sp.id,
                'name': sp.name,
                'quantity': float(sp.quantity),
                'unit_short': (sp.unit.short_name or sp.unit.name) if sp.unit else '',
                'machine_names': [m.inventory_number for m in sp.machines.all()[:3]],
            }
            for sp in low_sp
        ]

        return Response({
            'stats': {
                'total_machines': total_machines,
                'in_repair': levels['in_repair'],
                'overdue_to': levels['overdue'],
                'near_to': levels['near'],
                'current_month_expense': round(float(curr_exp), 2),
                'prev_month_expense': round(float(prev_exp), 2),
                'expense_change': pct_change(curr_exp, prev_exp),
                'total_warehouse_value': round(warehouse_val, 2),
            },
            'workshop_expenses': ws_data,
            'top_machines': top_machines,
            'monthly_chart': monthly_chart,
            'to_status': {
                'no_schedule': no_schedule,
                'ok': levels['ok'],
                'near': levels['near'],
                'overdue': levels['overdue'],
                'in_repair': levels['in_repair'],
            },
            'recent_to': recent_to,
            'low_stock': low_stock,
        })
