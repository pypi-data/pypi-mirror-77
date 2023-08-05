// Generated by CoffeeScript 1.9.3
var Rule, StyleSheet;

Rule = require('./Rule');

module.exports = StyleSheet = (function() {
  var self;

  self = StyleSheet;

  function StyleSheet() {
    this._rulesBySelector = {};
  }

  StyleSheet.prototype.setRule = function(selector, styles) {
    var key, val;
    if (typeof selector === 'string') {
      this._setRule(selector, styles);
    } else if (typeof selector === 'object') {
      for (key in selector) {
        val = selector[key];
        this._setRule(key, val);
      }
    }
    return this;
  };

  StyleSheet.prototype._setRule = function(s, styles) {
    var i, len, ref, selector;
    ref = self.splitSelectors(s);
    for (i = 0, len = ref.length; i < len; i++) {
      selector = ref[i];
      this._setSingleRule(selector, styles);
    }
    return this;
  };

  StyleSheet.prototype._setSingleRule = function(s, styles) {
    var rule, selector;
    selector = self.normalizeSelector(s);
    if (!(rule = this._rulesBySelector[selector])) {
      rule = new Rule(selector);
      this._rulesBySelector[selector] = rule;
    }
    rule.setStyles(styles);
    return this;
  };

  StyleSheet.prototype.getRulesFor = function(el) {
    var ref, rule, rules, selector;
    rules = [];
    ref = this._rulesBySelector;
    for (selector in ref) {
      rule = ref[selector];
      if (rule.selector.matches(el)) {
        rules.push(rule);
      }
    }
    return rules;
  };

  StyleSheet.normalizeSelector = function(selector) {
    return selector.replace(/[\s]+/g, ' ').replace(/[\s]*([>\,\+]{1})[\s]*/g, '$1').trim();
  };

  StyleSheet.splitSelectors = function(s) {
    return s.trim().split(',');
  };

  return StyleSheet;

})();
