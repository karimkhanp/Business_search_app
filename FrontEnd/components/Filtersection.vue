<template>
       <div class="container">
          <div class="main-filter-section">
            <div class="form-row">
              <div class="form-group col-md-2 text-left">
                <label class="typo__label">State</label>
                <multiselect
                  v-model="state"
                  :options="states"
                  :multiple="false"
                  :preselect-first="true"
                  placeholder="Any"
                  :close-on-select="true"
                  @input="$emit('searchByState', state)"
                  :clear-on-select="false"
                  :preserve-search="true" >
                  <template slot="selection"
                            slot-scope="{ values }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template slot="option" slot-scope="props">
                    <div class="option__desc">
                      <span class="option__small" v-html="props.option"></span>
                    </div>
                  </template>
                </multiselect>
              </div>
              <div class="form-group col-md-3 text-left">
                <label class="typo__label">City</label>
                <multiselect
                  v-model="city"
                  :options="cities"
                  :multiple="false"
                  :preselect-first="true"
                  placeholder="Any"
                  :close-on-select="true"
                  @input="$emit('searchByCity', city)"
                  :clear-on-select="false"
                  :preserve-search="true" >

                  <template slot="selection"
                            slot-scope="{ values }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template slot="option" slot-scope="props">
                    <div class="option__desc">
                      <span class="option__small" v-html="props.option"></span>
                    </div>
                  </template>
                </multiselect>
              </div>

              <div class="form-group col-md-3 text-left">
                <label class="typo__label">Company Size</label>
                <multiselect
                  v-model="employee"
                  :options="companySizes"
                  :multiple="true"
                  :preselect-first="true"
                  placeholder="Any"
                  :close-on-select="false"
                  @input="$emit('searchBySize', employee)"
                  :clear-on-select="false"
                  :preserve-search="true" >

                  <template slot="selection"
                            slot-scope="{ values }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template slot="option" slot-scope="props">
                    <div class="option__desc">
                      <span v-if="employee.includes(props.option)">
                        <input type="checkbox" value="" checked>
                      </span>
                      <span v-else>
                        <input type="checkbox" value="">
                      </span>
                      <span class="option__small" v-html="props.option"></span>
                    </div>
                  </template>
                </multiselect>
              </div>
              <div class="form-group col-md-1 text-left">
                <label for="inputPages">Records</label>
                <multiselect
                  v-model="rpp"
                  :options="recordOptions"
                  :multiple="false"
                  :preselect-first="true"
                  placeholder="Any"
                  :close-on-select="true"
                  @input="$emit('searchOnFilter', rpp)"
                  :clear-on-select="false"
                  :preserve-search="true" >
                  <template slot="selection" slot-scope="{ values }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template slot="option" slot-scope="props">
                  </template>
                </multiselect>
              </div>
              <div class="file-export form-group col-md-3 text-left">
                  <button class="export btn btn-primary" v-on:click="$emit('exportToFile')"> <img src="@/assets/img/download-icon.PNG" width="20px"/> &nbsp;  Export</button>
              </div>
            </div>
        </div>
  </div>
</template>

<script>

import constants from '../api/constants'
import Multiselect from 'vue-multiselect'

export default {
    name: 'FilterSection',
    props: {
       states: Array,
       cities: Array,
       companySizes: Array,
       recordOptions: Array
    },
    components: {
      Multiselect
    },
    data: function() {
      return {
        state: constants.ALL,
        city: constants.ALL,
        rpp: 15,
        employee: [constants.ANY]
      }
    }
}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
  button.export, button.export:hover {
    background-color: #EBCACA;
    border-radius: 8px;
    border: none!important;
    color: #374958;
    padding: 12px 30px;
    float: right;
  }

  .main-filter-section{
    background: #B3365B;
    border-radius: 8px;
    padding: 32px;
  }
  .form-row {
    align-items: center;
  }
  .main-filter-section select{
    background: #EBCACA;
    border-radius: 8px;
    padding: 5px;
    height: 45px;
  }

  .main-filter-section .form-group label{
    font-size: 16px;
    font-weight: 600;
    line-height: 20px;
    color: #C6C6C6 !important;
  }
  .main-filter-section .multiselect__single {
    background: #EBCACA !important;
  }
  .main-filter-section .multiselect{
    background: #EBCACA;
    border-radius: 8px;
  }
  .main-filter-section .multiselect__tags {
    background: #EBCACA;
  }
  .main-filter-section .multiselect--active .multiselect__tags {
    background: #fff;
  }
  .multiselect__tags {
    padding: 10px 40px 3px 12px !important;
    min-height: 48px;
    border-radius: 8px !important;
    border: 1px solid #ced4da !important;
  }
  .multiselect__input, .multiselect__single{
    border-radius: 8px !important;
    line-height: 24px;
  }
  .multiselect__content-wrapper .multiselect__element .option__desc span.option__small{
    margin-left: 10px;
  }
  .multiselect__select{
    height: 48px;
  }
  .multiselect__option{
    min-height: 44px;
  }
  .multiselect__placeholder {
    font-size: 16px !important;
    color: #495057 !important;
    margin-bottom: 8px !important;
  }
  .multiselect {
    min-height: 48px;
  }
  .multiselect__spinner {
    height: 46px;
    border-radius: 8px;
  }
  .multiselect--active .multiselect__tags {
    border-color: #B3365B !important;
  }
  .file-export {
     margin-top: 28px;
     display:flex;
     align-items: center;
     justify-content: flex-end;
  }
</style>
