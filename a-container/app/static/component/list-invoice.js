// 検索コンポーネント
var search = Vue.component('search', {
    template: `
    <b-input-group>
        <b-form-input v-model="search.searchInvoiceWord" id="searchInvoiceWord" size="sm"
            placeholder="🔍　No. or 日付 or 得意先名">
        </b-form-input>
        <b-input-group-append>
            <b-button variant="primary" size="sm" @click="this.searchInvoice">検索
            </b-button>
        </b-input-group-append>
    </b-input-group>
    `,
    data: {
        searchInvoiceWord: '',
        isMore: false,
    },
    props: {
        invoices: Array,
    },
    methods: {
        searchInvoice: function () {
            this.getInvoices(search.searchInvoiceWord);
        },
        getInvoices: async function (searchWord = '', offset = 0) {
            self = this;
            url = '/v1/invoices'
            await axios.get(url, {
                params: {
                    search: searchWord,
                    offset: offset,
                    moreCheck: true,
                }
            })
                .then(function (response) {
                    console.log(response);
                    search.invoices = response.data.invoices;
                    self.countChanged = 0;
                    search.isMore = response.data.isMore;
                });
            this.changeInvoices();
        },
        changeInvoices() {
            this.$emit('emit-invoices', search.invoices, search.searchInvoiceWord, search.isMore);
        },
    },
})

// 「全て表示」機能コンポーネント
var isShow = Vue.component('is-show', {
    template: `
    <b-row align-h="end">
        <b-form-checkbox class="mr-3" v-model="isShow.isInvoicesShowAll" @change="changeIsInvoicesShowAll">全て表示</b-form-checkbox>
    </b-row>
    `,
    data: {
        isInvoicesShowAll: false
    },
    methods: {
        changeIsInvoicesShowAll() {
            this.$emit('emit-show-all', isShow.isInvoicesShowAll);
        },
    },
})

// 日付範囲検索コンポーネント
let daySearch = Vue.component('day-search', {
    template: `
    <b-row align-h="end">
        <div id="searchDay">
            <b-form inline>
                <label>日付</label>
                <b-form-input v-model="daySearch.searchDayStart" id="searchDayStart" size="sm"
                    class="mr-2 ml-2" autocomplete="off" type="date" @change="changeSearchDayStart">
                </b-form-input>
                ～
                <b-form-input v-model="daySearch.searchDayEnd" id="searchDayEnd" size="sm"
                    class="ml-2" autocomplete="off" type="date" @change="changeSearchDayEnd">
                </b-form-input>
            </b-form>
        </div>
    </b-row>
    `,
    data: {
        searchDayStart: '',
        searchDayEnd: '',
    },
    methods: {
        changeSearchDayStart() {
            this.$emit('emit-day-start', daySearch.searchDayStart);
        },
        changeSearchDayEnd() {
            this.$emit('emit-day-end', daySearch.searchDayEnd);
        }
    }
})

// 表示件数コンポーネント
var indicateCount = Vue.component('indicate-count', {
    template: `
    <b-row align-h="end">
        <p class="mr-3">表示件数 {{ this.indicateCount }}件</p>
    </b-row>
    `,
    props: {
        indicateCount: Number,
    },
})

// 請求書一覧（通常）
Vue.component('invoice-list', {
    template: `
    <div>
        <b-table responsive hover small id="invoicetable" sort-by="ID" small label="Table Options"
            :items=invoicesIndicateIndex :sort-by.sync="this.sortByInvoices" :sort-desc.sync="this.sortDesc" :fields="[
        {  key: 'update', label: '' },
        {  key: 'id', thClass: 'd-none', tdClass: 'd-none' },
        {  key: 'applyNumber', label: '請求番号', thClass: 'text-center', tdClass: 'text-center' },
        {  key: 'applyDate', label: '日付', thClass: 'th-apply-date text-center', tdClass: 'text-center', sortable: true },
        {  key: 'customerAnyNumber', label: 'No.', thClass: 'th-customer-any-number text-center', tdClass: 'text-center', sortable: true },
        {  key: 'customerName', label: '得意先名', thClass: 'text-center', },
        {  key: 'title', label: '件名', thClass: 'text-center', },
        {  key: 'totalAmount', label: '請求金額', thClass: 'text-center', tdClass: 'text-right' },
        {  key: 'numberOfAttachments', label: '', tdClass: 'text-center' },
    ]" :tbody-tr-class="this.rowClass">
            <template v-slot:cell(update)="data">
                <router-link to="?page=show">
                    <b-button variant="primary" @click="selectInvoice(data.item)">
                        <i class="fas fa-edit"></i>
                    </b-button>
                </router-link>
            </template>
            <template v-slot:cell(applyDate)="data">
                {{formatDate(data.item.applyDate)}}
            </template>
            <template v-slot:cell(totalAmount)="data">
                {{amountCalculation(data.item)|nf}}
            </template>
            <template v-slot:cell(numberOfAttachments)="data">
                <b-img v-if="countedFiles[data.item.applyNumber] > 0"
                    src="../static/images/icon/icon_clip.png"></b-img>
            </template>
        </b-table>
    </div>
    `,
    props: {
        selectInvoice: Function,
        countedFiles: Object,
        invoicesIndicateIndex: Array,
        sortByInvoices: String,
        sortDesc: Boolean,
    },
    methods: {
        rowClass: function (item, type) {
            if (!item || type !== 'row') return
            if (!item.id) return "d-none";
        },
        //日付カラム
        formatDate(date) {
            if (!!date) return moment(date).format("YYYY/MM/DD");
        },
        //請求金額カラム
        amountCalculation(invoice) {
            if (!invoice.invoice_items.length) return 0;
            let amount = invoice.invoice_items.map(item => item.count * Math.round(item.price)).reduce((a, b) => a + b);
            if (invoice.isTaxExp === true) return Math.round(amount * (1 + invoice.tax / 100));
            return amount;
        },
    },
})

// 請求書一覧（未入金）
Vue.component('invoice-list-payment', {
    template: `
    <div>
        <b-table responsive hover small id="invoicetable" label="Table Options"
            :items=invoicesIndicateIndex :sort-by.sync="this.sortByInvoices" :sort-desc.sync="this.sortDesc" :fields="[
        {  key: 'update', label: '' },
        {  key: 'id', thClass: 'd-none', tdClass: 'd-none' },
        {  key: 'applyNumber', label: '請求番号', thClass: 'text-center', tdClass: 'text-center' },
        {  key: 'applyDate', label: '日付', thClass: 'th-apply-date text-center', tdClass: 'text-center', sortable: true },
        {  key: 'customerAnyNumber', label: 'No.', thClass: 'th-customer-any-number text-center', tdClass: 'text-center', sortable: true },
        {  key: 'customerName', label: '得意先名', thClass: 'text-center', },
        {  key: 'title', label: '件名', thClass: 'text-center', },
        {  key: 'unpaidAmount', label: '未入金額', thClass: 'text-center', tdClass: 'text-right' },
        {  key: 'numberOfAttachments', label: '', tdClass: 'text-center' },
    ]" :tbody-tr-class="this.rowClass">
            <template v-slot:cell(update)="data">
                <router-link to="?page=show">
                    <b-button variant="primary" @click="selectInvoice(data.item)">
                        <i class="fas fa-edit"></i>
                    </b-button>
                </router-link>
            </template>
            <template v-slot:cell(applyDate)="data">
                {{formatDate(data.item.applyDate)}}
            </template>
            <template v-slot:cell(unpaidAmount)="data">
                {{unpaidCalculation(data.item)|nf}}
            </template>
            <template v-slot:cell(numberOfAttachments)="data">
                <b-img v-if="countedFiles[data.item.applyNumber] > 0"
                    src="../static/images/icon/icon_clip.png"></b-img>
            </template>
        </b-table>
    </div>
    `,
    props: {
        selectInvoice: Function,
        countedFiles: Object,
        invoicesIndicateIndex: Array,
        sortByInvoices: String,
        sortDesc: Boolean,
    },
    methods: {
        rowClass: function (item, type) {
            if (!item || type !== 'row') return
            if (!item.id) return "d-none";
        },
        //日付カラム
        formatDate(date) {
            if (!!date) return moment(date).format("YYYY/MM/DD");
        },
        //請求金額カラム
        amountCalculation(invoice) {
            if (!invoice.invoice_items.length) return 0;
            let amount = invoice.invoice_items.map(item => item.count * Math.round(item.price)).reduce((a, b) => a + b);
            if (invoice.isTaxExp === true) return Math.round(amount * (1 + invoice.tax / 100));
            return amount;
        },
        // 未入金額
        unpaidCalculation(invoice) {
            if (!invoice.invoice_payments.length) return this.amountCalculation(invoice);
            let paidAmount = invoice.invoice_payments.map(payment => payment.paymentAmount).reduce((a, b) => a + b);
            let balance = this.amountCalculation(invoice) - paidAmount;
            if (balance < 0) return 0;
            return balance;
        },
    },
})