export default {
    data() {
        return {
            query: {
                date_from: '',
                date_till: ''
            },
            jobs: [],
            activeJob: undefined
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
        }
    },
    mounted() {
        this.getJobsList()
    },
    watch: {
        query: {
            handler(newQuery, oldQuery) {
                this.getJobsList()
            },
            deep: true
        }
    }
}
