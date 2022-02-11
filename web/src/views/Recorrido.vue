<template>
  <div v-if="loading">
    <Preloader color="blue" scale="0.6" />
  </div>
  <div
    v-else
    style="display: flex; flex-direction: column; align-items: center"
  >
    <h1>Recorrido {{ data.atributos.nombre }}</h1>
    <mapa tipo="recorrido" :data="this.data.atributos" :key="this.data"></mapa>

    <ul style="width: 100%">
      <hr />
      Nombre
      <li>
        {{ data.atributos.nombre }}
      </li>
      Descripción
      <li>
        {{ data.atributos.descripcion }}
      </li>

      <!-- Estado
      <li>
        {{ data.atributos.estado }}
      </li> -->
      <hr />
    </ul>
  </div>
</template>
<script>
import Mapa from './../components/Mapa.vue'
import Preloader from './../components/Preloader.vue'

export default {
  components: {
    mapa: Mapa,
    Preloader,
  },

  data() {
    return {
      zoom: 2,
      data: null,
      loading: true,
      recorridos: [],
    }
  },
  async created() {
    let id = this.$route.path.split('/')[2]
    console.log(id)

    const response = await fetch(
      `${process.env.VUE_APP_ROOT}api/recorrido/${id}`
    )
    let data = {}
    data = await response.json()
    if (data) {
      this.loading = false
    }
    // console.log(data)
    this.data = data
    this.recorridos = this.recorridos.push(data.atributos)
  },

  computed: {},
  methods: {
    log(a) {
      console.log(a)
    },
  },
}
</script>
