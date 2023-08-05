// Generated by CoffeeScript 1.9.3
var CSSSelect, Selector;

CSSSelect = require('css-select');

module.exports = Selector = (function() {
  var self;

  self = Selector;

  function Selector(text1) {
    this.text = text1;
    this._fn = CSSSelect.compile(this.text);
    this.priority = self.calculatePriority(this.text);
  }

  Selector.prototype.matches = function(elem) {
    return CSSSelect.is(elem, this._fn);
  };

  Selector.calculatePriority = function(text) {
    var n, priotrity;
    priotrity = 0;
    if (n = text.match(/[\#]{1}/g)) {
      priotrity += 100 * n.length;
    }
    if (n = text.match(/[a-zA-Z]+/g)) {
      priotrity += 2 * n.length;
    }
    if (n = text.match(/\*/g)) {
      priotrity += 1 * n.length;
    }
    return priotrity;
  };

  return Selector;

})();
