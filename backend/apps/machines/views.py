"""
Machines App Views
"""
import io
from django.utils import timezone
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from utils.permissions import IsAdmin, IsAdminOrMaster, IsAdminOrMasterOrOwner
from .models import (
    Machine, MachineType, MachineStatus,
    MachineStatusHistory, MachineAttachment, MachineAssignment
)
from .serializers import (
    MachineListSerializer, MachineDetailSerializer, MachineCreateUpdateSerializer,
    MachineTypeSerializer, MachineStatusSerializer, MachineStatusHistorySerializer,
    MachineAttachmentSerializer, MachineAttachmentCreateSerializer,
    MachineAssignmentSerializer, ChangeStatusSerializer
)
from .filters import MachineFilter
from apps.audit.signals import log_action


@extend_schema(tags=['machine-types'])
class MachineTypeViewSet(viewsets.ModelViewSet):
    """Управление типами станков"""
    queryset = MachineType.objects.all()
    serializer_class = MachineTypeSerializer
    permission_classes = [IsAdminOrMaster]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdmin()]


@extend_schema(tags=['machine-statuses'])
class MachineStatusViewSet(viewsets.ModelViewSet):
    """Управление статусами станков"""
    queryset = MachineStatus.objects.all()
    serializer_class = MachineStatusSerializer
    search_fields = ['name']
    ordering_fields = ['sort_order', 'name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdmin()]


@extend_schema(tags=['machines'])
@extend_schema_view(
    list=extend_schema(
        summary='Список станков',
        parameters=[
            OpenApiParameter('status', description='ID статуса'),
            OpenApiParameter('workshop', description='ID цеха'),
            OpenApiParameter('machine_type', description='ID типа'),
            OpenApiParameter('operator', description='ID оператора'),
            OpenApiParameter('search', description='Поиск по тексту'),
            OpenApiParameter('include_deleted', description='Включать удалённые', type=bool),
        ]
    ),
    retrieve=extend_schema(summary='Карточка станка'),
    create=extend_schema(summary='Добавить станок'),
    update=extend_schema(summary='Обновить станок'),
    partial_update=extend_schema(summary='Частично обновить станок'),
)
class MachineViewSet(viewsets.ModelViewSet):
    """
    Реестр станков. Поддерживает:
    - CRUD операции
    - Поиск, фильтрация, сортировка
    - Смена статуса с историей
    - Прикрепление файлов
    - Закрепление операторов
    - Импорт/экспорт Excel
    - Мягкое удаление и восстановление
    """
    queryset = Machine.objects.select_related(
        'machine_type', 'current_status', 'workshop', 'section',
        'assigned_operator', 'created_by'
    ).prefetch_related('attachments', 'status_history', 'assignments')
    filterset_class = MachineFilter
    search_fields = ['name', 'inventory_number', 'model', 'manufacturer', 'description']
    ordering_fields = ['name', 'inventory_number', 'created_at', 'updated_at']
    ordering = ['inventory_number']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrMasterOrOwner()]
        if self.action in ['create', 'update', 'partial_update', 'assign_operator',
                          'change_status', 'upload_attachment']:
            return [IsAdminOrMaster()]
        if self.action in ['destroy', 'restore', 'import_excel']:
            return [IsAdmin()]
        return [IsAdminOrMaster()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MachineDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return MachineCreateUpdateSerializer
        return MachineListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        include_deleted = self.request.query_params.get('include_deleted', 'false').lower() == 'true'
        if not include_deleted:
            qs = qs.filter(deleted_at__isnull=True)
        elif not self.request.user.is_admin:
            qs = qs.filter(deleted_at__isnull=True)
        return qs

    def perform_create(self, serializer):
        machine = serializer.save(created_by=self.request.user)
        log_action(self.request.user, 'create', machine, None, machine.__dict__)

    def perform_update(self, serializer):
        old_data = {f.name: getattr(serializer.instance, f.name) for f in serializer.instance._meta.fields}
        machine = serializer.save()
        new_data = {f.name: getattr(machine, f.name) for f in machine._meta.fields}
        log_action(self.request.user, 'update', machine, old_data, new_data)

    @extend_schema(summary='Мягкое удаление станка')
    def destroy(self, request, *args, **kwargs):
        machine = self.get_object()
        machine.deleted_at = timezone.now()
        machine.deleted_by = request.user
        machine.save()
        log_action(request.user, 'delete', machine, None, None)
        return Response({'detail': 'Станок помечен как удалённый'}, status=status.HTTP_200_OK)

    @extend_schema(summary='Восстановить удалённый станок')
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        machine = Machine.objects.get(pk=pk)
        machine.deleted_at = None
        machine.deleted_by = None
        machine.save()
        log_action(request.user, 'restore', machine, None, None)
        return Response({'detail': 'Станок восстановлен'})

    @extend_schema(summary='Сменить статус станка', request=ChangeStatusSerializer)
    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        machine = self.get_object()
        serializer = ChangeStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        comment = serializer.validated_data.get('comment', '')
        old_status = machine.current_status

        # Create history record
        MachineStatusHistory.objects.create(
            machine=machine,
            previous_status=old_status,
            new_status=new_status,
            changed_by=request.user,
            comment=comment
        )

        machine.current_status = new_status
        machine.save(update_fields=['current_status', 'updated_at'])
        log_action(request.user, 'status_change', machine,
                   {'status': str(old_status)}, {'status': str(new_status)})

        return Response(MachineDetailSerializer(machine, context={'request': request}).data)

    @extend_schema(summary='История статусов станка')
    @action(detail=True, methods=['get'], url_path='status-history')
    def status_history(self, request, pk=None):
        machine = self.get_object()
        history = machine.status_history.all()
        serializer = MachineStatusHistorySerializer(history, many=True)
        return Response(serializer.data)

    @extend_schema(summary='Загрузить файл к станку', request=MachineAttachmentCreateSerializer)
    @action(detail=True, methods=['post'], url_path='upload',
            parser_classes=[MultiPartParser, FormParser])
    def upload_attachment(self, request, pk=None):
        machine = self.get_object()
        serializer = MachineAttachmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = request.FILES['file']
        attachment = MachineAttachment.objects.create(
            machine=machine,
            file=file,
            original_filename=file.name,
            file_size=file.size,
            content_type=file.content_type,
            description=serializer.validated_data.get('description', ''),
            uploaded_by=request.user
        )
        return Response(
            MachineAttachmentSerializer(attachment, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    @extend_schema(summary='Закрепить оператора за станком')
    @action(detail=True, methods=['post'], url_path='assign-operator')
    def assign_operator(self, request, pk=None):
        from apps.employees.models import Employee
        machine = self.get_object()
        operator_id = request.data.get('operator_id')
        notes = request.data.get('notes', '')

        # Unassign current
        MachineAssignment.objects.filter(machine=machine, is_current=True).update(
            is_current=False, unassigned_at=timezone.now()
        )

        if operator_id:
            try:
                operator = Employee.objects.get(id=operator_id)
            except Employee.DoesNotExist:
                return Response({'detail': 'Оператор не найден'}, status=status.HTTP_404_NOT_FOUND)

            assignment = MachineAssignment.objects.create(
                machine=machine,
                operator=operator,
                assigned_by=request.user,
                notes=notes
            )
            machine.assigned_operator = operator
            machine.save(update_fields=['assigned_operator', 'updated_at'])
            return Response(MachineAssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)
        else:
            machine.assigned_operator = None
            machine.save(update_fields=['assigned_operator', 'updated_at'])
            return Response({'detail': 'Оператор откреплён'})

    @extend_schema(summary='Экспорт реестра в Excel')
    @action(detail=False, methods=['get'], url_path='export-excel')
    def export_excel(self, request):
        machines = self.filter_queryset(self.get_queryset())
        wb = self._build_excel_export(machines)
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="machines_export.xlsx"'
        return response

    def _build_excel_export(self, machines):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Реестр станков'

        headers = [
            'Инв. №', 'Наименование', 'Модель', 'Производитель',
            'Год выпуска', 'Тип станка', 'Статус', 'Цех', 'Участок',
            'Рабочее место', 'Оператор', 'Дата ввода', 'Описание'
        ]

        header_fill = PatternFill(start_color='1E3A5F', end_color='1E3A5F', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF', size=11)
        header_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
        thin_border = Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin')
        )

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num, value=header)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_align
            cell.border = thin_border

        ws.row_dimensions[1].height = 40

        for row_num, machine in enumerate(machines, 2):
            row_data = [
                machine.inventory_number,
                machine.name,
                machine.model or '',
                machine.manufacturer or '',
                machine.year_manufactured or '',
                machine.machine_type.name if machine.machine_type else '',
                machine.current_status.name if machine.current_status else '',
                machine.workshop.name if machine.workshop else '',
                machine.section.name if machine.section else '',
                machine.workplace or '',
                machine.assigned_operator.full_name if machine.assigned_operator else '',
                machine.commissioned_date.strftime('%d.%m.%Y') if machine.commissioned_date else '',
                machine.description or '',
            ]
            for col_num, value in enumerate(row_data, 1):
                cell = ws.cell(row=row_num, column=col_num, value=value)
                cell.border = thin_border
                cell.alignment = Alignment(vertical='center')
                if row_num % 2 == 0:
                    cell.fill = PatternFill(start_color='F0F4F8', end_color='F0F4F8', fill_type='solid')

        col_widths = [15, 30, 20, 20, 12, 20, 15, 20, 20, 15, 25, 15, 40]
        for col_num, width in enumerate(col_widths, 1):
            ws.column_dimensions[get_column_letter(col_num)].width = width

        ws.freeze_panes = 'A2'
        return wb

    @extend_schema(summary='Импорт станков из Excel')
    @action(detail=False, methods=['post'], url_path='import-excel',
            parser_classes=[MultiPartParser, FormParser])
    def import_excel(self, request):
        if 'file' not in request.FILES:
            return Response({'detail': 'Файл не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        errors = []
        created = 0
        updated = 0

        try:
            wb = openpyxl.load_workbook(file)
            ws = wb.active

            for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
                if not any(row):
                    continue

                inv_num = str(row[0]).strip() if row[0] else None
                if not inv_num:
                    errors.append({'row': row_num, 'error': 'Инвентарный номер обязателен'})
                    continue

                try:
                    machine, created_flag = Machine.objects.update_or_create(
                        inventory_number=inv_num,
                        defaults={
                            'name': str(row[1] or '').strip() or inv_num,
                            'model': str(row[2] or '').strip(),
                            'manufacturer': str(row[3] or '').strip(),
                            'created_by': request.user,
                        }
                    )
                    if created_flag:
                        created += 1
                    else:
                        updated += 1
                except Exception as e:
                    errors.append({'row': row_num, 'error': str(e)})

        except Exception as e:
            return Response({'detail': f'Ошибка чтения файла: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'created': created,
            'updated': updated,
            'errors': errors,
            'total_processed': created + updated + len(errors)
        })

    @extend_schema(summary='Шаблон Excel для импорта')
    @action(detail=False, methods=['get'], url_path='import-template')
    def import_template(self, request):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Шаблон импорта'
        headers = ['Инв. №*', 'Наименование*', 'Модель', 'Производитель', 'Год выпуска']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='1E3A5F', end_color='1E3A5F', fill_type='solid')

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="machines_import_template.xlsx"'
        return response
