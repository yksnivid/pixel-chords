<template>
  <Header />
  <v-container fluid>
    <v-card title="Favorites">
     <v-tabs v-model="tab" align-tabs="center">
      <v-tab>
        <template v-slot="prepend">
          Songs <v-chip class="mx-2" size="small"> {{songs.length}} </v-chip>
        </template>
      </v-tab>
      <v-tab>
        <template v-slot="prepend">
          Authors <v-chip class="mx-2" size="small"> {{authors.length}} </v-chip>
        </template>
      </v-tab>
     </v-tabs>
     <v-tabs-window v-model="tab">
       <v-tabs-window-item value="songs">
          <SongsList :songs="songs" />
       </v-tabs-window-item>
       <v-tabs-window-item value="authors">
         <AuthorsList :authors="authors"/>
       </v-tabs-window-item>
     </v-tabs-window>
    </v-card>
  </v-container>
</template>

<script>
import Header from "@/components/Header.vue";
import SongsList from "@/components/SongsList.vue";
import { mapGetters } from 'vuex';
import AuthorsList from "@/components/AuthorsList.vue";

export default {
  name: "Favorites",
  components: {AuthorsList, SongsList, Header},
  data() {
    return {
      songs: [],
      authors: [],
      tab: 'songs'
    }
  },
  computed: {
   ...mapGetters(['user'])
  },
  created() {
    this.fetchFavorites();
  },
  methods: {
    async fetchFavorites() {
      const response = await fetch(`/api/users/${this.user.id}/favorites`);
      const data = await response.json();
      this.songs = data.songs;
      this.authors = data.authors;
    }
  }
}
</script>

<style scoped>

</style>
