import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles.css'
// Los estilos para la denuncia estan aparte
import './estilo_denuncia.css'
import './map.css'

createApp(App).use(router).mount('#app')
