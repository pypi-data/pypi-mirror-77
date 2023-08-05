function _skipFirstGeneratorNext(fn) {
  return function () {
    var it = fn.apply(this, arguments);
    it.next();
    return it;
  };
}

module.exports = _skipFirstGeneratorNext;