"""
Mock Recipe Server for Mealie URL Import Testing (Luồng 1)
- Phục vụ Schema.org/Recipe JSON-LD qua HTTP port 9926
- Cho phép Mealie import công thức qua URL: http://host.docker.internal:9926/recipe/pho-bo
- Sử dụng thư viện chuẩn của Python (không yêu cầu cài thêm package)
"""

import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 9926

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Phở Bò Hà Nội</title>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Recipe",
    "name": "Phở Bò Hà Nội",
    "description": "Món phở bò truyền thống Việt Nam nước dùng đậm đà",
    "recipeYield": "4 servings",
    "recipeIngredient": [
      "500g beef brisket",
      "400g rice noodles",
      "1 onion (halved)",
      "2 tablespoons fish sauce",
      "1 cinnamon stick"
    ],
    "recipeInstructions": [
      {
        "@type": "HowToStep",
        "text": "Hầm xương và thịt bò với quế hồi trong 3 giờ."
      },
      {
        "@type": "HowToStep",
        "text": "Chần bánh phở và xếp vào tô."
      },
      {
        "@type": "HowToStep",
        "text": "Chan nước dùng nóng hổi và thêm hành ngò."
      }
    ]
  }
  </script>
</head>
<body>
  <h1>Phở Bò Hà Nội</h1>
  <p>Món phở bò truyền thống Việt Nam nước dùng đậm đà</p>
</body>
</html>
"""

class RecipeHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/recipe/pho-bo", "/recipe/pho-bo/", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(HTML_CONTENT.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
            print(f"[{self.log_date_time_string()}] 200 OK: Phục vụ công thức Phở Bò Hà Nội cho {self.client_address[0]}", flush=True)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Not Found")

    def log_message(self, format, *args):
        pass

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, RecipeHandler)
    print(f"Mock Recipe Server đang chạy tại http://0.0.0.0:{PORT} ...")
    print(f"URL để import vào Mealie: http://host.docker.internal:{PORT}/recipe/pho-bo")
    print("Nhấn Ctrl+C để dừng server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng server.")
        httpd.server_close()

if __name__ == "__main__":
    main()
