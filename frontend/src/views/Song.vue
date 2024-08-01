<template>
  <Header />
  <v-container>
    <v-card v-if="!loading" :subtitle="song.author.name">
      <template v-slot:title>
        <div v-if="!editMode">{{ song.title }}</div>
        <v-text-field v-else v-model="editor.title" density="compact" hide-details />
      </template>
      <template v-slot:prepend>
        <v-avatar
          :image="song.author.image"
          class="cursor-pointer"
          @click="$router.push(`/authors/${song.author.id}`)"
        ></v-avatar>
      </template>
      <template v-slot:append>
        <SongButtons v-if="!editMode" :song="song" />
        <div v-if="user.isAdmin">
          <v-btn
            v-if="editMode"
            icon="mdi-content-save"
            variant="plain"
            @click.stop="updateSong"
          ></v-btn>
          <v-btn
            :icon="editMode ? 'mdi-close' : 'mdi-pencil'"
            size="small"
            variant="plain"
            @click.stop="handleEditMode"
          ></v-btn>
        </div>
      </template>
      <v-card-text v-if="!editMode" class="text-justify">
        <v-btn-group class="ma-1" density="comfortable" rounded variant="outlined">
          <v-btn
            icon="mdi-minus"
            @click="changeTransposeSemitones(-1)"
            :readonly="song.transposeSemitones <= -12"
          ></v-btn>
          <v-btn
            text
            readonly
          >Transpose: {{ song.transposeSemitones > 0 ? '+' + song.transposeSemitones : song.transposeSemitones }}</v-btn>
          <v-btn
            icon="mdi-plus"
            @click="changeTransposeSemitones(1)"
            :readonly="song.transposeSemitones >= 12"
          ></v-btn>
        </v-btn-group>
        <v-btn-group class="ma-1" density="comfortable" rounded variant="outlined">
          <v-btn
            icon="mdi-minus"
            @click="fontSize -= 1"
          ></v-btn>
          <v-btn
            text
            readonly
          >Font size: {{ fontSize }}</v-btn>
          <v-btn
            icon="mdi-plus"
            @click="fontSize += 1"
          ></v-btn>
        </v-btn-group>
        <v-btn-group class="ma-1" density="comfortable" rounded variant="outlined">
          <v-btn
            icon="mdi-minus"
            :readonly="song.capoPosition < 1"
            @click="changeCapoPosition(-1)"
          ></v-btn>
          <v-btn
            text
            readonly
          >Capo: {{ song.capoPosition }}</v-btn>
          <v-btn
            icon="mdi-plus"
            :readonly="song.capoPosition >= 12"
            @click="changeCapoPosition(1)"
          ></v-btn>
        </v-btn-group>
      </v-card-text>
      <v-card-text :style="{ fontSize: fontSize + 'px' }" v-if="!editMode">
        <div v-html="formattedSong"></div>
      </v-card-text>
      <v-textarea v-else v-model="song.lyrics" rows="15" :style="{'font-family': 'monospace'}"></v-textarea>
    </v-card>
    <v-progress-circular
      v-else
      indeterminate
      color="primary"
    ></v-progress-circular>
  </v-container>
  <v-snackbar v-model="showMessage" timeout="3000">
    {{ message }}
    <template v-slot:actions>
      <v-btn variant="text" @click="showMessage = false">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import { mapGetters } from "vuex";
import Header from "@/components/Header.vue";
import SongButtons from "@/components/SongButtons.vue";
import ChordSheetJS from 'chordsheetjs';
import { debounce } from '@/utils/debounce.js';

const formatter = new ChordSheetJS.HtmlDivFormatter();
const parser = new ChordSheetJS.ChordsOverWordsParser();

export default {
  name: 'Song',
  components: {
    Header,
    SongButtons
  },
  data() {
    return {
      song: {
        id: null,
        title: null,
        lyrics: '',
        author: {
          id: null,
          name: null,
          image: null
        },
        capoPosition: 0,
        transposeSemitones: 0,
        isFavorite: false
      },

      editor: {
        title: '',
        lyrics: ''
      },
      editMode: false,

      fontSize: 16,
      loading: true,
      error: undefined,
      showMessage: false,
      message: null
    };
  },
  async created() {
    await this.loadSong(this.$route.params.song_id);
    this.debouncedSaveSongSettings = debounce(this.saveSongSettings, 1000);
  },
  beforeRouteUpdate(to, from, next) {
    this.loadSong(to.params.song_id);
    next();
  },
  computed: {
    ...mapGetters(['user']),
    formattedSong() {
      const song = parser.parse(this.song.lyrics);
      const songTransposed = song.transpose(this.song.transposeSemitones);
      return formatter.format(songTransposed);
    }
  },
  methods: {
    async loadSong(songId) {
      this.loading = true;
      try {
        const response = await fetch(`/api/songs/${songId}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.song = await response.json();

        if (!this.user.isLoggedIn) {
          const savedTranspose = localStorage.getItem(`song_${songId}_transpose`);
          const savedCapo = localStorage.getItem(`song_${songId}_capo`);
          if (savedTranspose !== null) {
            this.song.transposeSemitones = parseInt(savedTranspose);
          }
          if (savedCapo !== null) {
            this.song.capoPosition = parseInt(savedCapo);
          }
        }

      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    async updateSong() {
      try {
        const response = await fetch(`/api/songs/${this.song.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: this.editor.title,
            lyrics: this.editor.lyrics
          })
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        this.message = 'Song updated successfully';
        console.log('Song updated successfully, song id:', this.song.id);
        await this.loadSong(this.song.id);
      } catch (error) {
        this.message = 'Error while editing song';
        console.error('Error while updating song:', error);
      } finally {
        this.showMessage = true;
        this.editMode = false;
      }
    },
    async saveSongSettings() {
      if (this.user.isLoggedIn) {
        try {
          await fetch(`/api/users/${this.user.id}/songs/${this.song.id}/settings`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              transposeSemitones: this.song.transposeSemitones,
              capoPosition: this.song.capoPosition
            })
          });
        } catch (error) {
          console.error('Error while saving transpose:', error);
        }
      } else {
        localStorage.setItem(`song_${this.song.id}_transpose`, this.song.transposeSemitones);
        localStorage.setItem(`song_${this.song.id}_capo`, this.song.capoPosition);
      }
    },
    changeTransposeSemitones(amount) {
      this.song.transposeSemitones += amount;
      this.debouncedSaveSongSettings();
    },
    changeCapoPosition(amount) {
      this.song.capoPosition += amount;
      this.debouncedSaveSongSettings();
    },
    handleEditMode() {
      this.editMode = !this.editMode;
      if (this.editMode === true) {
        this.editor.title = this.song.title;
        this.editor.lyrics = this.song.lyrics;
      }
    }
  }
};
</script>

<style>

.paragraph {
  font-family: monospace;
}

.paragraph .row {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: flex-start;
}

/*.chord:empty {*/
/*  padding-right: 10px;*/
/*}*/

.lyrics:empty {
  padding-right: 10px;
}

.chord {
  border-radius: 10px;
  background-color: #ffe8f1;
  color: #ff81b1;
  padding: 0px 7px;
  display: inline-block;
}

.chord:after {
  /*content: '\200b';*/
}

.lyrics:after {
  content: '\200b';
}

</style>
