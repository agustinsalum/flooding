<template>
  <div>
    <h1>Puntos de encuentro</h1>
    <mapa tipo="punto" :data="this.data" :key="this.data"></mapa>
    <paginador
      tipo="punto"
      endpoint="puntos-encuentro"
      @change-data="getData"
    ></paginador>
  </div>
</template>
<script>
// import Preloader from './../components/Preloader.vue'
import Mapa from './../components/Mapa.vue'
import Paginator from '../components/Paginator.vue'

export default {
  components: {
    // Preloader,
    mapa: Mapa,
    paginador: Paginator,
  },
  props: {},
  data() {
    return {
      ok: true,
      error: '',
      data: [],
    }
  },
  async created() {},

  computed: {},
  methods: {
    getData(data) {
      this.loading = false
      this.data = data
    },
  },
}
</script>
