<!-- vue.js se compone de <template></template> ; <script></script> ; <style></style> -->

<!-- <template> COMIENZO </template> -->

<template>
  <div>
    <div class="container">
      <div class="row">
        <div tabindex="30">
          <div class="col-sm-12">
            <div class="mensaje_exito" v-if="mensaje_exito !== ''">
              <p style="white-space: pre-line">{{ mensaje_exito }}</p>
            </div>

            <h2><b>Realizá tu Denuncia</b></h2>
            <h4>
              <p>
                Debe especificar dónde está sucediendo el hecho que está
                denunciando. Una vez enviado el formulario quedará pendiente de
                aprobación por parte del personal.
              </p>
            </h4>
          </div>
        </div>

        <div tabindex="31">
          <div class="col-sm-12 text-center">
            <figure>
              <img
                class="w-full"
                style="max-width: 600px"
                src="../assets/denuncia_1.jpg"
                alt="Imagen de un escritorio, con una hoja para tomar nota de la denuncia."
              />
            </figure>
          </div>
        </div>
      </div>
      <h2><b>Formulario de denuncia</b></h2>

      <!-- oninvalid y onchange son adicionales del required. onchange para desaparecer el mensaje -->
      <!-- V-Model: Permite crear un modelo de datos bidireccional entre un elemento HTML concreto y una variable de Vue -->

      <form id="formulario">
        <label for="titulo">Titulo </label>
        <input
          class="input"
          type="text"
          placeholder="Escribe el titulo"
          required
          oninvalid="this.setCustomValidity('Ingrese un título')"
          onchange="this.setCustomValidity('')"
          v-model="denuncia.titulo"
        />

        <label for="categoria">Categoria </label>
        <select v-model="denuncia.categoria" class="input">
          <option value="Alcantarilla Tapada">Alcantarilla tapada</option>
          <option value="Basural">Basural</option>
          <option value="Desperfecto natural">Desperfecto natural</option>
        </select>

        <label for="descripcion">Descripción </label>
        <textarea
          class="input"
          for="descripcion"
          placeholder="describe brevemente en menos de 600 carácteres"
          maxlength="600"
          required
          oninvalid="this.setCustomValidity('Ingrese una descripcion')"
          onchange="this.setCustomValidity('')"
          v-model="denuncia.descripcion"
        ></textarea>

        <label for="mapa_simple">Ingrese el lugar en el mapa </label>

        <!-- Mapa component -->
        <mapa @marcar-punto="marcar" tipo="denuncia"></mapa>

        <!-- Esto creo que no es necesiario -->
        <input
          type="text"
          id="corx"
          name="corx"
          style="display: none"
          v-model="denuncia.latitud"
        />
        <input
          type="text"
          id="cory"
          name="cory"
          style="display: none"
          v-model="denuncia.longitud"
        />

        <label for="nombre">Nombre </label>
        <input
          class="input"
          type="text"
          placeholder="Ej: Juan"
          required
          oninvalid="this.setCustomValidity('Ingrese el nombre')"
          onchange="this.setCustomValidity('')"
          v-model="denuncia.nombre"
        />

        <label class="input" for="apellido">Apellido </label>
        <input
          class="input"
          type="text"
          placeholder="Ej: Perez"
          required
          oninvalid="this.setCustomValidity('Ingrese el apellido')"
          onchange="this.setCustomValidity('')"
          v-model="denuncia.apellido"
        />

        <label for="telefono">Telefono </label>
        <input
          class="input"
          type="text"
          placeholder="Codigo de area + Telefono"
          required
          oninvalid="this.setCustomValidity('Ingrese el telefono')"
          onchange="this.setCustomValidity('')"
          v-model="denuncia.telefono"
        />

        <label for="email">Email</label>
        <input
          class="input"
          type="email"
          placeholder="correo@dominio.com"
          required
          oninvalid="this.setCustomValidity('Ingrese el correo')"
          onchange="this.setCustomValidity('')"
          v-model="denuncia.email"
        />

        <div class="mensaje_error" v-if="mensaje !== ''">
          <p style="white-space: pre-line">{{ mensaje }}</p>
        </div>

        <!-- <input type="submit" name="enviar" value="enviar datos" /> -->
        <button class="boton" type="button" @click="crear()">Guardar</button>
      </form>
    </div>
  </div>
</template>

<!-- <template> FINALIZO </template> -->

<!-- <script> COMIENZA </script> -->

<script>
import Mapa from './../components/Mapa.vue'

// Mi mapa en el componente
export default {
  name: 'Denuncia',
  components: {
    mapa: Mapa,
  },

  // Metodos

  methods: {
    marcar(e) {
      console.log(e)
      this.denuncia.latitud = e.latitud
      this.denuncia.longitud = e.longitud
    },
    funcion_exitosa(mensaje) {
      document.getElementById('formulario').reset()
      this.denuncia = {
        titulo: '',
        categoria: '',
        descripcion: '',
        latitud: '',
        longitud: '',
        apellido: '',
        nombre: '',
        telefono: '',
        email: '',
      }
      this.mensaje = ''
      this.mensaje_exito = `La denuncia ${mensaje.atributos.titulo} de ${mensaje.atributos.nombre} fue creada exitosamente \n`
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth',
      })
    },

    async crear() {
      // Retorna la Promesa
      // Guardamos en response
      var response = await fetch(
        `${process.env.VUE_APP_ROOT}api/crear_denuncia`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            titulo: this.denuncia.titulo,
            categoria: this.denuncia.categoria,
            descripcion: this.denuncia.descripcion,
            latitud: this.denuncia.latitud,
            longitud: this.denuncia.longitud,
            apellido: this.denuncia.apellido,
            email: this.denuncia.email,
            nombre: this.denuncia.nombre,
            telefono: this.denuncia.telefono,
          }),
        }
      )

      // Obtenemos el mensaje de la API
      let mensaje = await response.json()
      mensaje.Error
        ? (this.mensaje = `La denuncia no pudo procesarse: \n  ${mensaje.Error}`)
        : this.funcion_exitosa(mensaje)

      // this.$router.push('/home')
    },
  },
  data() {
    return {
      mensaje: '',
      tipo: 'punto',
      mensaje_exito: '',
      id: this.$route.params.id,
      denuncia: {
        titulo: '',
        categoria: '',
        descripcion: '',
        latitud: '',
        longitud: '',
        apellido: '',
        nombre: '',
        telefono: '',
        email: '',
      },
    }
  },
}
</script>

<!-- <script> FINALIZO </script> -->
