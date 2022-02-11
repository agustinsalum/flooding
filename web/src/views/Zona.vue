<template>
  <div v-if="loading">
    <Preloader color="blue" scale="0.6" />
  </div>
  <div
    v-else
    style="display: flex; flex-direction: column; align-items: center"
  >
    <h1>Zona {{ data.atributos.nombre }}</h1>
    <mapa tipo="zona" :data="this.data.atributos" :key="this.data"></mapa>

    <ul style="width: 100%">
      <hr />
      Nombre
      <li>
        {{ data.atributos.nombre }}
      </li>

      <!-- Estado
      <li>
        {{ data.atributos.estado }}
      </li> -->

      Color
      <li style="display: flex; justify-content: space-between">
        <div>
          {{ data.atributos.color }}
        </div>
        <div style="width: 1rem; height: 1rem" ref="root"></div>
      </li>
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

  updated() {
    this.$refs.root.style.backgroundColor = this.data.atributos.color
  },

  data() {
    return {
      zoom: 2,
      data: [],
      zonas: [],
      loading: true,
    }
  },
  async created() {
    let id = this.$route.path.split('/')[2]
    console.log(id)

    const response = await fetch(
      `${process.env.VUE_APP_ROOT}api/zonas-inundables/${id}`
    )
    let data = {}
    data = await response.json()
    if (data) {
      this.loading = false
    }
    this.data = data
    this.zonas = this.zonas.push(data.atributos)
    // console.log(this.$refs.root)
  },

  computed: {},
  methods: {},
}
</script>
