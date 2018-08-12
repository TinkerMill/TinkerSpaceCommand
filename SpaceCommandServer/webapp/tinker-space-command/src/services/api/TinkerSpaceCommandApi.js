import {Rxios} from 'rxios'

const http = new Rxios({
  // all regular axios request configuration options are valid here
  // Check https://github.com/axios/axios#request-config
  baseUrl: 'http://ess-master1.local:5000/api/v1'
})

export default {
  getSensors () {
    console.log('Calling getSensors yada')
    return http.get('http://ess-master1.local:5000/api/v1/sensors')
  },

  getSensor (sensorId) {
    console.log('Calling getSensor yada')
    return http.get('http://ess-master1.local:5000/api/v1/sensor/' + sensorId)
  },

  getSpaces () {
    console.log('Calling getSpaces yada')
    return http.get('http://ess-master1.local:5000/api/v1/spaces')
  },

  getSpace (spaceId) {
    console.log('Calling getSpace yada')
    return http.get('http://ess-master1.local:5000/api/v1/space/' + spaceId)
  }
}
