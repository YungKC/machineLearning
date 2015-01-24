  var matchedObject = function(params) {
      importScripts('build/convnet.js');
      var net = load_pretrained(params.netConfig);
      var classes_txt = params.classes_txt;
      var rawData = params.rawData;
      var srcWidth = params.srcWidth;
      var srcHeight = params.srcHeight;
      var windowWidth = params.windowWidth;
      var windowHeight = params.windowHeight;
      var stride = params.stride;

      var num_classes = net.layers[net.layers.length - 1].out_depth;
      var notFoundType = num_classes - 1;

      var xLoc = 0,
          yLoc = 0,
          matchedType = notFoundType,
          maxProb = -1;

      var minX = Math.min(2,(srcWidth-windowWidth)/2),
          minY = Math.min(2,(srcHeight-windowHeight)/2),
          maxX = srcWidth-2-windowWidth,
          maxY = srcHeight-2-windowHeight;

      self.postMessage({FoundText: 'mins: (' + minX + ', ' + minY + ') to (' + maxX + ', ' + maxY + ')'}); 
      for (var y = 0; y + windowHeight <= srcHeight; y += stride) {
        for (var x = 0; x + windowWidth <= srcWidth; x += stride) {
          self.postMessage({'ProgressText': 'Processing at (' + x + ', ' + y + ')... '});

          var xs = sample_test_instance(rawData, srcWidth, srcHeight, x, y);
          var timeVal = new Date().getTime()
          var a = net.forward(xs[0]);
          if (y==0 && x==0) {
            self.postMessage({FoundText: '*** forward time: ' + (new Date().getTime() - timeVal)})
          }
          var foundType = -1;
          var typeProb = -1;
          for (var typeID = 0; typeID < num_classes; typeID++) {
              if (a.w[typeID] > typeProb) {
                  foundType = typeID;
                  typeProb = a.w[typeID];
              }
          }
          if (typeProb > maxProb && foundType != notFoundType && typeProb != 1) {
            self.postMessage({FoundText: 'Found at (' + x + ', ' + y + '): ' + classes_txt[foundType] + ' : ' + typeProb});
            // ensure the found location is not near the edge to filter out false positives
            if (x < minX || y < minY || x > maxX || y > maxY) {
              self.postMessage({FoundText: '-- Too near the edge. Rejected.'})
            } else {
              self.postMessage({FoundText: '-- Verified not near the edge. Accepted.'})
              maxProb = typeProb;
              matchedType = foundType;
              xLoc = x;
              yLoc = y;
            }
          }
        }
      };
      var result;
      if (matchedType != notFoundType) {
        result = {
          x: xLoc,
          y: yLoc,
          matchedType: matchedType,
          matchedProb: maxProb
        };
        self.postMessage({result:result, ResultText: 'Found ' + classes_txt[matchedType] + ' at (' + xLoc + ', ' + yLoc + ') with confidence of ' + maxProb});
      } else {
        self.postMessage({ResultText: 'Not Found!'});
      }
      return result;
  }

  // sample an area 
  var sample_test_instance = function(rawData, srcWidth, srcHeight, startX, startY) {
      var x = new self.convnetjs.Vol(32, 64, 3, 0.0);
      var W = srcWidth * 3;
      for (var yc = 0; yc < 64; yc++) {
          for (var xc = 0; xc < 32; xc++) {
              for (var dc = 0; dc < 3; dc++) {
                  var ix = ((srcWidth * (yc + startY) + (xc + startX)) * 3) + dc;
                  x.set(xc, yc, dc, rawData[ix]);
              }
          }
      }

      var xs = [];
      xs.push(x); // push an un-augmented copy

      // return multiple augmentations, and we will average the network over them
      // to increase performance
      return xs;
  }

  function load_pretrained(netConfigJson) {
      var net = new convnetjs.Net();
      net.fromJSON(netConfigJson);
      return net;
  }

  self.onmessage = function(e) {
    window = self;
    matchedObject(e.data.value);
  }