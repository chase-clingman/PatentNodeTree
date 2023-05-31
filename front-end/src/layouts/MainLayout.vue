<template>
  <q-layout view="hHh lpR fFf">

    <q-header bordered class="bg-white text-primary">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar square>
            <img src="logo.png">
          </q-avatar>
          <q-img src="logoText.png" style="width: 200px;" class="q-ml-sm"/>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>
