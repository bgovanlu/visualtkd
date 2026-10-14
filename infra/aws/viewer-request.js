// CloudFront viewer-request function for visualtkd.com (runtime cloudfront-js-2.0).
// tools/deploy_aws.py fills GO from site/_redirects and inlines this file into
// infra/aws/site.yaml; edit it here, never in the stack.
var HOST = 'visualtkd.com';
var GO = __GO__;

function handler(event) {
  var req = event.request;
  var uri = req.uri;
  var host = req.headers.host ? req.headers.host.value : '';

  // www (and the bare cloudfront.net name) -> the canonical host
  if (host !== HOST) return redirect(301, 'https://' + HOST + uri + query(req.querystring));

  // /go/<name>: short links behind the printed reference QR codes. 302 so a
  // destination can change without stale browser caches.
  if (uri.indexOf('/go/') === 0) {
    var to = GO[uri.slice(4).replace(/\/$/, '')];
    if (to) return redirect(302, to);
  }

  // Printed form QR codes point at /taegeuk/1 (no slash). Redirect to the
  // directory so the page's relative PDF link resolves, then serve its index.
  if (uri.endsWith('/')) {
    req.uri = uri + 'index.html';
  } else if (uri.slice(uri.lastIndexOf('/') + 1).indexOf('.') === -1) {
    return redirect(301, uri + '/' + query(req.querystring));
  }
  return req;
}

function redirect(code, location) {
  return {
    statusCode: code,
    statusDescription: code === 301 ? 'Moved Permanently' : 'Found',
    headers: { location: { value: location } }
  };
}

function query(qs) {
  var parts = [];
  for (var k in qs) {
    var vals = qs[k].multiValue ? qs[k].multiValue : [qs[k]];
    for (var i = 0; i < vals.length; i++) {
      parts.push(vals[i].value === '' ? k : k + '=' + vals[i].value);
    }
  }
  return parts.length ? '?' + parts.join('&') : '';
}
