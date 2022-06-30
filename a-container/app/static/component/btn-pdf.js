//invoice
Vue.component('btn-pdf-invoice', {
    template: `
    <b-dropdown split dropup id="dropdown-dropup" size="lg" @click="func('invoice')" 
        v-b-tooltip.hover.top="'印刷'">
        <template #button-content>
            <i class="fas fa-print"></i>
        </template>
        <b-dropdown-item @click="func('invoice','copy')">請求書控え</b-dropdown-item>
        <b-dropdown-item @click="func('invoice','nodate')">日付なし請求書</b-dropdown-item>
        <b-dropdown-item @click="func('delivery')">納品書</b-dropdown-item>
        <b-dropdown-item @click="func('receipt')">領収書</b-dropdown-item>
    </b-dropdown>
    `,
    props: {
        func: Function,
    },
});

//quotation
Vue.component('btn-pdf-quotation', {
    template: `
    <b-button pill size="lg" variant="primary" @click="func()" 
        v-b-tooltip.hover.top="'印刷'"><i class="fas fa-print"></i>
    </b-button>
    `,
    props: {
        func: Function,
    },
});
