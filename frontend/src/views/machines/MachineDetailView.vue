<template>
  <div class="animate-fade-in max-w-6xl mx-auto">

    <!-- Loading skeleton -->
    <div v-if="loading" class="space-y-6">
      <div class="flex items-center gap-4">
        <div class="skeleton w-10 h-10 rounded-xl flex-shrink-0"></div>
        <div class="skeleton h-8 w-72 rounded-lg"></div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <div class="skeleton h-64 rounded-xl"></div>
          <div class="skeleton h-48 rounded-xl"></div>
          <div class="skeleton h-36 rounded-xl"></div>
        </div>
        <div class="space-y-6">
          <div class="skeleton h-36 rounded-xl"></div>
          <div class="skeleton h-72 rounded-xl"></div>
        </div>
      </div>
    </div>

    <template v-else-if="machine">

      <!-- Back + header -->
      <div class="flex items-start gap-3 mb-5 sm:mb-7 flex-wrap">
        <button @click="$router.back()"
          class="mt-1 p-2 rounded-xl text-slate-500 hover:text-slate-700 hover:bg-slate-100
                 border border-transparent hover:border-slate-200
                 transition-all duration-200 cursor-pointer flex-shrink-0">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-3 flex-wrap">
            <h1 class="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">{{ machine.name }}</h1>
            <StatusBadge :status="machine.current_status_data?.name" :color="machine.current_status_data?.color" size="md" />
            <span v-if="machine.deleted_at"
              class="status-badge bg-rose-50 text-rose-700 border-rose-200">{{ t('machines.deleted_label') }}</span>
          </div>
          <span class="inline-flex items-center font-mono text-xs font-semibold text-indigo-700
                       bg-indigo-50 border border-indigo-100 px-2.5 py-0.5 rounded-md mt-2">
            {{ machine.inventory_number }}
          </span>
        </div>
        <div class="flex items-center gap-2 flex-shrink-0 flex-wrap">
          <button v-if="auth.canWrite && !machine.deleted_at"
            @click="showStatusModal = true"
            class="btn-md btn-secondary hover:border-indigo-200 hover:text-indigo-600
                   transition-all duration-200 cursor-pointer">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <span class="hidden sm:inline">{{ t('machines.detail_change_status') }}</span>
          </button>
          <RouterLink v-if="auth.canWrite && !machine.deleted_at"
            :to="`/machines/${machine.id}/edit`"
            class="btn-md btn-primary shadow-lg shadow-indigo-500/25
                   hover:shadow-indigo-500/40 hover:-translate-y-px transition-all duration-200">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
            <span class="hidden sm:inline">{{ t('machines.detail_edit') }}</span>
          </RouterLink>
        </div>
      </div>

      <!-- Main grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Left col -->
        <div class="lg:col-span-2 space-y-6">

          <!-- Basic info -->
          <div class="card p-6">
            <div class="section-header mb-5 pb-4 border-b border-slate-100">
              <div class="section-icon bg-indigo-50">
                <svg class="w-4 h-4 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
              </div>
              <h2 class="section-title">{{ t('machines.detail_basic') }}</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3">
              <InfoField :label="t('machines.detail_name')"         :value="machine.name" />
              <InfoField :label="t('machines.detail_inv')"          :value="machine.inventory_number" mono />
              <InfoField :label="t('machines.detail_model')"        :value="machine.model" />
              <InfoField :label="t('machines.detail_manufacturer')" :value="machine.manufacturer" />
              <InfoField :label="t('machines.detail_year')"         :value="machine.year_manufactured" />
              <InfoField :label="t('machines.detail_commissioned')" :value="formatDate(machine.commissioned_date)" />
              <InfoField :label="t('machines.detail_type')"         :value="machine.machine_type_name" />
              <InfoField :label="t('machines.detail_workplace')"    :value="machine.workplace" />
            </div>
            <div v-if="machine.description" class="mt-5 pt-5 border-t border-slate-100">
              <div class="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">
                {{ t('machines.detail_desc') }}
              </div>
              <p class="text-sm text-slate-700 whitespace-pre-line leading-relaxed">
                {{ machine.description }}
              </p>
            </div>
          </div>

          <!-- Location & operator -->
          <div class="card p-6">
            <div class="section-header mb-5 pb-4 border-b border-slate-100">
              <div class="section-icon bg-emerald-50">
                <svg class="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
              </div>
              <h2 class="section-title">{{ t('machines.detail_location') }}</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3">
              <InfoField :label="t('common.workshop')" :value="machine.workshop_name" />
              <InfoField :label="t('common.section')"  :value="machine.section_name" />
            </div>
            <div class="mt-5 pt-5 border-t border-slate-100">
              <div class="flex items-center justify-between mb-3">
                <span class="text-xs font-semibold text-slate-400 uppercase tracking-wide">{{ t('machines.detail_operator_label') }}</span>
                <button v-if="auth.canWrite" @click="showAssignModal = true"
                  class="inline-flex items-center gap-1.5 text-xs font-medium text-indigo-600
                         hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100
                         border border-indigo-100 px-2.5 py-1 rounded-full
                         transition-colors duration-150 cursor-pointer">
                  <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/>
                  </svg>
                  {{ machine.assigned_operator ? t('machines.detail_change_op') : t('machines.detail_assign_op') }}
                </button>
              </div>
              <div v-if="machine.operator_data"
                class="flex items-center gap-3.5 p-4 rounded-xl
                       bg-gradient-to-r from-indigo-50/60 to-slate-50
                       border border-indigo-100/70">
                <div class="w-10 h-10 bg-indigo-600 rounded-full flex items-center justify-center
                            flex-shrink-0 shadow-md shadow-indigo-500/25">
                  <span class="text-white font-bold text-sm">
                    {{ (machine.operator_data.first_name || '?')[0].toUpperCase() }}
                  </span>
                </div>
                <div>
                  <div class="text-sm font-semibold text-slate-900">{{ machine.operator_data.first_name }}</div>
                  <div class="text-xs text-slate-500 mt-0.5">{{ machine.operator_data.position }}</div>
                </div>
              </div>
              <div v-else-if="machine.assigned_brigade"
                class="flex items-center gap-3 p-4 bg-slate-50 border border-slate-200 rounded-xl">
                <svg class="w-5 h-5 text-slate-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
                <span class="text-sm font-medium text-slate-700">{{ machine.assigned_brigade }}</span>
              </div>
              <div v-else
                class="flex items-center gap-2.5 p-4 bg-slate-50/60
                       border border-dashed border-slate-200 rounded-xl">
                <svg class="w-4 h-4 text-slate-300 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                <span class="text-sm text-slate-400 italic">{{ t('machines.detail_no_operator') }}</span>
              </div>
            </div>
          </div>

          <!-- Attachments -->
          <div class="card p-6">
            <div class="flex items-center justify-between mb-5 pb-4 border-b border-slate-100">
              <div class="section-header">
                <div class="section-icon bg-violet-50">
                  <svg class="w-4 h-4 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"/>
                  </svg>
                </div>
                <h2 class="section-title">{{ t('machines.detail_files') }}</h2>
              </div>
              <label v-if="auth.canWrite" class="cursor-pointer">
                <input type="file" class="hidden" @change="handleUpload"
                  accept=".jpg,.jpeg,.png,.pdf,.doc,.docx" multiple />
                <span class="btn-sm btn-secondary hover:border-violet-200 hover:text-violet-600
                             transition-all duration-200">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                  </svg>
                  {{ t('machines.detail_upload') }}
                </span>
              </label>
            </div>
            <div v-if="machine.attachments.length === 0"
              class="flex flex-col items-center justify-center py-8 text-center
                     border border-dashed border-slate-200 rounded-xl bg-slate-50/50">
              <svg class="w-8 h-8 text-slate-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
              </svg>
              <span class="text-sm text-slate-400">{{ t('machines.detail_no_files') }}</span>
            </div>
            <div v-else class="space-y-2">
              <div v-for="att in machine.attachments" :key="att.id"
                class="flex items-center gap-3 p-3 rounded-xl border border-slate-100 bg-slate-50/60
                       hover:bg-white hover:border-slate-200 hover:shadow-sm
                       transition-all duration-150 group">
                <div :class="fileIconClass(att.content_type)"
                  class="w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-medium text-slate-800 truncate">{{ att.original_filename }}</div>
                  <div class="text-xs text-slate-400 tabular-nums mt-0.5">
                    {{ att.file_size_display }} · {{ formatDate(att.uploaded_at) }}
                  </div>
                </div>
                <a :href="att.file_url" target="_blank"
                  class="p-1.5 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-indigo-50
                         transition-colors duration-150 opacity-0 group-hover:opacity-100">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Right col -->
        <div class="space-y-6">

          <!-- Meta info -->
          <div class="card p-5">
            <div class="section-header mb-4 pb-3 border-b border-slate-100">
              <div class="section-icon bg-slate-100">
                <svg class="w-4 h-4 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <h2 class="section-title">{{ t('machines.detail_meta') }}</h2>
            </div>
            <div class="divide-y divide-slate-100">
              <div class="meta-row">
                <span class="meta-label">{{ t('machines.detail_created') }}</span>
                <span class="meta-value tabular-nums">{{ formatDateTime(machine.created_at) }}</span>
              </div>
              <div class="meta-row">
                <span class="meta-label">{{ t('machines.detail_author') }}</span>
                <span class="meta-value font-semibold">{{ machine.created_by_name || '—' }}</span>
              </div>
              <div class="meta-row">
                <span class="meta-label">{{ t('machines.detail_updated') }}</span>
                <span class="meta-value tabular-nums">{{ formatDateTime(machine.updated_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Status history -->
          <div class="card p-5">
            <div class="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
              <div class="section-header">
                <div class="section-icon bg-amber-50">
                  <svg class="w-4 h-4 text-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <h2 class="section-title">{{ t('machines.detail_history') }}</h2>
              </div>
              <span class="text-xs font-semibold text-slate-500 bg-slate-100
                           px-2 py-0.5 rounded-full tabular-nums">
                {{ machine.recent_status_history?.length || 0 }}
              </span>
            </div>
            <div v-if="!machine.recent_status_history?.length"
              class="text-sm text-slate-400 text-center py-6 italic">
              {{ t('machines.detail_history_empty') }}
            </div>
            <div v-else class="timeline">
              <div v-for="h in machine.recent_status_history" :key="h.id"
                class="timeline-item">
                <!-- Timeline line -->
                <div class="timeline-line"></div>
                <!-- Dot -->
                <div class="timeline-dot border-2 border-white shadow-sm"
                  :class="`status-dot-${h.new_status_color}`"></div>
                <div class="pb-4">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span :class="['status-badge', `status-${h.new_status_color}`]">
                      {{ h.new_status_name }}
                    </span>
                    <span v-if="h.previous_status_name"
                      class="inline-flex items-center gap-1 text-xs text-slate-400">
                      <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
                      </svg>
                      {{ h.previous_status_name }}
                    </span>
                  </div>
                  <div class="text-xs font-medium text-slate-600 mt-1.5">{{ h.changed_by_name }}</div>
                  <div class="text-xs text-slate-400 tabular-nums mt-0.5">{{ formatDateTime(h.changed_at) }}</div>
                  <div v-if="h.comment"
                    class="mt-2 text-xs text-slate-600 italic bg-slate-50
                           border-l-2 border-slate-200 pl-2.5 py-1 rounded-r-md leading-relaxed">
                    {{ h.comment }}
                  </div>
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
import { useI18n } from '@/i18n'

const auth = useAuthStore()
const toast = useToast()
const { t } = useI18n()
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
    toast.error(t('toast.machine_not_found'))
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
      toast.success(t('toast.file_uploaded'))
    } catch {
      toast.error(t('toast.file_error'))
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

<style scoped>
/* ── Section header ── */
.section-header {
  @apply flex items-center gap-3;
}
.section-icon {
  @apply w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0;
}
.section-title {
  @apply text-sm font-semibold text-slate-700;
}

/* ── Metadata rows ── */
.meta-row {
  @apply flex items-center justify-between py-2.5 text-sm;
}
.meta-label {
  @apply text-slate-500;
}
.meta-value {
  @apply text-slate-800 text-right;
}

/* ── Status history timeline ── */
.timeline {
  @apply space-y-0;
}
.timeline-item {
  @apply relative pl-6;
}
.timeline-line {
  @apply absolute left-[5px] top-4 bottom-0 w-px bg-slate-100;
}
.timeline-item:last-child .timeline-line {
  display: none;
}
.timeline-dot {
  @apply absolute left-0 top-1.5 w-3 h-3 rounded-full;
}

/* ── Reduced motion ── */
@media (prefers-reduced-motion: reduce) {
  .card, .btn-md, .btn-sm, .action-btn {
    transition: none;
  }
}
</style>
