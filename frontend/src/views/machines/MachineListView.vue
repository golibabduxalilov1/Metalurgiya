<template>
  <div class="animate-fade-in">
    <!-- Header -->
    <div class="page-header flex-wrap gap-4">
      <div>
        <h1 class="page-title">Реестр станков</h1>
        <p class="page-subtitle">Всего: {{ pagination.count }} станков</p>
      </div>
      <div class="flex items-center gap-2">
        <!-- Import -->
        <div v-if="auth.isAdmin" class="relative">
          <input ref="fileInput" type="file" accept=".xlsx" class="hidden" @change="handleImport" />
          <button @click="fileInput.click()" class="btn-md btn-secondary" :disabled="importing">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
            </svg>
            {{ importing ? 'Импорт...' : 'Импорт' }}
          </button>
        </div>
        <!-- Export -->
        <button @click="handleExport" class="btn-md btn-secondary" :disabled="exporting">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          {{ exporting ? 'Экспорт...' : 'Excel' }}
        </button>
        <!-- Add -->
        <RouterLink v-if="auth.canWrite" to="/machines/new" class="btn-md btn-primary">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          Добавить станок
        </RouterLink>
      </div>
    </div>

    <!-- Filters bar -->
    <div class="card p-4 mb-5">
      <div class="flex flex-wrap items-center gap-3">
        <!-- Search -->
        <div class="relative flex-1 min-w-[200px]">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input v-model="filters.search" @input="debouncedSearch"
            type="text" placeholder="Поиск по наименованию, инв. номеру, модели..."
            class="form-input pl-9 h-9" />
        </div>

        <!-- Status filter -->
        <select v-model="filters.status" @change="loadMachines" class="form-select h-9 w-44">
          <option value="">Все статусы</option>
          <option v-for="s in statusOptions" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>

        <!-- Workshop filter -->
        <select v-model="filters.workshop" @change="onWorkshopChange" class="form-select h-9 w-44">
          <option value="">Все цеха</option>
          <option v-for="w in workshopOptions" :key="w.id" :value="w.id">{{ w.name }}</option>
        </select>

        <!-- Machine type filter -->
        <select v-model="filters.machine_type" @change="loadMachines" class="form-select h-9 w-44">
          <option value="">Все типы</option>
          <option v-for="t in typeOptions" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>

        <!-- Include deleted -->
        <label v-if="auth.isAdmin" class="flex items-center gap-2 text-sm text-slate-600 cursor-pointer">
          <input type="checkbox" v-model="filters.include_deleted" @change="loadMachines"
            class="rounded border-slate-300 text-primary-600" />
          Показать удалённые
        </label>

        <!-- Reset -->
        <button v-if="hasActiveFilters" @click="resetFilters" class="btn-md btn-ghost text-xs">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
          Сбросить
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="card overflow-hidden">
      <!-- Loading -->
      <div v-if="loading" class="p-8">
        <div class="space-y-3">
          <div v-for="i in 8" :key="i" class="skeleton h-14 rounded-lg"></div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="machines.length === 0" class="empty-state">
        <svg class="empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
            d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18"/>
        </svg>
        <div class="empty-state-title">Станки не найдены</div>
        <div class="empty-state-text">Попробуйте изменить параметры фильтра или добавьте новый станок</div>
        <RouterLink v-if="auth.canWrite" to="/machines/new" class="btn-md btn-primary mt-4">
          Добавить станок
        </RouterLink>
      </div>

      <!-- Table -->
      <div v-else class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th class="sortable" @click="toggleSort('inventory_number')">
                Инв. № {{ sortIcon('inventory_number') }}
              </th>
              <th class="sortable" @click="toggleSort('name')">
                Наименование {{ sortIcon('name') }}
              </th>
              <th>Тип / Модель</th>
              <th>Статус</th>
              <th>Расположение</th>
              <th>Оператор</th>
              <th class="sortable" @click="toggleSort('updated_at')">
                Обновлён {{ sortIcon('updated_at') }}
              </th>
              <th class="text-right">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="machine in machines" :key="machine.id"
              :class="machine.deleted_at ? 'opacity-50 bg-red-50/30' : ''"
              class="cursor-pointer" @click="$router.push(`/machines/${machine.id}`)">

              <td>
                <span class="font-mono text-sm font-medium text-primary-700">
                  {{ machine.inventory_number }}
                </span>
              </td>

              <td>
                <div class="font-medium text-slate-900">{{ machine.name }}</div>
                <div v-if="machine.manufacturer" class="text-xs text-slate-400">{{ machine.manufacturer }}</div>
              </td>

              <td>
                <div v-if="machine.machine_type_name" class="text-sm text-slate-700">{{ machine.machine_type_name }}</div>
                <div v-if="machine.model" class="text-xs text-slate-400">{{ machine.model }}</div>
              </td>

              <td @click.stop>
                <StatusBadge :status="machine.current_status_name" :color="machine.current_status_color" />
                <div v-if="machine.deleted_at" class="text-xs text-red-500 mt-0.5">Удалён</div>
              </td>

              <td>
                <div v-if="machine.workshop_name" class="text-sm text-slate-700">{{ machine.workshop_name }}</div>
                <div v-if="machine.section_name" class="text-xs text-slate-400">{{ machine.section_name }}</div>
                <div v-if="machine.workplace" class="text-xs text-slate-400">{{ machine.workplace }}</div>
              </td>

              <td>
                <div v-if="machine.operator_name" class="text-sm text-slate-700">{{ machine.operator_name }}</div>
                <div v-else-if="machine.assigned_brigade" class="text-sm text-slate-700">{{ machine.assigned_brigade }}</div>
                <div v-else class="text-xs text-slate-400">—</div>
              </td>

              <td class="text-xs text-slate-400">{{ formatDate(machine.updated_at) }}</td>

              <td @click.stop>
                <div class="flex items-center justify-end gap-1">
                  <RouterLink :to="`/machines/${machine.id}`"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-primary-600 hover:bg-primary-50 transition-colors"
                    title="Просмотр">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                  </RouterLink>
                  <RouterLink v-if="auth.canWrite" :to="`/machines/${machine.id}/edit`"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition-colors"
                    title="Редактировать">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </RouterLink>
                  <button v-if="auth.isAdmin && !machine.deleted_at"
                    @click.stop="confirmDelete(machine)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition-colors"
                    title="Удалить">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                  <button v-if="auth.isAdmin && machine.deleted_at"
                    @click.stop="handleRestore(machine)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 transition-colors"
                    title="Восстановить">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.total_pages > 1"
        class="flex items-center justify-between px-4 py-3 border-t border-slate-200 bg-slate-50/60">
        <div class="text-sm text-slate-500">
          Стр. {{ pagination.current_page }} из {{ pagination.total_pages }}
          ({{ pagination.count }} записей)
        </div>
        <div class="flex items-center gap-2">
          <select v-model="filters.page_size" @change="loadMachines" class="form-select h-8 w-20 text-xs">
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
          <button @click="prevPage" :disabled="!pagination.previous"
            class="btn-sm btn-secondary disabled:opacity-40">
            ← Пред.
          </button>
          <button @click="nextPage" :disabled="!pagination.next"
            class="btn-sm btn-secondary disabled:opacity-40">
            След. →
          </button>
        </div>
      </div>
    </div>

    <!-- Delete confirm modal -->
    <ConfirmModal v-if="deleteTarget"
      title="Удалить станок?"
      :message="`Станок «${deleteTarget.name}» будет помечен как удалённый. Данные сохранятся.`"
      confirm-label="Удалить"
      confirm-class="btn-danger"
      @confirm="doDelete"
      @cancel="deleteTarget = null" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '@/store/auth'
import { machinesApi, statusesApi, workshopsApi, machineTypesApi } from '@/api'
import StatusBadge from '@/components/common/StatusBadge.vue'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import dayjs from 'dayjs'
import { useDebounceFn } from '@vueuse/core'

const auth = useAuthStore()
const toast = useToast()
const route = useRoute()
const router = useRouter()

const machines = ref([])
const loading = ref(true)
const importing = ref(false)
const exporting = ref(false)
const fileInput = ref(null)
const deleteTarget = ref(null)

const pagination = ref({ count: 0, current_page: 1, total_pages: 1, next: null, previous: null })

const filters = reactive({
  search: '',
  status: route.query.status || '',
  workshop: route.query.workshop || '',
  machine_type: '',
  include_deleted: false,
  page: 1,
  page_size: 25,
  ordering: 'inventory_number',
})

const statusOptions = ref([])
const workshopOptions = ref([])
const typeOptions = ref([])

const hasActiveFilters = computed(() =>
  filters.search || filters.status || filters.workshop || filters.machine_type
)

const debouncedSearch = useDebounceFn(() => {
  filters.page = 1
  loadMachines()
}, 400)

function toggleSort(field) {
  if (filters.ordering === field) filters.ordering = `-${field}`
  else if (filters.ordering === `-${field}`) filters.ordering = field
  else filters.ordering = field
  loadMachines()
}

function sortIcon(field) {
  if (filters.ordering === field) return '↑'
  if (filters.ordering === `-${field}`) return '↓'
  return ''
}

function formatDate(d) {
  return dayjs(d).format('DD.MM.YY HH:mm')
}

function resetFilters() {
  Object.assign(filters, { search: '', status: '', workshop: '', machine_type: '', include_deleted: false, page: 1 })
  loadMachines()
}

function onWorkshopChange() {
  filters.page = 1
  loadMachines()
}

async function loadMachines() {
  loading.value = true
  try {
    const params = {
      page: filters.page,
      page_size: filters.page_size,
      ordering: filters.ordering,
    }
    if (filters.search) params.search = filters.search
    if (filters.status) params.status = filters.status
    if (filters.workshop) params.workshop = filters.workshop
    if (filters.machine_type) params.machine_type = filters.machine_type
    if (filters.include_deleted) params.include_deleted = true

    const res = await machinesApi.list(params)
    machines.value = res.data.results || []
    pagination.value = {
      count: res.data.count,
      current_page: res.data.current_page,
      total_pages: res.data.total_pages,
      next: res.data.next,
      previous: res.data.previous,
    }
  } catch (e) {
    toast.error('Ошибка загрузки данных')
  } finally {
    loading.value = false
  }
}

function prevPage() { filters.page--; loadMachines() }
function nextPage() { filters.page++; loadMachines() }

function confirmDelete(machine) { deleteTarget.value = machine }

async function doDelete() {
  try {
    await machinesApi.delete(deleteTarget.value.id)
    toast.success('Станок удалён')
    deleteTarget.value = null
    loadMachines()
  } catch {
    toast.error('Ошибка при удалении')
  }
}

async function handleRestore(machine) {
  try {
    await machinesApi.restore(machine.id)
    toast.success('Станок восстановлен')
    loadMachines()
  } catch {
    toast.error('Ошибка при восстановлении')
  }
}

async function handleExport() {
  exporting.value = true
  try {
    const params = {}
    if (filters.status) params.status = filters.status
    if (filters.workshop) params.workshop = filters.workshop
    if (filters.search) params.search = filters.search
    const res = await machinesApi.exportExcel(params)
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = `machines_${dayjs().format('YYYY-MM-DD')}.xlsx`
    a.click()
    window.URL.revokeObjectURL(url)
    toast.success('Файл экспортирован')
  } catch {
    toast.error('Ошибка экспорта')
  } finally {
    exporting.value = false
  }
}

async function handleImport(e) {
  const file = e.target.files[0]
  if (!file) return
  importing.value = true
  const formData = new FormData()
  formData.append('file', file)
  try {
    const res = await machinesApi.importExcel(formData)
    const d = res.data
    toast.success(`Импорт завершён: ${d.created} создано, ${d.updated} обновлено`)
    if (d.errors.length > 0) toast.warning(`${d.errors.length} строк с ошибками`)
    loadMachines()
  } catch {
    toast.error('Ошибка импорта')
  } finally {
    importing.value = false
    e.target.value = ''
  }
}

async function loadOptions() {
  const [sRes, wRes, tRes] = await Promise.all([
    statusesApi.list(),
    workshopsApi.list({ page_size: 100 }),
    machineTypesApi.list({ page_size: 100 }),
  ])
  statusOptions.value = sRes.data.results || sRes.data
  workshopOptions.value = wRes.data.results || wRes.data
  typeOptions.value = tRes.data.results || tRes.data
}

onMounted(() => {
  loadOptions()
  loadMachines()
})
</script>
