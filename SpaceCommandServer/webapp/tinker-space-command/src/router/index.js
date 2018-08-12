import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '@/components/Dashboard'
import Sensors from '@/components/Sensors'
import Sensor from '@/components/Sensor'
import Spaces from '@/components/Spaces'
import Space from '@/components/Space'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/sensors',
      name: 'Sensors',
      component: Sensors
    },
    {
      path: '/sensor/:id',
      name: 'Sensor',
      component: Sensor
    },
    {
      path: '/spaces',
      name: 'Spaces',
      component: Spaces
    },
    {
      path: '/space/:id',
      name: 'Space',
      component: Space
    }
  ]
})
