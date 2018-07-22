import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '@/components/Dashboard'
import Sensors from '@/components/Sensors'
import Sensor from '@/components/Sensor'
import Locations from '@/components/Locations'
import Location from '@/components/Location'

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
      path: '/locations',
      name: 'Locations',
      component: Locations
    },
    {
      path: '/location/:id',
      name: 'Location',
      component: Location
    }
  ]
})
