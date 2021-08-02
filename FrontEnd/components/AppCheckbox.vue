<template>
        <span v-if="item && item.includes(option)" class="container">
            <input type="checkbox" value="" checked>
            <span class="checkmark"></span>
        </span>
        <span v-else>
            <input type="checkbox" value="">
            <span class="checkmark"></span>
        </span>
</template>

<script>


export default {
     name: 'AppCheckbox',
     props: {item: Array,
             option: String}
}
</script>

<style scoped>

/* The container */
.container {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: 21px;
  cursor: pointer;
  font-size: 22px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* Hide the browser's default checkbox */
.container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

/* Create a custom checkbox */
.checkmark {
  position: absolute;
  top: 10px;
  left: 15px;
  height: 20px;
  width: 20px;
  background-color: white;
  border: 2px solid #d48ea3;
  border-radius: 2px;
}

/* On mouse-over, add a grey background color */
.container:hover input ~ .checkmark {
  background-color: white;
}

/* When the checkbox is checked, add a blue background */
.container input:checked ~ .checkmark {
  background-color: #2196F3;
  position: absolute;
  top: 10px;
  left: 15px;
}

/* Create the checkmark/indicator (hidden when not checked) */
.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the checkmark when checked */
.container input:checked ~ .checkmark:after {
  display: block;
}

/* Style the checkmark/indicator */
.container .checkmark:after {
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 3px 3px 0;
  -webkit-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
}
</style>
