from http.server import HTTPServer, SimpleHTTPRequestHandler


def run():
    httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
