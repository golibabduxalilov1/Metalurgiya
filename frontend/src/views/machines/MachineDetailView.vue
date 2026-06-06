<template>
  <div class="animate-fade-in max-w-6xl mx-auto">
    <!-- Loading skeleton -->
    <div v-if="loading" class="space-y-6">
      <div class="skeleton h-10 w-64 rounded-lg"></div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 skeleton h-80 rounded-xl"></div>
        <div class="skeleton h-80 rounded-xl"></div>
      </div>
    </div>

    <template v-else-if="machine">
      <!-- Back + header -->
      <div class="flex items-center gap-4 mb-6">
        <button @click="$router.back()" class="p-2 rounded-lg text-slate-500 hover:bg-slate-200 transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        <div class="flex-1">
          <div class="flex items-center gap-3 flex-wrap">
            <h1 class="text-2xl font-bold text-slate-900">{{ machine.name }}</h1>
            <StatusBadge :status="machine.current_status_data?.name" :color="machine.current_status_data?.color" size="md" />
            <span v-if="machine.deleted_at" class="status-badge bg-red-100 text-red-700">Удалён</span>
          </div>
          <p class="text-slate-500 text-sm mt-0.5 font-mono">{{ machine.inventory_number }}</p>
        </div>
        <div class="flex items-center gap-2">
          <!-- Change status -->
          <button v-if="auth.canWrite && !machine.deleted_at"
            @click="showStatusModal = true"
            class="btn-md btn-secondary">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Сменить статус
          </button>
          <RouterLink v-if="auth.canWrite && !machine.deleted_at"
            :to="`/machines/${machine.id}/edit`" class="btn-md btn-primary">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            Редактировать
          </RouterLink>
        </div>
      </div>

      <!-- Main grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left col: main info + attachments -->
        <div class="lg:col-span-2 space-y-6">

          <!-- Basic info -->
          <div class="card p-6">
            <h2 class="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Основная информация</h2>
            <div class="grid grid-cols-2 gap-x-6 gap-y-4">
              <InfoField label="Наименование" :value="machine.name" />
              <InfoField label="Инвентарный номер" :value="machine.inventory_number" mono />
              <InfoField label="Модель" :value="machine.model" />
              <InfoField label="Производитель" :value="machine.manufacturer" />
              <InfoField label="Год выпуска" :value="machine.year_manufactured" />
              <InfoField label="Дата ввода в экспл." :value="formatDate(machine.commissioned_date)" />
              <InfoField label="Тип станка" :value="machine.machine_type_name" />
              <InfoField label="Рабочее место" :value="machine.workplace" />
            </div>
            <div v-if="machine.description" class="mt-4 pt-4 border-t border-slate-100">
              <div class="text-xs text-slate-500 font-medium mb-1">Описание / Комментарий</div>
              <p class="text-sm text-slate-700 whitespace-pre-line">{{ machine.description }}</p>
            </div>
          </div>

          <!-- Location & operator -->
          <div class="card p-6">
            <h2 class="text-sm font-semibold text-slate-500 uppercase tracking-wide mb-4">Расположение и оператор</h2>
            <div class="grid grid-cols-2 gap-x-6 gap-y-4">
              <InfoField label="Цех" :value="machine.workshop_name" />
              <InfoField label="Участок" :value="machine.section_name" />
            </div>
            <div class="mt-4 pt-4 border-t border-slate-100">
              <div class="flex items-center justify-between mb-3">
                <div class="text-xs text-slate-500 font-medium">Оператор</div>
                <button v-if="auth.canWrite" @click="showAssignModal = true"
                  class="text-xs text-primary-600 hover:text-primary-700 font-medium">
                  {{ machine.assigned_operator ? 'Изменить' : 'Закрепить' }}
                </button>
              </div>
              <div v-if="machine.operator_data" class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                <div class="w-9 h-9 bg-primary-100 rounded-full flex items-center justify-center">
                  <span class="text-primary-700 font-semibold text-sm">
                    {{ machine.operator_data.full_name[0] }}
                  </span>
                </div>
                <div>
                  <div class="text-sm font-medium text-slate-900">{{ machine.operator_data.full_name }}</div>
                  <div class="text-xs text-slate-500">{{ machine.operator_data.position }}</div>
                </div>
              </div>
              <div v-else-if="machine.assigned_brigade" class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg">
                <svg class="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
                <span class="text-sm text-slate-700">{{ machine.assigned_brigade }}</span>
              </div>
              <div v-else class="text-sm text-slate-400 italic">Оператор не назначен</div>
            </div>
          </div>

          <!-- Attachments -->
          <div class="card p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-sm font-semibold text-slate-500 uppercase tracking-wide">Файлы и документы</h2>
              <label v-if="auth.canWrite" class="cursor-pointer">
                <input type="file" class="hidden" @change="handleUpload"
                  accept=".jpg,.jpeg,.png,.pdf,.doc,.docx" multiple />
                <span class="btn-sm btn-secondary">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  Загрузить
                </span>
              </label>
            </div>
            <div v-if="machine.attachments.length === 0" class="text-sm text-slate-400 italic text-center py-4">
              Нет прикреплённых файлов
            </div>
            <div v-else class="space-y-2">
              <div v-for="att in machine.attachments" :key="att.id"
                class="flex items-center gap-3 p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
                <div :class="fileIconClass(att.content_type)" class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-medium text-slate-800 truncate">{{ att.original_filename }}</div>
                  <div class="text-xs text-slate-400">{{ att.file_size_display }} · {{ formatDate(att.uploaded_at) }}</div>
                </div>
                <a :href="att.file_url" target="_blank" class="p-1.5 text-slate-400 hover:text-primary-600 transition-colors">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Right col: status history + meta -->
        <div class="space-y-6">
          <!-- Meta info -->
          <div class="card p-5">
            <h2 class="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">Метаданные</h2>
            <div class="space-y-2.5">
              <div class="flex items-center justify-between text-sm">
                <span class="text-slate-500">Создан</span>
                <span class="text-slate-700">{{ formatDateTime(machine.created_at) }}</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-slate-500">Автор</span>
                <span class="text-slate-700">{{ machine.created_by_name || '—' }}</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-slate-500">Обновлён</span>
                <span class="text-slate-700">{{ formatDateTime(machine.updated_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Status history -->
          <div class="card p-5">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xs font-semibold text-slate-500 uppercase tracking-wide">История статусов</h2>
              <span class="text-xs text-slate-400">{{ machine.recent_status_history?.length || 0 }} записей</span>
            </div>
            <div v-if="!machine.recent_status_history?.length" class="text-sm text-slate-400 text-center py-4">
              История пуста
            </div>
            <div v-else class="space-y-3">
              <div v-for="h in machine.recent_status_history" :key="h.id" class="relative pl-5">
                <!-- Timeline line -->
                <div class="absolute left-1.5 top-4 bottom-0 w-px bg-slate-200"></div>
                <!-- Dot -->
                <div class="absolute left-0 top-1 w-3 h-3 rounded-full border-2 border-white shadow-sm"
                  :class="`bg-status-${colorMap[h.new_status_color] || 'gray'}`"></div>
                <div class="pb-3">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span :class="['status-badge', `status-${h.new_status_color}`]">
                      {{ h.new_status_name }}
                    </span>
                    <span v-if="h.previous_status_name" class="text-xs text-slate-400">
                      ← {{ h.previous_status_name }}
                    </span>
                  </div>
                  <div class="text-xs text-slate-500 mt-1">{{ h.changed_by_name }}</div>
                  <div class="text-xs text-slate-400">{{ formatDateTime(h.changed_at) }}</div>
                  <div v-if="h.comment" class="text-xs text-slate-600 mt-1 italic">"{{ h.comment }}"</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Change Status Modal -->
    <ChangeStatusModal
      v-if="showStatusModal"
      :machine-id="machine?.id"
      @updated="onStatusUpdated"
      @close="showStatusModal = false" />

    <!-- Assign Operator Modal -->
    <AssignOperatorModal
      v-if="showAssignModal"
      :machine="machine"
      @updated="onAssignUpdated"
      @close="showAssignModal = false" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '@/store/auth'
import { machinesApi } from '@/api'
import StatusBadge from '@/components/common/StatusBadge.vue'
import InfoField from '@/components/common/InfoField.vue'
import ChangeStatusModal from '@/components/machines/ChangeStatusModal.vue'
import AssignOperatorModal from '@/components/machines/AssignOperatorModal.vue'
import dayjs from 'dayjs'

const auth = useAuthStore()
const toast = useToast()
const route = useRoute()

const machine = ref(null)
const loading = ref(true)
const showStatusModal = ref(false)
const showAssignModal = ref(false)

const colorMap = { green: 'working', yellow: 'idle', red: 'repair', gray: 'retired', blue: 'maintenance' }

function formatDate(d) { return d ? dayjs(d).format('DD.MM.YYYY') : '—' }
function formatDateTime(d) { return d ? dayjs(d).format('DD.MM.YYYY HH:mm') : '—' }

function fileIconClass(type) {
  if (!type) return 'bg-slate-200 text-slate-500'
  if (type.includes('image')) return 'bg-blue-100 text-blue-600'
  if (type.includes('pdf')) return 'bg-red-100 text-red-600'
  return 'bg-slate-200 text-slate-500'
}

async function loadMachine() {
  loading.value = true
  try {
    const res = await machinesApi.get(route.params.id)
    machine.value = res.data
  } catch {
    toast.error('Станок не найден')
  } finally {
    loading.value = false
  }
}

async function handleUpload(e) {
  const files = e.target.files
  for (const file of files) {
    const formData = new FormData()
    formData.append('file', file)
    try {
      await machinesApi.upload(machine.value.id, formData)
      toast.success(`Файл "${file.name}" загружен`)
    } catch {
      toast.error(`Ошибка загрузки "${file.name}"`)
    }
  }
  e.target.value = ''
  loadMachine()
}

function onStatusUpdated() {
  showStatusModal.value = false
  loadMachine()
}

function onAssignUpdated() {
  showAssignModal.value = false
  loadMachine()
}

onMounted(loadMachine)
</script>
