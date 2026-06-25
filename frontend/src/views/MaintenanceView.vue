<template>
  <div class="animate-fade-in space-y-4">

    <!-- Header -->
    <div>
      <h1 class="text-xl font-bold text-slate-900">{{ t('maintenance.title') }}</h1>
      <p class="text-xs text-slate-400 mt-0.5">{{ t('maintenance.subtitle') }}</p>
    </div>

    <!-- Stats row -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <div class="stat-card border-rose-200 bg-rose-50">
        <div class="stat-value text-rose-600">{{ counts.overdue }}</div>
        <div class="stat-label text-rose-400">{{ t('maintenance.stat_overdue') }}</div>
      </div>
      <div class="stat-card border-yellow-200 bg-yellow-50">
        <div class="stat-value text-yellow-600">{{ counts.near }}</div>
        <div class="stat-label text-yellow-500">{{ t('maintenance.stat_near') }}</div>
      </div>
      <div class="stat-card border-blue-200 bg-blue-50">
        <div class="stat-value text-blue-600">{{ counts.in_repair }}</div>
        <div class="stat-label text-blue-500">{{ t('maintenance.stat_in_repair') }}</div>
      </div>
      <div class="stat-card border-slate-200 bg-slate-50">
        <div class="stat-value text-slate-700">{{ allMachines.length }}</div>
        <div class="stat-label text-slate-400">{{ t('machines.title') }}</div>
      </div>
    </div>

    <!-- Search -->
    <div class="relative">
      <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
      <input v-model="search" type="text" :placeholder="t('common.search')"
        class="w-full pl-9 pr-4 py-2 text-sm border border-slate-200 rounded-xl bg-white
               focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all" />
    </div>

    <!-- Kanban board -->
    <div class="kanban-board">

      <!-- 1. Без графика -->
      <div class="kanban-col">
        <div class="kanban-hdr kanban-hdr--none">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-slate-400"></div>
            <span class="kanban-hdr-title">{{ t('maintenance.kanban_no_schedule') }}</span>
          </div>
          <span class="kanban-badge bg-slate-200 text-slate-600">{{ filteredNoSchedule.length }}</span>
        </div>
        <div class="kanban-cards">
          <p v-if="loading" class="kanban-empty">...</p>
          <p v-else-if="filteredNoSchedule.length === 0" class="kanban-empty">{{ t('maintenance.kanban_empty') }}</p>
          <div v-for="m in filteredNoSchedule" :key="m.id"
            class="kanban-card kanban-card--none group">
            <div class="font-medium text-sm text-slate-800 truncate">{{ m.name }}</div>
            <div class="text-xs text-slate-400 mt-0.5">{{ m.inventory_number }}</div>
            <div v-if="m.workshop_name" class="text-xs text-slate-400 truncate">{{ m.workshop_name }}</div>
            <div class="mt-3">
              <button @click="openSimpleSchedule(m)"
                class="w-full text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700
                       rounded-lg px-3 py-1.5 transition-colors">
                {{ t('maintenance.kanban_set_schedule') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Муҳлати яқин (near) -->
      <div class="kanban-col">
        <div class="kanban-hdr kanban-hdr--near">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-yellow-500"></div>
            <span class="kanban-hdr-title">{{ t('maintenance.kanban_near') }}</span>
          </div>
          <span class="kanban-badge bg-yellow-100 text-yellow-700">{{ filteredNear.length }}</span>
        </div>
        <div class="kanban-cards">
          <p v-if="loading" class="kanban-empty">...</p>
          <p v-else-if="filteredNear.length === 0" class="kanban-empty">{{ t('maintenance.kanban_empty') }}</p>
          <RouterLink v-for="item in filteredNear" :key="item.machine"
            :to="`/machines/${item.machine}`"
            class="kanban-card kanban-card--near block relative">
            <!-- Edit btn top-right -->
            <button @click.prevent.stop="openEdit(item)" class="edit-btn" :title="t('maintenance.schedule_edit')">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </button>
            <div class="font-medium text-sm text-slate-800 truncate pr-7">{{ item.machine_name }}</div>
            <div class="text-xs text-slate-400 mt-0.5">{{ item.machine_inventory }}</div>
            <div v-if="item.machine_workshop" class="text-xs text-slate-400 truncate">{{ item.machine_workshop }}</div>
            <div class="my-2 border-t border-slate-100"></div>
            <div class="flex justify-between text-xs mb-1">
              <span class="text-slate-400">{{ t('maintenance.col_next') }}</span>
              <span class="font-semibold text-yellow-600 tabular-nums">{{ formatDate(item.next_maintenance_date) }}</span>
            </div>
            <div class="text-xs font-bold text-yellow-600 mb-3">{{ daysLabel(item) }}</div>
            <button @click.prevent.stop="doStartRepair(item)"
              class="w-full text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700
                     rounded-lg px-3 py-1.5 transition-colors">
              {{ t('maintenance.kanban_repair_start') }}
            </button>
          </RouterLink>
        </div>
      </div>

      <!-- 3. Просрочено (overdue) -->
      <div class="kanban-col">
        <div class="kanban-hdr kanban-hdr--overdue">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-rose-500"></div>
            <span class="kanban-hdr-title">{{ t('maintenance.kanban_overdue') }}</span>
          </div>
          <span class="kanban-badge bg-rose-100 text-rose-700">{{ filteredOverdue.length }}</span>
        </div>
        <div class="kanban-cards">
          <p v-if="loading" class="kanban-empty">...</p>
          <p v-else-if="filteredOverdue.length === 0" class="kanban-empty">{{ t('maintenance.kanban_empty') }}</p>
          <RouterLink v-for="item in filteredOverdue" :key="item.machine"
            :to="`/machines/${item.machine}`"
            class="kanban-card kanban-card--overdue block relative">
            <!-- Edit btn top-right -->
            <button @click.prevent.stop="openEdit(item)" class="edit-btn" :title="t('maintenance.schedule_edit')">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </button>
            <div class="font-medium text-sm text-slate-800 truncate pr-7">{{ item.machine_name }}</div>
            <div class="text-xs text-slate-400 mt-0.5">{{ item.machine_inventory }}</div>
            <div v-if="item.machine_workshop" class="text-xs text-slate-400 truncate">{{ item.machine_workshop }}</div>
            <div class="my-2 border-t border-slate-100"></div>
            <div class="flex justify-between text-xs mb-1">
              <span class="text-slate-400">{{ t('maintenance.col_next') }}</span>
              <span class="font-semibold text-rose-600 tabular-nums">{{ formatDate(item.next_maintenance_date) }}</span>
            </div>
            <div class="text-xs font-bold text-rose-600 mb-3">{{ daysLabel(item) }}</div>
            <button @click.prevent.stop="doStartRepair(item)"
              class="w-full text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700
                     rounded-lg px-3 py-1.5 transition-colors">
              {{ t('maintenance.kanban_repair_start') }}
            </button>
          </RouterLink>
        </div>
      </div>

      <!-- 4. Jarayonda (in_repair) -->
      <div class="kanban-col">
        <div class="kanban-hdr kanban-hdr--repair">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-blue-500"></div>
            <span class="kanban-hdr-title">{{ t('maintenance.kanban_in_repair') }}</span>
          </div>
          <span class="kanban-badge bg-blue-100 text-blue-700">{{ filteredInRepair.length }}</span>
        </div>
        <div class="kanban-cards">
          <p v-if="loading" class="kanban-empty">...</p>
          <p v-else-if="filteredInRepair.length === 0" class="kanban-empty">{{ t('maintenance.kanban_empty') }}</p>
          <div v-for="item in filteredInRepair" :key="item.machine"
            class="kanban-card kanban-card--repair relative">
            <!-- Edit btn top-right -->
            <button @click.stop="openEdit(item)" class="edit-btn" :title="t('maintenance.schedule_edit')">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </button>
            <!-- Header strip -->
            <div class="flex items-start gap-2 mb-2 pr-7">
              <div class="min-w-0">
                <div class="font-semibold text-sm text-slate-900 truncate">{{ item.machine_name }}</div>
                <div v-if="item.machine_workshop" class="text-xs text-blue-600 font-medium truncate mt-0.5">{{ item.machine_workshop }}</div>
                <div class="text-xs text-slate-400 mt-0.5">{{ item.machine_inventory }}</div>
              </div>
              <span class="relative flex-shrink-0 mt-0.5 ml-auto">
                <span class="animate-ping absolute inline-flex h-2.5 w-2.5 rounded-full bg-blue-400 opacity-75"></span>
                <span class="relative inline-flex h-2.5 w-2.5 rounded-full bg-blue-500"></span>
              </span>
            </div>
            <!-- Repair started -->
            <div class="bg-blue-50 border border-blue-100 rounded-lg px-2.5 py-1.5 mb-2">
              <div class="text-[10px] text-blue-400 uppercase tracking-wide font-medium">{{ t('maintenance.kanban_repair_since') }}</div>
              <div class="text-xs font-bold text-blue-700 tabular-nums mt-0.5">{{ formatDateTime(item.repair_started_at) }}</div>
            </div>
            <!-- Task progress -->
            <div class="mb-3">
              <div class="flex items-center justify-between text-xs mb-1">
                <span class="text-slate-500 font-medium">{{ t('maintenance.task_title') }}</span>
                <span class="text-slate-600 font-semibold tabular-nums">{{ item.tasks_done }} / {{ item.tasks_total }}</span>
              </div>
              <div class="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full transition-all duration-300"
                  :style="`width: ${item.tasks_total > 0 ? Math.round(item.tasks_done / item.tasks_total * 100) : 0}%`">
                </div>
              </div>
              <div v-if="item.tasks_total > 0" class="text-[10px] text-slate-400 mt-0.5">
                {{ item.tasks_total }} {{ t('maintenance.task_of') }} {{ item.tasks_done }} {{ t('maintenance.task_done_suffix') }}
              </div>
              <div v-else class="text-[10px] text-slate-400 mt-0.5 italic">{{ t('maintenance.task_none') }}</div>
            </div>
            <!-- Jami xarajat -->
            <div v-if="Number(item.total_expense) > 0"
              class="text-[11px] text-violet-600 font-medium mb-2">
              {{ t('machines.total_expense') }}: <strong>${{ Number(item.total_expense).toFixed(2) }}</strong>
            </div>
            <!-- Buttons -->
            <div class="flex gap-1.5">
              <RouterLink :to="`/maintenance/${item.machine}`"
                class="flex-1 text-xs font-semibold text-blue-700 bg-blue-50 hover:bg-blue-100
                       border border-blue-200 rounded-lg py-1.5 transition-colors text-center">
                {{ t('maintenance.kanban_detail') }}
              </RouterLink>
              <button @click="openComplete(item)"
                class="flex-1 text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-700
                       rounded-lg py-1.5 transition-colors">
                {{ t('maintenance.kanban_repair_done') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 5. В норме (ok) -->
      <div class="kanban-col">
        <div class="kanban-hdr kanban-hdr--ok">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-emerald-500"></div>
            <span class="kanban-hdr-title">{{ t('maintenance.kanban_ok') }}</span>
          </div>
          <span class="kanban-badge bg-emerald-100 text-emerald-700">{{ filteredOk.length }}</span>
        </div>
        <div class="kanban-cards">
          <p v-if="loading" class="kanban-empty">...</p>
          <p v-else-if="filteredOk.length === 0" class="kanban-empty">{{ t('maintenance.kanban_empty') }}</p>
          <RouterLink v-for="item in filteredOk" :key="item.machine"
            :to="`/machines/${item.machine}`"
            class="kanban-card kanban-card--ok block relative">
            <!-- Edit btn top-right -->
            <button @click.prevent.stop="openEdit(item)" class="edit-btn" :title="t('maintenance.schedule_edit')">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
            </button>
            <div class="font-medium text-sm text-slate-800 truncate pr-7">{{ item.machine_name }}</div>
            <div class="text-xs text-slate-400 mt-0.5">{{ item.machine_inventory }}</div>
            <div v-if="item.machine_workshop" class="text-xs text-slate-400 truncate">{{ item.machine_workshop }}</div>
            <div class="my-2 border-t border-slate-100"></div>
            <div class="flex justify-between text-xs">
              <span class="text-slate-400">{{ t('maintenance.col_next') }}</span>
              <span class="font-semibold text-emerald-600 tabular-nums">{{ formatDate(item.next_maintenance_date) }}</span>
            </div>
            <div class="text-xs font-medium text-emerald-600 mt-0.5">{{ daysLabel(item) }}</div>
            <div v-if="Number(item.total_expense) > 0"
              class="mt-2 text-[11px] text-violet-600 font-medium">
              {{ t('machines.total_expense') }}: <strong>${{ Number(item.total_expense).toFixed(2) }}</strong>
            </div>
          </RouterLink>
        </div>
      </div>

    </div><!-- /kanban-board -->

    <!-- Simple Schedule Modal (faqat birinchi marta, "Назначить" tugmasidan) -->
    <Transition name="modal">
      <div v-if="showSimpleModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[2px]" @click="showSimpleModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 space-y-5">

          <!-- Header -->
          <div>
            <h3 class="text-base font-bold text-slate-900">{{ t('maintenance.kanban_set_schedule') }}</h3>
            <p class="text-sm text-slate-500 mt-0.5">{{ simpleMachine?.name }}</p>
          </div>

          <!-- Oxirgi TO sanasi -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">
              {{ t('maintenance.form_last_date') }} <span class="text-rose-500">*</span>
            </label>
            <input v-model="simpleForm.last_date" type="date"
              class="w-full text-sm border rounded-xl px-4 py-2.5 transition-all
                     focus:outline-none focus:ring-2 focus:ring-indigo-300"
              :class="simpleError && !simpleForm.last_date ? 'border-rose-300' : 'border-slate-200'" />
            <p class="text-xs text-slate-400 mt-1.5">{{ t('maintenance.simple_last_date_hint') }}</p>
          </div>

          <!-- Interval -->
          <div>
            <label class="block text-sm font-semibold text-slate-700 mb-2">
              {{ t('maintenance.simple_interval') }} *
            </label>
            <div class="grid grid-cols-3 gap-2">
              <button v-for="m in [1,2,3,6,12]" :key="m"
                @click="simpleForm.interval = m; simpleShowCustom = false"
                type="button"
                :class="[
                  'py-2 text-sm rounded-xl border transition-all font-medium cursor-pointer',
                  simpleForm.interval === m && !simpleShowCustom
                    ? 'bg-indigo-600 border-indigo-600 text-white shadow-sm'
                    : 'border-slate-200 bg-slate-50 text-slate-600 hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700'
                ]">
                {{ m }} {{ t('maintenance.simple_month_short') }}
              </button>
              <button
                @click="simpleShowCustom = true; simpleForm.interval = null"
                type="button"
                :class="[
                  'py-2 text-sm rounded-xl border transition-all font-medium cursor-pointer',
                  simpleShowCustom
                    ? 'bg-indigo-600 border-indigo-600 text-white shadow-sm'
                    : 'border-slate-200 bg-slate-50 text-slate-600 hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700'
                ]">
                {{ t('maintenance.month_other') }}
              </button>
            </div>
            <input v-if="simpleShowCustom"
              v-model.number="simpleForm.interval" type="number" min="1" max="60"
              :placeholder="t('maintenance.form_interval_ph')"
              class="mt-2 w-full text-sm border border-slate-200 rounded-xl px-3 py-2
                     focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all" />
          </div>

          <p v-if="simpleError" class="text-xs text-rose-500 bg-rose-50 border border-rose-100 rounded-lg px-3 py-2">
            {{ simpleError }}
          </p>

          <!-- Actions -->
          <div class="flex gap-2 pt-1">
            <button @click="showSimpleModal = false"
              class="flex-1 py-2.5 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button @click="saveSimpleSchedule" :disabled="simpleSaving"
              class="flex-1 py-2.5 text-sm text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl
                     transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
              {{ simpleSaving ? t('common.saving') : t('common.save') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

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
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">{{ t('maintenance.form_interval') }} *</label>
              <div class="grid grid-cols-3 gap-2">
                <button v-for="m in intervalOptions" :key="m"
                  @click="form.interval_months = m; showCustomInterval = false"
                  :class="['interval-btn', form.interval_months === m && !showCustomInterval ? 'interval-btn--active' : '']">
                  {{ t(`maintenance.month_${m}`) }}
                </button>
                <button @click="showCustomInterval = true; form.interval_months = null"
                  :class="['interval-btn', showCustomInterval ? 'interval-btn--active' : '']">
                  {{ t('maintenance.month_other') }}
                </button>
              </div>
              <input v-if="showCustomInterval" v-model.number="form.interval_months" type="number" min="1" max="60"
                :placeholder="t('maintenance.form_interval_ph')"
                class="mt-2 w-full text-sm border border-slate-200 rounded-xl px-3 py-2
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all"/>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">
                {{ t('maintenance.form_last_date') }} <span class="text-rose-500">*</span>
              </label>
              <input v-model="form.last_maintenance_date" type="date"
                class="w-full text-sm border rounded-xl px-3 py-2 focus:outline-none focus:ring-2 transition-all"
                :class="formError && !form.last_maintenance_date
                  ? 'border-rose-300 focus:ring-rose-300'
                  : 'border-slate-200 focus:ring-indigo-300'" />
              <p class="text-xs text-slate-400 mt-1">{{ t('maintenance.form_last_date_hint') }}</p>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">{{ t('maintenance.form_notes') }}</label>
              <textarea v-model="form.notes" rows="2" :placeholder="t('maintenance.form_notes_ph')"
                class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 resize-none
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all"></textarea>
            </div>
          </div>
          <p v-if="formError" class="text-xs text-rose-500">{{ formError }}</p>
          <div class="flex gap-2 pt-1">
            <button @click="closeModal" class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button @click="saveSchedule" :disabled="saving"
              class="flex-1 py-2 text-sm text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition-colors disabled:opacity-60">
              {{ saving ? t('common.saving') : t('common.save') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Repair Detail Modal -->
    <Transition name="modal">
      <div v-if="showDetailModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[2px]" @click="showDetailModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md flex flex-col max-h-[90vh]">

          <!-- Modal header -->
          <div class="px-5 pt-5 pb-4 border-b border-slate-100 flex-shrink-0">
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <h3 class="text-base font-bold text-slate-900 truncate">{{ detailItem?.machine_name }}</h3>
                <p v-if="detailItem?.machine_workshop" class="text-xs text-blue-600 font-medium mt-0.5">{{ detailItem?.machine_workshop }}</p>
                <p class="text-xs text-slate-400 mt-0.5">{{ detailItem?.machine_inventory }}</p>
              </div>
              <button @click="showDetailModal = false"
                class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors flex-shrink-0">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
            <!-- Repair started badge -->
            <div class="mt-3 inline-flex items-center gap-1.5 bg-blue-50 border border-blue-100 rounded-lg px-2.5 py-1.5">
              <svg class="w-3.5 h-3.5 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="text-xs text-blue-400">{{ t('maintenance.kanban_repair_since') }}:</span>
              <span class="text-xs font-bold text-blue-700">{{ formatDateTime(detailItem?.repair_started_at) }}</span>
            </div>
          </div>

          <!-- Tasks list -->
          <div class="flex-1 overflow-y-auto px-5 py-4">
            <div class="flex items-center justify-between mb-3">
              <h4 class="text-sm font-semibold text-slate-700">{{ t('maintenance.task_title') }}</h4>
              <span v-if="detailTasks.length > 0"
                class="text-xs font-bold text-slate-500 tabular-nums bg-slate-100 px-2 py-0.5 rounded-full">
                {{ detailTasks.filter(t => t.is_done).length }} / {{ detailTasks.length }}
              </span>
            </div>

            <!-- Progress bar -->
            <div v-if="detailTasks.length > 0" class="h-1.5 bg-slate-100 rounded-full mb-4 overflow-hidden">
              <div class="h-full bg-blue-500 rounded-full transition-all duration-300"
                :style="`width: ${Math.round(detailTasks.filter(x => x.is_done).length / detailTasks.length * 100)}%`">
              </div>
            </div>

            <div v-if="tasksLoading" class="space-y-2">
              <div v-for="i in 3" :key="i" class="skeleton h-10 rounded-lg"></div>
            </div>
            <div v-else-if="detailTasks.length === 0" class="py-6 text-center text-sm text-slate-400 italic">
              {{ t('maintenance.task_none') }}
            </div>
            <div v-else class="space-y-1.5">
              <div v-for="task in detailTasks" :key="task.id"
                class="flex items-center gap-3 p-2.5 rounded-xl border transition-colors"
                :class="task.is_done ? 'bg-emerald-50 border-emerald-100' : 'bg-white border-slate-100 hover:border-slate-200'">
                <button @click="toggleTask(task)"
                  class="w-5 h-5 rounded-full border-2 flex-shrink-0 flex items-center justify-center transition-all"
                  :class="task.is_done ? 'bg-emerald-500 border-emerald-500' : 'border-slate-300 hover:border-blue-400'">
                  <svg v-if="task.is_done" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                  </svg>
                </button>
                <span class="flex-1 text-sm min-w-0 truncate"
                  :class="task.is_done ? 'line-through text-slate-400' : 'text-slate-700'">
                  {{ task.title }}
                </span>
                <button @click="deleteTask(task)"
                  class="p-1 rounded-lg text-slate-300 hover:text-rose-500 hover:bg-rose-50 transition-colors flex-shrink-0">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Add task -->
            <div class="flex gap-2 mt-4">
              <input v-model="newTaskTitle" type="text" :placeholder="t('maintenance.task_add_ph')"
                @keydown.enter="addTask"
                class="flex-1 text-sm border border-slate-200 rounded-xl px-3 py-2
                       focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all" />
              <button @click="addTask" :disabled="!newTaskTitle.trim()"
                class="px-3 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700
                       rounded-xl transition-colors disabled:opacity-40 disabled:cursor-not-allowed">
                {{ t('maintenance.task_add_btn') }}
              </button>
            </div>
          </div>

          <!-- Footer -->
          <div class="px-5 pb-5 pt-3 border-t border-slate-100 flex-shrink-0 flex gap-2">
            <button @click="showDetailModal = false"
              class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button @click="openComplete(detailItem); showDetailModal = false"
              class="flex-1 py-2 text-sm text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl transition-colors">
              {{ t('maintenance.kanban_repair_done') }}
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
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">{{ t('maintenance.complete_date') }} *</label>
              <input v-model="completeForm.completion_date" type="date"
                class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all"/>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1.5">{{ t('maintenance.complete_notes') }}</label>
              <textarea v-model="completeForm.notes" rows="2" :placeholder="t('maintenance.complete_notes_ph')"
                class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 resize-none
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all"></textarea>
            </div>
          </div>
          <div class="flex gap-2">
            <button @click="showCompleteModal = false" class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button @click="markComplete" :disabled="saving"
              class="flex-1 py-2 text-sm text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl transition-colors disabled:opacity-60">
              {{ saving ? t('common.saving') : t('maintenance.complete_btn') }}
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
          <h3 class="text-base font-bold text-slate-900">{{ t('maintenance.delete_confirm_title') }}</h3>
          <p class="text-sm text-slate-600"><strong>{{ deleteTarget?.machine_name }}</strong> — {{ t('maintenance.delete_confirm_msg') }}</p>
          <div class="flex gap-2">
            <button @click="showDeleteModal = false" class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button @click="doDelete" :disabled="saving"
              class="flex-1 py-2 text-sm text-white bg-rose-600 hover:bg-rose-700 rounded-xl transition-colors disabled:opacity-60">
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

const { t } = useI18n()
const toast = useToast()

const loading = ref(true)
const saving = ref(false)
const search = ref('')
const schedules = ref([])
const allMachines = ref([])
const intervalOptions = [1, 2, 3, 6, 12]
const showCustomInterval = ref(false)

// ── Helpers ──
function formatDate(d) { return d ? dayjs(d).format('DD.MM.YYYY') : '—' }
function formatDateTime(d) { return d ? dayjs(d).format('DD.MM.YYYY HH:mm') : '—' }

function today() {
  const d = new Date()
  d.setHours(0, 0, 0, 0)
  return d
}

function parseDateOnly(dateStr) {
  // Parse 'YYYY-MM-DD' without timezone shift
  const [y, m, day] = dateStr.split('-').map(Number)
  const d = new Date(y, m - 1, day)
  d.setHours(0, 0, 0, 0)
  return d
}

function getDaysUntil(dateStr) {
  if (!dateStr) return null
  const ms = parseDateOnly(dateStr) - today()
  return Math.round(ms / 86400000)
}

// Frontend-side alert level (timezone-safe):
// <0      → overdue
// 0–30    → near (Муҳлати яқин)
// >30     → ok
function computeAlertLevel(s) {
  if (s.in_repair) return 'in_repair'
  const days = getDaysUntil(s.next_maintenance_date)
  if (days === null) return 'ok'
  if (days < 0) return 'overdue'
  if (days <= 7) return 'near'
  return 'ok'
}

function daysLabel(item) {
  const days = getDaysUntil(item.next_maintenance_date)
  if (days === null) return '—'
  if (days === 0) return t('maintenance.today')
  if (days === 1) return t('maintenance.tomorrow')
  if (days < 0) return `${Math.abs(days)} ${t('maintenance.days_overdue')}`
  return `${days} ${t('maintenance.days_until')}`
}

function matchSearch(name, inv, workshop) {
  if (!search.value) return true
  const q = search.value.toLowerCase()
  return (name || '').toLowerCase().includes(q) ||
         (inv || '').toLowerCase().includes(q) ||
         (workshop || '').toLowerCase().includes(q)
}

// ── Column computed ──
const machinesWithScheduleIds = computed(() => new Set(schedules.value.map(s => s.machine)))

const filteredNoSchedule = computed(() =>
  allMachines.value.filter(m =>
    !machinesWithScheduleIds.value.has(m.id) &&
    matchSearch(m.name, m.inventory_number, m.workshop_name)
  )
)

const filteredNear = computed(() =>
  schedules.value.filter(s =>
    computeAlertLevel(s) === 'near' &&
    matchSearch(s.machine_name, s.machine_inventory, s.machine_workshop)
  )
)

const filteredInRepair = computed(() =>
  schedules.value.filter(s =>
    computeAlertLevel(s) === 'in_repair' &&
    matchSearch(s.machine_name, s.machine_inventory, s.machine_workshop)
  )
)

const filteredOverdue = computed(() =>
  schedules.value.filter(s =>
    computeAlertLevel(s) === 'overdue' &&
    matchSearch(s.machine_name, s.machine_inventory, s.machine_workshop)
  )
)

const filteredOk = computed(() =>
  schedules.value.filter(s =>
    computeAlertLevel(s) === 'ok' &&
    matchSearch(s.machine_name, s.machine_inventory, s.machine_workshop)
  )
)

const counts = computed(() => ({
  no_schedule: allMachines.value.filter(m => !machinesWithScheduleIds.value.has(m.id)).length,
  near:       schedules.value.filter(s => computeAlertLevel(s) === 'near').length,
  in_repair:  schedules.value.filter(s => computeAlertLevel(s) === 'in_repair').length,
  overdue:    schedules.value.filter(s => computeAlertLevel(s) === 'overdue').length,
  ok:         schedules.value.filter(s => computeAlertLevel(s) === 'ok').length,
}))

// ── Load ──
async function loadData() {
  loading.value = true
  try {
    const [alertsRes, machinesRes] = await Promise.all([
      maintenanceApi.all(),
      machinesApi.list({ page_size: 200 }),
    ])
    schedules.value = alertsRes.data.results || alertsRes.data || []
    allMachines.value = machinesRes.data.results || []
  } catch {
    toast.error(t('toast.load_error'))
  } finally {
    loading.value = false
  }
}

// ── Simple schedule modal (first-time assign) ──
const showSimpleModal = ref(false)
const simpleMachine = ref(null)
const simpleSaving = ref(false)
const simpleError = ref('')
const simpleShowCustom = ref(false)
const simpleForm = ref({ last_date: dayjs().format('YYYY-MM-DD'), interval: 3 })

function openSimpleSchedule(machine) {
  simpleMachine.value = machine
  simpleForm.value = { last_date: dayjs().format('YYYY-MM-DD'), interval: 3 }
  simpleShowCustom.value = false
  simpleError.value = ''
  showSimpleModal.value = true
}

async function saveSimpleSchedule() {
  if (!simpleForm.value.last_date) {
    simpleError.value = t('maintenance.simple_error_date')
    return
  }
  if (!simpleForm.value.interval || simpleForm.value.interval < 1) {
    simpleError.value = t('maintenance.simple_error_interval')
    return
  }
  simpleSaving.value = true
  simpleError.value = ''
  try {
    await maintenanceApi.set(simpleMachine.value.id, {
      last_maintenance_date: simpleForm.value.last_date,
      interval_months: simpleForm.value.interval,
      notes: '',
    })
    showSimpleModal.value = false
    await loadData()
  } catch (e) {
    simpleError.value = e.response?.data?.message || t('toast.error')
  } finally {
    simpleSaving.value = false
  }
}

// ── Schedule form ──
const showFormModal = ref(false)
const editingItem = ref(null)
const formMachine = ref(null)
const formError = ref('')
const form = ref({ interval_months: 3, last_maintenance_date: '', notes: '' })

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
  form.value = { interval_months: 3, last_maintenance_date: dayjs().format('YYYY-MM-DD'), notes: '' }
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
    formError.value = e.response?.data?.message || e.response?.data?.errors?.last_maintenance_date?.[0] || t('toast.error')
  } finally {
    saving.value = false
  }
}

// ── Start repair ──
async function doStartRepair(item) {
  saving.value = true
  try {
    await maintenanceApi.startRepair(item.machine)
    await loadData()
  } catch {
    toast.error(t('toast.error'))
  } finally {
    saving.value = false
  }
}

// ── Repair detail modal ──
const showDetailModal = ref(false)
const detailItem = ref(null)
const detailTasks = ref([])
const tasksLoading = ref(false)
const newTaskTitle = ref('')

async function openRepairDetail(item) {
  detailItem.value = item
  showDetailModal.value = true
  tasksLoading.value = true
  newTaskTitle.value = ''
  try {
    const res = await maintenanceApi.tasks(item.machine)
    detailTasks.value = res.data
  } catch {
    toast.error(t('toast.load_error'))
  } finally {
    tasksLoading.value = false
  }
}

async function addTask() {
  if (!newTaskTitle.value.trim()) return
  try {
    const res = await maintenanceApi.addTask(detailItem.value.machine, { title: newTaskTitle.value.trim() })
    detailTasks.value.push(res.data)
    newTaskTitle.value = ''
    await refreshSchedule(detailItem.value.machine)
  } catch {
    toast.error(t('toast.error'))
  }
}

async function toggleTask(task) {
  try {
    const res = await maintenanceApi.toggleTask(detailItem.value.machine, task.id, { is_done: !task.is_done })
    const idx = detailTasks.value.findIndex(t => t.id === task.id)
    if (idx !== -1) detailTasks.value[idx] = res.data
    await refreshSchedule(detailItem.value.machine)
  } catch {
    toast.error(t('toast.error'))
  }
}

async function deleteTask(task) {
  try {
    await maintenanceApi.deleteTask(detailItem.value.machine, task.id)
    detailTasks.value = detailTasks.value.filter(t => t.id !== task.id)
    await refreshSchedule(detailItem.value.machine)
  } catch {
    toast.error(t('toast.error'))
  }
}

async function refreshSchedule(machineId) {
  try {
    const res = await maintenanceApi.all()
    const updated = (res.data.results || res.data || []).find(s => s.machine === machineId)
    if (updated) {
      const idx = schedules.value.findIndex(s => s.machine === machineId)
      if (idx !== -1) schedules.value[idx] = updated
      if (detailItem.value?.machine === machineId) detailItem.value = updated
    }
  } catch { /* silent */ }
}

// ── Complete modal ──
const showCompleteModal = ref(false)
const completeItem = ref(null)
const completeForm = ref({ completion_date: '', notes: '' })

function openComplete(item) {
  completeItem.value = item
  completeForm.value = { completion_date: dayjs().format('YYYY-MM-DD'), notes: '' }
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

function confirmDelete(item) { deleteTarget.value = item; showDeleteModal.value = true }

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
/* ── Stats ── */
.stat-pill {
  @apply flex flex-col items-center justify-center border rounded-xl py-2.5 px-2 text-center;
}
.stat-val { @apply text-xl font-bold tabular-nums; }
.stat-lbl { @apply text-[10px] font-medium uppercase tracking-wide mt-0.5 leading-tight; }

.stat-card  { @apply rounded-2xl border p-4; }
.stat-value { @apply text-2xl font-bold tabular-nums; }
.stat-label { @apply text-xs font-medium mt-0.5 uppercase tracking-wide; }

/* ── Kanban board ── */
.kanban-board {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 8px;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}
.kanban-board::-webkit-scrollbar { height: 5px; }
.kanban-board::-webkit-scrollbar-track { background: transparent; }
.kanban-board::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 9999px; }

/* Mobile: fixed width → scroll. Desktop: fill equally */
.kanban-col {
  flex: 0 0 256px;
  min-width: 256px;
  display: flex;
  flex-direction: column;
}
@media (min-width: 1024px) {
  .kanban-board { overflow-x: visible; }
  .kanban-col   { flex: 1 1 0; min-width: 0; }
}

/* ── Column header ── */
.kanban-hdr {
  @apply flex items-center justify-between px-3 py-2.5 rounded-t-xl border border-b-0;
  flex-shrink: 0;
}
.kanban-hdr--none   { @apply bg-slate-100 border-slate-200; }
.kanban-hdr--near   { @apply bg-yellow-50 border-yellow-200; }
.kanban-hdr--repair { @apply bg-blue-50 border-blue-200; }
.kanban-hdr--overdue{ @apply bg-rose-50 border-rose-200; }
.kanban-hdr--ok     { @apply bg-emerald-50 border-emerald-200; }

.kanban-hdr-title { @apply text-sm font-semibold text-slate-700; }
.kanban-badge     { @apply text-xs font-bold px-2 py-0.5 rounded-full; }

/* ── Cards area ── */
.kanban-cards {
  @apply border border-slate-200 rounded-b-xl bg-slate-50/60 p-2 space-y-2 overflow-y-auto;
  height: calc(100vh - 310px);
  min-height: 200px;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}
.kanban-cards::-webkit-scrollbar { width: 4px; }
.kanban-cards::-webkit-scrollbar-track { background: transparent; }
.kanban-cards::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 9999px; }

.kanban-empty { @apply p-6 text-center text-xs text-slate-400 italic; }

/* ── Card ── */
.kanban-card {
  @apply bg-white rounded-xl border p-3 shadow-sm transition-all duration-150 select-none;
}
.kanban-card:hover           { @apply shadow-md; }
/* Tahrirlash tugmasi — o'ng yuqori burchak */
.edit-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 6px;
  color: #94a3b8;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  z-index: 1;
}
.edit-btn:hover { background: #e2e8f0; color: #475569; }

.kanban-card--none    { @apply border-slate-200 hover:border-slate-300; }
.kanban-card--near    { @apply border-yellow-200 hover:border-yellow-300; }
.kanban-card--repair  { @apply border-blue-200 hover:border-blue-300; }
.kanban-card--overdue { @apply border-rose-200 hover:border-rose-300; }
.kanban-card--ok      { @apply border-emerald-100 hover:border-emerald-200; }

/* ── Modal ── */
.interval-btn {
  @apply text-xs py-1.5 px-2 rounded-lg border border-slate-200 bg-slate-50 text-slate-600
         hover:bg-indigo-50 hover:border-indigo-200 hover:text-indigo-600
         transition-colors cursor-pointer text-center;
}
.interval-btn--active { @apply bg-indigo-100 border-indigo-300 text-indigo-700 font-semibold; }

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s; }
.modal-enter-from, .modal-leave-to       { opacity: 0; }
</style>
