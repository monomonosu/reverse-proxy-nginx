Vue.component('sc-upload', {
    template:
    `
    <div>
        <!-- アップロード機能　-->
        <b-row>
            <b-col md="3">
                <b-form @submit="uploadFile" id="upform">
                    <b-input-group block>
                        <b-button pill type="submit" class="mr-3">
                            <span v-if="!isUploading">確定</span>
                            <b-spinner v-else label="Spinning" small></b-spinner>
                        </b-button>
                        <b-form-file v-model="form.file" size="lg" browse-text="+"
                            placeholder="クリックまたはドラッグ..." drop-placeholder="Drop file here...">
                        </b-form-file>
                    </b-input-group>
                </b-form>        
            </b-col>
            <b-col>
                <template v-if="uploadListMode=='list'">
                    <b-table-simple hover small caption-top responsive class="box">
                        <template v-for="f in dicFiles">
                            <b-tr>
                                <b-td width="5%">
                                    <input type="checkbox" v-model="f.isSelect" size="sm">
                                </b-td>
                                <b-td width="15%">
                                    <div @click="selectImgUrl=f.url">
                                        <b-img :src="f.urlThumb" width="90" fluid></b-img>
                                    </div>
                                </b-td>
                                <b-td class="ml-5">{{f.filename}}</b-td>
                            </b-tr>
                        </template>
                    </b-table-simple>
                </template>
                <template v-if="uploadListMode=='card'">
                    <div class="file-card ">
                        <template v-for="f in dicFiles">
                            <b-card border-variant="light">
                                <b-img :src="'../'+f.thumbPath" width="90" fluid></b-img>
                                <input type="checkbox" v-model="f.isSelect"
                                    class="image-in-check">
                            </b-card>
                            <!--
                                    <b-card style="width: 5rem;" 
                                        :img-src= "'../'+f.thumbPath"
                                        img-top
                                    >
                                        <input type="checkbox" v-model="f.isSelect" class="image-in-check"> 
                                    </b-card>
                                -->
                        </template>
                    </div>
                </template>
            </b-col>
            <b-col md="1">
                <b-button @click="deleteFiles(invoice.applyNumber)" class="mr-2 mb-3"><i
                        class="fas fa-trash-alt"></i>
                </b-button>
                <b-button v-if="uploadListMode=='list'" @click="uploadListMode='card'"
                    class="mr-2">
                    card</b-button>
                <b-button v-if="uploadListMode=='card'" @click="uploadListMode='list'"
                    class="mr-2">
                    list</b-button>
            </b-col>
        </b-row>    <!--アップロード機能ここまで-->
    </div>
    `,
    data: function(){
        return {
            isResult: '', // nonuse
            dicFiles: [],
            form: {
                file: '',
                fileId: ''
            },
            uploadListMode: 'card', //list,card
            isUploading: false    
        }
    },
    props: {
        modalName: String, // no use
        modalMessage: String, //nouse
        fileId: String
    },
    methods: {
        select() {
            this.$emit("selected", isResult);
        },
        //focusOK() {
        //    this.$refs.focusThis.focus();
        //},
                    //---- upload funcrions --
        getFileList: async function (fid) {
            self = this;
            url = "list-files/s/upload/" + fid;
            await axios.get(url)
                .then(function (response) {
                    console.log(response.data);
                    self.dicFiles = response.data;
                })
        },
        clearFileList: function () {
            this.dicFiles = {};
        },
        uploadFile: async function (event) {
            self = this;
            event.preventDefault();
            this.isUploading = true;
            let files = event.target.files;
            const formData = new FormData();
            formData.append('file', self.form.file);
            formData.append('fileId', self.fileId);
            await axios.post("upload-files/s/upload", formData)
                .then((res) => {
                    self.getFileList(self.fileId);
                })
                .catch((err) => {
                    console.log(err)
                });
            this.isUploading = false;

        },
        deleteFiles: async function (fid) {
            self = this;
            url = "delete-files/s";
            await axios.delete(url, {
                data: self.dicFiles
            }
            ).then(function (response) {
                console.log(response.data);
                self.getFileList(fid);
            });
        },
        // ---- end upload functions -----   
    },
    mounted: function(){
        console.log(this.fileId)
        this.getFileList(this.fileId);
    }
})
