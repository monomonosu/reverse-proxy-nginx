//info
Vue.component('confirm-modal', {
    template: `
    <div>
        <b-modal id="confirmModal" hide-footer>
            <template #modal-title>
                {{title}}
            </template>
            <div class="d-block text-center">
                <p style="color: #ffffff;background-color: #10afc5;"><span>{{message}}</span></p>
            </div>
        </b-modal>
    <div>
    `,
    props: {
        title: String,
        message: String,
    },
})

//danger
Vue.component('confirm-modal-danger', {
    template: `
    <div>
        <b-modal id="confirmModalDanger" hide-footer>
            <template #modal-title>
                {{title}}
            </template>
            <div class="d-block text-center">
                <p style="color: #ffffff;background-color: #ed254e;"><span>{{message}}</span></p>
            </div>
        </b-modal>
    <div>
    `,
    props: {
        title: String,
        message: String,
    },
})