Vue.component('sc-menu', {
    template: `  
    <div>
    <b-button  size="lg" v-b-toggle.sidebar-right><i class="fas fa-bars"></i></b-button>
    <b-sidebar id="sidebar-right" aria-labelledby="sidebar-right-title" no-header right shadow :visible="visible">
        <template #default="{ hide }">
            <div class="p-3">
                <b-button variant="danger" @click="hide"><b-icon icon="arrow-right"></b-icon>
                </b-button>
                <b-img src="../static/images/logo_a_color2.png"
                    style="width: 50%; " center ></b-img>
                <nav class="mt-3">
                    <b-nav vertical class="mb-4">
                        <b-button variant="primary" block href="/"><i class="fas fa-home"></i>　TOP
                        </b-button>
                    </b-nav>
                    <b-nav vertical>
                        <b-button variant="primary" block href="/check-page">
                        <b-icon icon="check"></b-icon> チェック
                        </b-button>
                        <b-button variant="primary" block href="/customer-page"><i
                                class="fas fa-building"></i>　得意先
                        </b-button>
                        <b-button variant="primary" block href="/item-page"><i class="fas fa-box"></i>　商　品
                        </b-button>
                        <b-button variant="primary" block href="/invoice-page"><i
                                class="fas fa-copy"></i>　請求書</b-button>
                        <b-button variant="primary" block href="/quotation-page"><i
                                class="far fa-copy"></i>　見積書</b-button>
                        <b-button variant="primary" block href="/memo-page"><i
                                class="fas fa-book-open"></i>　メ　モ</b-button>
                        <b-button block href="/setting-page" >
                                </b-icon><b-icon icon="gear-fill"></b-icon>　各種設定</b-button>
                        <b-button block @click="goMW" >
                                </b-icon><b-icon icon="front"></b-icon>　マルチウィンドウ</b-button>

                        <b-button block href="/logout" variant="outline-primary">
                                <b-img src="../static/images/icon/icon_logout.png"></b-img>　ログアウト</b-button>
                    </b-nav>
                </nav>
            </div>
        </template>
    </b-sidebar>
    </div>
    `,
    props: {
        visible:{
            type:Boolean,
            default: false
        }
    },
    methods:{
        goMW: function(){
            localStorage.setItem('wMode','mw');
            window.location.href = '/';
        }
    }
});
