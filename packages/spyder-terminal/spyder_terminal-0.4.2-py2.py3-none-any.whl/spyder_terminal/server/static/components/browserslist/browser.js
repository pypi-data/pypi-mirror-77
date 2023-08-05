var BrowserslistError = require('./error')

function noop () { }

module.exports = {
  loadQueries: function loadQueries () {
    throw new BrowserslistError(
      'Sharable configs are not supported in client-side build of Browserslist')
  },

  getStat: function getStat (opts) {
    return opts.stats
  },

  loadConfig: function loadConfig (opts) {
    if (opts.config) {
      throw new BrowserslistError(
        'Browserslist config are not supported in client-side build')
    }
  },

  loadCountry: function loadCountry () {
    throw new BrowserslistError(
      'Country statistics is not supported ' +
      'in client-side build of Browserslist')
  },

  currentNode: function currentNode (resolve, context) {
    return resolve(['maintained node versions'], context)[0]
  },

  parseConfig: noop,

  readConfig: noop,

  findConfig: noop,

  clearCaches: noop,

  oldDataWarning: noop
}
