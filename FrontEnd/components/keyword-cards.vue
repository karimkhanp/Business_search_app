<template>
        <div class="keyword-card">
            <div v-if="category">Category: <span>{{category}}</span><a v-on:click="remove(`category`)">x</a> </div>
            <div v-if="jobTitle">Job Title: <span>{{jobTitle}}</span><a v-on:click="remove(`jobTitle`)">x</a> </div>
            <div v-if="country && country.length>0">Country: <span>{{country.join(',')}}</span><a v-on:click="remove(`country`)">x</a></div>
            <div v-if="city">City: <span>{{city}}</span><a v-on:click="remove(`city`)">x</a> </div>
            <div v-if="employee">Company Size: <span>{{employee.join(', ')}}</span><a v-on:click="remove(`employee`)">x</a></div>
        </div>
</template>
<script>

export default {
    name: 'KeywordCard',
    props: {
        category: String,
        jobTitle: String,
        country: Array,
        city: String,
        employee: Array
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
      background-color: #01579B;
      border-radius: 10px;
      display: inline-block;
      color: white;
      margin: 5px 10px;
      padding: 2px 10px;
      max-width: 100%;
      height: auto;
      word-wrap: break-word;
  }

  .keyword-card span {
    font-weight: bold;
  }

  .keyword-card  a {
    text-decoration: none;
    font-size: 20px;
    color: white;
    font-weight: bold;
    margin-left: 10px;
    cursor: pointer;
  }
</style>
