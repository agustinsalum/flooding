import http from '../../http-common'

class DataService {
  getAll(endpoint, params) {
    return http.get(`${endpoint}`, { params })
  }

  // other CRUD methods
}

export default new DataService()
