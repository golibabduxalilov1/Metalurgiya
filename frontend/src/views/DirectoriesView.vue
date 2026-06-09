<template>
  <div class="animate-fade-in">
    <div class="page-header">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-violet-100 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
          </svg>
        </div>
        <div>
          <h1 class="page-title">{{ t('directories.title') }}</h1>
          <p class="page-subtitle">{{ t('directories.subtitle') }}</p>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 bg-slate-100 p-1 rounded-xl mb-6 overflow-x-auto w-full sm:w-fit">
      <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
        :class="[
          'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-150 cursor-pointer select-none whitespace-nowrap',
          activeTab === tab.id
            ? 'bg-white text-indigo-700 shadow-sm ring-1 ring-slate-200/60'
            : 'text-slate-500 hover:text-slate-700'
        ]">
        {{ tab.label }}
      </button>
    </div>

    <!-- Workshops tab -->
    <div v-if="activeTab === 'workshops'" class="space-y-6">
      <DirectoryPanel
        :title="t('directories.panel_workshops')"
        :items="workshops"
        :loading="loadingWs"
        @add="openAdd('workshop')"
        @edit="openEdit('workshop', $event)"
        @delete="openDelete('workshop', $event)"
      />
      <DirectoryPanel
        :title="t('directories.panel_sections')"
        :items="sections"
        :loading="loadingWs"
        :columns="['name', 'workshop_name']"
        @add="openAdd('section')"
        @edit="openEdit('section', $event)"
        @delete="openDelete('section', $event)"
      />
    </div>

    <!-- Machine types tab -->
    <div v-if="activeTab === 'types'">
      <DirectoryPanel
        :title="t('directories.panel_types')"
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
        <div class="flex items-center justify-between px-5 py-4 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-7 h-7 rounded-lg bg-amber-100 flex items-center justify-center flex-shrink-0">
              <svg class="w-3.5 h-3.5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h3 class="text-sm font-semibold text-slate-700">{{ t('directories.panel_statuses') }}</h3>
          </div>
          <button @click="openAdd('status')" class="btn-sm btn-primary">{{ t('directories.add_btn') }}</button>
        </div>
        <div v-if="loadingStatuses" class="p-4 space-y-2">
          <div v-for="i in 5" :key="i" class="skeleton h-11 rounded-lg"
            :style="{ animationDelay: `${(i-1)*50}ms` }"></div>
        </div>
        <div v-else class="divide-y divide-slate-100">
          <div v-for="s in statuses" :key="s.id" class="status-row flex items-center gap-2.5 sm:gap-3.5 px-4 sm:px-5 py-3 flex-wrap">
            <span :class="['status-dot', `status-dot-${s.color}`]"></span>
            <span class="flex-1 text-sm font-medium text-slate-800">{{ s.name }}</span>
            <span class="inline-flex items-center gap-1 text-xs text-slate-500 tabular-nums">
              <span class="bg-slate-100 border border-slate-200 font-semibold px-1.5 py-0.5 rounded-full">{{ s.machines_count }}</span>
              ст.
            </span>
            <span v-if="s.requires_comment"
              class="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">
              {{ t('directories.requires_comment') }}
            </span>
            <button @click="openEdit('status', s)"
              class="p-1.5 rounded-lg text-slate-400 hover:text-amber-600 hover:bg-amber-50 transition-colors">
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </button>
            <button @click="openDelete('status', s)"
              class="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors">
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7V4a1 1 0 011-1h4a1 1 0 011 1v3M4 7h16"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit modal -->
    <Transition name="modal-fade">
      <div v-if="showModal" class="modal-backdrop" @click.self="showModal = false">
        <div class="modal-box max-w-md modal-enter">
          <div class="modal-header">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
                </svg>
              </div>
              <h3 class="text-base font-semibold text-slate-800">{{ editTarget ? t('directories.modal_edit') : t('directories.modal_add') }}</h3>
            </div>
            <button @click="showModal = false"
              class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors cursor-pointer">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <div class="modal-body space-y-4">
            <div>
              <label class="form-label">{{ t('directories.form_name') }}</label>
              <input v-model="form.name" type="text" class="form-input" :placeholder="t('directories.form_name_ph')" />
            </div>
            <!-- Section: workshop select -->
            <div v-if="modalType === 'section'">
              <label class="form-label">{{ t('directories.form_workshop') }}</label>
              <div class="relative">
                <select v-model="form.workshop" class="form-select appearance-none pr-8">
                  <option value="">{{ t('common.not_selected') }}</option>
                  <option v-for="w in workshops" :key="w.id" :value="w.id">{{ w.name }}</option>
                </select>
                <svg class="absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </div>
            </div>
            <!-- Status fields -->
            <template v-if="modalType === 'status'">
              <div>
                <label class="form-label">{{ t('directories.form_color') }}</label>
                <div class="flex items-center gap-2.5 mt-1">
                  <button v-for="c in ['green','yellow','red','gray','blue']" :key="c"
                    type="button" @click="form.color = c"
                    :class="['w-7 h-7 rounded-full transition-all duration-150 flex-shrink-0',
                      form.color === c ? 'ring-2 ring-offset-2 ring-indigo-400 scale-110' : 'hover:scale-105']"
                    :style="getColorStyle(c)">
                  </button>
                </div>
              </div>
              <label class="flex items-center gap-3 p-3 rounded-xl border border-slate-200 cursor-pointer
                hover:border-indigo-200 hover:bg-indigo-50/30 transition-all duration-150">
                <input type="checkbox" v-model="form.requires_comment"
                  class="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"/>
                <span class="text-sm text-slate-700">{{ t('directories.form_requires_comment') }}</span>
              </label>
            </template>
            <!-- Description -->
            <div v-if="modalType !== 'status'">
              <label class="form-label">{{ t('directories.form_desc') }}</label>
              <textarea v-model="form.description" class="form-textarea" rows="2"
                :placeholder="t('directories.form_desc_ph')"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="showModal = false" class="btn-md btn-secondary">{{ t('common.cancel') }}</button>
            <button @click="handleSave" :disabled="saving || !canSave" class="btn-md btn-primary inline-flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
              <svg v-if="saving" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              {{ saving ? t('common.saving') : t('common.save') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Delete confirm modal -->
    <ConfirmModal v-if="deleteTarget"
      :title="t('directories.delete_title')"
      :message="`«${deleteTarget.item.name}» ${t('directories.delete_msg_suffix')}`"
      :confirm-label="t('directories.delete_confirm')"
      confirm-class="btn-danger"
      @confirm="doDelete"
      @cancel="deleteTarget = null" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { workshopsApi, machineTypesApi, statusesApi } from '@/api'
import DirectoryPanel from '@/components/common/DirectoryPanel.vue'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import { useI18n } from '@/i18n'

const toast = useToast()
const { t } = useI18n()
const activeTab = ref('workshops')
const tabs = computed(() => [
  { id: 'workshops', label: t('directories.tab_workshops') },
  { id: 'types', label: t('directories.tab_types') },
  { id: 'statuses', label: t('directories.tab_statuses') },
])

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
const deleteTarget = ref(null)
const form = reactive({ name: '', description: '', workshop: '', color: 'gray', requires_comment: false })

const canSave = computed(() => {
  if (!form.name.trim()) return false
  if (modalType.value === 'section' && !form.workshop) return false
  return true
})

const colorStyles = { green: '#10B981', yellow: '#F59E0B', red: '#EF4444', gray: '#6B7280', blue: '#3B82F6' }
function getColorStyle(c) { return `background-color: ${colorStyles[c]}` }

function openAdd(type) { modalType.value = type; editTarget.value = null; Object.assign(form, { name: '', description: '', workshop: '', color: 'gray', requires_comment: false }); showModal.value = true }
function openEdit(type, item) { modalType.value = type; editTarget.value = item; Object.assign(form, item); showModal.value = true }
function openDelete(type, item) { deleteTarget.value = { type, item } }

async function doDelete() {
  try {
    const { type, item } = deleteTarget.value
    if (type === 'workshop') await workshopsApi.delete(item.id)
    else if (type === 'section') await workshopsApi.deleteSection(item.id)
    else if (type === 'type') await machineTypesApi.delete(item.id)
    else if (type === 'status') await statusesApi.delete(item.id)
    toast.success(t('toast.delete_success'))
    deleteTarget.value = null
    loadAll()
  } catch (e) {
    toast.error(e.response?.data?.message || t('toast.delete_error'))
  }
}

async function handleSave() {
  saving.value = true
  try {
    const payloadMap = {
      workshop: { name: form.name, description: form.description },
      section:  { name: form.name, description: form.description, workshop: form.workshop },
      type:     { name: form.name, description: form.description },
      status:   { name: form.name, color: form.color, requires_comment: form.requires_comment },
    }
    const apiMap = {
      workshop: workshopsApi,
      section:  { create: d => workshopsApi.createSection(d), update: (id, d) => workshopsApi.updateSection(id, d) },
      type:     machineTypesApi,
      status:   statusesApi,
    }
    const api = apiMap[modalType.value]
    const payload = payloadMap[modalType.value]
    if (editTarget.value) {
      await api.update(editTarget.value.id, payload)
      toast.success(t('toast.update_success'))
    } else {
      await api.create(payload)
      toast.success(t('toast.create_success'))
    }
    showModal.value = false
    loadAll()
  } catch (e) { toast.error(e.response?.data?.message || t('toast.error')) }
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

<style scoped>
.status-row {
  border-left: 2px solid transparent;
  transition: background-color 100ms ease, border-color 150ms ease;
}
.status-row:hover {
  background-color: rgba(99, 102, 241, 0.03);
  border-left-color: rgba(99, 102, 241, 0.3);
}
.modal-enter {
  animation: modalSlideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes modalSlideUp {
  from { opacity: 0; transform: translateY(16px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }
</style>
