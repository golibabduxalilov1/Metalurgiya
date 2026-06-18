import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { public: true, layout: 'auth' }
  },
  {
    path: '/',
    component: () => import('@/layouts/AppLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue'),
        meta: { title: 'Главная', icon: 'home' }
      },
      // Machines
      {
        path: 'machines',
        name: 'Machines',
        component: () => import('@/views/machines/MachineListView.vue'),
        meta: { title: 'Реестр станков', icon: 'cpu-chip', section: 'machines' }
      },
      {
        path: 'machines/new',
        name: 'MachineCreate',
        component: () => import('@/views/machines/MachineFormView.vue'),
        meta: { title: 'Добавить станок', roles: ['admin', 'master'], section: 'machines' }
      },
      {
        path: 'machines/:id',
        name: 'MachineDetail',
        component: () => import('@/views/machines/MachineDetailView.vue'),
        meta: { title: 'Карточка станка', section: 'machines' }
      },
      {
        path: 'machines/:id/edit',
        name: 'MachineEdit',
        component: () => import('@/views/machines/MachineFormView.vue'),
        meta: { title: 'Редактировать станок', roles: ['admin', 'master'], section: 'machines' }
      },
      // Employees
      {
        path: 'employees',
        name: 'Employees',
        component: () => import('@/views/EmployeesView.vue'),
        meta: { title: 'Сотрудники', icon: 'users', roles: ['admin', 'master'], section: 'employees' }
      },
      // Directories (Admin only)
      {
        path: 'directories',
        name: 'Directories',
        component: () => import('@/views/DirectoriesView.vue'),
        meta: { title: 'Справочники', icon: 'book-open', roles: ['admin'], section: 'directories' }
      },
      // Users
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/UsersView.vue'),
        meta: { title: 'Пользователи', icon: 'user-group', roles: ['admin'], section: 'users' }
      },
      // Audit log
      {
        path: 'audit',
        name: 'Audit',
        component: () => import('@/views/AuditView.vue'),
        meta: { title: 'Журнал аудита', icon: 'document-text', roles: ['admin'], section: 'audit' }
      },
      // Warehouse (Склад)
      {
        path: 'sklad',
        name: 'Sklad',
        component: () => import('@/views/SkaldView.vue'),
        meta: { title: 'Склад', icon: 'cube', section: 'sklad' }
      },
      // Maintenance (ТО)
      {
        path: 'maintenance',
        name: 'Maintenance',
        component: () => import('@/views/MaintenanceView.vue'),
        meta: { title: 'Техническое обслуживание (ТО)', icon: 'wrench', roles: ['admin'], section: 'maintenance' }
      },
      // Profile
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/ProfileView.vue'),
        meta: { title: 'Мой профиль' }
      },
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { public: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0 }
  }
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()

  // Initialize auth state on first load
  if (!auth.initialized) {
    await auth.fetchMe()
  }

  // Public routes
  if (to.meta.public) {
    if (auth.isAuthenticated && to.name === 'Login') {
      return next('/')
    }
    return next()
  }

  // Require authentication
  if (!auth.isAuthenticated) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }

  // Role-based access — bypassed if section is explicitly granted via allowed_sections
  if (to.meta.roles && !auth.hasRole(...to.meta.roles)) {
    const explicitlyGranted = to.meta.section &&
      auth.user?.allowed_sections?.includes(to.meta.section)
    if (!explicitlyGranted) {
      return next('/dashboard')
    }
  }

  // Section-based access: when allowed_sections is set, restrict to listed sections only
  if (to.meta.section) {
    const sections = auth.user?.allowed_sections
    if (sections && !sections.includes(to.meta.section)) {
      return next('/dashboard')
    }
  }

  next()
})

export default router
