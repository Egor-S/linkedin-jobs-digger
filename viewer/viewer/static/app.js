export default {
    data() {
        return {
            jobs: [],
            activeJob: undefined
        }
    },
    methods: {
        async getJobsList() {
            this.jobs = await fetch("/api/jobs").then(d => d.json())
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
    }
}
