<template>
  <div>
    <div class="main-header">
      <Header />
    </div>
    <Nuxt/>
  </div>
</template>

<script>
  import Header from '../components/Header';

  export default {
    components: {
      Header
    }
  }
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  .main-header nav.navbar{
    position: absolute;
    width: 100%;
  }
</style>
