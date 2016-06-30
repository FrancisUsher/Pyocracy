(function () {
    window.linear = {
        slope: function (x1, y1, x2, y2) {
            if (x1 == x2) return false;
            return (y1 - y2) / (x1 - x2);
        },
        yInt: function (x1, y1, x2, y2) {
            if (x1 === x2) return y1 === 0 ? 0 : false;
            if (y1 === y2) return y1;
            return y1 - this.slope(x1, y1, x2, y2) * x1 ;
        },
        getXInt: function (x1, y1, x2, y2) {
            var slope;
            if (y1 === y2) return x1 == 0 ? 0 : false;
            if (x1 === x2) return x1;
            return (-1 * ((slope = this.slope(x1, y1, x2, y2)) * x1 - y1)) / slope;
        },
        getIntersection: function (x11, y11, x12, y12, x21, y21, x22, y22) {
            var slope1, slope2, yint1, yint2, intx, inty;
            if (x11 == x21 && y11 == y21) return [x11, y11];
            if (x12 == x22 && y12 == y22) return [x12, y22];
            
            slope1 = this.slope(x11, y11, x12, y12);
            slope2 = this.slope(x21, y21, x22, y22);
            if (slope1 === slope2) return false;

            yint1 = this.yInt(x11, y11, x12, y12);
            yint2 = this.yInt(x21, y21, x22, y22);
            if (yint1 === yint2) return yint1 === false ? false : [0, yint1];

            if (slope1 === false) return [y21, slope2 * y21 + yint2];
            if (slope2 === false) return [y11, slope1 * y11 + yint1];
            intx = (slope1 * x11 + yint1 - yint2)/ slope2;
            return [intx, slope1 * intx + yint1];
        }
    }
}());

var imageObj = new Image();
var c = document.getElementById('testCanvas');
var cx = c.getContext('2d');
imageObj.onload = function()
{
    cx.save();
    cx.beginPath();
    cx.moveTo(0,0);
    cx.lineTo(240,0);
    cx.lineTo(500,550);
    cx.lineTo(0,400);
    //var ptrn = cx.createPattern(imageObj, 'repeat');
    //cx.fillStyle = ptrn;
    
    cx.fill();
    //cx.clip();
    //cx.drawImage(imageObj, 10, 50);
};

function drawHalfScreenTriangle(angle1, angle2){
    return;
    
}

function drawHalfScreenLine(canvas, angle){
    var cx = c.getContext('2d');
    var cOrigin = normalizeToCanvasOrigin(canvas, {xPos:0, yPos:0});
    var cDest = getPointOnAngle(canvas, angle);
    cx.moveTo(cOrigin.xPos, cOrigin.yPos);
    cx.beginPath();
    cx.lineTo(cDest.xPos, cDest.yPos);
    cx.stroke();
}

function drawHalfScreenLineTo(canvas, point){
    var cx = c.getContext('2d');
    var cOrigin = normalizeToCanvasOrigin(canvas, {xPos:0, yPos:0});
    cx.moveTo(cOrigin.xPos, cOrigin.yPos);
    cx.beginPath();
    cx.lineTo(point.xPos, point.yPos);
    cx.stroke();
}

function getPointOnAngle(canvas, angle){
    var halfPI = Math.PI / 2;
    angle = angle % (Math.PI * 2),
    tanCalc = Math.tan(angle);
    
    var xCenter = canvas.width / 2,
        yCenter = canvas.height / 2;
    
    var xDirection;
    if(angle == halfPI){
        // Draw vertical line up
        return normalizeToCanvasOrigin(canvas, {xPos: 0, yPos: 1 * 300});
    } else if(angle == 3 * halfPI){
        // Draw vertical line down
        return normalizeToCanvasOrigin(canvas, {xPos: 0, yPos: -1* 300});
    } else if(angle  < halfPI || angle > 3 * halfPI){
        // Draw line right
        return normalizeToCanvasOrigin(canvas, {xPos: 1* 300, yPos: tanCalc* 300});
    } else {
        // Draw line left
        return normalizeToCanvasOrigin(canvas, {xPos: -1* 300, yPos: -tanCalc* 300});
    }
}

function normalizeToCanvasOrigin(canvas, xyPos){
    var xCenter = canvas.width / 2,
        yCenter = canvas.height / 2;
    return {xPos: xCenter - xyPos.xPos, yPos: yCenter - xyPos.yPos}
}

/**
 * This is a basic example on how to develop a custom node renderer. In
 * this example, the renderer will display an image clipped in a disc,
 * with a border colored according the node's "color" value.
 *
 * If a node as the value "image" to its attribute "type", then it will
 * displayed with the node renderer "sigma.canvas.nodes.image", with the
 * url being its "url" value.
 *
 * IMPORTANT: This node renderer just works with the canvas renderer. If
 * you do want to display images with the WebGL renderer, you will have
 * to develop a specific WebGL node renderer.
 */
sigma.utils.pkg('sigma.canvas.nodes');
sigma.canvas.nodes.image = (function() {
  var _cache = {},
      _loading = {},
      _callbacks = {};

  // Return the renderer itself:
  var renderer = function(node, context, settings) {
    var args = arguments,
        prefix = settings('prefix') || '',
        size = node[prefix + 'size'],
        color = node.color || settings('defaultNodeColor'),
        url = node.url;

    if (_cache[url]) {
      context.save();

      // Draw the clipping disc:
      context.beginPath();
      context.arc(
        node[prefix + 'x'],
        node[prefix + 'y'],
        node[prefix + 'size'],
        0,
        Math.PI * 2,
        true
      );
      context.closePath();
      context.fillStyle = "LightBlue";
      context.fill();
      context.clip();

      // Draw the image
      context.drawImage(
        _cache[url],
        node[prefix + 'x'] - size,
        node[prefix + 'y'] - size,
        2 * size,
        2 * size
      );

      // Quit the "clipping mode":
      context.restore();

      // Draw the border:
      context.beginPath();
      context.arc(
        node[prefix + 'x'],
        node[prefix + 'y'],
        node[prefix + 'size'],
        0,
        Math.PI * 2,
        true
      );
      context.lineWidth = size / 5;
      context.strokeStyle = node.color || settings('defaultNodeColor');
      context.stroke();
    } else {
      sigma.canvas.nodes.image.cache(url);
      sigma.canvas.nodes.def.apply(
        sigma.canvas.nodes,
        args
      );
    }
  };

  // Let's add a public method to cache images, to make it possible to
  // preload images before the initial rendering:
  renderer.cache = function(url, callback) {
    if (callback)
      _callbacks[url] = callback;

    if (_loading[url])
      return;

    var img = new Image();

    img.onload = function() {
      _loading[url] = false;
      _cache[url] = img;

      if (_callbacks[url]) {
        _callbacks[url].call(this, img);
        delete _callbacks[url];
      }
    };

    _loading[url] = true;
    img.src = url;
  };

  return renderer;
})();

// Now that's the renderer has been implemented, let's generate a graph
// to render:
var i,
    s,
    img,
    N = 20,
    E = 60,
    g = {
      nodes: [],
      edges: []
    },
    loaded = 0,
    colors = [
      '#617db4',
      '#668f3c',
      '#c6583e',
      '#b956af'
    ];
  

  
$.getJSON( "glyphicon_urls.json", function( data ) {
    var urls = data["urls"];
    function addImageNode(id, label, imageURL, xPos, yPos){
        g.nodes.push({
            id: id,
            label: label,
            type: 'image',
            url: imageURL,
            x: xPos,
            y: yPos,
            size: 2,
            color: colors[Math.floor(Math.random() * colors.length)]
          });
    }
    function generateLabel(url){
        return url.split('_')[url.split('_').length - 1].split('.')[0];
    }
    urls.forEach(function(url, i) {
        addImageNode('n' + i, generateLabel(url), url, i % 10, i / 10);
    });

    for (i = 0; i < E; i++)
      g.edges.push({
        id: 'e' + i,
        source: 'n' + (Math.random() * N | 0),
        target: 'n' + (Math.random() * N | 0),
        size: Math.random()
      });

    // Then, wait for all images to be loaded before instantiating sigma:
    urls.forEach(function(url) {
      sigma.canvas.nodes.image.cache(
        url,
        function() {
          if (++loaded === urls.length)
            // Instantiate sigma:
            s = new sigma({
              graph: g,
              renderer: {
                // IMPORTANT:
                // This works only with the canvas renderer, so the
                // renderer type set as "canvas" is necessary here.
                container: document.getElementById('graph-container'),
                type: 'canvas'
              },
              settings: {
                minNodeSize: 8,
                maxNodeSize: 16,
              }
            });
        }
      );
    });
});