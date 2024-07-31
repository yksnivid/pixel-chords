<template>
  <v-list-item
    title="Change email"
    prepend-icon="mdi-key"
    @click="dialog = true"
  ></v-list-item>
  <v-dialog v-model="dialog" max-width="600">
    <v-card title="Change email">
      <template v-slot:text>
        <v-text-field
          v-model="user.email"
          append-inner-icon="mdi-pencil"
          readonly
        ></v-text-field>
        Work in progress...
      </template>
      <template v-slot:actions>
        <v-btn
          text="Change email"
          color="error"
          disabled
        ></v-btn>
        <v-btn
          text="Close"
          @click="dialog = false"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
  <MessageSnackbar v-model="showMessage" :message="message" />

</template>

<script>
import MessageSnackbar from "@/components/MessageSnackbar.vue";
import {mapGetters} from "vuex";

export default {
  name: "ChangeEmail",
  components: {MessageSnackbar},
  data() {
    return {
      dialog: false,

      showMessage: false,
      message: ''
    };
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
  }
}
</script>

<style scoped>

</style>
