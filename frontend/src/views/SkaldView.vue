<template>
  <div class="animate-fade-in space-y-5">

    <!-- Header -->
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div>
        <h1 class="text-xl font-bold text-slate-900">{{ t('sklad.title') }}</h1>
        <p class="text-xs text-slate-400 mt-0.5">{{ t('sklad.subtitle') }}</p>
      </div>
      <button @click="openAdd"
        class="flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-indigo-600
               hover:bg-indigo-700 rounded-xl transition-colors shadow-sm cursor-pointer">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
        </svg>
        {{ t('sklad.add_btn') }}
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
      <div class="stat-card border-indigo-200 bg-indigo-50">
        <div class="stat-value text-indigo-600">{{ spareParts.length }}</div>
        <div class="stat-label text-indigo-400">{{ t('sklad.total_parts') }}</div>
      </div>
      <div class="stat-card border-slate-200 bg-slate-50">
        <div class="stat-value text-slate-600">{{ uniqueSuppliers }}</div>
        <div class="stat-label text-slate-400">{{ t('sklad.suppliers_count') }}</div>
      </div>
      <div class="stat-card border-emerald-200 bg-emerald-50 col-span-2 sm:col-span-1">
        <div class="stat-value text-emerald-600">{{ totalLinkedMachines }}</div>
        <div class="stat-label text-emerald-400">{{ t('sklad.linked_machines') }}</div>
      </div>
    </div>

    <!-- Search + Table -->
    <div class="card overflow-hidden">
      <div class="p-4 border-b border-slate-100">
        <div class="relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input v-model="search" type="text" :placeholder="t('common.search')"
            class="w-full pl-9 pr-4 py-2 text-sm border border-slate-200 rounded-xl bg-slate-50
                   focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:bg-white transition-all" />
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="p-10 text-center text-slate-400 text-sm">
        <div class="w-6 h-6 border-2 border-indigo-300 border-t-indigo-600 rounded-full animate-spin mx-auto mb-2"></div>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredParts.length === 0" class="p-12 text-center">
        <div class="w-14 h-14 mx-auto mb-3 rounded-2xl bg-slate-100 flex items-center justify-center">
          <svg class="w-7 h-7 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
          </svg>
        </div>
        <p class="text-slate-500 text-sm font-medium">{{ t('sklad.not_found') }}</p>
        <p class="text-slate-300 text-xs mt-1">{{ t('common.try_change_filters') }}</p>
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-50 border-b border-slate-100">
            <tr>
              <th class="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{{ t('sklad.col_name') }}</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide hidden sm:table-cell">{{ t('sklad.col_supplier') }}</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">{{ t('sklad.col_price') }}</th>
              <th class="text-left px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide hidden md:table-cell">{{ t('sklad.col_machines') }}</th>
              <th class="px-4 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide text-right">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="part in filteredParts" :key="part.id" class="hover:bg-slate-50 transition-colors">
              <td class="px-4 py-3">
                <div class="font-medium text-slate-800">{{ part.name }}</div>
              </td>
              <td class="px-4 py-3 text-slate-600 hidden sm:table-cell">
                <span v-if="part.supplier">{{ part.supplier }}</span>
                <span v-else class="text-slate-300">—</span>
              </td>
              <td class="px-4 py-3">
                <span v-if="part.price" class="font-semibold text-slate-800 tabular-nums">
                  {{ formatPrice(part.price) }}
                </span>
                <span v-else class="text-slate-300">—</span>
              </td>
              <td class="px-4 py-3 hidden md:table-cell">
                <div v-if="part.machines_data?.length" class="flex flex-wrap gap-1">
                  <span v-for="m in part.machines_data" :key="m.id"
                    class="inline-flex text-xs bg-indigo-50 text-indigo-700 border border-indigo-100
                           px-2 py-0.5 rounded-full whitespace-nowrap">
                    {{ m.inventory_number }}
                  </span>
                </div>
                <span v-else class="text-slate-300">—</span>
              </td>
              <td class="px-4 py-3">
                <div class="flex items-center justify-end gap-1">
                  <button @click="openEdit(part)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition-colors cursor-pointer"
                    :title="t('common.edit')">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                  <button @click="confirmDelete(part)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors cursor-pointer"
                    :title="t('common.delete')">
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

    <!-- Add / Edit Modal -->
    <Transition name="modal">
      <div v-if="showFormModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[2px]" @click="closeModal"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[92vh] flex flex-col">
          <div class="p-6 overflow-y-auto space-y-4">

            <h3 class="text-base font-bold text-slate-900">
              {{ editingPart ? t('sklad.form_title_edit') : t('sklad.form_title_add') }}
            </h3>

            <!-- Name -->
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">
                {{ t('sklad.form_name') }} *
              </label>
              <input v-model="form.name" type="text" :placeholder="t('sklad.form_name_ph')"
                class="w-full text-sm border rounded-xl px-3 py-2
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all"
                :class="formError && !form.name.trim() ? 'border-rose-300' : 'border-slate-200'" />
            </div>

            <!-- Price -->
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">
                {{ t('sklad.form_price') }}
              </label>
              <input v-model="form.price" type="number" min="0" step="0.01"
                :placeholder="t('sklad.form_price_ph')"
                class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all" />
            </div>

            <!-- Supplier -->
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">
                {{ t('sklad.form_supplier') }}
              </label>
              <input v-model="form.supplier" type="text" :placeholder="t('sklad.form_supplier_ph')"
                class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all" />
            </div>

            <!-- Machines -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-xs font-semibold text-slate-600">{{ t('sklad.form_machines') }}</label>
                <!-- Toggle -->
                <div class="flex items-center gap-2">
                  <span class="text-xs text-slate-400">{{ t('sklad.single_machine') }}</span>
                  <button type="button" @click="toggleMultiMode"
                    :class="['toggle-switch', multiMode ? 'toggle-switch--on' : '']">
                    <span class="toggle-thumb" :class="multiMode ? 'toggle-thumb--on' : ''"></span>
                  </button>
                  <span class="text-xs text-slate-400">{{ t('sklad.multi_machine') }}</span>
                </div>
              </div>

              <!-- Single select -->
              <div v-if="!multiMode">
                <select v-model="singleMachineId"
                  class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 bg-white
                         focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all">
                  <option :value="null">{{ t('common.not_selected') }}</option>
                  <option v-for="m in allMachines" :key="m.id" :value="m.id">
                    {{ m.inventory_number }} — {{ m.name }}
                  </option>
                </select>
              </div>

              <!-- Multi checkbox list -->
              <div v-else class="border border-slate-200 rounded-xl overflow-hidden">
                <!-- Search within list -->
                <div class="px-3 py-2 border-b border-slate-100 bg-slate-50">
                  <input v-model="machineSearch" type="text"
                    :placeholder="t('common.search')"
                    class="w-full text-xs border-0 bg-transparent focus:outline-none text-slate-600 placeholder-slate-300" />
                </div>
                <div class="max-h-44 overflow-y-auto">
                  <div v-if="filteredMachinesForForm.length === 0" class="p-3 text-xs text-slate-400 text-center">
                    {{ t('common.no_data') }}
                  </div>
                  <label v-for="m in filteredMachinesForForm" :key="m.id"
                    class="flex items-center gap-3 px-3 py-2.5 hover:bg-indigo-50 cursor-pointer
                           transition-colors border-b border-slate-50 last:border-0">
                    <input type="checkbox" :value="m.id" v-model="form.machines"
                      class="w-4 h-4 rounded border-slate-300 text-indigo-600
                             focus:ring-indigo-300 cursor-pointer flex-shrink-0" />
                    <div class="flex-1 min-w-0">
                      <div class="text-xs font-medium text-slate-800 truncate">{{ m.name }}</div>
                      <div class="text-xs text-slate-400">{{ m.inventory_number }}</div>
                    </div>
                  </label>
                </div>
              </div>

              <div v-if="multiMode && form.machines.length > 0"
                class="mt-1.5 text-xs text-indigo-600 font-medium">
                {{ form.machines.length }} {{ t('sklad.machines_selected') }}
              </div>
            </div>

            <p v-if="formError" class="text-xs text-rose-500 bg-rose-50 border border-rose-100 rounded-lg px-3 py-2">
              {{ formError }}
            </p>
          </div>

          <div class="p-4 pt-0 flex gap-2">
            <button @click="closeModal"
              class="flex-1 py-2.5 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors cursor-pointer">
              {{ t('common.cancel') }}
            </button>
            <button @click="savePart" :disabled="saving"
              class="flex-1 py-2.5 text-sm text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl
                     transition-colors disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer">
              {{ saving ? t('common.saving') : t('common.save') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Delete confirm -->
    <Transition name="modal">
      <div v-if="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[2px]" @click="showDeleteModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 space-y-4">
          <h3 class="text-base font-bold text-slate-900">{{ t('sklad.delete_title') }}</h3>
          <p class="text-sm text-slate-600">
            <strong>{{ deleteTarget?.name }}</strong> — {{ t('sklad.delete_msg') }}
          </p>
          <div class="flex gap-2">
            <button @click="showDeleteModal = false"
              class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors cursor-pointer">
              {{ t('common.cancel') }}
            </button>
            <button @click="doDelete" :disabled="saving"
              class="flex-1 py-2 text-sm text-white bg-rose-600 hover:bg-rose-700 rounded-xl
                     transition-colors disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer">
              {{ saving ? '...' : t('common.delete') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useToast } from 'vue-toastification'
import { useI18n } from '@/i18n'
import { warehouseApi, machinesApi } from '@/api'

const { t } = useI18n()
const toast = useToast()

const loading = ref(true)
const saving = ref(false)
const search = ref('')
const machineSearch = ref('')

const spareParts = ref([])
const allMachines = ref([])

// ── Computed stats ──
const uniqueSuppliers = computed(() => {
  const s = new Set(spareParts.value.map(p => p.supplier).filter(Boolean))
  return s.size
})

const totalLinkedMachines = computed(() => {
  const ids = new Set()
  spareParts.value.forEach(p => p.machines_data?.forEach(m => ids.add(m.id)))
  return ids.size
})

const filteredParts = computed(() => {
  if (!search.value) return spareParts.value
  const q = search.value.toLowerCase()
  return spareParts.value.filter(p =>
    p.name.toLowerCase().includes(q) ||
    (p.supplier || '').toLowerCase().includes(q)
  )
})

const filteredMachinesForForm = computed(() => {
  if (!machineSearch.value) return allMachines.value
  const q = machineSearch.value.toLowerCase()
  return allMachines.value.filter(m =>
    m.name.toLowerCase().includes(q) ||
    m.inventory_number.toLowerCase().includes(q)
  )
})

function formatPrice(val) {
  return '$ ' + Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// ── Load ──
async function loadData() {
  loading.value = true
  try {
    const [partsRes, machinesRes] = await Promise.all([
      warehouseApi.list(),
      machinesApi.list({ page_size: 500 }),
    ])
    spareParts.value = partsRes.data.results ?? partsRes.data
    allMachines.value = machinesRes.data.results ?? []
  } catch {
    toast.error(t('toast.load_error'))
  } finally {
    loading.value = false
  }
}

// ── Form ──
const showFormModal = ref(false)
const editingPart = ref(null)
const formError = ref('')
const multiMode = ref(false)
const singleMachineId = ref(null)

const form = ref({
  name: '',
  price: '',
  supplier: '',
  machines: [],
})

function openAdd() {
  editingPart.value = null
  multiMode.value = false
  singleMachineId.value = null
  machineSearch.value = ''
  form.value = { name: '', price: '', supplier: '', machines: [] }
  formError.value = ''
  showFormModal.value = true
}

function openEdit(part) {
  editingPart.value = part
  const machineIds = part.machines_data?.map(m => m.id) ?? []
  multiMode.value = machineIds.length > 1
  singleMachineId.value = machineIds.length === 1 ? machineIds[0] : (machineIds.length === 0 ? null : null)
  machineSearch.value = ''
  form.value = {
    name: part.name,
    price: part.price ?? '',
    supplier: part.supplier ?? '',
    machines: machineIds,
  }
  formError.value = ''
  showFormModal.value = true
}

function toggleMultiMode() {
  if (!multiMode.value) {
    // switching to multi — seed from single
    form.value.machines = singleMachineId.value ? [singleMachineId.value] : []
  } else {
    // switching to single — take first selected
    singleMachineId.value = form.value.machines[0] ?? null
  }
  multiMode.value = !multiMode.value
  machineSearch.value = ''
}

function closeModal() {
  showFormModal.value = false
  editingPart.value = null
}

async function savePart() {
  if (!form.value.name.trim()) {
    formError.value = t('toast.form_check')
    return
  }
  const machineIds = multiMode.value
    ? form.value.machines
    : (singleMachineId.value ? [singleMachineId.value] : [])

  const payload = {
    name: form.value.name.trim(),
    price: form.value.price !== '' ? form.value.price : null,
    supplier: form.value.supplier.trim(),
    machines: machineIds,
  }

  saving.value = true
  formError.value = ''
  try {
    if (editingPart.value) {
      await warehouseApi.update(editingPart.value.id, payload)
      toast.success(t('toast.update_success'))
    } else {
      await warehouseApi.create(payload)
      toast.success(t('toast.create_success'))
    }
    closeModal()
    await loadData()
  } catch (e) {
    const data = e.response?.data
    formError.value = data?.name?.[0] || data?.detail || data?.message || t('toast.error')
  } finally {
    saving.value = false
  }
}

// ── Delete ──
const showDeleteModal = ref(false)
const deleteTarget = ref(null)

function confirmDelete(part) {
  deleteTarget.value = part
  showDeleteModal.value = true
}

async function doDelete() {
  saving.value = true
  try {
    await warehouseApi.delete(deleteTarget.value.id)
    toast.success(t('toast.delete_success'))
    showDeleteModal.value = false
    await loadData()
  } catch {
    toast.error(t('toast.delete_error'))
  } finally {
    saving.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.card { @apply bg-white rounded-2xl border border-slate-200 shadow-sm; }

.stat-card { @apply rounded-2xl border p-4; }
.stat-value { @apply text-2xl font-bold tabular-nums; }
.stat-label { @apply text-xs font-medium mt-0.5 uppercase tracking-wide; }

.toggle-switch {
  @apply relative inline-flex items-center w-10 h-6 rounded-full
         border-2 border-slate-200 bg-slate-100
         transition-all duration-200 cursor-pointer flex-shrink-0;
}
.toggle-switch--on {
  @apply bg-indigo-500 border-indigo-500;
}
.toggle-thumb {
  @apply absolute left-0.5 w-4 h-4 bg-white rounded-full shadow
         transition-transform duration-200;
}
.toggle-thumb--on {
  @apply translate-x-4;
}

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
