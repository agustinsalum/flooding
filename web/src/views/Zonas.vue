<template>
  <div>
    <h1>Zonas de inundación</h1>
    <mapa tipo="zona" :data="this.data" :key="this.data"></mapa>

    <paginador
      tipo="zona"
      endpoint="zonas"
      @change-data="getData"
    ></paginador>
  </div>
</template>
<script>
import Mapa from './../components/Mapa.vue'
import Paginator from '../components/Paginator.vue'

export default {
  components: {
    mapa: Mapa,
    paginador: Paginator,
  },
  props: {},
  data() {
    return {
      zoom: 2,
      ok: true,
      error: '',
      data: [],
    }
  },

  computed: {},
  methods: {
    getData(data) {
      this.data = data
    },
  },
}
</script>
