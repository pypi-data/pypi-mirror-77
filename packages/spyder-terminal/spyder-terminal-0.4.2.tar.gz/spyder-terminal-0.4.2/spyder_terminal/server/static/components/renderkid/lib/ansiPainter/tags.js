// Generated by CoffeeScript 1.9.3
var color, colors, i, len, tags;

module.exports = tags = {
  'none': {
    color: 'none',
    bg: 'none'
  },
  'bg-none': {
    color: 'inherit',
    bg: 'none'
  },
  'color-none': {
    color: 'none',
    bg: 'inherit'
  }
};

colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'grey', 'bright-red', 'bright-green', 'bright-yellow', 'bright-blue', 'bright-magenta', 'bright-cyan', 'bright-white'];

for (i = 0, len = colors.length; i < len; i++) {
  color = colors[i];
  tags[color] = {
    color: color,
    bg: 'inherit'
  };
  tags["color-" + color] = {
    color: color,
    bg: 'inherit'
  };
  tags["bg-" + color] = {
    color: 'inherit',
    bg: color
  };
}
