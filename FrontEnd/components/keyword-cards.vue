<template>
        <div class="container ">
          <div class="keyword-card">
            <template v-for="item of items">
               <div :key="item.key" v-if="item.value">{{item.key}}: <span>{{item.value}}</span><a v-on:click="remove(item.key)">x</a> </div>
            </template>
          </div>
        </div>
</template>
<script>

export default {
    name: 'KeywordCard',
    props: {
      items: Array
    },
    methods: {
        remove(type) {
            this.$emit("remove", type);
        }
    }
}
</script>

<style scoped>
  .keyword-card {
     display: flex;
     flex-wrap: wrap;
     font-style: normal;
  }

  .keyword-card div {
      background-color: #16263a;
      color: #4a5461;
      border-radius: 10px;
      display: inline-block;
      margin: 5px 5px;
      padding: 2px 10px;
      max-width: 100%;
      height: auto;
      word-wrap: break-word;
      font-size: 14px;
  }

  .keyword-card span {
    color: white;
    opacity: 0.8;
  }

  .keyword-card  a {
    text-decoration: none;
    font-size: 20px;
    margin-left: 10px;
    cursor: pointer;
    color: white;
    opacity: 0.8;
  }
</style>
