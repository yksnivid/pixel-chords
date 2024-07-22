<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-card>
      <v-card-title class="headline">Sign Up</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitRegister">
          <v-text-field
            v-model="registerData.username"
            label="Username"
            required
          ></v-text-field>
          <v-text-field
            v-model="registerData.email"
            label="Email"
            required
          ></v-text-field>
          <v-text-field
            v-model="registerData.password"
            label="Password"
            type="password"
            required
          ></v-text-field>
          <v-btn type="submit" color="primary">Submit</v-btn>
          <v-alert v-if="errorMessage" type="error">{{ errorMessage }}</v-alert>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn text @click="closeDialog">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'RegisterDialog',
  props: {
    modelValue: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      dialog: false,
      registerData: {
        username: '',
        email: '',
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
    async submitRegister() {
      try {
        const response = await fetch('/api/users', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.registerData)
        });
        const data = await response.json();
        if (response.ok) {
          this.dialog = false;
          this.errorMessage = null;
        } else {
          this.errorMessage = data.error;
        }
      } catch (error) {
        this.errorMessage = 'Failed to register';
      }
    },
    closeDialog() {
      this.dialog = false;
    },
  },
};
</script>

<style scoped>
</style>
