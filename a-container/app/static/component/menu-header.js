Vue.component('menu-header', {
    template: `
    <div>
        <b-card class="fixed-top header" style="background: rgba(255,255,255,0.5);">
            <b-row>
                <b-col></b-col>
                <b-col cols="11">
                    <b-row>
                        <b-col>
                            <router-link to="?page=store">
                                <b-button pill variant="success" class="mr-3" @click="mainAddRow();">＋新規作成
                                </b-button>
                            </router-link>
                        </b-col>
                        <b-col class="text-right">
                            <sc-menu v-if="modeName!='mw'"></sc-menu>
                        </b-col>
                    </b-row>
                </b-col>
                <b-col></b-col>
            </b-row>
        </b-card>
    </div>
    `,
    props: {
        mainAddRow: Function,
        modeName: String,
    },
})

Vue.component('setting-header', {
    template: `
    <div>
        <b-card class="fixed-top header" style="background: rgba(255,255,255,0.5);">
            <b-row>
                <b-col></b-col>
                <b-col cols="11">
                    <b-row>
                        <b-col class="pc-mode">
                            <b-button href="/setting-page">会社情報</b-button>
                            <b-button href="/user-page">ユーザー</b-button>
                            <b-button href="/category-page">カテゴリ</b-button>
                            <b-button href="/maker-page">メーカー</b-button>
                            <b-button href="/unit-page">単位</b-button>
                            <b-button href="/dust-select-page">削除済み</b-button>
                        </b-col>
                        <b-col class="sm-mode">
                            <b-button href="/setting-page" v-b-tooltip.hover.top="'会社情報'">
                                <b-icon icon="building"></b-icon>
                            </b-button>
                            <b-button href="/user-page" v-b-tooltip.hover.top="'ユーザー登録'">
                                <b-icon icon="person-plus-fill"></b-icon>
                            </b-button>
                            <b-button href="/category-page" v-b-tooltip.hover.top="'カテゴリ登録'">
                                <b-icon icon="folder2"></b-icon>
                            </b-button>
                            <b-button href="/maker-page" v-b-tooltip.hover.top="'メーカー登録'">
                                <b-icon icon="shop"></b-icon>
                            </b-button>
                            <b-button href="/unit-page" v-b-tooltip.hover.top="'単位登録'">
                                <b-icon icon="hammer"></i>
                            </b-button>
                            <b-button href="/dust-select-page" v-b-tooltip.hover.top="'削除済み参照'">
                                <b-icon icon="file-earmark-x"></b-icon>
                            </b-button>
                        </b-col>
                        <b-col cols="2" class="text-right">
                            <sc-menu v-if="modeName!='mw'"></sc-menu>
                        </b-col>
                    </b-row>
                </b-col>
                <b-col></b-col>
            </b-row>
        </b-card>
    </div>
    `,
    props: {
        modeName: String,
    },
})