#!/usr/bin/env python3
"""Dev server for the Toco site — serves fresh files, never cached HTML."""
import http.server, functools, os

ROOT = os.path.dirname(os.path.abspath(__file__))

class FreshHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # HTML/CSS/JS always revalidated; images may cache briefly
        if self.path.endswith(('.html', '/', '.js', '.css', '.svg')) or '.' not in self.path.split('/')[-1]:
            self.send_header('Cache-Control', 'no-store, must-revalidate')
        else:
            self.send_header('Cache-Control', 'max-age=60')
        super().end_headers()

if __name__ == '__main__':
    handler = functools.partial(FreshHandler, directory=ROOT)
    http.server.ThreadingHTTPServer(('127.0.0.1', 4173), handler).serve_forever()
