"""Dashboard API — analytics with date-range filtering."""
import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.permissions import IsAdminOrMasterOrOwner


def _monthly_breakdown(date_from, date_to, cost_fn):
    result = []
    current = date_from.replace(day=1)
    while current <= date_to:
        if current.month == 12:
            nxt = current.replace(year=current.year + 1, month=1, day=1)
        else:
            nxt = current.replace(month=current.month + 1, day=1)
        month_end = nxt - datetime.timedelta(days=1)
        ms = max(current, date_from)
        me = min(month_end, date_to)
        result.append({
            'month': current.strftime('%Y-%m'),
            'month_label': current.strftime('%b %Y'),
            'cost': round(cost_fn(ms, me), 2),
        })
        current = nxt
    return result


def _naive(dt):
    if dt is None:
        return None
    if timezone.is_aware(dt):
        return timezone.localtime(dt).replace(tzinfo=None)
    return dt


class DashboardView(APIView):
    permission_classes = [IsAdminOrMasterOrOwner]

    def get(self, request):
        from apps.machines.models import Machine, MaintenanceSchedule, MaintenanceHistory, TaskSparePart
        from apps.workshops.models import Workshop
        from django.db.models import Sum

        today = timezone.now().date()

        try:
            date_from = datetime.date.fromisoformat(request.query_params['date_from'])
        except (KeyError, ValueError, TypeError):
            date_from = today - datetime.timedelta(days=30)

        try:
            date_to = datetime.date.fromisoformat(request.query_params['date_to'])
        except (KeyError, ValueError, TypeError):
            date_to = today

        if date_from > date_to:
            date_from, date_to = date_to, date_from

        period_days = (date_to - date_from).days + 1
        total_period_hours = period_days * 24
        prev_date_to = date_from - datetime.timedelta(days=1)
        prev_date_from = prev_date_to - datetime.timedelta(days=period_days - 1)

        period_start_dt = datetime.datetime.combine(date_from, datetime.time.min)
        period_end_dt = datetime.datetime.combine(date_to, datetime.time.max)

        # ── All active machines ──
        machines = list(
            Machine.objects.filter(deleted_at__isnull=True)
            .select_related('current_status', 'workshop')
        )

        # ── Machine hours (repair duration from MaintenanceHistory) ──
        repairs = list(
            MaintenanceHistory.objects.filter(
                repair_started_at__isnull=False,
                repair_started_at__date__lte=date_to,
                completed_at__date__gte=date_from,
            ).select_related('machine', 'machine__workshop')
        )

        repair_map = {}
        for h in repairs:
            mid = h.machine_id
            rs = _naive(h.repair_started_at)
            ce = _naive(h.completed_at)
            start = max(rs, period_start_dt)
            end = min(ce, period_end_dt)
            hours = max((end - start).total_seconds() / 3600, 0)
            if mid not in repair_map:
                repair_map[mid] = {
                    'machine_name': h.machine.name,
                    'inventory_number': h.machine.inventory_number,
                    'workshop_name': h.machine.workshop.name if h.machine.workshop else '—',
                    'repair_hours': 0.0,
                }
            repair_map[mid]['repair_hours'] += hours

        # Ongoing repairs (started but not completed)
        now_naive = _naive(timezone.now())
        for sched in MaintenanceSchedule.objects.filter(
            machine__deleted_at__isnull=True,
            repair_started_at__isnull=False,
        ).select_related('machine', 'machine__workshop'):
            rs = _naive(sched.repair_started_at)
            start = max(rs, period_start_dt)
            end = min(now_naive, period_end_dt)
            if end > start:
                hours = (end - start).total_seconds() / 3600
                mid = sched.machine_id
                if mid not in repair_map:
                    repair_map[mid] = {
                        'machine_name': sched.machine.name,
                        'inventory_number': sched.machine.inventory_number,
                        'workshop_name': sched.machine.workshop.name if sched.machine.workshop else '—',
                        'repair_hours': 0.0,
                    }
                repair_map[mid]['repair_hours'] += hours

        machine_hours_items = []
        for m in machines:
            data = repair_map.get(m.id)
            rh = round(min(data['repair_hours'], total_period_hours), 1) if data else 0.0
            wh = round(max(total_period_hours - rh, 0), 1)
            machine_hours_items.append({
                'machine_id': m.id,
                'machine_name': m.name,
                'inventory_number': m.inventory_number,
                'workshop_id': m.workshop_id,
                'workshop_name': m.workshop.name if m.workshop else None,
                'work_hours': wh,
                'repair_hours': rh,
                'idle_hours': 0.0,
                'total_hours': total_period_hours,
            })

        total_repair_h = round(sum(x['repair_hours'] for x in machine_hours_items), 1)
        total_work_h = round(sum(x['work_hours'] for x in machine_hours_items), 1)
        total_idle_h = round(sum(x['idle_hours'] for x in machine_hours_items), 1)

        # ── Group machine hours by workshop for the chart/drill-down ──
        workshop_hours_map = {}
        for item in machine_hours_items:
            wid = item['workshop_id']
            wname = item['workshop_name'] or "Boshqa"
            if wid not in workshop_hours_map:
                workshop_hours_map[wid] = {
                    'workshop_id': wid,
                    'workshop_name': wname,
                    'work_hours': 0.0,
                    'repair_hours': 0.0,
                    'idle_hours': 0.0,
                    'machines': [],
                }
            entry = workshop_hours_map[wid]
            entry['work_hours'] = round(entry['work_hours'] + item['work_hours'], 1)
            entry['repair_hours'] = round(entry['repair_hours'] + item['repair_hours'], 1)
            entry['idle_hours'] = round(entry['idle_hours'] + item['idle_hours'], 1)
            entry['machines'].append({
                'machine_id': item['machine_id'],
                'machine_name': item['machine_name'],
                'inventory_number': item['inventory_number'],
                'work_hours': item['work_hours'],
                'repair_hours': item['repair_hours'],
                'idle_hours': item['idle_hours'],
            })

        named_workshops = sorted(
            (w for w in workshop_hours_map.values() if w['workshop_id'] is not None),
            key=lambda x: x['repair_hours'], reverse=True,
        )
        other_workshops = [w for w in workshop_hours_map.values() if w['workshop_id'] is None]
        machine_hours_by_workshop = named_workshops + other_workshops

        # ── TO expenses ──
        to_qs = MaintenanceHistory.objects.filter(
            completed_at__date__gte=date_from,
            completed_at__date__lte=date_to,
        )
        total_to = float(to_qs.aggregate(t=Sum('total_cost'))['t'] or 0)

        workshop_to = []
        for ws in Workshop.objects.all():
            mids = list(Machine.objects.filter(workshop=ws, deleted_at__isnull=True).values_list('id', flat=True))
            if not mids:
                continue
            cost = float(to_qs.filter(machine_id__in=mids).aggregate(t=Sum('total_cost'))['t'] or 0)
            if cost > 0:
                workshop_to.append({
                    'workshop_id': ws.id,
                    'workshop_name': ws.name,
                    'cost': round(cost, 2),
                    'machines_count': len(mids),
                })
        workshop_to.sort(key=lambda x: x['cost'], reverse=True)

        raw_machine_to = list(
            to_qs.values('machine_id', 'machine__name', 'machine__inventory_number', 'machine__workshop__name')
            .annotate(cost=Sum('total_cost'))
            .order_by('-cost')[:10]
        )
        max_cost = max((float(r['cost']) for r in raw_machine_to), default=1) or 1
        machine_to = [{
            'machine_id': r['machine_id'],
            'machine_name': r['machine__name'],
            'inventory_number': r['machine__inventory_number'],
            'workshop_name': r['machine__workshop__name'] or '—',
            'cost': round(float(r['cost']), 2),
            'percentage': round(float(r['cost']) / max_cost * 100),
        } for r in raw_machine_to]

        monthly_to = _monthly_breakdown(date_from, date_to, lambda ms, me: float(
            MaintenanceHistory.objects.filter(
                completed_at__date__gte=ms, completed_at__date__lte=me
            ).aggregate(t=Sum('total_cost'))['t'] or 0
        ))

        # ── Warehouse expenses ──
        wh_qs = TaskSparePart.objects.filter(
            deducted=True,
            created_at__date__gte=date_from,
            created_at__date__lte=date_to,
        )
        total_wh = float(wh_qs.aggregate(t=Sum('cost'))['t'] or 0)

        top_parts_raw = list(
            wh_qs.values('spare_part_id', 'spare_part__name', 'spare_part__unit__short_name', 'spare_part__unit__name')
            .annotate(total_cost=Sum('cost'), total_qty=Sum('quantity_used'))
            .order_by('-total_cost')[:5]
        )
        top_spare_parts = [{
            'id': r['spare_part_id'],
            'name': r['spare_part__name'],
            'unit': r['spare_part__unit__short_name'] or r['spare_part__unit__name'] or '',
            'total_cost': round(float(r['total_cost'] or 0), 2),
            'total_qty': round(float(r['total_qty'] or 0), 3),
        } for r in top_parts_raw]

        # ── Total expenses ──
        total_cost = total_to + total_wh
        to_pct = round(total_to / total_cost * 100, 1) if total_cost else 0
        wh_pct = round(100 - to_pct, 1) if total_cost else 0

        prev_to = float(
            MaintenanceHistory.objects.filter(
                completed_at__date__gte=prev_date_from,
                completed_at__date__lte=prev_date_to,
            ).aggregate(t=Sum('total_cost'))['t'] or 0
        )
        prev_wh = float(
            TaskSparePart.objects.filter(
                deducted=True,
                created_at__date__gte=prev_date_from,
                created_at__date__lte=prev_date_to,
            ).aggregate(t=Sum('cost'))['t'] or 0
        )
        prev_total = prev_to + prev_wh
        change_pct = round((total_cost - prev_total) / prev_total * 100, 1) if prev_total else None

        # ── Machine status (current, not date-filtered) ──
        schedules_map = {
            s.machine_id: s
            for s in MaintenanceSchedule.objects.filter(machine__deleted_at__isnull=True)
        }
        groups = {'working': [], 'in_repair': [], 'stopped': [], 'no_schedule': []}
        for m in machines:
            info = {
                'machine_id': m.id,
                'machine_name': m.name,
                'inventory_number': m.inventory_number,
                'workshop_name': m.workshop.name if m.workshop else '—',
                'status_name': m.current_status.name if m.current_status else '—',
                'status_color': m.current_status.color if m.current_status else 'gray',
            }
            sched = schedules_map.get(m.id)
            if sched and sched.in_repair:
                groups['in_repair'].append(info)
            elif not sched:
                groups['no_schedule'].append(info)
            elif m.current_status and m.current_status.color in ('red', 'gray'):
                groups['stopped'].append(info)
            else:
                groups['working'].append(info)

        machine_status = {k: {'count': len(v), 'machines': v} for k, v in groups.items()}

        return Response({
            'period': {
                'date_from': date_from.isoformat(),
                'date_to': date_to.isoformat(),
                'days': period_days,
            },
            'machine_hours': {
                'by_workshop': machine_hours_by_workshop,
                'total_work_hours': total_work_h,
                'total_repair_hours': total_repair_h,
                'total_idle_hours': total_idle_h,
                'period_hours': total_period_hours,
            },
            'to_expenses': {
                'total': round(total_to, 2),
                'by_workshop': workshop_to,
                'by_machine': machine_to,
                'monthly_chart': monthly_to,
            },
            'warehouse_expenses': {
                'total': round(total_wh, 2),
                'top_parts': top_spare_parts,
            },
            'total_expenses': {
                'total': round(total_cost, 2),
                'to_amount': round(total_to, 2),
                'warehouse_amount': round(total_wh, 2),
                'to_pct': to_pct,
                'warehouse_pct': wh_pct,
                'prev_total': round(prev_total, 2),
                'change_pct': change_pct,
                'change_amount': round(total_cost - prev_total, 2),
            },
            'machine_status': machine_status,
            'total_machines': len(machines),
        })
