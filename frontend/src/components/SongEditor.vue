<template>
  <v-dialog
    :model-value="editorDialog"
    fullscreen
  >
    <v-container>
      <v-card :subtitle="author.name">
        <template v-slot:title>
          <v-text-field v-model="song.title" label="Title" density="compact" hide-details />
        </template>
        <template v-slot:prepend>
          <v-avatar
            :image="author.image"
            class="cursor-pointer"
            @click="$router.push(`/authors/${author.id}`)"
          ></v-avatar>
        </template>
        <template v-slot:append>
          <v-btn
            icon="mdi-content-save"
            variant="plain"
            :disabled="song.title.length < 1 || song.lyrics.length < 1"
            @click.stop="addSong"
          ></v-btn>
          <v-btn
            icon="mdi-close"
            size="small"
            variant="plain"
            @click.stop="$emit('update:modelValue', false)"
          ></v-btn>
        </template>
        <v-textarea v-model="song.lyrics" rows="15" :style="{'font-family': 'monospace'}"></v-textarea>
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
  name: "SongEditor",
  props: {
    author: {
      type: Object,
      required: true
    },
    editorDialog: undefined
  },
  data() {
    return {
      song: {
        id: null,
        title: '',
        lyrics: ''
      },
      message: null,
      showMessage: false
    }
  },
  methods: {
    async addSong() {
      try {
        const response = await fetch(`/api/songs`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            author_id: this.author.id,
            title: this.song.title,
            lyrics: this.song.lyrics
          })
        })
        const data = await response.json()
        this.message = data.message;
        this.$router.push(`/authors/${this.author.id}/songs/${data.id}`)
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
