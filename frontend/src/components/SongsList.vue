<template>
  <v-list>
    <v-list-item
      v-for="song in songs"
      :key="song.id"
      :title="`${song.author.name} - ${song.title}`"
      :prepend-avatar="song.author.image"
      @click="$router.push(`/authors/${song.author.id}/songs/${song.id}`)"
    >
      <template v-slot:append>
        <SongButtons
          :song="song"
        />
      </template>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: "SongsList",
  props: {
    songs: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
