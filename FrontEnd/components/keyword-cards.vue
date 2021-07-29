<template>
        <div class="container ">
          <div class="keyword-card">
            <template v-for="item of items">
               <div :key="item.key" v-if="item.value"><span>{{item.key}}:&nbsp;</span>{{item.value}}<a v-on:click="remove(item.key)">x</a></div>
            </template>
          </div>
        </div>
</template>
<script>

export default {
    name: 'KeywordCard',
    props: {
      items: Array,
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
      background-color: #1c3246;
      color: #c0c0c0;
      border-radius: 8px;
      display: inline-block;
      margin: 8px 15px 8px 0px;
      padding: 4px 10px;
      max-width: 100%;
      height: auto;
      font-weight: bold;
      word-wrap: break-word;
      font-size: 14px;
      display: flex;
      align-items: center;
  }

  .keyword-card span {
    color: #aeb1b3;
    display: flex;
    align-items: center;
  }

  .keyword-card  a {
    text-decoration: none;
    font-size: 28px;
    margin-left: 10px;
    cursor: pointer;
    color: #c0c0c0;
    font-weight: 60;
    margin-bottom: 4px;
  }
</style>
