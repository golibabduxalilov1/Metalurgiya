<template>
  <div class="app-layout">

    <!-- Mobile backdrop -->
    <Transition name="fade">
      <div v-if="mobileMenuOpen"
        class="fixed inset-0 bg-black/40 backdrop-blur-[2px] z-30 lg:hidden cursor-pointer"
        @click="mobileMenuOpen = false">
      </div>
    </Transition>

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed top-0 left-0 h-full z-40 flex flex-col bg-white border-r border-slate-100',
        'w-[260px] lg:transition-[width] lg:duration-300',
        sidebarCollapsed ? 'lg:w-[72px]' : 'lg:w-[260px]',
        mobileMenuOpen ? 'translate-x-0 transition-transform duration-300' : '-translate-x-full transition-transform duration-300 lg:translate-x-0 lg:transition-none',
      ]"
    >
      <!-- Logo -->
      <RouterLink to="/dashboard" class="flex justify-center items-center px-4 py-5 border-b border-slate-100">
        <Transition name="fade">
          <img v-if="sidebarShowContent" src="@/assets/logo.svg" alt="Logo" class="h-8 w-auto" />
          <img v-else src="@/assets/logo.svg" alt="Logo" class="h-7 w-7 object-contain" />
        </Transition>
      </RouterLink>

      <!-- Navigation -->
      <nav class="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
        <!-- Main -->
        <div v-if="sidebarShowContent" class="px-3 mb-1.5">
          <span class="text-[10px] font-semibold uppercase tracking-widest">{{ t('nav.main') }}</span>
        </div>
        <NavItem v-for="item in mainNavItems" :key="item.name"
          :item="item" :collapsed="sidebarCollapsed && !mobileMenuOpen" />

        <!-- Management -->
        <template v-if="managementNavItems.length > 0">
          <div v-if="sidebarShowContent" class="px-3 mt-5 mb-1.5">
            <span class="text-[10px] font-semibold  uppercase tracking-widest">{{ t('nav.management') }}</span>
          </div>
          <div v-if="!sidebarShowContent" class="border-t border-slate-100 my-2 mx-1"></div>
          <NavItem v-for="item in managementNavItems" :key="item.name"
            :item="item" :collapsed="sidebarCollapsed && !mobileMenuOpen" />
        </template>

        <!-- Admin / Extended access -->
        <template v-if="adminNavItems.length > 0">
          <div v-if="sidebarShowContent" class="px-3 mt-5 mb-1.5">
            <span class="text-[10px] font-semibold  uppercase tracking-widest">{{ t('nav.administration') }}</span>
          </div>
          <div v-if="!sidebarShowContent" class="border-t border-slate-100 my-2 mx-1"></div>
          <NavItem v-for="item in adminNavItems" :key="item.name"
            :item="item" :collapsed="sidebarCollapsed && !mobileMenuOpen" />
        </template>
      </nav>

      <!-- User section -->
      <div class="border-t border-slate-100 p-3 space-y-1">
        <RouterLink to="/profile"
          class="flex items-center gap-3 p-2 rounded-xl hover:bg-slate-50 transition-colors group cursor-pointer">
          <div class="relative flex-shrink-0">
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center">
              <span class="text-white text-xs font-bold select-none">{{ userInitials }}</span>
            </div>
            <span class="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-emerald-400 border-2 border-white"></span>
          </div>
          <Transition name="fade">
            <div v-if="sidebarShowContent" class="overflow-hidden flex-1 min-w-0">
              <div class="text-slate-800 text-sm font-semibold truncate group-hover:text-indigo-600 transition-colors">{{ auth.userFullName }}</div>
              <div class="text-slate-400 text-xs truncate">{{ auth.userRole }}</div>
            </div>
          </Transition>
        </RouterLink>
        <button v-if="sidebarShowContent"
          @click="auth.logout"
          class="w-full flex items-center gap-2 px-2 py-1.5 text-slate-400 hover:text-rose-500
                 hover:bg-rose-50 rounded-lg text-sm transition-colors cursor-pointer">
          <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          {{ t('nav.logout') }}
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <div class="flex-1 min-w-0 flex flex-col min-h-screen transition-all duration-300 ml-0"
      :class="sidebarCollapsed ? 'lg:ml-[72px]' : 'lg:ml-[260px]'">

      <!-- Top bar -->
      <header class="fixed top-0 left-0 right-0 z-30 h-16 bg-white/95 backdrop-blur-sm border-b border-slate-100
        flex items-center px-4 lg:px-6 gap-3 shadow-[0_1px_8px_rgba(15,23,42,0.06)] transition-all duration-300"
        :class="sidebarCollapsed ? 'lg:left-[72px]' : 'lg:left-[260px]'">

        <!-- Toggle sidebar / hamburger -->
        <button @click="toggleMenu"
          class="lg:hidden p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors cursor-pointer flex-shrink-0">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <!-- Breadcrumb (hidden on mobile) -->
        <div class="hidden sm:flex items-center gap-1.5 text-sm min-w-0">
          <span class="text-slate-400 flex-shrink-0">{{ t('nav.home') }}</span>
          <svg class="w-3.5 h-3.5 text-slate-300 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
          <span class="text-slate-700 font-medium truncate">{{ currentPageTitle }}</span>
        </div>

        <div class="flex-1"></div>

        <!-- Role badge (hidden on mobile) -->
        <div class="hidden sm:block" :class="roleBadgeClass">{{ auth.userRole }}</div>

        <!-- Notifications -->
        <div class="relative" ref="notifRef">
          <button @click="notifOpen = !notifOpen"
            class="relative p-2 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors cursor-pointer flex-shrink-0">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <span v-if="maintenanceBadgeCount > 0"
              class="absolute top-1 right-1 min-w-[16px] h-4 px-0.5 rounded-full text-[10px] font-bold
                     flex items-center justify-center leading-none
                     text-white pointer-events-none"
              :class="maintenanceAlerts.overdue_count > 0 ? 'bg-rose-500' : 'bg-amber-500'">
              {{ maintenanceBadgeCount > 99 ? '99+' : maintenanceBadgeCount }}
            </span>
          </button>

          <!-- Dropdown -->
          <Transition name="notif-drop">
            <div v-if="notifOpen"
              class="absolute right-0 top-full mt-2 w-72 bg-white rounded-2xl border border-slate-200
                     shadow-xl shadow-slate-200/60 z-50 overflow-hidden">
              <div class="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
                <span class="text-sm font-semibold text-slate-800">{{ t('nav.notifications') }}</span>
                <span v-if="maintenanceBadgeCount > 0"
                  class="text-xs font-bold px-2 py-0.5 rounded-full"
                  :class="maintenanceAlerts.overdue_count > 0 ? 'bg-rose-100 text-rose-600' : 'bg-amber-100 text-amber-600'">
                  {{ maintenanceBadgeCount }}
                </span>
              </div>

              <div v-if="maintenanceBadgeCount === 0 && maintenanceAlerts.warning_count === 0"
                class="px-4 py-6 text-center text-slate-400 text-sm">
                {{ t('nav.no_notifications') }}
              </div>

              <div v-else class="divide-y divide-slate-50">
                <RouterLink v-if="maintenanceAlerts.overdue_count > 0" to="/maintenance"
                  @click="notifOpen = false"
                  class="flex items-center gap-3 px-4 py-3 hover:bg-rose-50 transition-colors group">
                  <span class="w-8 h-8 rounded-xl bg-rose-100 flex items-center justify-center flex-shrink-0">
                    <svg class="w-4 h-4 text-rose-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                  </span>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-semibold text-rose-700">{{ t('maintenance.alert_overdue') }}</p>
                    <p class="text-xs text-slate-500">{{ maintenanceAlerts.overdue_count }} {{ t('maintenance.alert_banner_overdue') }}</p>
                  </div>
                  <svg class="w-4 h-4 text-slate-300 group-hover:text-rose-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
                  </svg>
                </RouterLink>

                <RouterLink v-if="maintenanceAlerts.critical_count > 0" to="/maintenance"
                  @click="notifOpen = false"
                  class="flex items-center gap-3 px-4 py-3 hover:bg-amber-50 transition-colors group">
                  <span class="w-8 h-8 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
                    <svg class="w-4 h-4 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                  </span>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-semibold text-amber-700">{{ t('maintenance.alert_critical') }}</p>
                    <p class="text-xs text-slate-500">{{ maintenanceAlerts.critical_count }} {{ t('maintenance.alert_banner_critical') }}</p>
                  </div>
                  <svg class="w-4 h-4 text-slate-300 group-hover:text-amber-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
                  </svg>
                </RouterLink>

                <RouterLink v-if="maintenanceAlerts.warning_count > 0" to="/maintenance"
                  @click="notifOpen = false"
                  class="flex items-center gap-3 px-4 py-3 hover:bg-yellow-50 transition-colors group">
                  <span class="w-8 h-8 rounded-xl bg-yellow-100 flex items-center justify-center flex-shrink-0">
                    <svg class="w-4 h-4 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                    </svg>
                  </span>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-semibold text-yellow-700">{{ t('maintenance.alert_warning') }}</p>
                    <p class="text-xs text-slate-500">{{ maintenanceAlerts.warning_count }} {{ t('maintenance.alert_banner_warning') }}</p>
                  </div>
                  <svg class="w-4 h-4 text-slate-300 group-hover:text-yellow-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
                  </svg>
                </RouterLink>
              </div>

              <div v-if="maintenanceBadgeCount > 0" class="px-4 py-2.5 border-t border-slate-100 bg-slate-50">
                <RouterLink to="/maintenance" @click="notifOpen = false"
                  class="text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors">
                  {{ t('maintenance.alert_banner_link') }} →
                </RouterLink>
              </div>
            </div>
          </Transition>
        </div>

        <!-- User avatar -->
        <RouterLink to="/profile"
          class="flex items-center gap-2 sm:gap-2.5 sm:pl-2 sm:pr-3 py-1.5 sm:rounded-xl hover:bg-slate-100 transition-colors cursor-pointer">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 flex items-center justify-center flex-shrink-0">
            <span class="text-white text-xs font-bold select-none">{{ userInitials }}</span>
          </div>
          <span class="text-sm font-medium text-slate-700 hidden md:block">{{ auth.userFullName }}</span>
        </RouterLink>
      </header>

      <!-- Page content -->
      <main class="flex-1 pt-16">
        <div class="p-3 sm:p-4 md:p-6">
          <RouterView v-slot="{ Component, route }">
            <Transition name="fade" mode="out-in">
              <component :is="Component" :key="route.path" />
            </Transition>
          </RouterView>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { RouterView, RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { useI18n } from '@/i18n'
import NavItem from '@/components/common/NavItem.vue'
import { maintenanceApi } from '@/api'

const auth = useAuthStore()
const { t } = useI18n()
const route = useRoute()
const sidebarCollapsed = ref(false)
const mobileMenuOpen = ref(false)

const maintenanceAlerts = ref({ overdue_count: 0, critical_count: 0, warning_count: 0, total: 0 })
const notifOpen = ref(false)
const notifRef = ref(null)

function handleOutsideClick(e) {
  if (notifRef.value && !notifRef.value.contains(e.target)) {
    notifOpen.value = false
  }
}

onUnmounted(() => document.removeEventListener('click', handleOutsideClick))

async function loadMaintenanceAlerts() {
  try {
    const res = await maintenanceApi.alerts()
    maintenanceAlerts.value = res.data
  } catch {
    // silently fail
  }
}

onMounted(() => {
  if (auth.isAdmin) loadMaintenanceAlerts()
  document.addEventListener('click', handleOutsideClick)
})

watch(() => route.path, () => {
  mobileMenuOpen.value = false
  if (auth.isAdmin && (route.path === '/dashboard' || route.path === '/machines' || route.path === '/maintenance')) {
    loadMaintenanceAlerts()
  }
})

const sidebarShowContent = computed(() => !sidebarCollapsed.value || mobileMenuOpen.value)

function toggleMenu() {
  if (window.innerWidth < 1024) {
    mobileMenuOpen.value = !mobileMenuOpen.value
  } else {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
}


const userInitials = computed(() => {
  const name = auth.userFullName
  if (!name) return '?'
  const parts = name.split(' ')
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase()
  return name[0].toUpperCase()
})

const routeTitleMap = {
  Dashboard: 'nav.home',
  Machines: 'nav.machines',
  MachineCreate: 'nav.machine_add',
  MachineDetail: 'nav.machine_card',
  MachineEdit: 'nav.machine_edit',
  Employees: 'nav.employees',
  Sklad: 'nav.sklad',
  Directories: 'nav.directories',
  Users: 'nav.users',
  Audit: 'nav.audit',
  Maintenance: 'nav.maintenance',
  Profile: 'nav.profile',
}

const maintenanceBadgeCount = computed(() => {
  return maintenanceAlerts.value.overdue_count + maintenanceAlerts.value.critical_count
})

const currentPageTitle = computed(() => {
  const key = routeTitleMap[route.name]
  return key ? t(key) : (route.meta?.title || '')
})

const roleBadgeClass = computed(() => {
  const role = auth.user?.role
  if (role === 'admin') return 'role-admin'
  if (role === 'master') return 'role-master'
  return 'role-operator'
})

// Returns true if the current user can access a section.
// When allowed_sections is null → use role-based defaults.
// When allowed_sections is set → only sections explicitly listed are accessible.
function canAccess(section, baseRoles) {
  const allowedSections = auth.user?.allowed_sections
  if (allowedSections) {
    return allowedSections.includes(section)
  }
  return baseRoles.includes(auth.user?.role)
}

const mainNavItems = computed(() => {
  const items = [{ name: 'Dashboard', label: t('nav.home'), icon: 'home', to: '/dashboard' }]
  if (canAccess('machines', ['admin', 'master', 'operator'])) {
    items.push({ name: 'Machines', label: t('nav.machines'), icon: 'cog', to: '/machines' })
  }
  return items
})

const managementNavItems = computed(() => {
  const items = []
  if (canAccess('employees', ['admin', 'master'])) {
    items.push({ name: 'Employees', label: t('nav.employees'), icon: 'users', to: '/employees' })
  }
  if (canAccess('sklad', ['admin', 'master'])) {
    items.push({ name: 'Sklad', label: t('nav.sklad'), icon: 'cube', to: '/sklad' })
  }
  return items
})

const adminNavItems = computed(() => {
  const items = []
  if (canAccess('maintenance', ['admin'])) {
    items.push({
      name: 'Maintenance',
      label: t('nav.maintenance'),
      icon: 'wrench',
      to: '/maintenance',
      badge: maintenanceBadgeCount.value || undefined,
      badgeColor: maintenanceAlerts.value.overdue_count > 0 ? 'rose' : 'amber',
    })
  }
  if (canAccess('directories', ['admin'])) {
    items.push({ name: 'Directories', label: t('nav.directories'), icon: 'book', to: '/directories' })
  }
  if (canAccess('users', ['admin'])) {
    items.push({ name: 'Users', label: t('nav.users'), icon: 'user-group', to: '/users' })
  }
  if (canAccess('audit', ['admin'])) {
    items.push({ name: 'Audit', label: t('nav.audit'), icon: 'document', to: '/audit' })
  }
  return items
})
</script>

<style scoped>
.notif-drop-enter-active { transition: opacity 0.15s, transform 0.15s; }
.notif-drop-leave-active { transition: opacity 0.1s, transform 0.1s; }
.notif-drop-enter-from  { opacity: 0; transform: translateY(-6px) scale(0.97); }
.notif-drop-leave-to    { opacity: 0; transform: translateY(-4px) scale(0.98); }
</style>
