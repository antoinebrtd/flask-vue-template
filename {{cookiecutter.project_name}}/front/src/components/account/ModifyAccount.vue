<template>
    {% raw %}
    <v-row justify="center" align="center" style="height: 100%">
        <v-col cols="6" class="py-0">

            <v-avatar :size="140" color="secondary">
                <img v-if="user.profile.picture" :src="user.profile.picture" :alt="user.profile.name">
                <v-icon v-else large color="white">account_circle</v-icon>
                <upload-button
                        buttonId="picture"
                        :tooltip="!user.profile.picture ? 'Upload a profile picture' : 'Change your profile picture'"
                        :icon="!user.profile.picture ? 'add' : 'edit'"
                        :upload="changeProfilePicture"
                        color="primary"
                        fab absolute bottom right small
                ></upload-button>
            </v-avatar>

            <v-card color="transparent" elevation="0">
                <v-card-text class="display-1 white--text mb-5">{{ user.profile.name }}</v-card-text>

                <v-card-text class="text-start" v-for="field in fields" :key="field.field">
                    <v-row dense>
                        <v-col cols="8">
                            <span class="primary--text font-weight-light">{{ field.text }}</span>
                        </v-col>
                        <v-col cols="4" class="py-0">
                            <v-row dense justify="end" align="center" v-if="!field.modify">
                                <v-btn icon text small @click="field.modify = true">
                                    <v-icon small color="white">
                                        edit
                                    </v-icon>
                                </v-btn>
                            </v-row>
                            <v-row dense justify="end" align="center" v-else>
                                <v-btn icon text small
                                       @click="field.modify = false; field.value = user.profile[field.field]">
                                    <v-icon small color="error">
                                        cancel
                                    </v-icon>
                                </v-btn>
                                <v-btn icon text small @click="updateField(field)" :disabled="!field.value">
                                    <v-icon small color="primary">
                                        save
                                    </v-icon>
                                </v-btn>
                            </v-row>
                        </v-col>
                    </v-row>
                    <v-divider color="white" class="mb-3"></v-divider>
                    <v-text-field
                            v-if="field.modify"
                            v-model="field.value"
                            dark
                            clearable
                            class="my-0 py-0 title"
                    ></v-text-field>
                    <span class="white--text title" v-else>{{ user.profile[field.field] }}</span>
                </v-card-text>

                <v-card-text class="text-start pb-0">
                    <v-row dense>
                        <v-col cols="8">
                            <span class="primary--text font-weight-light">Email</span>
                        </v-col>
                        <v-col cols="4" class="py-0">
                            <v-row dense justify="end" align="center">
                                <v-btn icon text small>
                                    <v-icon small color="white">
                                        edit
                                    </v-icon>
                                </v-btn>
                            </v-row>
                        </v-col>
                    </v-row>
                    <v-divider color="white" class="mb-3"></v-divider>
                    <v-row align="center">
                        <v-col cols="8" class="pt-0">
                            <span class="white--text title">{{ user.profile.email }}</span>
                        </v-col>
                        <v-col cols="4" class="pt-0">
                            <v-row align="center" justify="end">
                                <v-icon v-if="user.account_activated" small color="tertiary" class="mr-3">verified_user</v-icon>
                            </v-row>
                        </v-col>
                    </v-row>
                </v-card-text>

                <v-card-text class="text-start pb-0">
                    <v-row dense>
                        <v-col cols="8">
                            <span class="primary--text font-weight-light">Password</span>
                        </v-col>
                        <v-col cols="4" class="py-0">
                            <v-row dense justify="end" align="center">
                                <v-btn icon text small>
                                    <v-icon small color="white">
                                        edit
                                    </v-icon>
                                </v-btn>
                            </v-row>
                        </v-col>
                    </v-row>
                    <v-divider color="white" class="mb-3"></v-divider>
                    <span class="white--text title">
                                <v-icon v-for="i in [1, 2, 3, 4, 5, 6, 7, 8]" :key="i" small color="white">fiber_manual_record</v-icon>
                            </span>
                </v-card-text>
            </v-card>

        </v-col>
    </v-row>
    {% endraw %}
</template>

<script>
    import axios from 'axios';
    import notifications from '@/modules/notifications';
    import UploadButton from "../util/UploadButton";

    export default {
        name: "ModifyAccount",
        components: {UploadButton},
        props: {
            user: Object,
            updateUser: Function
        },
        data() {
            return {
                uploadingPicture: false,
                fields: [
                    {
                        text: 'First name',
                        value: null,
                        modify: false,
                        field: 'first_name'
                    },
                    {
                        text: 'Last name',
                        value: null,
                        modify: false,
                        field: 'last_name'
                    }
                ],
            }
        },
        mounted() {
            for (let i = 0; i < this.fields.length; i++) {
                this.fields[i].value = this.user.profile[this.fields[i].field]
            }
        },
        methods: {
            updateField(field) {
                axios.patch(process.env.VUE_APP_API_URL + `/users/${this.user.profile.id}`,
                    {value: field.value},
                    {params: {field: field.field}}
                ).then(response => {
                    if (response.data.msg === 'success') {
                        this.$emit('update', response.data.user);
                        field.modify = false
                    }
                }).catch(error => {
                    if (error.response) {
                        notifications.addNotification(error.response.data.error);
                    } else {
                        notifications.addNotification('We\'re sorry, an error occurred')
                    }
                    field.modify = false
                })
            },
            changeProfilePicture(file) {
                this.uploadingPicture = true;
                let formData = new FormData();
                formData.append('file', file);
                axios.patch(process.env.VUE_APP_API_URL + `/users/${this.user.profile.id}/profile-picture`, formData,
                    {headers: {'Content-Type': 'multipart/form-data'}}).then((response) => {
                    if (response.data.msg === 'success') {
                        this.$emit('update', response.data.user);
                        this.uploadingPicture = false;
                    }
                }).catch(error => {
                    this.uploadingPicture = false;
                    if (error.response) {
                        notifications.addNotification(error.response.data.error);
                    } else {
                        notifications.addNotification('We\'re sorry, an error occurred')
                    }
                })
            }
        }
    }
</script>

<style scoped>

</style>