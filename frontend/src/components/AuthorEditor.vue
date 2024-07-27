<template>
  <v-dialog
    :model-value="editorDialog"
    fullscreen
  >
    <v-container>
      <v-card :title="author.name">
        <template v-slot:title>
          <v-text-field v-model="author.name" label="Name" density="compact" hide-details />
        </template>
        <template v-slot:prepend>
          <v-avatar
            class="cursor-pointer"
          ></v-avatar>
        </template>
        <template v-slot:append>
          <v-btn
            icon="mdi-content-save"
            variant="plain"
            :disabled="author.name.length < 1 || author.about.length < 1"
            @click.stop="addAuthor"
          ></v-btn>
          <v-btn
            icon="mdi-close"
            size="small"
            variant="plain"
            @click.stop="$emit('update:modelValue', false)"
          ></v-btn>
        </template>
        <v-textarea v-model="author.about" rows="15" :style="{'font-family': 'monospace'}"></v-textarea>
      </v-card>
    </v-container>
    <v-snackbar v-model="showMessage" timeout="3000">
      {{ message }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showMessage = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-dialog>
</template>

<script>
export default {
  name: "AuthorEditor",
  props: {
    editorDialog: false
  },
  data() {
    return {
      author: {
        name: '',
        about: '',
        image: ''
      },
      showMessage: false,
      message: null
    };
  },
  methods: {
    async addAuthor() {
      try {
        const response = await fetch('/api/authors', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.author)
        })
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.message = data.message;
        this.$router.push(`/authors/${data.id}`)
      } catch (error) {
        this.message = error.message;
      } finally {
        this.showMessage = true;
      }
    }
  }
}
</script>

<style scoped>

</style>
