// Generated by CoffeeScript 1.9.3
var Bullet, _Declaration,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_Declaration = require('./_Declaration');

module.exports = Bullet = (function(superClass) {
  var self;

  extend(Bullet, superClass);

  function Bullet() {
    return Bullet.__super__.constructor.apply(this, arguments);
  }

  self = Bullet;

  Bullet.prototype._set = function(val) {
    var alignment, bg, char, color, enabled, m, original;
    val = String(val);
    original = val;
    char = null;
    enabled = false;
    color = 'none';
    bg = 'none';
    if (m = val.match(/\"([^"]+)\"/) || (m = val.match(/\'([^']+)\'/))) {
      char = m[1];
      val = val.replace(m[0], '');
      enabled = true;
    }
    if (m = val.match(/(none|left|right|center)/)) {
      alignment = m[1];
      val = val.replace(m[0], '');
    } else {
      alignment = 'left';
    }
    if (alignment === 'none') {
      enabled = false;
    }
    if (m = val.match(/color\:([\w\-]+)/)) {
      color = m[1];
      val = val.replace(m[0], '');
    }
    if (m = val.match(/bg\:([\w\-]+)/)) {
      bg = m[1];
      val = val.replace(m[0], '');
    }
    if (val.trim() !== '') {
      throw Error("Unrecognizable value `" + original + "` for `" + this.prop + "`");
    }
    return this.val = {
      enabled: enabled,
      char: char,
      alignment: alignment,
      background: bg,
      color: color
    };
  };

  return Bullet;

})(_Declaration);
