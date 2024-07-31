<template>
  <v-list-item
    title="Change password"
    prepend-icon="mdi-key"
    @click="dialog = true"
  ></v-list-item>
  <v-dialog v-model="dialog" max-width="600">
    <v-card title="Change password">
      <template v-slot:text>
        <v-form ref="form">
          <v-text-field
            v-model="currentPassword"
            label="Current password"
            @click:append-inner="visible = !visible"
            :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
            :type="visible ? 'text' : 'password'"
            :rules="[value => value.length > 0 || 'Too short']"
            required
          ></v-text-field>
          <v-text-field
            v-model="newPassword"
            label="New password"
            @click:append-inner="visible = !visible"
            :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
            :type="visible ? 'text' : 'password'"
            :rules="[value => value.length >= 6 || 'Too short', value => value !== currentPassword || 'Please enter new password']"
            required
          ></v-text-field>
          <v-text-field
            v-if="!visible"
            v-model="confirmNewPassword"
            label="Confirm new password"
            :rules="[value => value === newPassword || 'Passwords do not match']"
            :type="visible ? 'text' : 'password'"
            required
          ></v-text-field>
        </v-form>
      </template>
      <template v-slot:actions>
        <v-btn
          text="Change password"
          color="error"
          @click="changePassword"
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
  name: "ChangePassword",
  components: {MessageSnackbar},
  data() {
    return {
      dialog: false,
      isValid: false,

      currentPassword: '',
      newPassword: '',
      confirmNewPassword: '',

      visible: false,

      showMessage: false,
      message: ''
    };
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
    async changePassword() {
      const { valid } = await this.$refs.form.validate()
      if (!valid) {
        this.message = 'Please fill out all required fields';
        this.showMessage = true;
        return;
      }
      try {
        const response = await fetch(`/api/users/${this.user.id}/password`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            currentPassword: this.currentPassword,
            newPassword: this.newPassword
          })
        })

        if (response.status === 429) {
          this.message = 'Too many failed attempts. Please try again later.';
          this.showMessage = true;
          return;
        }

        const data = await response.json();
        this.message = data.message;

      } catch (error) {
        console.error(error);
        this.message = 'Failed to change password';
      } finally {
        this.showMessage = true;
      }
    }
  }
}
</script>

<style scoped>

</style>
