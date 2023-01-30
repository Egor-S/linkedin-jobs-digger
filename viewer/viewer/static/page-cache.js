export default {
    _key(key) {
        return `${window.location.pathname}@${key}`
    },
    put(key, value) {
        window.localStorage.setItem(this._key(key), JSON.stringify(value))
    },
    get(key, default_value) {
        let v = window.localStorage.getItem(this._key(key))
        return (v === null) ? default_value : JSON.parse(v)
    },
    remove(key) {
        window.localStorage.removeItem(this._key(key))
    }
}
