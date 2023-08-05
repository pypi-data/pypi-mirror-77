"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = cloneDeepWithoutLoc;

var _cloneNode = _interopRequireDefault(require("./cloneNode"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function cloneDeepWithoutLoc(node) {
  return (0, _cloneNode.default)(node, true, true);
}