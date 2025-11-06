<template>
  <router-view />
</template>

<style>
:root {
  --burgundy:#7a1732;
  --burgundy-700:#5f1227;
  --gray-50:#f6f7f8; 
  --gray-200:#e5e7eb; 
  --gray-500:#6b7280; 
  --gray-800:#1f2937;
  --white:#ffffff; 
  --radius:14px; 
  --shadow:0 8px 24px rgba(0,0,0,.08); 
  --container:1180px;
}

* {
  box-sizing:border-box;
  margin:0;
  padding:0
}

html, body {
  height:100%;
  font-size:16px;
  line-height:1.5

}
body {
  margin:0;
  font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  color:var(--gray-800);
  background:linear-gradient(0deg,var(--gray-50),#ffffff);

}
.container {
  max-width:var(--container);
  margin:0 auto;
  padding:0 20px
}
</style>