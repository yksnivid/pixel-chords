<template>
  <v-dialog
    :model-value="modelValue"
    max-width="600"
  >
    <v-card
      :text='`Are you sure you want to delete song "${song.title}"?`'
      title="Delete song"
    >
      <template v-slot:actions>
        <v-btn
          text="Yes, delete"
          @click="deleteSong"
          color="error"
        ></v-btn>
        <v-btn
          text="No"
          @click="$emit('update:modelValue', false)"
        ></v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "DeleteSongDialog",
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    song: {
      type: Object,
      required: true
    }
  },
  methods: {
    async deleteSong() {
      try {
        const response = await fetch(`/api/songs/${this.song.id}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (!response.ok) {
          throw new Error('Failed to delete song');
        }
        console.log('Deleted song:', this.song.id);
        this.$emit('update:modelValue', false);
        this.$router.go();
      } catch (error) {
        console.error('Error while deleting song:', error);
      }
    },
  }
}
</script>

<style scoped>

</style>
