<template>
  <Header />
  <v-container>
    <v-card>
      <v-card-title>{{song.author}} - {{ song.title }}</v-card-title>
      <v-card-text>
        <pre>{{ song.lyrics }}</pre>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import Header  from "@/components/Header.vue";
export default {
  name: 'Song',
  components: {
    Header
  },
  data() {
    return {
      song: {
        title: null,
        author: null,
        lyrics: null,
      },
      loading: true,
      error: undefined,
    };
  },
  async created() {
    const { author, title } = this.$route.params;
    try {
      const response = await fetch(`/api/songs/${author}/${title}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      this.song = await response.json();
    } catch (error) {
      this.error = error.message;
    } finally {
      this.loading = false;
    }
  }
};
</script>

<style scoped>
pre {
  white-space: pre-wrap;
}
</style>
