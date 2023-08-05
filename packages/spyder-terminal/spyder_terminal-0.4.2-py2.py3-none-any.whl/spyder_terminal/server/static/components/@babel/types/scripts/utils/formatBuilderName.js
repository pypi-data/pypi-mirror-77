"use strict";

const toLowerCase = Function.call.bind("".toLowerCase);

module.exports = function formatBuilderName(type) {
  // FunctionExpression -> functionExpression
  // JSXIdentifier -> jsxIdentifier
  // V8IntrinsicIdentifier -> v8IntrinsicIdentifier
  return type.replace(/^([A-Z](?=[a-z0-9])|[A-Z]+(?=[A-Z]))/, toLowerCase);
};
