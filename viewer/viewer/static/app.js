import PageCache from "./page-cache.js";

export default {
    data() {
        return {
            query: PageCache.get('query', {
                date_till: '',
                date_from: '',
                keyword: ''
            }),
            jobs: [],
            activeJob: undefined,
            selection: {
                active: false,
                tooltipStyle: {left: 0, top: 0}
            },
            flags: PageCache.get('flags', [])
        }
    },
    methods: {
        async getJobsList() {
            this.jobs = await fetch("/api/jobs?" + new URLSearchParams(this.query)).then(d => d.json())
        },
        async getJobDescription(job_id) {
            this.activeJob = await fetch(`/api/jobs/${job_id}`).then(d => d.json())
        },
        getJobURL(job_id) {
            return `https://www.linkedin.com/jobs/view/${job_id}/`
        },
        selectionUpdate() {
            let selection = window.getSelection()
            let range = selection.getRangeAt(0)
            let rect = range.getBoundingClientRect()
            let tooltipRect = this.$refs['selectionTooltip'].getBoundingClientRect()
            let viewPane = this.$refs['viewPane']
            let viewRect = viewPane.getBoundingClientRect()

            this.selection.active = rect.width > 0
            this.selection.tooltipStyle.left = (rect.left - viewRect.left + rect.width / 2 - tooltipRect.width / 2) + 'px'
            this.selection.tooltipStyle.top = (rect.top - viewRect.top + viewPane.scrollTop - tooltipRect.height - 5) + 'px'
        },
        async createFlag(positive) {
            let text = window.getSelection().toString()
            let toDel = this.flags.filter(flag => flag.text.toLowerCase() === text.toLowerCase() && flag.positive === positive)
            this.flags = this.flags.filter(flag => flag.text.toLowerCase() !== text.toLowerCase())
            if (!toDel.length)
                this.flags.push({text: text, positive: positive})
            PageCache.put('flags', this.flags)
        }
    },
    computed: {
        jobDescriptionHTML() {
            if (!this.activeJob)
                return

            let html = this.activeJob.description.text
            let flags = this.flags
            if (this.query.keyword)
                flags = this.flags.concat([{text: this.query.keyword, positive: true}])

            flags.forEach(({text, positive}) => {
                let cls = positive ? 'positive' : 'negative'
                html = html.replace(new RegExp(`(${text})`, 'gmi'), `<span class="${cls}">\$1</span>`)
            })
            return html
        }
    },
    mounted() {
        this.getJobsList()
    },
    watch: {
        query: {
            handler(query) {
                this.getJobsList()
                PageCache.put('query', query)
            },
            deep: true
        }
    }
}
