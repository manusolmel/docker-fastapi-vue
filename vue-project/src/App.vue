<script setup>
import { ref, onMounted } from 'vue'

const motos = ref([])
const nuevaMoto = ref({ brand: '', model: '', stock: true })

const agregarMoto = async () => {
  try {
    const response = await fetch('http://localhost:8000/motos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nuevaMoto.value)
    })
    
    if (response.ok) {
      const motoGuardada = await response.json()
      motos.value.push(motoGuardada) 
      nuevaMoto.value = { brand: '', model: '', stock: true } 
    }
  } catch (err) {
    console.error("Error al guardar:", err)
  }
}
onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/motos')
    motos.value = await response.json()
    console.log("Motos cargadas:", motos.value)
  } catch (error) {
    console.error("Error conectando con el backend:", error)
  }
})

</script>

<template>
  <form @submit.prevent="agregarMoto" style="margin-bottom: 20px; border: 1px solid #444; padding: 15px;">
  <h3>Añadir Nueva Moto</h3>
  <input v-model="nuevaMoto.brand" placeholder="Marca (ej: Suzuki)" required>
  <input v-model="nuevaMoto.model" placeholder="Modelo (ej: SV650)" required>
  <label>
    <input type="checkbox" v-model="nuevaMoto.stock"> ¿En Stock?
  </label>
  <button type="submit">Guardar Moto</button>
</form>

  <h1>Garaje de Motos</h1>
  <ul>
    <li v-for="moto in motos" :key="moto.id">
      {{ moto.brand }} - {{ moto.model }} (Stock: {{ moto.stock }})
    </li>
  </ul>
</template>