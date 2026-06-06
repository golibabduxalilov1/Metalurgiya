<template>
  <div class="animate-fade-in">
    <div class="page-header">
      <div>
        <h1 class="page-title">Справочники</h1>
        <p class="page-subtitle">Управление классификаторами системы</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 bg-slate-100 p-1 rounded-xl w-fit mb-6">
      <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
        :class="[
          'px-4 py-2 text-sm font-medium rounded-lg transition-all',
          activeTab === tab.id ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-800'
        ]">
        {{ tab.label }}
      </button>
    </div>

    <!-- Workshops tab -->
    <div v-if="activeTab === 'workshops'">
      <DirectoryPanel
        title="Цеха"
        :items="workshops"
        :loading="loadingWs"
        @add="openAdd('workshop')"
        @edit="openEdit('workshop', $event)"
        @delete="openDelete('workshop', $event)"
      />
      <!-- Sections sub-panel -->
      <div class="mt-6">
        <DirectoryPanel
          title="Участки"
          :items="sections"
          :loading="loadingWs"
          :columns="['name', 'workshop_name']"
          @add="openAdd('section')"
          @edit="openEdit('section', $event)"
          @delete="openDelete('section', $event)"
        />
      </div>
    </div>

    <!-- Machine types tab -->
    <div v-if="activeTab === 'types'">
      <DirectoryPanel
        title="Типы станков"
        :items="machineTypes"
        :loading="loadingTypes"
        @add="openAdd('type')"
        @edit="openEdit('type', $event)"
        @delete="openDelete('type', $event)"
      />
    </div>

    <!-- Statuses tab -->
    <div v-if="activeTab === 'statuses'">
      <div class="card overflow-hidden">
        <div class="flex items-center justify-between p-5 border-b border-slate-100">
          <h3 class="font-semibold text-slate-800">Статусы станков</h3>
          <button @click="openAdd('status')" class="btn-sm btn-primary">+ Добавить</button>
        </div>
        <div v-if="loadingStatuses" class="p-6 space-y-2">
          <div v-for="i in 5" :key="i" class="skeleton h-12 rounded-lg"></div>
        </div>
        <div v-else class="divide-y divide-slate-100">
          <div v-for="s in statuses" :key="s.id"
            class="flex items-center gap-4 px-5 py-3 hover:bg-slate-50 transition-colors">
            <span :class="['status-dot', `status-dot-${s.color}`]"></span>
            <span class="flex-1 text-sm font-medium text-slate-800">{{ s.name }}</span>
            <span class="text-xs text-slate-400">{{ s.machines_count }} станков</span>
            <span v-if="s.requires_comment" class="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">Требует комментарий</span>
            <div class="flex items-center gap-1">
              <button @click="openEdit('status', s)" class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition-colors">
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit modal -->
    <div v-if="showModal" class="modal-backdrop" @click.self="showModal = false">
      <div class="modal-box max-w-md">
        <div class="modal-header">
          <h3 class="text-lg font-semibold">{{ editTarget ? 'Редактировать' : 'Добавить' }}</h3>
          <button @click="showModal = false" class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="modal-body space-y-4">
          <div>
            <label class="form-label">Наименование *</label>
            <input v-model="form.name" type="text" class="form-input" />
          </div>
          <!-- Section: workshop -->
          <div v-if="modalType === 'section'">
            <label class="form-label">Цех *</label>
            <select v-model="form.workshop" class="form-select">
              <option value="">— не выбрано —</option>
              <option v-for="w in workshops" :key="w.id" :value="w.id">{{ w.name }}</option>
            </select>
          </div>
          <!-- Status: color + requires_comment -->
          <template v-if="modalType === 'status'">
            <div>
              <label class="form-label">Цвет</label>
              <div class="flex gap-2">
                <button v-for="c in ['green','yellow','red','gray','blue']" :key="c"
                  type="button" @click="form.color = c"
                  :class="['w-8 h-8 rounded-full transition-all', `status-dot-${c}`, form.color === c ? 'ring-2 ring-primary-500 ring-offset-2' : '']"
                  :style="getColorStyle(c)">
                </button>
              </div>
            </div>
            <label class="flex items-center gap-2 text-sm cursor-pointer">
              <input type="checkbox" v-model="form.requires_comment" class="rounded border-slate-300 text-primary-600"/>
              <span class="text-slate-700">Требовать комментарий при выборе</span>
            </label>
          </template>
          <!-- Common description -->
          <div v-if="modalType !== 'status'">
            <label class="form-label">Описание</label>
            <textarea v-model="form.description" class="form-textarea" rows="2"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showModal = false" class="btn-md btn-secondary">Отмена</button>
          <button @click="handleSave" :disabled="saving" class="btn-md btn-primary">{{ saving ? 'Сохранение...' : 'Сохранить' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { workshopsApi, machineTypesApi, statusesApi } from '@/api'
import DirectoryPanel from '@/components/common/DirectoryPanel.vue'

const toast = useToast()
const activeTab = ref('workshops')
const tabs = [
  { id: 'workshops', label: 'Цеха и участки' },
  { id: 'types', label: 'Типы станков' },
  { id: 'statuses', label: 'Статусы' },
]

const workshops = ref([])
const sections = ref([])
const machineTypes = ref([])
const statuses = ref([])
const loadingWs = ref(false)
const loadingTypes = ref(false)
const loadingStatuses = ref(false)

const showModal = ref(false)
const saving = ref(false)
const editTarget = ref(null)
const modalType = ref('')
const form = reactive({ name: '', description: '', workshop: '', color: 'gray', requires_comment: false })

const colorStyles = { green: '#10B981', yellow: '#F59E0B', red: '#EF4444', gray: '#6B7280', blue: '#3B82F6' }
function getColorStyle(c) { return `background-color: ${colorStyles[c]}` }

function openAdd(type) { modalType.value = type; editTarget.value = null; Object.assign(form, { name: '', description: '', workshop: '', color: 'gray', requires_comment: false }); showModal.value = true }
function openEdit(type, item) { modalType.value = type; editTarget.value = item; Object.assign(form, item); showModal.value = true }
function openDelete() { /* TODO */ }

async function handleSave() {
  saving.value = true
  try {
    const apiMap = { workshop: workshopsApi, section: { create: d => workshopsApi.createSection(d), update: (id, d) => workshopsApi.updateSection(id, d) }, type: machineTypesApi, status: statusesApi }
    const api = apiMap[modalType.value]
    if (editTarget.value) { await api.update(editTarget.value.id, form); toast.success('Обновлено') }
    else { await api.create ? api.create(form) : null; toast.success('Создано') }
    showModal.value = false
    loadAll()
  } catch (e) { toast.error(e.response?.data?.message || 'Ошибка') }
  finally { saving.value = false }
}

async function loadAll() {
  loadingWs.value = true
  const [wRes, sRes] = await Promise.all([workshopsApi.list({ page_size: 200 }), workshopsApi.sections({ page_size: 200 })])
  workshops.value = wRes.data.results || wRes.data
  sections.value = sRes.data.results || sRes.data
  loadingWs.value = false

  loadingTypes.value = true
  const tRes = await machineTypesApi.list({ page_size: 200 })
  machineTypes.value = tRes.data.results || tRes.data
  loadingTypes.value = false

  loadingStatuses.value = true
  const stRes = await statusesApi.list()
  statuses.value = stRes.data.results || stRes.data
  loadingStatuses.value = false
}

onMounted(loadAll)
</script>
