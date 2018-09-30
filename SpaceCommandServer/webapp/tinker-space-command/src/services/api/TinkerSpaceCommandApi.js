import {Rxios} from 'rxios'

const http = new Rxios({
  // all regular axios request configuration options are valid here
  // Check https://github.com/axios/axios#request-config
  baseURL: 'http://ess-master1.local:5000/api/v1'
})

export default {
  getSensors () {
    return http.get('/sensors')
  },

  getSensor (sensorId) {
    return http.get('/sensor/' + sensorId)
  },

  getSensorChannelDataQuery (sensorId, channelId, startDate, endDate) {
    return http.get(
      '/query/sensor/' + sensorId + '?channel=' + channelId +
      '&startDateTime=' + startDate + 'T00:00:00MST' +
      '&endDateTime=' + endDate + 'T00:00:00MST')
  },

  getSpaces () {
    return http.get('/spaces')
  },

  getSpace (spaceId) {
    return http.get('/space/' + spaceId)
  }
}
