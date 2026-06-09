<template>
  <div class="animate-fade-in space-y-5">

    <!-- Header -->
    <div class="page-header flex-wrap gap-4">
      <div>
        <h1 class="page-title">{{ t('machines.title') }}</h1>
        <p class="page-subtitle flex items-center gap-1.5">
          {{ t('machines.subtitle_total') }}
          <span class="inline-flex items-center font-bold text-indigo-700 bg-indigo-50
                       border border-indigo-100 text-xs px-2.5 py-0.5 rounded-full
                       tabular-nums shadow-inner">
            {{ pagination.count }}
          </span>
          {{ t('machines.subtitle_units') }}
        </p>
      </div>
      <div class="flex items-center gap-2 flex-wrap justify-end">
        <!-- Import -->
        <div v-if="auth.isAdmin" class="relative">
          <input ref="fileInput" type="file" accept=".xlsx" class="hidden" @change="handleImport" />
          <button @click="fileInput.click()"
            class="btn-md btn-secondary hover:border-indigo-200 hover:text-indigo-600 transition-all duration-200"
            :disabled="importing">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>
            </svg>
            <span class="hidden sm:inline">{{ importing ? t('machines.importing') : t('machines.import_btn') }}</span>
          </button>
        </div>
        <!-- Export -->
        <button @click="handleExport"
          class="btn-md btn-secondary hover:border-emerald-200 hover:text-emerald-600 transition-all duration-200"
          :disabled="exporting">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          {{ exporting ? t('machines.exporting') : t('machines.export_btn') }}
        </button>
        <!-- Add -->
        <RouterLink v-if="auth.canWrite" to="/machines/new"
          class="btn-md btn-primary shadow-lg shadow-indigo-500/25
                 hover:shadow-indigo-500/40 hover:-translate-y-px transition-all duration-200">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          <span class="hidden sm:inline">{{ t('machines.add') }}</span>
        </RouterLink>
      </div>
    </div>

    <!-- Filters bar -->
    <div class="bg-white border border-slate-200 rounded-xl p-3 sm:p-4 shadow-sm">
      <div class="flex flex-col gap-2">
        <!-- Search: always full width -->
        <div class="relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none"
            fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input v-model="filters.search" @input="debouncedSearch"
            type="text" :placeholder="t('machines.search_ph')"
            class="form-input pl-9 h-9 text-sm bg-slate-50 hover:border-slate-300
                   focus:bg-white transition-all duration-200 w-full" />
        </div>

        <!-- Selects: 2-col on mobile, inline on sm+ -->
        <div class="grid grid-cols-2 sm:flex sm:flex-wrap gap-2">
          <div class="relative">
            <select v-model="filters.status" @change="loadMachines" class="filter-select w-full">
              <option value="">{{ t('machines.all_statuses') }}</option>
              <option v-for="s in statusOptions" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
            <svg class="select-chevron" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
          <div class="relative">
            <select v-model="filters.workshop" @change="onWorkshopChange" class="filter-select w-full">
              <option value="">{{ t('common.all_workshops') }}</option>
              <option v-for="w in workshopOptions" :key="w.id" :value="w.id">{{ w.name }}</option>
            </select>
            <svg class="select-chevron" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
          <div class="relative col-span-2 sm:col-span-1">
            <select v-model="filters.machine_type" @change="loadMachines" class="filter-select w-full">
              <option value="">{{ t('machines.all_types') }}</option>
              <option v-for="tp in typeOptions" :key="tp.id" :value="tp.id">{{ tp.name }}</option>
            </select>
            <svg class="select-chevron" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </div>

        <!-- Checkbox + Reset -->
        <div class="flex items-center gap-2 flex-wrap">
          <label v-if="auth.isAdmin"
            class="flex items-center gap-2 text-sm text-slate-600 cursor-pointer select-none
                   px-2 py-1 rounded-lg hover:bg-slate-50 transition-colors duration-150">
            <input type="checkbox" v-model="filters.include_deleted" @change="loadMachines"
              class="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500/30" />
            {{ t('machines.show_deleted') }}
          </label>
          <Transition name="fade">
            <button v-if="hasActiveFilters" @click="resetFilters"
              class="inline-flex items-center gap-1.5 text-xs font-medium text-rose-500
                     bg-rose-50 border border-rose-100 hover:bg-rose-100
                     px-3 py-1.5 rounded-lg transition-all duration-150 cursor-pointer">
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              {{ t('common.reset') }}
            </button>
          </Transition>
        </div>
      </div>
    </div>

    <!-- Table card -->
    <div class="bg-white border border-slate-200 rounded-xl shadow-sm">

      <!-- Loading skeletons -->
      <div v-if="loading" class="p-6 space-y-2.5">
        <div v-for="i in 8" :key="i"
          class="skeleton h-12 rounded-lg"
          :style="{ animationDelay: `${(i - 1) * 50}ms` }">
        </div>
      </div>

      <!-- Empty state -->
      <div v-else-if="machines.length === 0"
        class="flex flex-col items-center justify-center py-20 text-center px-4">
        <div class="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18"/>
          </svg>
        </div>
        <div class="text-lg font-semibold text-slate-700 mb-1">{{ t('machines.not_found') }}</div>
        <div class="text-sm text-slate-400 max-w-xs">
          {{ t('machines.not_found_hint') }}
        </div>
        <RouterLink v-if="auth.canWrite" to="/machines/new"
          class="btn-md btn-primary mt-5 shadow-lg shadow-indigo-500/25">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          {{ t('machines.add') }}
        </RouterLink>
      </div>

      <!-- Mobile card list -->
      <template v-else>
      <div class="sm:hidden divide-y divide-slate-100">
        <div v-for="machine in machines" :key="machine.id"
          :class="['px-4 py-3.5 cursor-pointer active:bg-slate-50', machine.deleted_at ? 'opacity-50 bg-rose-50/30' : '']"
          @click="$router.push(`/machines/${machine.id}`)">
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0 flex-1">
              <div class="flex items-center gap-2 flex-wrap mb-1.5">
                <span class="font-mono text-xs font-semibold text-indigo-700 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-md">
                  {{ machine.inventory_number }}
                </span>
                <StatusBadge :status="machine.current_status_name" :color="machine.current_status_color" />
              </div>
              <div class="font-semibold text-slate-900 text-sm leading-snug">{{ machine.name }}</div>
              <div v-if="machine.manufacturer" class="text-xs text-slate-400">{{ machine.manufacturer }}</div>
              <div class="mt-1.5 grid grid-cols-2 gap-x-3 gap-y-0.5 text-xs text-slate-500">
                <div v-if="machine.machine_type_name">{{ machine.machine_type_name }}</div>
                <div v-if="machine.workshop_name">{{ machine.workshop_name }}</div>
                <div v-if="machine.operator_name" class="text-slate-400">{{ machine.operator_name }}</div>
              </div>
            </div>
            <div class="flex items-center gap-1 flex-shrink-0" @click.stop>
              <RouterLink :to="`/machines/${machine.id}`" class="action-btn hover:text-indigo-600 hover:bg-indigo-50">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
              </RouterLink>
              <RouterLink v-if="auth.canWrite" :to="`/machines/${machine.id}/edit`" class="action-btn hover:text-amber-600 hover:bg-amber-50">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Desktop table (sm+) with horizontal scroll -->
      <div class="hidden sm:block overflow-x-auto">
        <table class="w-full text-sm min-w-[800px]">
          <thead>
            <tr class="border-b border-slate-200 bg-slate-50/80">
              <th class="th-col sortable-col" @click="toggleSort('inventory_number')">
                <span class="inline-flex items-center gap-1.5">
                  {{ t('machines.col_inv') }}
                  <svg v-if="filters.ordering === 'inventory_number'"
                    class="w-3 h-3 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"/>
                  </svg>
                  <svg v-else-if="filters.ordering === '-inventory_number'"
                    class="w-3 h-3 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
                  </svg>
                  <svg v-else class="w-3 h-3 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4"/>
                  </svg>
                </span>
              </th>
              <th class="th-col sortable-col" @click="toggleSort('name')">
                <span class="inline-flex items-center gap-1.5">
                  {{ t('machines.col_name') }}
                  <svg v-if="filters.ordering === 'name'"
                    class="w-3 h-3 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"/>
                  </svg>
                  <svg v-else-if="filters.ordering === '-name'"
                    class="w-3 h-3 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
                  </svg>
                  <svg v-else class="w-3 h-3 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4"/>
                  </svg>
                </span>
              </th>
              <th class="th-col">{{ t('machines.col_type_model') }}</th>
              <th class="th-col">{{ t('common.status') }}</th>
              <th class="th-col">{{ t('machines.col_location') }}</th>
              <th class="th-col">{{ t('machines.col_operator') }}</th>
              <th class="th-col sortable-col" @click="toggleSort('updated_at')">
                <span class="inline-flex items-center gap-1.5">
                  {{ t('machines.col_updated') }}
                  <svg v-if="filters.ordering === 'updated_at'"
                    class="w-3 h-3 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7"/>
                  </svg>
                  <svg v-else-if="filters.ordering === '-updated_at'"
                    class="w-3 h-3 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/>
                  </svg>
                  <svg v-else class="w-3 h-3 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4"/>
                  </svg>
                </span>
              </th>
              <th class="th-col text-right">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100/80">
            <tr v-for="machine in machines" :key="machine.id"
              :class="[
                'table-row group cursor-pointer',
                machine.deleted_at ? 'opacity-50 bg-rose-50/30' : ''
              ]"
              @click="$router.push(`/machines/${machine.id}`)">

              <td class="td-col">
                <span class="font-mono text-xs font-semibold text-indigo-700
                             bg-indigo-50 border border-indigo-100
                             px-2 py-0.5 rounded-md whitespace-nowrap">
                  {{ machine.inventory_number }}
                </span>
              </td>

              <td class="td-col">
                <div class="font-semibold text-slate-900 group-hover:text-indigo-600
                            transition-colors duration-150 leading-snug">
                  {{ machine.name }}
                </div>
                <div v-if="machine.manufacturer" class="text-xs text-slate-400 mt-0.5">
                  {{ machine.manufacturer }}
                </div>
              </td>

              <td class="td-col">
                <div v-if="machine.machine_type_name" class="text-sm text-slate-700 font-medium">
                  {{ machine.machine_type_name }}
                </div>
                <div v-if="machine.model" class="text-xs text-slate-400 mt-0.5">{{ machine.model }}</div>
              </td>

              <td class="td-col" @click.stop>
                <StatusBadge :status="machine.current_status_name" :color="machine.current_status_color" />
                <div v-if="machine.deleted_at" class="text-xs text-rose-500 mt-1 font-medium">{{ t('machines.deleted_label') }}</div>
              </td>

              <td class="td-col">
                <div v-if="machine.workshop_name" class="text-sm text-slate-700 font-medium">
                  {{ machine.workshop_name }}
                </div>
                <div v-if="machine.section_name" class="text-xs text-slate-400 mt-0.5">
                  {{ machine.section_name }}
                </div>
                <div v-if="machine.workplace" class="text-xs text-slate-400">{{ machine.workplace }}</div>
              </td>

              <td class="td-col">
                <div v-if="machine.operator_name" class="text-sm text-slate-700">{{ machine.operator_name }}</div>
                <div v-else-if="machine.assigned_brigade" class="text-sm text-slate-700">{{ machine.assigned_brigade }}</div>
                <div v-else class="text-xs text-slate-300 italic">—</div>
              </td>

              <td class="td-col">
                <div class="inline-flex items-center gap-1 text-xs text-slate-400 tabular-nums">
                  {{ formatDate(machine.updated_at) }}
                  <svg class="w-3 h-3 text-slate-300 opacity-0 group-hover:opacity-100 transition-opacity duration-150"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
                  </svg>
                </div>
              </td>

              <td class="td-col" @click.stop>
                <div class="flex items-center justify-end gap-1">
                  <RouterLink :to="`/machines/${machine.id}`"
                    class="action-btn hover:text-indigo-600 hover:bg-indigo-50"
                    title="Просмотр">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                  </RouterLink>
                  <RouterLink v-if="auth.canWrite" :to="`/machines/${machine.id}/edit`"
                    class="action-btn hover:text-amber-600 hover:bg-amber-50"
                    title="Редактировать">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </RouterLink>
                  <button v-if="auth.isAdmin && !machine.deleted_at"
                    @click.stop="confirmDelete(machine)"
                    class="action-btn hover:text-rose-600 hover:bg-rose-50"
                    title="Удалить">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                  <button v-if="auth.isAdmin && machine.deleted_at"
                    @click.stop="handleRestore(machine)"
                    class="action-btn hover:text-emerald-600 hover:bg-emerald-50"
                    title="Восстановить">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      </template>

      <!-- Pagination -->
      <div v-if="pagination.total_pages > 1"
        class="flex flex-wrap items-center justify-between gap-3 px-4 sm:px-5 py-3 border-t border-slate-100 bg-slate-50/50">
        <div class="text-sm text-slate-500 tabular-nums">
          {{ t('machines.page_label') }}
          <span class="font-semibold text-slate-700">{{ pagination.current_page }}</span>
          {{ t('machines.page_of') }}
          <span class="font-semibold text-slate-700">{{ pagination.total_pages }}</span>
          <span class="text-slate-400 ml-1 hidden sm:inline">({{ pagination.count }} {{ t('machines.page_records') }})</span>
        </div>
        <div class="flex items-center gap-2">
          <select v-model="filters.page_size" @change="loadMachines"
            class="form-select h-8 w-20 text-xs rounded-lg bg-white border-slate-200">
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
          <button @click="prevPage" :disabled="!pagination.previous"
            class="pag-btn disabled:opacity-40 disabled:cursor-not-allowed">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
            </svg>
            {{ t('common.prev') }}
          </button>
          <button @click="nextPage" :disabled="!pagination.next"
            class="pag-btn disabled:opacity-40 disabled:cursor-not-allowed">
            {{ t('common.next') }}
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Delete confirm modal -->
    <ConfirmModal v-if="deleteTarget"
      :title="t('machines.delete_title')"
      :message="`${t('machines.col_name')} «${deleteTarget.name}» ${t('machines.delete_msg_suffix')}`"
      :confirm-label="t('machines.delete_confirm')"
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
import { useI18n } from '@/i18n'

const auth = useAuthStore()
const toast = useToast()
const { t } = useI18n()
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
  machine_type: route.query.machine_type || '',
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
    toast.error(t('toast.load_data_error'))
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
    toast.success(t('toast.machine_deleted'))
    deleteTarget.value = null
    loadMachines()
  } catch {
    toast.error(t('toast.delete_error'))
  }
}

async function handleRestore(machine) {
  try {
    await machinesApi.restore(machine.id)
    toast.success(t('toast.machine_restored'))
    loadMachines()
  } catch {
    toast.error(t('toast.restore_error'))
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
    toast.success(t('toast.export_success'))
  } catch {
    toast.error(t('toast.export_error'))
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
    toast.success(`${t('toast.import_done_prefix')}: ${d.created} ${t('toast.import_created')}, ${d.updated} ${t('toast.import_updated')}`)
    if (d.errors.length > 0) toast.warning(`${d.errors.length} ${t('toast.import_errors')}`)
    loadMachines()
  } catch {
    toast.error(t('toast.import_error'))
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

<style scoped>
/* ── Table header cells ── */
.th-col {
  @apply px-4 py-3 text-left text-xs font-semibold text-slate-500
         uppercase tracking-wide whitespace-nowrap select-none;
}
.sortable-col {
  @apply cursor-pointer hover:text-slate-700 hover:bg-slate-100/80 transition-colors duration-150;
}

/* ── Table data cells ── */
.td-col {
  @apply px-4 py-3 align-middle text-slate-700;
}

/* ── Table row — accent left border on hover ── */
.table-row {
  border-left: 2px solid transparent;
  transition: background-color 100ms ease, border-color 150ms ease;
}
.table-row:hover {
  background-color: rgba(99, 102, 241, 0.03);
  border-left-color: rgba(99, 102, 241, 0.35);
}

/* ── Action icon buttons ── */
.action-btn {
  @apply p-1.5 rounded-lg text-slate-400 transition-colors duration-150 cursor-pointer
         inline-flex items-center justify-center;
}

/* ── Filter select — hides default arrow, uses custom SVG chevron ── */
.filter-select {
  @apply form-input h-9 text-sm bg-slate-50 border-slate-200 pl-3 pr-8
         hover:border-slate-300 transition-colors duration-150
         appearance-none cursor-pointer rounded-lg;
}
.select-chevron {
  @apply absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none;
}

/* ── Pagination button ── */
.pag-btn {
  @apply inline-flex items-center gap-1 text-xs font-medium px-3 py-1.5 rounded-lg
         border border-slate-200 bg-white text-slate-600
         hover:bg-slate-50 hover:border-slate-300
         transition-all duration-150 cursor-pointer;
}

/* ── Fade transition for reset button ── */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* ── Respect prefers-reduced-motion ── */
@media (prefers-reduced-motion: reduce) {
  .table-row,
  .action-btn,
  .pag-btn,
  .filter-select {
    transition: none;
  }
}
</style>
