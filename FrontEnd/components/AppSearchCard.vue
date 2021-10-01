<template>
  <div class="search-card">
          <h3 class="card-title mb-4">Search</h3>
          <div class="input-group custom-input-group mb-2">
            <div class="input-group-prepend">
              <span class="input-group-text-custom" id="basic-addon1">
                <span class="mdi mdi-magnify"></span>
              </span>
            </div>
            <input type="text" class="form-control uplood-control" placeholder="Intent Keywords" aria-label="Username" v-model="keyword" aria-describedby="basic-addon1" required>
          </div>
          <div class="input-group custom-input-group mb-2 mag-icon-search">
            <multiselect
              v-model="industry"
              :options="industryOptions"
              :multiple="true"
              :close-on-select="false"
              :clear-on-select="false"
              :hideSelected="false"
              :taggable="false"
              placeholder="Industries"
              :preserve-search="true"
              :internal-search="false"
              @search-change="asyncFindIndustries" >
              <template slot="selection" slot-scope="{ values, search, isOpen }">
                <span class="multiselect__single" style="padding-left: 0px;" v-if="values.length">{{values.join(',')}}</span>
              </template>
                  <template
                    slot="option"
                    slot-scope="props">
                    <div class="option__desc">
                      <app-checkbox :item="industry" :option="props.option" />
                      <span class="option__small">{{ props.option }}</span>
                    </div>
                  </template>
            </multiselect>
          </div>
          <div class="input-group custom-input-group mb-2 mag-icon-search">
          <vue-simple-suggest
            v-model="jobTitle"
            placeholder="Job Titles"
            :list="jobTitleOptions"
            :filter-by-query="true">
          </vue-simple-suggest>
          </div>
           <div class="input-group custom-input-group mb-2">
                <multiselect
                  v-model="revenue"
                  :options="revenueOptions"
                  :multiple="true"
                  :preselect-first="false"
                  placeholder="Revenue"
                  :close-on-select="false"
                  :clear-on-select="false"
                  :preserve-search="true" >
                  <template slot="selection"
                            slot-scope="{ values }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template
                    slot="option"
                    slot-scope="props">
                    <div class="option__desc">
                      <app-checkbox :item="revenue" :option="props.option" />
                      <span class="option__small">{{ props.option }}</span>
                    </div>
                  </template>
                </multiselect>
            </div>
            <div class="input-group custom-input-group mb-2">
                <multiselect
                  v-model="employee"
                  :options="companySizes"
                  :multiple="true"
                  :preselect-first="false"
                  placeholder="Company size"
                  :close-on-select="false"
                  :clear-on-select="false"
                  :preserve-search="true" >
                  <template slot="selection"
                            slot-scope="{ values }">
                    <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
                  </template>
                  <template
                    slot="option"
                    slot-scope="props">
                    <div class="option__desc">
                      <app-checkbox :item="employee" :option="props.option" />
                      <span class="option__small">{{ props.option }}</span>
                    </div>
                  </template>
                </multiselect>
          </div>
          <div class="input-group custom-input-group mb-2">
            <div class="input-group-prepend">
              <span class="input-group-text-custom" id="basic-addon1">
                <span class="mdi mdi-map-marker-outline"></span>
              </span>
            </div>
            <multiselect class="country-select"
              v-model="country"
              :options="countries"
              :multiple="true"
              :internal-search="false"
              :close-on-select="false"
              :clear-on-select="false"
              :hideSelected="false"
              :taggable="false"
              placeholder="Countries"
              :preserve-search="true"
              @search-change="asyncFindCountries">
              <template slot="selection" slot-scope="{ values }">
                <span class="multiselect__single" v-if="values.length">{{values.join(', ')}}</span>
              </template>
              <template
                slot="option"
                slot-scope="props">
                <div class="option__desc">
                  <app-checkbox :item="country" :option="props.option" />
                  <span class="option__small">{{ props.option }}</span>
                </div>
              </template>
              <template slot="selection">
                <span class="mdi mdi-magnify"></span>
              </template>
            </multiselect>
          </div>
          <div class="input-group custom-input-group mb-2 upload">
            <input type="text" class="form-control upload-control" placeholder="ABM/TAL" aria-label="Companies" v-model="companies" aria-describedby="basic-addon1" required>
            <label for="file-upload">
                <input type="file" id="file-upload" ref="input" @change="processFile"/>
                <span class="mdi mdi-upload"></span>
                 Upload
            </label>
            <div class="info-circle">
               <span class="mdi mdi-information-outline"></span><span class="tooltiptext">Only .txt,.csv and .xsl file</span>
            </div>
          </div>
          <div class="country-buttons text-left my-4" >
            <a class="card-tab-btn" v-on:click="showCountry(selectedCountry)" :class="selectedCountryGroup.includes(selectedCountry) ? 'active' : ''" :key="index" v-for="selectedCountry, index in countryGroups">{{selectedCountry}}</a>
            <div class="show-city mt-3" v-if="!isHidden">
                <div class="close-city">
                    <a class="btn-dark " v-on:click="isHidden = true">x</a>
                </div>
                <div class="city-list">
                    <a class="card-tab-btn " @click="removeCountry(city)" :key="index" v-for="city, index in countryList">
                      {{city}}
                      <span v-if="!countrySelected.includes(city)" class="mdi mdi-check-bold ml-2"></span>
                    </a>
                </div>
            </div>
          </div>
          <div class="line-seperator"></div>
          <button class="btn-search-lg text-white my-4" type="button" data-toggle="button" @click="$emit('search', { industry, country, jobTitle, keyword, companies, countryList, employee, revenue})"  :disabled="keyword.trim() == ''" title="Search" >Search</button>
        </div>
</template>

<script>
import constants from "../api/constants"
import AppCheckbox from './AppCheckbox.vue'
import readXlsxFile from 'read-excel-file'
import Multiselect from 'vue-multiselect'
import { mapGetters } from 'vuex'
import VueSimpleSuggest from 'vue-simple-suggest'
import 'vue-simple-suggest/dist/styles.css' 

export default {
  name: "SearchCard",
    props: {
      countryGroups: Array,
      jobTitles: Array
  },
  data () {
    return {
      industry : [],
      jobTitle: constants.EMPTY_STRING,
      companies: constants.EMPTY_STRING,
      revenue:[] ,
      revenueOptions: constants.REVENUES,
      country: [],
      employee: [constants.ANY],
      countryList: [],
      isHidden: true,
      jobSearchSlotText: constants.LOADING,
      selectedCountryGroup: [],
      keyword: constants.EMPTY_STRING,
      countrySelected: [],
      countries: constants.COUNTRIES,
      constJobTitles: [],
      constIndustries: constants.INDUSTRIES,
      industryOptions: constants.INDUSTRIES,
      companySizes: constants.COMPANY_SIZES,
      jobTitleOptions: []
    }
  },
  computed: {
    ...mapGetters({
        getCountryList: 'index-module/country-list'
    })
  },
  watch: {
     jobTitles(val, oldVal) {
       this.jobTitleOptions = val;
       this.constJobTitles = val;
     }
  },
  components: {
    Multiselect,
    VueSimpleSuggest,
    AppCheckbox
  },
  methods: { 
      async asyncFindIndustries(query) {
        if(query!=constants.EMPTY_STRING) {
          this.industryOptions= this.constIndustries.filter(industry=> industry.toLowerCase().startsWith(query.toLowerCase()));
        }
      },
      async asyncFindJobTitles(query) {
        this.jobTitleOptions = this.constJobTitles.filter(job => job.toLowerCase().startsWith(query.toLowerCase()));
      },
      async asyncFindCountries(query) {
        this.countries = constants.COUNTRIES.filter((country)=> country.toLowerCase().startsWith(query.toLowerCase()));
      },
      processFile(event) {
           let file = event.target.files[0];
           if(file.type.match(/.sheet$/)) {
            readXlsxFile(file).then((allRows) => {
              const combinedRows = allRows.reduce((combinedRows, row)=> {
                   combinedRows = [...combinedRows, ...row];
                   return combinedRows;
              }, []);
              this.companies = combinedRows.join(",");
              this.companies = this.companies.substring(0, this.companies.length - 1);
          });
        }
        if(!file.type || file.type.match(/text\/plain/)) {
          const reader = new FileReader();
          reader.readAsText(file);
          reader.onload = (_event) => {
            this.companies = reader.result;
           }
        }
        this.$refs.input.value='';
      },
      notEmptyAndNull(item) {
         return item!=null && item!= constants.EMPTY_STRING;
      },
      showCountry(selectedCountry) {
        if(this.selectedCountryGroup.includes(selectedCountry)) {
          var index = this.selectedCountryGroup.indexOf(selectedCountry);
          this.selectedCountryGroup.splice(index, 1);
          this.$store.dispatch('index-module/load-country-group', selectedCountry).then(()=> {
              this.countryList = this.countryList.filter((country)=> !this.getCountryList.includes(country));
          });
          if(this.selectedCountryGroup.length==0) {
            this.isHidden = true;
          }
        }  else  {
          this.selectedCountryGroup.push(selectedCountry);
          this.isHidden = false;
          this.$store.dispatch('index-module/load-country-group', selectedCountry).then(()=> {
              this.countryList = [...this.countryList, ...this.getCountryList];
          });
        }
      },
      removeCountry(country){
          const index = this.countrySelected.indexOf(country);
          if (index > -1) {
            this.countrySelected.splice(index, 1);
          } else {
            this.countrySelected.push(country);
          }
          this.$emit('removeCountry', this.countrySelected);
      },
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
  .search-card{
    background: #FFFFFF;
    border-radius: 8px;
    padding: 40px;
    font-family: 'Mulish'
  }
  .search-card .card-title{
    font-size: 20px;
    font-weight: 600;
    line-height: 25px;
    text-align: left;
  }
  .country {
    margin-bottom: 1rem;
  }

  .country-select .multiselect__tags {
    padding-left: 40px !important;
  }

  input[type="file"] {
    display: none;
  }

  input[type="text"]::placeholder {
    color: #374958;
    font-family: 'Mulish';
    font-weight: 400;
    font-size: 14px;
  }

  .vue-simple-suggest.designed .input-wrapper input.default-input::placeholder {
    color: #374958 !important;
    font-family: 'Mulish';
    font-weight: 400;
    font-size: 14px;
  }

  ::-ms-input-placeholder {
      color: #374958;
      font-family: 'Mulish';
      font-weight: 400;
      font-size: 14px;
  }

  .icon-upload {
    font-size: 22px;
  }

  .country .multiselect__placeholder {
    padding: 0 0 0 32px !important;
    font-size: 16px !important;
    color: #374958 !important;
    margin-bottom: 8px !important;
  }
  .multiselect__placeholder {
    font-family: 'Mulish';
    font-size: 16px !important;
    color: #374958 !important;
    margin-bottom: 8px !important;
  }

  .line {
    border: 1px solid grey;
  }
.card-tab-btn{
  border: 1px solid #C6C6C6;
  box-sizing: border-box;
  border-radius: 8px;
  padding: 10px 20px;
  color: #374958;
  text-decoration: none;
  cursor: pointer;
}
.card-tab-btn.active{
  border: 1px solid #B3365B;
  background: #B3365B;
  color: #fff;
}
.input-group-text-custom{
    display: flex;
    align-items: center;
    padding: 5px 0 0 12px;
    margin-bottom: 0;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #374958;
    text-align: center;
    white-space: nowrap;
    border-radius: 0.25rem;
  }
  .input-group-text-custom .mdi{
    font-size: 26px;
  }
  .custom-input-group{
    border-radius: 8px;
  }

  .upload label {
    width: 38%;
    margin-left: 5%;
    display: flex;
    align-items: center;
    margin-bottom: 0;
    height: 50px;
    padding: 4px;
    border-radius: 6px;
    overflow: hidden;
    background-color: #B3365B;
    color: white;
  }

  .upload .info-circle {
    margin-left: 1%;
    width: 8%;
    font-size: 26px;
    text-align: center;
    display: flex;
    align-items: center;
  }

  .info-circle .tooltiptext{
      visibility: hidden;
      width: 120px;
      background-color: white;
      color: #374958;
      text-align: center;
      border-radius: 6px;
      font-size: 14px;
      padding: 8px;
      position: absolute;
      right: -122px;
      top: 5px;
      border: 1px solid #E0E0E0;
      z-index: 1;
  }

  .info-circle .tooltiptext::after {
      content: " ";
      position: absolute;
      top: 13%; /* At the bottom of the tooltip */
      left: 0%;
      margin-left: -15px;
      border-width: 7px;
      border-style: solid;
      border-color: transparent #E0E0E0 transparent transparent;
      z-index: 1;
}

  .info-circle:hover .tooltiptext {
       visibility: visible;
  }

  .custom-input-group label span {
    display: inline-block;
    width: 30%;
  }

  .custom-input-group .form-control{
    border-radius: 8px !important;
    padding: 1.5rem 0.75rem;
    padding-left: 45px;
    color: #374958 !important;
  }

  .upload .upload-control {
    padding-left: 12px !important;
    max-width: 48%;
  }

.custom-input-group .form-control:focus {
  box-shadow: none;
}

.search-card .input-group.custom-input-group .input-group-prepend{
  position: absolute;
  z-index: 5;
}


.search-card .input-group.custom-input-group .form-control:focus{
  border-color: #B3365B !important;
}

.hr-seperator{
  border: 1px solid #C6C6C6;
  margin-top: 25px;
  margin-bottom: 15px;
}

.line-seperator {
  margin-top: 6px;
  margin-bottom: 14px;
  height:1px;
  background-color: #C6C6C6;
}

.score-number{
  color: #B3365B;
}

.score-section{
  font-weight: 600;
  font-size: 14px;
  line-height: 18px;
}

.btn-search-lg{
  background: #B3365B;
  border-radius: 8px;
  padding: 0.75rem 60px;
  border: 0;
  line-height: 23px;
  width: 100%;
  font-size: 18px;
  font-style: normal;
  font-weight: 600;
  color: #E7E7E7;
  height: 48px !important;
  margin: 4px 0!important;
}

.show-city {
  height: 110px;
  display: flex;
  flex-direction: column;
}

.close-city {
  display: flex;
  justify-content: flex-end;
}

.close-city a.btn-dark{
    border-radius: 50%;
    padding: 2px 7px;
    margin-bottom: 3px;
}

.city-list{
    height: 110px;
    padding: 10px 10px;
    overflow-y : scroll;
    overflow-x : hidden;
    border-radius: 6px;
    box-shadow: 0px 2px 8px rgba(40, 41, 61, 0.08), 0px 20px 32px rgba(96, 97, 112, 0.24);
}

.form-group {
  padding: 0 6px!important;
}

.city-list a{
    padding: 1px 6px !important;
}

.mdi-check-bold{
    color: rgb(255, 255, 255);
    background: #B3365B;
    border-radius: 100%;
    height: 36px;
    width: 36px;
    padding: 3px 4px;
    font-size: 7px;
}

.vue-simple-suggest.designed {
  width: 100% !important;
}

.vue-simple-suggest.designed .suggestions {
  height: 250px !important;
  overflow-y: auto!important;
}

.vue-simple-suggest.designed .input-wrapper input{
  border-radius: 8px !important;
  border: 1px solid #ced4da !important;
  width: 100%!important;
  min-height: 48px;
  padding: 10px !important;
}

.suggestions .suggest-item {
  text-align: left !important;
}

.vue-simple-suggest.designed .suggestions .suggest-item {
  color: black !important;
}

.vue-simple-suggest.designed .suggestions .suggest-item.hover {
  background-color: #EBCACA !important;
  color: #B3365B !important;
}

.vue-simple-suggest.designed .suggestions .suggest-item.selected {
  background-color: #EBCACA !important;
  color: #B3365B !important;
}

.vue-slider.vue-slider-ltr{
  margin-top: 35px;
}

.popular-heading,
.popular-item{
  font-size: 14px;
  line-height: 18px;
  color: #374958;
}
.popular-heading{
  font-weight: 600;
}
.popular-item{
  font-weight: 700;
  border-bottom: 1px solid #C6C6C6;
  cursor: pointer;
}
</style>
