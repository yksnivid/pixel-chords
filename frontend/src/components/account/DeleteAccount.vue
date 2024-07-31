<template>
  <v-list-item title="Delete account" prepend-icon="mdi-delete" @click="dialog = true"/>
  <v-dialog v-model="dialog" max-width="600">
    <v-card title="Delete account">
      <template v-slot:text>
        <v-form ref="form">
          <div class="pb-4">Are you sure you want to delete account?</div>
          <v-text-field
            v-model="password"
            label="Password"
            :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
            :type="visible ? 'text' : 'password'"
            :rules="[value => value.length >= 6 || 'Too short']"
            required
            @click:append-inner="visible = !visible"
          ></v-text-field>
        </v-form>
      </template>
      <template v-slot:actions>
        <v-btn
          text="Yes, delete"
          @click="deleteAccount"
          color="error"
        ></v-btn>
        <v-btn
          text="No"
          @click="dialog = false"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
  <MessageSnackbar v-model="showMessage" :message="message" />
</template>

<script>
import {mapGetters} from "vuex";
import MessageSnackbar from "@/components/MessageSnackbar.vue";

export default {
  name: "DeleteAccount",
  components: {MessageSnackbar},
  data() {
    return {
      dialog: false,

      password: '',
      visible: false,

      showMessage: false,
      message: ''
    }
  },
  computed: {
    ...mapGetters(['user'])
  },
  methods: {
    async deleteAccount() {
      const { valid } = await this.$refs.form.validate()
      if (!valid) {
        this.message = 'Please fill out all required fields';
        this.showMessage = true;
        return;
      }
      try {
        const response = await fetch(`/api/users/${this.user.id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            password: this.password
          })
        })
        const data = await response.json();
        if (response.ok) {
          await this.logout();
        } else {
          this.showMessage = true;
          this.message = data.message;
        }
      } catch (error) {
        console.error(error);
        this.showMessage = true;
        this.message = 'Failed to delete account. Please try again later.';
      }
    }
  }
}
</script>

<style scoped>

</style>
