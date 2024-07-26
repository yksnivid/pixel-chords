<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title class="headline">Sign In</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitLogin">
          <v-text-field
            v-model="loginData.username"
            label="Username"
            required
          ></v-text-field>
          <v-text-field
            v-model="loginData.password"
            label="Password"
            type="password"
            required
          ></v-text-field>
          <v-btn type="submit" color="primary">Login</v-btn>
        </v-form>
      </v-card-text>
      <v-card-text v-if="errorMessage">
        <v-alert type="error">{{ errorMessage }}</v-alert>
      </v-card-text>
      <v-card-text>
        <v-row class="px-5" align="center" justify="space-between">
            Not registered yet?
            <v-btn text color="success" @click="openRegisterDialog">Sign Up</v-btn>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeDialog">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <register-dialog v-model="registerDialog"></register-dialog>
</template>

<script>
import { mapActions } from 'vuex';
import RegisterDialog from './RegisterDialog.vue';

export default {
  name: 'LoginDialog',
  components: {
    RegisterDialog,
  },
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      dialog: false,
      registerDialog: false,
      loginData: {
        username: '',
        password: '',
      },
      errorMessage: null,
    };
  },
  watch: {
    modelValue(val) {
      this.dialog = val;
    },
    dialog(val) {
      this.$emit('update:modelValue', val);
    },
  },
  methods: {
    ...mapActions(['login']),
    async submitLogin() {
      const result = await this.login(this.loginData);
      if (result.success) {
        this.dialog = false;
        this.errorMessage = null;
      } else {
        this.errorMessage = result.error;
      }
    },
    closeDialog() {
      this.dialog = false;
    },
    openRegisterDialog() {
      this.dialog = false;
      this.registerDialog = true;
    },
  },
};
</script>

<style scoped>
</style>
