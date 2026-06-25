<template>
  <div class="animate-fade-in max-w-3xl mx-auto space-y-5">

    <!-- Back + header -->
    <div class="flex items-center gap-3">
      <RouterLink to="/maintenance"
        class="p-2 rounded-xl text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors flex-shrink-0">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
        </svg>
      </RouterLink>
      <div class="min-w-0">
        <h1 class="text-xl font-bold text-slate-900 truncate">{{ machine?.name || '...' }}</h1>
        <p class="text-xs text-slate-400 mt-0.5">TO jadvali · {{ t('maintenance.kanban_in_repair') }}</p>
      </div>
    </div>

    <!-- Loading skeleton -->
    <template v-if="loading">
      <div class="skeleton h-40 rounded-2xl"></div>
      <div class="skeleton h-64 rounded-2xl"></div>
    </template>

    <template v-else-if="machine && schedule">

      <!-- ── Machine info card ── -->
      <div class="card p-5 space-y-4">
        <h2 class="text-sm font-semibold text-slate-700 flex items-center gap-2">
          <svg class="w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18"/>
          </svg>
          {{ t('maintenance.machine_info') }}
        </h2>

        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <div class="info-block">
            <div class="info-label">{{ t('machines.col_name') }}</div>
            <div class="info-val">{{ machine.name }}</div>
          </div>
          <div class="info-block">
            <div class="info-label">{{ t('machines.col_inventory') }}</div>
            <div class="info-val tabular-nums">{{ machine.inventory_number }}</div>
          </div>
          <div class="info-block">
            <div class="info-label">{{ t('machines.col_workshop') }}</div>
            <div class="info-val">{{ machine.workshop_name || '—' }}</div>
          </div>
          <div class="info-block">
            <div class="info-label">{{ t('maintenance.col_interval') }}</div>
            <div class="info-val">{{ schedule.interval_months }} {{ t('maintenance.interval_months') }}</div>
          </div>
          <div class="info-block">
            <div class="info-label">{{ t('maintenance.col_last') }}</div>
            <div class="info-val tabular-nums">{{ formatDate(schedule.last_maintenance_date) }}</div>
          </div>
          <div class="info-block">
            <div class="info-label">{{ t('maintenance.col_next') }}</div>
            <div class="info-val tabular-nums">{{ formatDate(schedule.next_maintenance_date) }}</div>
          </div>
        </div>

        <!-- Repair started badge -->
        <div v-if="schedule.repair_started_at"
          class="flex items-center gap-2 bg-blue-50 border border-blue-100 rounded-xl px-4 py-2.5">
          <span class="relative flex-shrink-0">
            <span class="animate-ping absolute inline-flex h-2.5 w-2.5 rounded-full bg-blue-400 opacity-60"></span>
            <span class="relative inline-flex h-2.5 w-2.5 rounded-full bg-blue-500"></span>
          </span>
          <span class="text-xs text-blue-500 font-medium">{{ t('maintenance.kanban_repair_since') }}:</span>
          <span class="text-sm font-bold text-blue-700 tabular-nums">{{ formatDateTime(schedule.repair_started_at) }}</span>
        </div>
      </div>

      <!-- ── Tasks card ── -->
      <div class="card">
        <!-- Tasks header -->
        <div class="flex items-center justify-between px-5 py-4 border-b border-slate-100">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-xl bg-blue-100 flex items-center justify-center flex-shrink-0">
              <svg class="w-4 h-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
              </svg>
            </div>
            <div>
              <h2 class="text-sm font-semibold text-slate-800">{{ t('maintenance.task_title') }}</h2>
              <p class="text-xs text-slate-400 mt-0.5">
                {{ doneTasks }} / {{ tasks.length }} {{ t('maintenance.task_done_suffix') }}
              </p>
            </div>
          </div>
          <button v-if="auth.isAdmin"
            @click="showAddForm = !showAddForm"
            class="flex items-center gap-1.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700
                   rounded-xl px-3 py-2 transition-colors">
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
            </svg>
            {{ t('maintenance.task_add_label') }}
          </button>
        </div>

        <!-- Progress bar -->
        <div v-if="tasks.length > 0" class="px-5 pt-3">
          <div class="flex items-center justify-between text-xs text-slate-400 mb-1.5">
            <span>{{ t('maintenance.task_title') }}</span>
            <span class="font-semibold tabular-nums">{{ Math.round(doneTasks / tasks.length * 100) }}%</span>
          </div>
          <div class="h-2 bg-slate-100 rounded-full overflow-hidden">
            <div class="h-full rounded-full transition-all duration-500"
              :class="allDone ? 'bg-emerald-500' : 'bg-blue-500'"
              :style="`width: ${tasks.length > 0 ? Math.round(doneTasks / tasks.length * 100) : 0}%`">
            </div>
          </div>
        </div>

        <!-- Add task form -->
        <Transition name="slide-down">
          <div v-if="showAddForm" class="px-5 pt-4 pb-1">
            <div class="bg-blue-50 border border-blue-100 rounded-2xl p-4 space-y-3">
              <h3 class="text-xs font-semibold text-blue-700 uppercase tracking-wide">{{ t('maintenance.task_add_label') }}</h3>
              <!-- Task name -->
              <div>
                <label class="block text-xs font-medium text-slate-600 mb-1">{{ t('maintenance.task_name') }} *</label>
                <input v-model="newTask.title" type="text" :placeholder="t('maintenance.task_name_ph')"
                  class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 bg-white
                         focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all"
                  :class="formError && !newTask.title.trim() ? 'border-rose-300' : ''" />
              </div>
              <!-- Assignee + due date row -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-medium text-slate-600 mb-1">{{ t('maintenance.task_assignee') }}</label>
                  <select v-model="newTask.assignee"
                    class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 bg-white
                           focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all">
                    <option :value="null">— {{ t('common.not_selected') }} —</option>
                    <option v-for="u in employees" :key="u.id" :value="u.id">
                      {{ u.full_name }} — {{ u.role_display }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block text-xs font-medium text-slate-600 mb-1">{{ t('maintenance.task_due_date') }}</label>
                  <input v-model="newTask.due_date" type="date"
                    class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 bg-white
                           focus:outline-none focus:ring-2 focus:ring-blue-300 transition-all" />
                </div>
              </div>
              <p v-if="formError" class="text-xs text-rose-500">{{ formError }}</p>
              <div class="flex gap-2 pt-1">
                <button @click="showAddForm = false; resetForm()"
                  class="flex-1 py-2 text-sm text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 rounded-xl transition-colors">
                  {{ t('common.cancel') }}
                </button>
                <button @click="addTask" :disabled="saving"
                  class="flex-1 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-colors disabled:opacity-50">
                  {{ saving ? t('common.saving') : t('maintenance.task_add_btn') }}
                </button>
              </div>
            </div>
          </div>
        </Transition>

        <!-- Task list -->
        <div class="px-5 py-4 space-y-2">
          <div v-if="tasks.length === 0" class="py-8 text-center text-slate-400 text-sm italic">
            {{ t('maintenance.task_none') }}
          </div>

          <div class="space-y-2">
            <div v-for="taskItem in tasks" :key="taskItem.id"
              class="rounded-xl border transition-all duration-150"
              :class="taskItem.is_done ? 'bg-slate-50/60 border-slate-100' : 'bg-white border-slate-100 hover:border-slate-200 hover:shadow-sm'">

              <!-- Top row: checkbox + content + delete -->
              <div class="flex items-start gap-3 p-3">
                <!-- Checkbox -->
                <button
                  @click="taskItem.is_mine ? toggleTask(taskItem) : null"
                  class="task-check flex-shrink-0"
                  :class="[
                    taskItem.is_done ? 'task-check--done' : 'task-check--pending',
                    !taskItem.is_mine ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'
                  ]"
                  :title="!taskItem.is_mine ? 'Faqat biriktirilgan xodim belgilashi mumkin' : ''"
                  :disabled="!taskItem.is_mine">
                  <svg v-if="taskItem.is_done" class="w-3.5 h-3.5 text-white" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                  </svg>
                </button>

                <!-- Content -->
                <div class="flex-1 min-w-0">
                  <div class="text-sm font-medium truncate"
                    :class="taskItem.is_done ? 'line-through text-slate-400' : 'text-slate-800'">
                    {{ taskItem.title }}
                  </div>
                  <div class="flex flex-wrap items-center gap-2 mt-1">
                    <span v-if="taskItem.assignee_name"
                      class="inline-flex items-center gap-1 text-[11px] text-slate-500 bg-slate-100 rounded-full px-2 py-0.5">
                      <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                      </svg>
                      {{ taskItem.assignee_name }}
                    </span>
                    <span v-if="taskItem.due_date"
                      class="inline-flex items-center gap-1 text-[11px] rounded-full px-2 py-0.5"
                      :class="isDueDatePast(taskItem.due_date) && !taskItem.is_done
                        ? 'bg-rose-100 text-rose-600'
                        : 'bg-slate-100 text-slate-500'">
                      <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                      </svg>
                      {{ formatDate(taskItem.due_date) }}
                    </span>
                    <span v-if="taskItem.is_done && taskItem.done_at"
                      class="text-[11px] text-emerald-600">
                      ✓ {{ formatDateTime(taskItem.done_at) }}
                    </span>
                  </div>
                </div>

                <!-- Delete -->
                <button @click="deleteTask(taskItem)"
                  class="p-1.5 rounded-lg text-slate-300 hover:text-rose-500 hover:bg-rose-50 transition-colors flex-shrink-0">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                </button>
              </div>

              <!-- Sarflangan ehtiyot qismlar (inside task card) -->
              <div v-if="taskItem.spare_parts_used?.length"
                class="mx-3 mb-2 bg-amber-50 border border-amber-100 rounded-xl px-3 py-2 space-y-1">
                <div class="text-[10px] font-semibold text-amber-600 uppercase tracking-wide mb-1.5">
                  {{ t('maintenance.sp_used_title') }}
                </div>
                <div v-for="sp in taskItem.spare_parts_used" :key="sp.id"
                  class="flex items-center justify-between text-xs">
                  <span class="text-slate-700 truncate mr-2">{{ sp.spare_part_name }}</span>
                  <div class="flex items-center gap-1.5 flex-shrink-0">
                    <div class="text-right">
                      <span class="font-semibold tabular-nums text-amber-700">
                        {{ sp.quantity_used }} {{ sp.unit_short || '' }}
                      </span>
                      <div v-if="sp.notes" class="text-[10px] text-slate-400 italic max-w-[120px] truncate">{{ sp.notes }}</div>
                    </div>
                    <button v-if="!taskItem.is_done" @click="removeTaskSparePart(taskItem, sp)"
                      class="text-slate-300 hover:text-rose-500 transition-colors">
                      <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Add spare part button — visible to assignee and admin -->
              <div v-if="!taskItem.is_done && taskItem.is_mine" class="px-3 pb-3">
                <button @click="openSpModal(taskItem)"
                  class="flex items-center gap-1.5 text-[11px] font-medium text-indigo-600
                         hover:text-indigo-700 hover:bg-indigo-50 border border-indigo-100
                         rounded-lg px-2.5 py-1.5 transition-colors">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
                  </svg>
                  {{ t('maintenance.sp_add_btn') }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer: all done banner + complete button -->
        <div class="px-5 pb-5 space-y-3">
          <Transition name="slide-down">
            <div v-if="allDone && tasks.length > 0"
              class="flex items-center gap-2 bg-emerald-50 border border-emerald-200 rounded-xl px-4 py-3">
              <svg class="w-4 h-4 text-emerald-600 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="text-sm font-medium text-emerald-700">{{ t('maintenance.task_all_done') }}</span>
            </div>
          </Transition>

          <button @click="auth.isAdmin ? openComplete() : null"
            :disabled="!auth.isAdmin || !allDone || tasks.length === 0"
            :title="!auth.isAdmin
              ? 'Faqat administrator yakunlay oladi'
              : (!allDone ? t('maintenance.repair_finish_hint') : '')"
            class="w-full py-3 text-sm font-semibold rounded-xl transition-all duration-200"
            :class="auth.isAdmin && allDone && tasks.length > 0
              ? 'text-white bg-emerald-600 hover:bg-emerald-700 shadow-sm hover:shadow-md cursor-pointer'
              : 'text-slate-400 bg-slate-100 cursor-not-allowed'">
            {{ t('maintenance.repair_finish') }}
          </button>
        </div>
      </div>
    </template>

    <!-- Spare Parts Modal -->
    <Transition name="modal">
      <div v-if="showSpModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[2px]" @click="showSpModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md flex flex-col max-h-[85vh]">

          <!-- Header -->
          <div class="px-5 pt-5 pb-3 border-b border-slate-100 flex-shrink-0">
            <div class="flex items-center justify-between">
              <h3 class="text-base font-bold text-slate-900">{{ t('maintenance.sp_modal_title') }}</h3>
              <button @click="showSpModal = false"
                class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 transition-colors">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
            <p class="text-xs text-slate-400 mt-0.5 truncate">{{ spModalTask?.title }}</p>
            <!-- Search -->
            <div class="relative mt-3">
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              <input v-model="spSearch" type="text" :placeholder="t('maintenance.sp_search_ph')"
                class="w-full pl-9 pr-4 py-2 text-sm border border-slate-200 rounded-xl bg-slate-50
                       focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all" />
            </div>
          </div>

          <!-- List -->
          <div class="flex-1 overflow-y-auto px-3 py-2">
            <div v-if="sparePartsLoading" class="p-6 text-center text-slate-400 text-sm">...</div>
            <div v-else-if="filteredSpareParts.length === 0"
              class="p-6 text-center text-slate-400 text-sm italic">
              {{ t('maintenance.sp_none') }}
            </div>
            <div v-else class="space-y-1">
              <div v-for="sp in filteredSpareParts" :key="sp.id"
                @click="selectSp(sp)"
                class="flex items-center justify-between px-3 py-2.5 rounded-xl cursor-pointer transition-colors"
                :class="selectedSp?.id === sp.id
                  ? 'bg-indigo-50 border border-indigo-200'
                  : 'hover:bg-slate-50 border border-transparent'">
                <div class="min-w-0">
                  <div class="text-sm font-medium text-slate-800 truncate">{{ sp.name }}</div>
                  <div class="text-xs text-slate-400 mt-0.5">
                    {{ t('maintenance.sp_available') }}:
                    <span :class="sp.quantity != null && sp.quantity <= 0 ? 'text-rose-500 font-semibold' : 'text-slate-600 font-semibold'">
                      {{ sp.quantity != null ? sp.quantity : '∞' }}
                      {{ sp.unit_data?.short_name || sp.unit_data?.name || '' }}
                    </span>
                  </div>
                </div>
                <svg v-if="selectedSp?.id === sp.id" class="w-4 h-4 text-indigo-600 flex-shrink-0 ml-2"
                  fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
            </div>
          </div>

          <!-- Quantity input (shows when part selected) -->
          <Transition name="slide-down">
            <div v-if="selectedSp" class="px-5 pb-4 pt-3 border-t border-slate-100 flex-shrink-0 space-y-3">
              <div class="bg-indigo-50 border border-indigo-100 rounded-xl px-3 py-2">
                <div class="text-xs text-indigo-400 font-medium">Tanlangan</div>
                <div class="text-sm font-semibold text-indigo-800 mt-0.5">{{ selectedSp.name }}</div>
                <div class="text-xs text-indigo-400 mt-0.5">
                  {{ t('maintenance.sp_available') }}: {{ selectedSp.quantity != null ? selectedSp.quantity : '∞' }}
                  {{ selectedSp.unit_data?.short_name || '' }}
                </div>
              </div>

              <div>
                <label class="block text-xs font-medium text-slate-600 mb-1.5">
                  {{ t('maintenance.sp_qty_label') }}
                  <span v-if="selectedSp.unit_data"> ({{ selectedSp.unit_data.short_name || selectedSp.unit_data.name }})</span>
                  *
                </label>
                <input v-model.number="spQuantity" type="number" min="0.001" step="0.001"
                  :placeholder="t('maintenance.sp_qty_ph')"
                  class="w-full text-sm border rounded-xl px-3 py-2 transition-all focus:outline-none focus:ring-2"
                  :class="spInsufficient
                    ? 'border-rose-300 bg-rose-50 focus:ring-rose-300'
                    : 'border-slate-200 focus:ring-indigo-300'" />
                <p v-if="spInsufficient" class="text-xs text-rose-600 mt-1 font-medium">
                  ⚠ {{ t('maintenance.sp_insufficient') }}.
                  {{ t('maintenance.sp_available') }}: {{ selectedSp.quantity }} {{ selectedSp.unit_data?.short_name || '' }}
                </p>
              </div>

              <!-- Notes / description -->
              <div>
                <label class="block text-xs font-medium text-slate-600 mb-1.5">
                  Izoh (ixtiyoriy)
                </label>
                <textarea v-model="spNotes" rows="2"
                  placeholder="Nima uchun ishlatildi, qayerga o'rnatildi..."
                  class="w-full text-sm border border-slate-200 rounded-xl px-3 py-2 resize-none
                         focus:outline-none focus:ring-2 focus:ring-indigo-300 transition-all"></textarea>
              </div>

              <div class="flex gap-2">
                <button @click="selectedSp = null; spQuantity = ''; spNotes = ''"
                  class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
                  {{ t('common.cancel') }}
                </button>
                <button @click="confirmAddSp"
                  :disabled="!spQuantity || spQuantity <= 0 || spInsufficient || spSaving"
                  class="flex-1 py-2 text-sm text-white bg-indigo-600 hover:bg-indigo-700
                         rounded-xl transition-colors disabled:opacity-40 disabled:cursor-not-allowed">
                  {{ spSaving ? '...' : t('maintenance.task_add_btn') }}
                </button>
              </div>
            </div>
          </Transition>

        </div>
      </div>
    </Transition>

    <!-- Complete Modal -->
    <Transition name="modal">
      <div v-if="showCompleteModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-[2px]" @click="showCompleteModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-sm p-6 space-y-4">
          <h3 class="text-base font-bold text-slate-900">{{ t('maintenance.complete_title') }}</h3>
          <p class="text-sm text-slate-500 -mt-2">{{ machine?.name }}</p>
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
            <button @click="showCompleteModal = false"
              class="flex-1 py-2 text-sm text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button @click="markComplete" :disabled="completeSaving"
              class="flex-1 py-2 text-sm text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl transition-colors disabled:opacity-60">
              {{ completeSaving ? t('common.saving') : t('maintenance.complete_btn') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useI18n } from '@/i18n'
import { useAuthStore } from '@/store/auth'
import { maintenanceApi, machinesApi, usersApi, warehouseApi } from '@/api'

import dayjs from 'dayjs'

const { t } = useI18n()
const toast = useToast()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const machineId = Number(route.params.machineId)

const loading = ref(true)
const saving = ref(false)
const machine = ref(null)
const schedule = ref(null)
const tasks = ref([])
const employees = ref([])

// ── Computed ──
const doneTasks = computed(() => tasks.value.filter(t => t.is_done).length)
const allDone = computed(() => tasks.value.length > 0 && doneTasks.value === tasks.value.length)

// ── Helpers ──
function formatDate(d) { return d ? dayjs(d).format('DD.MM.YYYY') : '—' }
function formatDateTime(d) { return d ? dayjs(d).format('DD.MM.YYYY HH:mm') : '—' }
function isDueDatePast(d) { return d && dayjs(d).isBefore(dayjs(), 'day') }

// ── Load ──
async function loadAll() {
  loading.value = true
  try {
    const requests = [
      machinesApi.get(machineId),
      maintenanceApi.get(machineId),
      maintenanceApi.tasks(machineId),
    ]
    if (auth.canWrite) {
      requests.push(usersApi.list({ page_size: 200, is_active: 'true' }))
    }
    const [machineRes, scheduleRes, tasksRes, empRes] = await Promise.all(requests)
    machine.value = machineRes.data
    schedule.value = scheduleRes.data
    tasks.value = tasksRes.data
    if (empRes) employees.value = empRes.data.results || empRes.data
  } catch {
    toast.error(t('toast.load_error'))
  } finally {
    loading.value = false
  }
}

// ── Add task form ──
const showAddForm = ref(false)
const formError = ref('')
const newTask = ref({ title: '', assignee: null, due_date: '' })

function resetForm() {
  newTask.value = { title: '', assignee: null, due_date: '' }
  formError.value = ''
}

async function addTask() {
  if (!newTask.value.title.trim()) {
    formError.value = t('toast.form_check')
    return
  }
  saving.value = true
  formError.value = ''
  try {
    const payload = {
      title: newTask.value.title.trim(),
      assignee: newTask.value.assignee || null,
      due_date: newTask.value.due_date || null,
    }
    const res = await maintenanceApi.addTask(machineId, payload)
    tasks.value.push(res.data)
    showAddForm.value = false
    resetForm()
    await refreshSchedule()
  } catch {
    toast.error(t('toast.error'))
  } finally {
    saving.value = false
  }
}

async function toggleTask(taskItem) {
  try {
    const res = await maintenanceApi.toggleTask(machineId, taskItem.id, { is_done: !taskItem.is_done })
    const idx = tasks.value.findIndex(t => t.id === taskItem.id)
    if (idx !== -1) tasks.value[idx] = res.data
    await refreshSchedule()
  } catch (e) {
    const msg = e.response?.data?.detail || e.response?.data?.message || t('toast.error')
    toast.error(msg, { timeout: 6000 })
  }
}

async function deleteTask(task) {
  try {
    await maintenanceApi.deleteTask(machineId, task.id)
    tasks.value = tasks.value.filter(t => t.id !== task.id)
    await refreshSchedule()
  } catch {
    toast.error(t('toast.error'))
  }
}

async function refreshSchedule() {
  try {
    const res = await maintenanceApi.get(machineId)
    schedule.value = res.data
  } catch { /* silent */ }
}

// ── Spare Parts Modal ──
const showSpModal = ref(false)
const spModalTask = ref(null)
const spSearch = ref('')
const sparePartsLoading = ref(false)
const allSpareParts = ref([])
const selectedSp = ref(null)
const spQuantity = ref('')
const spNotes = ref('')
const spSaving = ref(false)

const filteredSpareParts = computed(() => {
  const q = spSearch.value.toLowerCase()
  return allSpareParts.value.filter(sp =>
    !q || sp.name.toLowerCase().includes(q)
  )
})

const spInsufficient = computed(() => {
  if (!selectedSp.value || !spQuantity.value) return false
  const available = selectedSp.value.quantity
  if (available == null) return false
  return Number(spQuantity.value) > Number(available)
})

async function openSpModal(task) {
  spModalTask.value = task
  selectedSp.value = null
  spQuantity.value = ''
  spNotes.value = ''
  spSearch.value = ''
  showSpModal.value = true
  // Always reload filtered by current machine
  sparePartsLoading.value = true
  allSpareParts.value = []
  try {
    const res = await warehouseApi.list({ page_size: 500, machines: machineId })
    allSpareParts.value = res.data.results ?? res.data
  } catch {
    toast.error(t('toast.load_error'))
  } finally {
    sparePartsLoading.value = false
  }
}

function selectSp(sp) {
  selectedSp.value = sp
  spQuantity.value = ''
}

async function confirmAddSp() {
  if (!spQuantity.value || Number(spQuantity.value) <= 0 || spInsufficient.value) return
  spSaving.value = true
  try {
    const res = await maintenanceApi.addTaskSparePart(machineId, spModalTask.value.id, {
      spare_part: selectedSp.value.id,
      quantity_used: spQuantity.value,
      notes: spNotes.value,
    })
    const task = tasks.value.find(t => t.id === spModalTask.value.id)
    if (task) {
      if (!task.spare_parts_used) task.spare_parts_used = []
      task.spare_parts_used.push(res.data)
    }
    // Refresh spare parts list to show updated quantities
    allSpareParts.value = []
    selectedSp.value = null
    spQuantity.value = ''
    spNotes.value = ''
    showSpModal.value = false
  } catch (e) {
    toast.error(e.response?.data?.detail || t('toast.error'))
  } finally {
    spSaving.value = false
  }
}

async function removeTaskSparePart(task, usage) {
  try {
    await maintenanceApi.removeTaskSparePart(machineId, task.id, usage.id)
    const found = tasks.value.find(x => x.id === task.id)
    if (found) found.spare_parts_used = (found.spare_parts_used || []).filter(s => s.id !== usage.id)
  } catch {
    toast.error(t('toast.error'))
  }
}

// ── Complete modal ──
const showCompleteModal = ref(false)
const completeSaving = ref(false)
const completeForm = ref({ completion_date: '', notes: '' })

function openComplete() {
  completeForm.value = { completion_date: dayjs().format('YYYY-MM-DD'), notes: '' }
  showCompleteModal.value = true
}

async function markComplete() {
  if (!completeForm.value.completion_date) return
  completeSaving.value = true
  try {
    await maintenanceApi.complete(machineId, completeForm.value)
    toast.success(t('maintenance.complete_success'))
    showCompleteModal.value = false
    router.push('/maintenance')
  } catch (e) {
    const msg = e.response?.data?.detail || e.response?.data?.message || t('toast.error')
    toast.error(msg, { timeout: 8000 })
  } finally {
    completeSaving.value = false
  }
}

onMounted(loadAll)
</script>

<style scoped>
.card { @apply bg-white rounded-2xl border border-slate-200 shadow-sm; }

.info-block { @apply bg-slate-50 rounded-xl p-3; }
.info-label { @apply text-[10px] font-semibold text-slate-400 uppercase tracking-wide; }
.info-val   { @apply text-sm font-semibold text-slate-800 mt-0.5 truncate; }

/* ── Task row ── */
.task-row {
  @apply flex items-start gap-3 p-3 rounded-xl border transition-all duration-150;
  position: relative;
}
.task-row--pending { @apply bg-white border-slate-100 hover:border-slate-200 hover:shadow-sm; }
.task-row--done    { @apply bg-slate-50/60 border-slate-100; }

.task-check {
  @apply w-5 h-5 rounded-full border-2 flex items-center justify-center
         transition-all duration-200 flex-shrink-0 mt-0.5 cursor-pointer;
}
.task-check--pending { @apply border-slate-300 hover:border-blue-400 hover:bg-blue-50; }
.task-check--done    { @apply bg-emerald-500 border-emerald-500; }

/* ── Transitions ── */
.slide-down-enter-active { transition: all 0.2s ease; }
.slide-down-leave-active { transition: all 0.15s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-8px); }

.task-list-enter-active { transition: all 0.25s ease; }
.task-list-leave-active { transition: all 0.2s ease; }
.task-list-enter-from   { opacity: 0; transform: translateX(-12px); }
.task-list-leave-to     { opacity: 0; transform: translateX(12px); }

.modal-enter-active, .modal-leave-active { transition: opacity 0.2s; }
.modal-enter-from, .modal-leave-to       { opacity: 0; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.animate-fade-in { animation: fadeIn 0.25s ease; }
</style>
