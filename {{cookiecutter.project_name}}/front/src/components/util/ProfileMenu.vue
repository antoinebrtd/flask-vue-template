<template>
    {% raw %}
    <v-slide-x-transition>
        <v-menu v-model="menu" :close-on-content-click="false" :nudge-width="250" offset-x offset-y>
            <template v-slot:activator="{ on }">
                <v-btn v-on="on" fab icon small>
                    <v-avatar :size="36">
                        <img v-if="user.profile.picture" :src="user.profile.picture" :alt="user.profile.name">
                        <v-icon v-else large :color="transparentHeader ? 'white' : ''">account_circle</v-icon>
                    </v-avatar>
                </v-btn>
            </template>

            <v-list>
                <v-list-item @click="$router.replace(`/accounts/${user.profile.id}`)" class="py-1">
                    <v-list-item-avatar size="30" class="ml-2">
                        <img v-if="user.profile.picture" :src="user.profile.picture"
                             :alt="user.profile.name">
                        <v-icon v-else large>account_circle</v-icon>
                    </v-list-item-avatar>

                    <v-list-item-group>
                        <v-list-item-group>My account</v-list-item-group>
                    </v-list-item-group>
                    <v-spacer></v-spacer>
                    <v-list-item-icon>
                        <v-icon v-if="user.accountActivated" small color="tertiary">verified_user</v-icon>
                    </v-list-item-icon>
                </v-list-item>
                <v-divider color="primary"></v-divider>
                <v-list-item @click="$router.replace('/settings')">
                    <v-list-item-icon>
                        <v-icon small color="primary" class="ml-4">settings</v-icon>
                    </v-list-item-icon>
                    <v-list-item-group>
                        <v-list-item-group>Settings</v-list-item-group>
                    </v-list-item-group>
                </v-list-item>
                <v-list-item @click="logout">
                    <v-list-item-icon>
                        <v-icon small color="error" class="ml-4">logout</v-icon>
                    </v-list-item-icon>
                    <v-list-item-group>
                        <v-list-item-group>Logout</v-list-item-group>
                    </v-list-item-group>
                </v-list-item>
            </v-list>
        </v-menu>
    </v-slide-x-transition>
    {% endraw %}
</template>

<script>
    import auth from "@/modules/auth";

    export default {
        name: "ProfileMenu",
        props: {
            transparentHeader: Boolean
        },
        data() {
            return {
                user: auth.user,
                menu: false
            }
        },
        methods: {
            logout() {
                auth.logout();
            },
        }
    }
</script>

<style scoped>

</style>
