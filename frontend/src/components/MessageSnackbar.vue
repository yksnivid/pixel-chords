<template>
  <v-snackbar
    :model-value="modelValue"
    @update:modelValue="$emit('update:modelValue', false)"
  >
    {{ message }}
    <template v-slot:actions>
      <v-btn variant="text" @click="$emit('update:modelValue', false)">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  name: "MessageSnackbar",
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    message: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>

</style>
