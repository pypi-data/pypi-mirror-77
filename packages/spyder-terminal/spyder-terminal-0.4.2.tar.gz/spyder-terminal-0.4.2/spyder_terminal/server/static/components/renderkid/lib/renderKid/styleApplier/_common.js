// Generated by CoffeeScript 1.9.3
var AnsiPainter, _common;

AnsiPainter = require('../../AnsiPainter');

module.exports = _common = {
  getStyleTagsFor: function(style) {
    var i, len, ret, tag, tagName, tagsToAdd;
    tagsToAdd = [];
    if (style.color != null) {
      tagName = 'color-' + style.color;
      if (AnsiPainter.tags[tagName] == null) {
        throw Error("Unknown color `" + style.color + "`");
      }
      tagsToAdd.push(tagName);
    }
    if (style.background != null) {
      tagName = 'bg-' + style.background;
      if (AnsiPainter.tags[tagName] == null) {
        throw Error("Unknown background `" + style.background + "`");
      }
      tagsToAdd.push(tagName);
    }
    ret = {
      before: '',
      after: ''
    };
    for (i = 0, len = tagsToAdd.length; i < len; i++) {
      tag = tagsToAdd[i];
      ret.before = ("<" + tag + ">") + ret.before;
      ret.after = ret.after + ("</" + tag + ">");
    }
    return ret;
  }
};
