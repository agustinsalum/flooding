<template>
  <div>
    <h1>Recorridos de evacuación</h1>
    <mapa tipo="recorrido" :data="this.data" :key="this.data"></mapa>
    <paginador
      tipo="recorrido"
      endpoint="recorridos-evacuacion"
      @change-data="getData"
    ></paginador>
  </div>
</template>
<script>
import Paginator from '../components/Paginator.vue'
import Mapa from './../components/Mapa.vue'

export default {
  components: {
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

  computed: {},
  methods: {
    getData(data) {
      this.data = data
    },
  },
}
</script>
