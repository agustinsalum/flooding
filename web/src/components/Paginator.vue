<template>
  <div v-if="loading">
    <Preloader color="blue" scale="0.6" />
  </div>
  <div v-else>
    <div
      class="flex-center column w-full"
      v-on:change="$emit('changeData', this.data)"
    >
      <div class="col-md-8">
        <div class="input-group mb-3">
          <input
            type="text"
            class="input2"
            placeholder="Buscar por nombre"
            v-model="name"
          />
          <div class="flex-center">
            <button
              class="m-4 p-8"
              type="button"
              @click=";(page = 1), retrieveData()"
            >
              Buscar
            </button>
            <button class="m-4 p-8" type="button" @click="reset()">
              Limpiar
            </button>
          </div>
        </div>
      </div>

      <div v-if="ok === true" class="col-md-12 pading">
        <div class="mb-3">
          Items por Página:
          <select
            class="select2"
            v-model="pageSize"
            @change="handlePageSizeChange($event)"
          >
            <option v-for="size in pageSizes" :key="size" :value="size">
              {{ size }}
            </option>
          </select>
        </div>

        <div v-if="ok === true" class="col-md-6">
          <h4>Páginas:</h4>
          <ul class="flexin">
            <li
              class="list-group-item"
              :class="{ active: index + 1 == currentIndex }"
              v-for="(page, index) in pages"
              :key="index"
              @click="handlePageChange(index + 1)"
            >
              <p>
                {{ index + 1 }}
              </p>
            </li>
          </ul>

          <div class="flex-center">
            <button
              class="m-4 p-8"
              @click="handlePageChange(parseInt(currentIndex) - 1)"
            >
              Anterior
            </button>
            <button
              class="m-4 p-8"
              @click="handlePageChange(parseInt(currentIndex) + 1)"
            >
              Siguiente
            </button>
          </div>
        </div>
      </div>

      <div v-if="ok === true" class="w-full">
        <h4>Lista:</h4>
        <ul class="list-group" id="tutorials-list">
          <li
            class="list-group-item"
            v-for="(data, index) in data"
            :key="index"
          >
            <div v-if="tipo !== 'punto'">
              <div class="flex-center justify-between">
                <div>
                  <router-link
                    :to="{
                      name: `${tipo}`,
                      params: { id: data.id },
                    }"
                  >
                    {{ data.nombre }}
                  </router-link>
                </div>
                <div>
                  <button>
                    <router-link
                      :to="{
                        name: `${tipo}`,
                        params: { id: data.id },
                      }"
                    >
                      Ver
                    </router-link>
                  </button>
                </div>
              </div>
            </div>

            <div v-else>
              {{ data.nombre }}
            </div>
          </li>
        </ul>
      </div>

      <div style="padding: 4rem" v-if="ok === false">
        {{ error }}

        <div style="padding: 4rem">
          <button
            class="btn btn-outline-secondary"
            type="button"
            @click="reset()"
          >
            Limpiar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Preloader from './../components/Preloader.vue'
import DataService from '../services/DataService'

export default {
  props: {
    endpoint: String,
    tipo: String,
  },
  components: {
    Preloader,
  },
  data() {
    return {
      zoom: 2,
      loading: true,
      // paginacion
      ok: true,
      error: '',
      pages: 3,
      data: [],
      currentIndex: -1,
      name: '',
      page: 1,
      count: 0,
      pageSize: 3,
      pageSizes: [1, 3, 6, 9],
    }
  },
  async created() {
    this.retrieveData()
  },

  computed: {},
  methods: {
    // metodos paginacion

    reset() {
      this.name = ''
      this.retrieveData()
    },

    getRequestParams(name, page, pageSize) {
      let params = {}

      if (name) {
        params['name'] = name
      }

      if (page) {
        params['page'] = page
      }

      if (pageSize) {
        params['size'] = pageSize
      }

      return params
    },

    retrieveData() {
      const params = this.getRequestParams(this.name, this.page, this.pageSize)

      DataService.getAll(`${this.endpoint}`, params)
        .then((response) => {
          const { data, totalItems, ok, error, pagina } = response.data
          console.log(ok)
          if (ok === 'true') {
            this.currentIndex = pagina
            this.ok = true
            this.data = data
            this.count = totalItems
            let pags = Math.ceil(response.data.totalItems / this.pageSize)

            pags === 0 ? (this.pages = 1) : (this.pages = pags)

            this.loading = false
            console.log(response.data)
            this.$emit('changeData', this.data)
          } else {
            this.ok = false
            this.error = error
          }
        })
        .catch((e) => {
          console.log(e)
        })
    },

    handlePageChange(value) {
      if (value <= this.pages) this.page = value
      this.retrieveData()
    },

    handlePageSizeChange(event) {
      this.pageSize = event.target.value
      this.page = 1
      this.retrieveData()
    },
  },
}
</script>
