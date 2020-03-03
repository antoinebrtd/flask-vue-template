<template>
    {% raw %}
    <v-container fluid class="pa-0">
        <v-row no-gutters justify="center" align="center">
            <v-col cols="12" class="mb-5">
                <div class="tree-container">
                    <v-row align="start" justify="center">
                        <v-col cols="12" class="my-5">
                            <v-card color="transparent" class="text-center" elevation="0">
                                <v-card-text class="font-weight-bold primary--text display-1 appear">
                                    Your app's architecture
                                </v-card-text>
                            </v-card>
                        </v-col>
                        <v-col cols="3" class="mt-5">
                            <v-row align="start" justify="start" class="tree">
                                <v-fade-transition>
                                    <v-treeview
                                            v-if="displayTree"
                                            :open.sync="open"
                                            :items="tree"
                                            activatable
                                            item-key="id"
                                            open-on-click
                                            dense
                                            hoverable
                                            shaped
                                            transition
                                            dark
                                            :active.sync="selected"
                                            return-object
                                            class="appear"
                                    >
                                        <template v-slot:prepend="{ item, open }">
                                            <v-icon v-if="!item.file">
                                                {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
                                            </v-icon>
                                            <v-icon v-else>
                                                {{ files[item.file] }}
                                            </v-icon>
                                        </template>
                                    </v-treeview>
                                </v-fade-transition>
                            </v-row>
                        </v-col>
                        <v-col cols="5" style="height: 100%" class="mt-5">
                            <v-card class="hint mx-5 pa-5 appear" elevation="5">
                                <v-card-actions>
                                    <v-select :items="folders" v-model="folder" @change="easeGetTree"
                                              label="Select a folder"></v-select>
                                </v-card-actions>
                                <v-card-text v-if="selected.length === 0">Select a file to see some hints
                                </v-card-text>
                                <v-card-text v-else class="primary--text title">{{ selected[0].description }}
                                </v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>
                </div>
            </v-col>
            <v-col cols="12" class="mt-5">
                <v-card class="text-center" color="transparent" elevation="0">
                    <v-card-text class="display-1 font-weight-bold">Your options</v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
    {% endraw %}
</template>

<script>
    import axios from 'axios';
    import notifications from '@/modules/notifications';

    export default {
        name: "About",
        data() {
            return {
                displayTree: false,
                files: {
                    docker: 'mdi-docker',
                    py: 'mdi-language-python',
                    html: 'mdi-language-html5',
                    js: 'mdi-language-javascript',
                    json: 'mdi-json',
                    md: 'mdi-markdown',
                    pdf: 'mdi-file-pdf',
                    ico: 'mdi-file-image',
                    png: 'mdi-file-image',
                    jpg: 'mdi-file-image',
                    txt: 'mdi-file-document-outline',
                    env: 'mdi-file-settings-variant',
                    vue: 'mdi-vuejs',
                },
                tree: null,
                selected: [],
                open: [],
                folders: [
                    {text: 'Back end', value: 'back'},
                    {text: 'Front end', value: 'front'}
                ],
                folder: null
            }
        },
        mounted() {
            this.folder = this.folders[0].value;
            this.getTree();
        },
        methods: {
            easeGetTree() {
                this.open = [];
                this.selected = [];
                setTimeout(() => {
                    this.getTree()
                }, 500)
            },
            getTree() {
                this.displayTree = false;
                axios.get(process.env.VUE_APP_API_URL + '/tree', {params: {folder: this.folder}}).then(response => {
                    if (response.data.msg === 'success') {
                        this.tree = response.data.tree;
                        this.open.push(this.tree[0].id);
                        this.displayTree = true
                    }
                }).catch(error => {
                    notifications.addNotification('An error occurred');
                    this.tree = [];
                    this.displayTree = true;
                })
            }
        }
    }
</script>

<style scoped>
    .tree-container {
        padding-top: 120px;
        padding-bottom: 60px;
        background-image: url('../assets/grey_background.jpeg');
        -webkit-clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%);
        clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%);
    }

    .tree::-webkit-scrollbar {
        display: none;
    }

    @media (max-height: 900px) {
        .tree {
            overflow-y: scroll;
            max-height: 490px;
            min-height: 450px;
            -ms-overflow-style: none;
        }
    }

    @media (min-height: 901px) {
        .tree {
            overflow-y: scroll;
            max-height: 650px;
            min-height: 450px;
            -ms-overflow-style: none;
        }

    }

    .appear {
        transition: visibility 0.2s, opacity 0.4s linear;
    }

    .hint {
        border-radius: 10px;
        height: 100%;
        margin-top: 80px;
    }
</style>