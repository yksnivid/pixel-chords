<template>
  <v-row justify="center" no-gutters>
    <v-col cols="12">
      <h1>404 Not Found</h1>
    </v-col>
    <v-col cols="12" class="px-10">
      <p>The page you are looking for does not exist.</p>
    </v-col>
    <v-col cols="12">
<pre>
/\_/\
( o.o )
> ^ <
</pre>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "NotFound"
}
</script>

<style scoped>
div {
  text-align: center;
  margin-top: 50px;
  font-family: 'Courier New', Courier, monospace;
}

pre {
  font-size: 48px;
  line-height: 1.1;
  margin: 0 auto;
  font-family: 'Courier New', Courier, monospace;
}
</style>
