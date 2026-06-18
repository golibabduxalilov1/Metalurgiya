<template>
  <div class="animate-fade-in space-y-5">

    <!-- Header -->
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div>
        <h1 class="text-xl font-bold text-slate-900">{{ t('maintenance.title') }}</h1>
        <p class="text-xs text-slate-400 mt-0.5">{{ t('maintenance.subtitle') }}</p>
      </div>
      <!-- Filter tabs -->
      <div class="flex gap-1 flex-wrap">
        <button v-for="f in filters" :key="f.key"
          @click="activeFilter = f.key"
          :class="['filter-btn', activeFilter === f.key ? 'filter-btn--active' : '']">
          {{ t(`maintenance.filter_${f.key}`) }}
          <span v-if="f.key !== 'all' && alertCounts[f.key]"
            :class="['badge-count', f.key === 'overdue' ? 'badge-rose' : f.key === 'critical' ? 'badge-amber' : 'badge-yellow']">
            {{ alertCounts[f.key] }}
          </span>
        </button>
      </div>
    </div>

    <!-- Summary cards -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <div class="stat-card border-rose-200 bg-rose-50">
        <div class="stat-value text-rose-600">{{ alertCounts.overdue }}</div>
        <div class="stat-label text-rose-400">{{ t('maintenance.filter_overdue') }}</div>
      </div>
      <div class="stat-card border-amber-200 bg-amber-50">
        <div class="stat-value text-amber-600">{{ alertCounts.critical }}</div>
        <div class="stat-label text-amber-400">{{ t('maintenance.filter_critical') }}</div>
      </div>
      <div class="stat-card border-yellow-200 bg-yellow-50">
        <div class="stat-value text-yellow-600">{{ alertCounts.warning }}</div>
        <div class="stat-label text-yellow-500">{{ t('maintenance.filter_warning') }}</div>
      </div>
      <div class="stat-card border-slate-200 bg-slate-50">
        <div class="stat-value text-slate-600">{{ totalMachines }}</div>
        <div class="stat-label text-slate-400">{{ t('machines.title') }}</div>
      </div>
    </div>

    <!-- Search + Table -->
    <div class="card overflow-hidden">
      <!-- Search bar -->
      <div class="p-4 border-b border-slate-100">
        <div class="relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            v-model="search"
            type="text"
            :placeholder="t('common.search')"
            class="w-full pl-9 pr-4 py-2 text-sm border border-slate-200 rounded-xl bg-slate-50
                   focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:bg-white transition-all"
          />
        </div>
      </div>

      <!-- Table -->
      <div v-if="loading" class="p-8 text-center text-slate-400 text-sm">
        <div class="w-6 h-6 border-2 border-indigo-300 border-t-indigo-600 rounded-full animate-spin mx-auto mb-2"></div>
        Yuklanmoqda...
      </div>

      <div v-else-if="filteredMachines.length === 0" class="p-12 text-center text-slate-400 text-sm">
        {{ t('machines.not_found') }}
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-50 border-b border-slate-100">
            <tr>
              <th class="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{{ t('maintenance.col_machine') }}</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{{ t('maintenance.col_interval') }}</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide hidden sm:table-cell">{{ t('maintenance.col_last') }}</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{{ t('maintenance.col_next') }}</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{{ t('maintenance.col_status') }}</th>
              <th class="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide text-right">{{ t('maintenance.col_actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="item in filteredMachines" :key="item.machine"
              class="hover:bg-slate-50 transition-colors">
              <td class="px-4 py-3">
                <div class="font-medium text-slate-800 truncate max-w-[180px]">{{ item.machine_name }}</div>
                <div class="text-xs text-slate-400">{{ item.machine_inventory }}</div>
                <div v-if="item.machine_workshop" class="text-xs text-slate-400">{{ item.machine_workshop }}</div>
              </td>
              <td class="px-4 py-3 text-slate-600">
                <span v-if="item.interval_months">
                  {{ item.interval_months }} {{ t('maintenance.interval_months') }}
                </span>
                <span v-else class="text-slate-300">—</span>
              </td>
              <td class="px-4 py-3 text-slate-600 hidden sm:table-cell">
                {{ item.last_maintenance_date ? formatDate(item.last_maintenance_date) : '—' }}
              </td>
              <td class="px-4 py-3">
                <div class="font-medium" :class="nextDateClass(item.alert_level)">
                  {{ formatDate(item.next_maintenance_date) }}
                </div>
                <div class="text-xs mt-0.5" :class="nextDateClass(item.alert_level)">
                  {{ daysLabel(item) }}
                </div>
              </td>
              <td class="px-4 py-3">
                <span :class="['alert-badge', `alert-${item.alert_level}`]">
                  {{ t(`maintenance.alert_${item.alert_level}`) }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center justify-end gap-1">
                  <RouterLink :to="`/machines/${item.machine}`"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors"
                    :title="t('machines.detail_back')">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                    </svg>
                  </RouterLink>
                  <button @click="canMarkComplete(item) && openComplete(item)"
                    :disabled="!canMarkComplete(item)"
                    :title="canMarkComplete(item) ? t('maintenance.mark_complete') : t('maintenance.mark_complete_locked')"
                    :class="[
                      'p-1.5 rounded-lg transition-colors',
                      canMarkComplete(item)
                        ? 'text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 cursor-pointer'
                        : 'text-slate-200 cursor-not-allowed'
                    ]">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </button>
                  <button @click="openEdit(item)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition-colors"
                    :title="t('maintenance.schedule_edit')">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button @click="confirmDelete(item)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                    :title="t('maintenance.schedule_delete')">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Machines WITHOUT a schedule (admin can add them) -->
    <div v-if="activeFilter === 'all'" class="card overflow-hidden">
      <div class="p-4 border-b border-slate-100 flex items-center justify-between">
        <h2 class="text-sm font-semibold text-slate-700">{{ t('maintenance.no_schedules') }}</h2>
        <span class="text-xs text-slate-400">{{ machinesWithoutSchedule.length }} ta</span>
      </div>
      <div v-if="machinesWithoutSchedule.length === 0" class="p-6 text-center text-slate-400 text-sm">
        Barcha stanoklar uchun ТО jadvali belgilangan
      </div>
      <div v-else class="divide-y divide-slate-50">
        <div v-for="m in machinesWithoutSchedule" :key="m.id"
          class="flex items-center gap-3 px-4 py-3 hover:bg-slate-50 transition-colors">
          <div class="flex-1 min-w-0">
            <div class="font-medium text-slate-800 truncate">{{ m.name }}</div>
            <div class="text-xs text-slate-400">{{ m.inventory_number }} · {{ m.workshop_name || '' }}</div>
          </div>
          <button @click="openSetForMachine(m)"
            class="flex items-center gap-1.5 text-xs font-medium text-indigo-600 hover:text-indigo-700
                   bg-indigo-50 hover:bg-indigo-100 border border-indigo-100 px-2.5 py-1 rounded-full
                   transition-colors flex-shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
            </svg>
            {{ t('maintenance.schedule_set') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Schedule Form Modal -->
    <Transition name="modal">
      <div v-if="showFormModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[2px]" @click="closeModal"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 space-y-4">
          <h3 class="text-base font-bold text-slate-900">
            {{ editingItem ? t('maintenance.form_title_edit') : t('maintenance.form_title_set') }}
          </h3>
          <p v-if="formMachine" class="text-sm text-slate-500 -mt-2">
            {{ formMachine.name || formMachine.machine_name }}
          </p>

          <div class="space-y-3">
            <!-- Interval -->
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">
                {{ t('maintenance.form_interval') }} *
              </label>
              <div class="grid grid-cols-3 gap-2">
                <button v-for="m in intervalOptions" :key="m"
                  @click="form.interval_months = m; showCustomInterval = false"
                  :class="['interval-btn', form.interval_months === m && !showCustomInterval ? 'interval-btn--active' : '']">
                  {{ t(`maintenance.month_${m}`) }}
                </button>
                <button
                  @click="showCustomInterval = true; form.interval_months = null"
                  :class="['interval-btn', showCustomInterval ? 'interval-btn--active' : '']">
                  {{ t('maintenance.month_other') }}
                </button>
              </div>
              <input v-if="showCustomInterval" v-model.number="form.interval_months" type="number" min="1" max="60"
                :placeholder="t('maintenance.form_interval_ph')"
                class="mt-2 w-full text-sm border border-slate-200 rounded-xl px-3 py-2
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all"/>
            </div>

            <!-- Last maintenance date -->
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">
                {{ t('maintenance.form_last_date') }}
              </label>
              <input v-model="form.last_maintenance_date" type="date"
                class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all"/>
            </div>

            <!-- Notes -->
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">
                {{ t('maintenance.form_notes') }}
              </label>
              <textarea v-model="form.notes" rows="2"
                :placeholder="t('maintenance.form_notes_ph')"
                class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 resize-none
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all">
              </textarea>
            </div>
          </div>

          <p v-if="formError" class="text-xs text-rose-500">{{ formError }}</p>

          <div class="flex gap-2 pt-1">
            <button @click="closeModal"
              class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button @click="saveSchedule" :disabled="saving"
              class="flex-1 py-2 text-sm text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition-colors
                     disabled:opacity-60 disabled:cursor-not-allowed">
              {{ saving ? t('common.saving') : t('common.save') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Complete Modal -->
    <Transition name="modal">
      <div v-if="showCompleteModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[2px]" @click="showCompleteModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 space-y-4">
          <h3 class="text-base font-bold text-slate-900">{{ t('maintenance.complete_title') }}</h3>
          <p class="text-sm text-slate-500 -mt-2">{{ completeItem?.machine_name }}</p>

          <div class="space-y-3">
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">
                {{ t('maintenance.complete_date') }} *
              </label>
              <input v-model="completeForm.completion_date" type="date"
                class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all"/>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">
                {{ t('maintenance.complete_notes') }}
              </label>
              <textarea v-model="completeForm.notes" rows="2"
                :placeholder="t('maintenance.complete_notes_ph')"
                class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 resize-none
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all">
              </textarea>
            </div>
          </div>

          <div class="flex gap-2">
            <button @click="showCompleteModal = false"
              class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button @click="markComplete" :disabled="saving"
              class="flex-1 py-2 text-sm text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl transition-colors
                     disabled:opacity-60 disabled:cursor-not-allowed">
              {{ saving ? t('common.saving') : t('maintenance.complete_btn') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Delete confirm modal -->
    <Transition name="modal">
      <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[2px]" @click="showDeleteModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 space-y-4">
          <h3 class="text-base font-bold text-slate-900">{{ t('maintenance.delete_confirm_title') }}</h3>
          <p class="text-sm text-slate-600">
            <strong>{{ deleteTarget?.machine_name }}</strong> — {{ t('maintenance.delete_confirm_msg') }}
          </p>
          <div class="flex gap-2">
            <button @click="showDeleteModal = false"
              class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button @click="doDelete" :disabled="saving"
              class="flex-1 py-2 text-sm text-white bg-rose-600 hover:bg-rose-700 rounded-xl transition-colors
                     disabled:opacity-60 disabled:cursor-not-allowed">
              {{ saving ? '...' : t('common.delete') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useI18n } from '@/i18n'
import { maintenanceApi, machinesApi } from '@/api'
import dayjs from 'dayjs'
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter'
dayjs.extend(isSameOrAfter)

const { t } = useI18n()
const toast = useToast()

const loading = ref(true)
const saving = ref(false)
const search = ref('')
const activeFilter = ref('all')

const schedules = ref([])
const allMachines = ref([])

const filters = [
  { key: 'all' },
  { key: 'overdue' },
  { key: 'critical' },
  { key: 'warning' },
  { key: 'ok' },
]

const intervalOptions = [1, 2, 3, 6, 12]
const showCustomInterval = ref(false)

const alertCounts = computed(() => ({
  overdue: schedules.value.filter(s => s.alert_level === 'overdue').length,
  critical: schedules.value.filter(s => s.alert_level === 'critical').length,
  warning: schedules.value.filter(s => s.alert_level === 'warning').length,
  ok: schedules.value.filter(s => s.alert_level === 'ok').length,
}))

const totalMachines = computed(() => allMachines.value.length)

const machinesWithScheduleIds = computed(() => new Set(schedules.value.map(s => s.machine)))

const machinesWithoutSchedule = computed(() =>
  allMachines.value.filter(m => !machinesWithScheduleIds.value.has(m.id))
    .filter(m => !search.value || m.name.toLowerCase().includes(search.value.toLowerCase())
      || m.inventory_number.toLowerCase().includes(search.value.toLowerCase()))
)

const filteredMachines = computed(() => {
  let list = schedules.value
  if (activeFilter.value !== 'all') {
    list = list.filter(s => s.alert_level === activeFilter.value)
  }
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(s =>
      s.machine_name?.toLowerCase().includes(q) ||
      s.machine_inventory?.toLowerCase().includes(q) ||
      s.machine_workshop?.toLowerCase().includes(q)
    )
  }
  return list
})

function formatDate(d) {
  if (!d) return '—'
  return dayjs(d).format('DD.MM.YYYY')
}

function daysLabel(item) {
  const days = item.days_until
  if (days === 0) return t('maintenance.today')
  if (days === 1) return t('maintenance.tomorrow')
  if (days < 0) return `${Math.abs(days)} ${t('maintenance.days_overdue')}`
  return `${days} ${t('maintenance.days_until')}`
}

function canMarkComplete(item) {
  if (!item.next_maintenance_date) return false
  return dayjs().startOf('day').isSameOrAfter(dayjs(item.next_maintenance_date).startOf('day'))
}

function nextDateClass(level) {
  if (level === 'overdue') return 'text-rose-600'
  if (level === 'critical') return 'text-amber-600'
  if (level === 'warning') return 'text-yellow-600'
  return 'text-slate-700'
}

// ── Load data ──
async function loadData() {
  loading.value = true
  try {
    const [alertsRes, machinesRes] = await Promise.all([
      maintenanceApi.all(),
      machinesApi.list({ page_size: 200 }),
    ])
    schedules.value = alertsRes.data.results || []
    allMachines.value = machinesRes.data.results || []
  } catch {
    toast.error(t('toast.load_error'))
  } finally {
    loading.value = false
  }
}

// ── Form modal ──
const showFormModal = ref(false)
const editingItem = ref(null)
const formMachine = ref(null)
const formError = ref('')
const form = ref({
  interval_months: 3,
  last_maintenance_date: '',
  notes: '',
})

function openEdit(item) {
  editingItem.value = item
  formMachine.value = item
  showCustomInterval.value = !intervalOptions.includes(item.interval_months)
  form.value = {
    interval_months: item.interval_months,
    last_maintenance_date: item.last_maintenance_date || dayjs().format('YYYY-MM-DD'),
    notes: item.notes || '',
  }
  formError.value = ''
  showFormModal.value = true
}

function openSetForMachine(machine) {
  editingItem.value = null
  formMachine.value = machine
  showCustomInterval.value = false
  form.value = {
    interval_months: 3,
    last_maintenance_date: dayjs().format('YYYY-MM-DD'),
    notes: '',
  }
  formError.value = ''
  showFormModal.value = true
}

function closeModal() {
  showFormModal.value = false
  editingItem.value = null
  formMachine.value = null
  showCustomInterval.value = false
}

async function saveSchedule() {
  if (!form.value.interval_months || !form.value.last_maintenance_date) {
    formError.value = t('toast.form_check')
    return
  }
  saving.value = true
  formError.value = ''
  try {
    const machineId = editingItem.value ? editingItem.value.machine : formMachine.value.id
    const payload = {
      interval_months: form.value.interval_months,
      last_maintenance_date: form.value.last_maintenance_date,
      notes: form.value.notes,
    }
    if (editingItem.value) {
      await maintenanceApi.update(machineId, payload)
    } else {
      await maintenanceApi.set(machineId, payload)
    }
    toast.success(t('maintenance.saved_success'))
    closeModal()
    await loadData()
  } catch (e) {
    const msg = e.response?.data?.message || e.response?.data?.errors?.last_maintenance_date?.[0] || t('toast.error')
    formError.value = msg
  } finally {
    saving.value = false
  }
}

// ── Complete modal ──
const showCompleteModal = ref(false)
const completeItem = ref(null)
const completeForm = ref({ completion_date: '', notes: '' })

function openComplete(item) {
  completeItem.value = item
  completeForm.value = {
    completion_date: dayjs().format('YYYY-MM-DD'),
    notes: '',
  }
  showCompleteModal.value = true
}

async function markComplete() {
  if (!completeForm.value.completion_date) return
  saving.value = true
  try {
    await maintenanceApi.complete(completeItem.value.machine, completeForm.value)
    toast.success(t('maintenance.complete_success'))
    showCompleteModal.value = false
    await loadData()
  } catch (e) {
    toast.error(e.response?.data?.message || t('toast.error'))
  } finally {
    saving.value = false
  }
}

// ── Delete ──
const showDeleteModal = ref(false)
const deleteTarget = ref(null)

function confirmDelete(item) {
  deleteTarget.value = item
  showDeleteModal.value = true
}

async function doDelete() {
  saving.value = true
  try {
    await maintenanceApi.delete(deleteTarget.value.machine)
    toast.success(t('maintenance.deleted_success'))
    showDeleteModal.value = false
    await loadData()
  } catch {
    toast.error(t('toast.error'))
  } finally {
    saving.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.card { @apply bg-white rounded-2xl border border-slate-200 shadow-sm; }

.filter-btn {
  @apply flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-xl border border-slate-200
         bg-white text-slate-600 hover:bg-indigo-50 hover:border-indigo-200 hover:text-indigo-600
         transition-colors cursor-pointer;
}
.filter-btn--active {
  @apply bg-indigo-50 border-indigo-200 text-indigo-700;
}

.badge-count {
  @apply text-[10px] font-bold rounded-full px-1.5 py-0.5 leading-none;
}
.badge-rose   { @apply bg-rose-100 text-rose-600; }
.badge-amber  { @apply bg-amber-100 text-amber-600; }
.badge-yellow { @apply bg-yellow-100 text-yellow-600; }

.stat-card {
  @apply rounded-2xl border p-4;
}
.stat-value { @apply text-2xl font-bold tabular-nums; }
.stat-label { @apply text-xs font-medium mt-0.5 uppercase tracking-wide; }

.alert-badge {
  @apply inline-flex items-center text-xs font-semibold px-2 py-0.5 rounded-full;
}
.alert-overdue  { @apply bg-rose-100 text-rose-700; }
.alert-critical { @apply bg-amber-100 text-amber-700; }
.alert-warning  { @apply bg-yellow-100 text-yellow-700; }
.alert-ok       { @apply bg-emerald-100 text-emerald-700; }

.interval-btn {
  @apply text-xs py-1.5 px-2 rounded-lg border border-slate-200 bg-slate-50
         text-slate-600 hover:bg-indigo-50 hover:border-indigo-200 hover:text-indigo-600
         transition-colors cursor-pointer text-center;
}
.interval-btn--active {
  @apply bg-indigo-100 border-indigo-300 text-indigo-700 font-semibold;
}

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
