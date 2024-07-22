<template>
  <Header />
  <v-container>
    <v-card>
      <v-row justify="end" align="center" class="pa-2">
        <v-col class="px-4" cols="auto">
          <p class="heading-text">Transpose chords:</p>
        </v-col>
        <v-col class="px-4" cols="auto">
          <v-btn-toggle rounded dense group>
            <v-btn text icon="mdi-minus" small />
            <v-btn text icon="mdi-plus" small />
          </v-btn-toggle>
        </v-col>
      </v-row>
      <v-card-title>{{song.author}} - {{ song.title }}</v-card-title>
      <v-card-text>
        <div v-html="formattedSong"></div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import Header  from "@/components/Header.vue";
import ChordSheetJS from 'chordsheetjs';

const formatter = new ChordSheetJS.HtmlTableFormatter;
const parser = new ChordSheetJS.ChordsOverWordsParser();

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
        lyrics: '',
      },
      loading: true,
      error: undefined
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
  },
  computed: {
    formattedSong() {
      return formatter.format(parser.parse(this.song.lyrics));
    }
  }
};
</script>

<style>
    .chord {
        color: #e89380; /* Цвет аккорда */
    }
    .row .lyrics {
        white-space: pre;
        display: contents;
    }
    .row .chord {
        white-space: pre;
        display: table-cell;
    }
</style>
