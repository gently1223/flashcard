<template>
  <v-container  :class="{
        'container pa-4 my-12': $vuetify.breakpoint.smAndDown,
        'container pa-10 my-12': $vuetify.breakpoint.mdAndUp,
      }">
    <!-- avatar -->
    <v-row class="justify-center">
      <v-avatar size="150px">
        <img src="../assets/img/avatar.jpg" />
      </v-avatar>
    </v-row>
    <!-- name -->
    <v-row class="justify-center pb-5">
      <span class="title text-secondary py-2 font-weight-bold">{{ name }}</span>
    </v-row>
    <v-row>
        <v-col cols="12" lg="6">
            <p class="title text-secondary py-2 font-weight-bold">{{book_title}}</p>
            <div class="row justify-space-between mt-5 mb-5">
                <v-btn color="primary" @click="showModal = true">
                    Select Exercise
                </v-btn>
                <v-btn
                    class="mx-2"
                    dark
                    color="teal"
                    @click="showSettingsModal = true;"
                >
                <v-icon dark>
                    mdi-format-list-bulleted-square
                </v-icon>
                </v-btn>
            </div>
            <div class="imageZoom">
                <vue-hover-zoom
                    showWhenImageLoaded="true"
                    :imageUrl="getImgUrl()"
                >
                </vue-hover-zoom>
            </div>
            
        </v-col>
        <v-col cols="12" lg="6">
            <p class="title text-secondary py-2 font-weight-bold">EXERCISE</p>
            <v-select
                :items="uptodown_items"
                label="Up to Down"
                dense
                solo
            ></v-select>
            <v-img
              :aspect-ratio="16/9"
              :height="500"
              :src="getImgUrl()"
            ></v-img>
            <p class="title text-secondary py-2 font-weight-bold">Answer</p>
            <v-img
              :aspect-ratio="16/9"
              :height="200"
              :src="getAnswerUrl()">
            </v-img>
            <v-row class="mt-5 justify-center">
                <v-btn
                  rounded
                  color="primary"
                  dark
                >
                  Check Answer
                </v-btn>
                &nbsp;&nbsp;&nbsp;              
              <p class="py-2 font-weight-bold">Preview: </p>&nbsp;<p class="py-2 font-weight-bold">Correct</p>
            </v-row>
            <v-row class="mt-5 justify-space-between dialog">
                <v-col>
                <v-btn
                  class="ma-2"
                  outlined
                  color="indigo"
                  width="120"
                >
                  Correct
                </v-btn>
                <p>{{level[0]}}</p>
                </v-col>
                <v-col>
                <v-btn
                  class="ma-2"
                  outlined
                  color="indigo"
                  width="120"
                >
                  Easy
                </v-btn>
                <p>{{level[1]}}</p>
                </v-col>
                <v-col>
                <v-btn
                  class="ma-2"
                  outlined
                  color="indigo"
                  width="120"
                >
                  Mistake
                </v-btn>
                <p>{{level[2]}}</p>
                </v-col>
                <v-col>
                <v-btn
                  class="ma-2"
                  outlined
                  color="indigo"
                  width="120"
                >
                  Difficult
                </v-btn>
                <p>{{level[3]}}</p>
                </v-col>
                <v-col>
                <v-btn
                  class="ma-2"
                  outlined
                  color="indigo"
                  width="120"
                >
                  Skip
                </v-btn>
                </v-col>
            </v-row>
            <v-row class="mt-10">
              <v-col>
                <v-btn
                  rounded
                  color="primary"
                  dark
                  width="150"
                >
                  Restart
                </v-btn>
              </v-col>
              <v-col>
                <v-select
                  :items="items"
                  :style="{width: '100px'}"
                  label="In Order"
                  dense
                  outlined
                  width="150"
                ></v-select>
              </v-col>
              <v-col>
                <v-btn
                    rounded
                    width="150"
                >
                  Close
                </v-btn>
              </v-col>
              <v-col>
                <v-btn
                  rounded
                  color="primary"
                  darkwidth="150"
                >
                  Check Progress
                </v-btn>
              </v-col>
            </v-row>
        </v-col>
    </v-row>

    <!-- List Modal -->
    <transition name="fade" appear>
        <div class="modal-overlay"
            v-if="showModal"
            @click="showModal = false">
        </div>
    </transition>
    <transition name="pop" appear>
        <div class="modal"
            role="dialog"
            v-if="showModal"
            >
            <h1>SELECT EXERCISE BOOK</h1>
            <v-list shaped dense min-height="240">
                <v-subheader>SUBJECTS</v-subheader>
                <v-list-item-group
                    v-model="selectedItem"
                    color="primary">
                        <v-list-item
                            v-for="(item, i) in items"
                            :key="i">
                            <v-list-item-icon>
                              <v-icon v-text="item.icon"></v-icon>
                            </v-list-item-icon>
                            <v-list-item-content>
                              <v-list-item-title v-text="item.text"></v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                </v-list-item-group>
            </v-list>
            <v-file-input
                v-model="files"
                color="deep-purple accent-4"
                counter
                label="File input"
                multiple
                placeholder="Select your files"
                prepend-icon="mdi-paperclip"
                outlined
                :show-size="1000"
            >
                <template v-slot:selection="{ index, text }">
                    <v-chip
                      v-if="index < 2"
                      color="deep-purple accent-4"
                      dark
                      label
                      small
                    >
                      {{ text }}
                    </v-chip>

                    <span
                      v-else-if="index === 2"
                      class="text-overline grey--text text--darken-3 mx-2"
                    >
                      +{{ files.length - 2 }} File(s)
                    </span>
                </template>
            </v-file-input>
            <v-btn color="primary" @click="onClickOk">OK</v-btn>&nbsp;&nbsp;&nbsp;
            <v-btn outlined color="indigo" @click="showModal = false">CANCEL</v-btn>
        </div>
    </transition>
    <!-- Treeview Modal -->
    <transition name="fade" appear>
        <div class="modal-overlay"
            v-if="showTreeviewModal"
            @click="showTreeviewModal = false"></div>
    </transition>
    <transition name="pop" appear>
        <div class="modal"
              role="dialog"
              v-if="showTreeviewModal"
              >
            <h1>SELECT CONTENTS</h1>
            <v-treeview class="treeview"
              selectable
              :items="rows"
              @update:active="onOpen"
              @input="onSelected"
            ></v-treeview>
            <v-btn color="primary" @click="onTreeviewOk">OK</v-btn>
        </div>
    </transition>
    <!-- Setting Modal -->
    <transition name="fade" appear>
      <div class="modal-overlay"
          v-if="showSettingsModal"
          @click="showSettingsModal = false"></div>
    </transition>
    <transition name="pop" appear>
      <div class="modal faq-body"
            role="dialog"
            v-if="showSettingsModal"
            >
          <h3>Waiting period for looking back</h3>
          <v-row>
              <v-col cols="4" class=" text-left">Correct(not difficult)</v-col>
              <v-col cols="4"><vue-numeric-input v-model="not_difficult_value" :min="1" controls-type="updown" autofocus>
                              </vue-numeric-input>
              </v-col>
              <v-col cols="4">
                  <v-combobox
                    v-model="not_difficult_value_combo"
                    :items="not_difficult_value_items"
                    solo dense
                  ></v-combobox>
              </v-col>
          </v-row>
          <v-row>
              <v-col cols="4" class=" text-left">Correct(easy)</v-col>
              <v-col cols="4"><vue-numeric-input v-model="easy_value" :min="1" :max="30" controls-type="updown" autofocus>
                              </vue-numeric-input>
              </v-col>
              <v-col cols="4">
                  <v-combobox
                    v-model="easy_value_combo"
                    :items="easy_value_items"
                    solo dense
                  ></v-combobox>
              </v-col>
          </v-row>
          <v-row>
              <v-col cols="4" class=" text-left">Wrong(mistake)</v-col>
              <v-col cols="4"><vue-numeric-input v-model="mistake_value" :min="1" :max="30" controls-type="updown" autofocus>
                              </vue-numeric-input>
              </v-col>
              <v-col cols="4">
                  <v-combobox
                    v-model="mistake_value_combo"
                    :items="mistake_value_items"
                    solo dense
                  ></v-combobox>
              </v-col>
          </v-row>
          <v-row>
              <v-col cols="4" class=" text-left">Wrong(difficult)</v-col>
              <v-col cols="4"><vue-numeric-input v-model="difficult_value" :min="1" :max="30" controls-type="updown" autofocus>
                              </vue-numeric-input>
              </v-col>
              <v-col cols="4">
                  <v-combobox
                    v-model="difficult_value_combo"
                    :items="difficult_value_items"
                    solo dense
                  ></v-combobox>
              </v-col>
          </v-row>
          <h3>Planning</h3>
          <v-row class="mb-4">
              <v-col cols="4" class=" text-left">Number of exercises to do </v-col>
              <v-col cols="4" class=" text-left"><vue-numeric-input v-model="number_exercises_value" :min="1" :max="30" controls-type="updown" autofocus>
                              </vue-numeric-input>
              </v-col>
          </v-row>
          <v-row class="mb-4">
              <v-col cols="4" class=" text-left">Day of exercise </v-col>
              <v-col cols="2">
              <v-checkbox
                v-model="mon"
                label="Mon"
                color="primary"
                hide-details
              ></v-checkbox>
              </v-col>
              <v-col cols="2">
              <v-checkbox
                v-model="tue"
                label="Tue"
                color="primary"
                hide-details
              ></v-checkbox>
              </v-col>
              <v-col cols="2">
              <v-checkbox
                v-model="wen"
                label="Wen"
                color="primary"
                hide-details
              ></v-checkbox>
              </v-col>
              <v-col cols="2">
              <v-checkbox
                v-model="thu"
                label="Thu"
                color="primary"
                hide-details
              ></v-checkbox>
              </v-col>
              <v-col cols="2">
              <v-checkbox
                v-model="fri"
                label="Fri"
                color="primary"
                hide-details
              ></v-checkbox>
              </v-col>
              <v-col cols="2">
              <v-checkbox
                v-model="sat"
                label="Sat"
                color="primary"
                hide-details
              ></v-checkbox>
              </v-col>
              <v-col cols="2">
              <v-checkbox
                v-model="sun"
                label="Sun"
                color="primary"
                hide-details
              ></v-checkbox>
              </v-col>
          </v-row>

            <v-row class="mb-4">
              <v-col cols="4" class=" text-left">Start day of exercise </v-col>
              <v-col cols="4" class=" text-left">
                <v-menu
                v-model="menu2"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="date"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="date"
                  @input="menu2 = false"
                ></v-date-picker>
              </v-menu>
              </v-col>
          </v-row>
          <h3>Reward</h3>
          <v-row class="mb-4">
              <v-col cols="6">points </v-col>
              <v-col cols="3"><vue-numeric-input v-model="points_value" :min="1" controls-type="updown" autofocus>
                              </vue-numeric-input>
              </v-col>
          </v-row>
          <v-btn color="primary" @click="onSettingsOk">OK</v-btn>&nbsp;&nbsp;&nbsp;
          <v-btn outlined color="indigo" @click="showSettingsModal = false">CANCEL</v-btn>
      </div>
    </transition>
  </v-container>
</template>

<script>
import VueNumericInput from 'vue-numeric-input'
import VueHoverZoom from 'vue-hover-zoom'
import axios from 'axios'
import Vue from 'vue'
import VueToast from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css';
import VueSession from 'vue-session'
Vue.use(VueSession)
export default {
  components: {
      VueNumericInput,
      VueHoverZoom
  },
  data: () => ({
      imgAnswerURL: 'OM1-1.jpeg',
      // imgURL: 'https://picsum.photos/id/1005/600/200',
      temp:"",
      imgURL: 'OM1-1.jpeg',
      showModal: false,
      showTreeviewModal: false,
      showSettingsModal: false,
      selectedItem: 0,
      not_difficult_value: 1,
      easy_value: 1,
      mistake_value: 1,
      difficult_value: 1,
      number_exercises_value: 1,
      uptodown_items: [
          'History',
      ],
      level: ["1 days" ,"4 weeks","4 hours","1 hours"],
      not_difficult_value_combo: ['weeks'],
      not_difficult_value_items: [
          'weeks',
          'days',
          'hours',
          'minutes',
        ],
      easy_value_combo: ['weeks'],
      easy_value_items: [
          'weeks',
          'days',
          'hours',
          'minutes',
        ],
      mistake_value_combo: ['weeks'],
      mistake_value_items: [
          'weeks',
          'days',
          'hours',
          'minutes',
        ],
      difficult_value_combo: ['weeks'],
      difficult_value_items: [
          'weeks',
          'days',
          'hours',
          'minutes',
        ],
      points_value: 34,
      mon: false,
      tue: false,
      wen: false, 
      thu: false,
      fri: false,
      sat: false,
      sun: false,
      items: [],
      files: [],
      rows: [],
      allrows: [],
      treeview_id: [],
      username: "",
      date: "2022-05-20",
      menu: false,
      modal: false,
      menu2: false,
      setting_id : 1,
      setting_form: [],
      uuid_rows: [],
      title_rows: [],
      book_uuid: "",
      book_title: "",
      page_list:[],
  }),

  computed: {
    formData: {
      get: function () {
        return this.$store.getters["authPageModule/getFormData"];
      },
    },
    name() {
      if (!this.formData.username) return "FLASH CARD";
      else return "FLASH CARD";
    },
  },
  async created(){
    this.username = this.$session.get('username')
      Vue.$toast.open('Please wait until loading page..');
      axios.get('http://localhost:8000/api/question_book/')
      .then(response => {
        for(var i = 0; i < response.data.length; i++)
        {
          this.items.push({text: response.data[i].file_name, icon: 'mdi-book'})
          this.uuid_rows.push(response.data[i].uuid)
          this.allrows.push(response.data[i].contents)
          this.title_rows.push(response.data[i].file_name)
        }
      });
      axios.get('http://localhost:8000/api/setting/?user_id='+this.username)
      .then(response => {
        this.setting_form.push(response.data[0])
        this.setting_id = response.data[0].id
        this.points_value = response.data[0].data.reward.point
        this.mon = response.data[0].data.plan.monday
        this.tue = response.data[0].data.plan.tuesday
        this.wen = response.data[0].data.plan.wednesday 
        this.thu = response.data[0].data.plan.thursday
        this.fri = response.data[0].data.plan.friday
        this.sat = response.data[0].data.plan.saturday
        this.sun = response.data[0].data.plan.sunday
        this.difficult_value_combo = response.data[0].data.period.difficult_unit
        this.mistake_value_combo = response.data[0].data.period.miss_unit
        this.easy_value_combo = response.data[0].data.period.easy_unit
        this.not_difficult_value_combo = response.data[0].data.period.standard_unit
        this.not_difficult_value = response.data[0].data.period.standard_num
        this.easy_value = response.data[0].data.period.easy_num
        this.mistake_value = response.data[0].data.period.miss_num
        this.difficult_value = response.data[0].data.period.difficult_num
        this.date = response.data[0].data.plan.start
      })
  },
  methods: {
    onOpen(e) {
      if (!this.__initial) {
        this.__initial = true
        return
      }
    },
    onSelected(e) {
      console.log('checkbox clicked', e)
      this.treeview_id = e
    },
    getPageList(item){
      console.log(item)
      console.log(item.children)
      console.log(item.children.length)
      if(item.children.length > 0) {
        for(var i=0; i<item.children.length; i++){
          console.log("child:"+item.children[i])
          this.getPageList(item.children[i])
        }
      }
      if(item.children.length == 0){
        if(this.treeview_id.indexOf(item.id) != -1){
          this.page_list.push(item.startPage)
        }
      }
      console.log("Result: "+this.page_list )
    },
    onClickOk() {
        this.showModal = false;
        this.showTreeviewModal = true;
        this.rows = this.allrows[this.selectedItem]
        this.book_uuid = this.uuid_rows[this.selectedItem]
        this.book_title = this.title_rows[this.selectedItem]
    },
    getImgUrl() {
      var images = require.context('../assets/img/', false, /\.jpeg$/)
      return images('./' + this.imgURL)
    },
    getAnswerUrl() {
      var images = require.context('../assets/img/', false, /\.jpeg$/)
      return images('./' + this.imgAnswerURL)
    },
    onTreeviewOk() {
      this.showTreeviewModal = false;
      console.log("ssssssssssss "+this.treeview_id)
      for(var i=0; i<this.rows.length; i++){
        this.getPageList(this.rows[i])
      }
      console.log("Result:" + this.page_list)
      this.axios
        .get('https://api/getmaxcount/?book_uuid='+this.book_uuid+'&pageList='+this.page_list)
        .then((response) => {
          this.$swal({
            title: "Success",
            text: "Your Subject was selected successfully",
            icon: "success",
            confirmButtonText: "Done",
          });
          this.page_list = []
        })
        .catch((error) => {
          this.$swal({
            title: "Oops, Something went wrong ! ",
            text: error.message,
            icon: "warning",
          });
        });
    },
    onSettingsOk() {
        //fake post request
      this.showSettingsModal = false;
      
      var temp = this.setting_form[0]
      temp.data.reward.point = this.points_value
      temp.data.plan.monday = this.mon
      temp.data.plan.tuesday = this.tue 
      temp.data.plan.wednesday = this.wen
      temp.data.plan.thursday = this.thu
      temp.data.plan.friday = this.fri
      temp.data.plan.saturday = this.sat
      temp.data.plan.sunday = this.sun
      temp.data.period.difficult_unit = this.difficult_value_combo
      temp.data.period.miss_unit = this.mistake_value_combo
      temp.data.period.easy_unit = this.easy_value_combo
      temp.data.period.standard_unit = this.not_difficult_value_combo
      temp.data.period.standard_num = this.not_difficult_value
      temp.data.period.easy_num = this.easy_value
      temp.data.period.miss_num = this.mistake_value
      temp.data.period.difficult_num = this.difficult_value
      temp.data.plan.start = this.date
      console.log(temp)
      this.axios
        .put("http://localhost:8000/api/setting/"+this.setting_id+"/", temp)
        .then((response) => {
          this.$swal({
            title: "Updated",
            text: "The Setting was updated successfully",
            icon: "success",
            confirmButtonText: "Done",
          });
        })
        .catch((error) => {
          this.$swal({
            title: "Oops, Something went wrong ! ",
            text: error.message,
            icon: "warning",
          });
        });
    },
    backToPreviousPage() {
      this.$router.back();
    },
    updateInfo() {
      //fake post request
      this.axios
        .get("https://jsonplaceholder.typicode.com/todos/1")
        .then((response) => {
          this.$swal({
            title: "Updated",
            text: "Your profile was updated successfully",
            icon: "success",
            confirmButtonText: "Done",
          });
        })
        .catch((error) => {
          this.$swal({
            title: "Oops, Something went wrong ! ",
            text: error.message,
            icon: "warning",
          });
        });
    },
  },
};
</script>

<style>
#parent { white-space: nowrap; }
.child { display: inline-block; }
.zoom {
  transition: transfrom .2s;
}
.treeview {
  flex : -1;
}
.zoom:hover {
  transform: scale(1.5);
}
.hover-zoom-image {
  width: 100%!important;
}
.dialog {
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  transition: 0.3s;
}
.dialog:hover {
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
</style>