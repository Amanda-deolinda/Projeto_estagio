<template>
  <div class="app">
    <!-- Container de busca com ícone e estilização -->
    <div class="search-container">
      <input
        type="text"
        v-model="query"
        @input="buscarOperadoras"
        placeholder="Buscar operadoras..."
        class="search-input"
      />
      <i v-if="carregando" class="loader"></i> <!-- Ícone de carregamento -->
    </div>

    <!-- Mensagem de carregamento -->
    <div v-if="carregando" class="loading-message">Carregando...</div>
    <ul v-else class="operadoras-list">
      <li v-for="op in operadoras" :key="op.Registro_ANS" class="operadora-item">
        <span class="op-name">{{ op.Razao_Social }}</span>
        <span v-if="op.Nome_Fantasia" class="op-fantasia">({{ op.Nome_Fantasia }})</span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      operadoras: [],
      carregando: false,
      timeout: null
    };
  },
  methods: {
    buscarOperadoras() {
      clearTimeout(this.timeout);
      this.timeout = setTimeout(() => {
        this.carregando = true;
        axios.get('http://localhost:5000/search', { params: { q: this.query } })
          .then(resposta => {
            this.operadoras = resposta.data;
            this.carregando = false;
          })
          .catch(erro => {
            console.error(erro);
            this.carregando = false;
          });
      }, 300); // Debounce de 300ms
    }
  }
};
</script>

<style scoped>
/* Estilos gerais */
body {
  background-color: #000000; /* Fundo preto para a página */
  font-family: Arial, sans-serif;
  color: #ecf0f1; /* Texto claro */
  margin: 0;
  padding: 0;
}

.app {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  background-color: #f2f2f2; /* Fundo cinza claro para o conteúdo */
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Container do campo de busca */
.search-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 10px;
  border-radius: 20px;
  border: 1px solid #ccc;
  font-size: 16px;
  outline: none;
  transition: border 0.3s ease;
  background-color: #ecf0f1; /* Fundo claro para o campo de busca */
  color: #333; /* Texto escuro no campo de busca */
}

.search-input:focus {
  border-color: #3498db;
}

/* Ícone de carregamento */
.loader {
  position: absolute;
  right: 10px;
  font-size: 20px;
  color: #3498db; /* Cor azul para o ícone */
  animation: spin 1s infinite linear;
}

/* Animação de giro para o ícone */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Mensagem de "Carregando..." */
.loading-message {
  text-align: center;
  font-size: 18px;
  color: #ecf0f1; /* Texto claro */
}

/* Estilo da lista de operadoras */
.operadoras-list {
  list-style: none;
  padding: 0;
}

.operadora-item {
  background: #bdc3c7; /* Fundo cinza claro para itens */
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.3s ease;
  color: #333; /* Texto escuro */
}

.operadora-item:hover {
  background: #95a5a6; /* Fundo mais escuro ao passar o mouse */
}

.op-name {
  font-weight: bold;
}

.op-fantasia {
  color: #7f8c8d; /* Cor mais suave para o nome fantasia */
  font-style: italic;
}
</style>