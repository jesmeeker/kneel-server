import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_metals, get_single_metal, create_metal, delete_metal, update_metal, get_all_orders, get_single_order, create_order, delete_order, update_order, get_all_sizes, get_single_size, create_size, delete_size, update_size, get_all_styles, get_single_style, create_style, delete_style, update_style

method_mapper = {
    'orders': {'single': get_single_order, 'all': get_all_orders},
    'metals': {'single': get_single_metal, 'all': get_all_metals},
    'sizes': {'single': get_single_size, 'all': get_all_sizes},
    'styles': {'single': get_single_style, 'all': get_all_styles}
}


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def get_all_or_single(self, resource, id):
        if id is not None:
            response = method_mapper[resource]["single"](id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = method_mapper[resource]["all"]()

        return response

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    def do_GET(self):
        """Handles GET requests to the server """

        response = None
        (resource, id) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id)
        self.wfile.write(json.dumps(response).encode())
        # response = {}  # Default response

        # # Parse the URL and capture the tuple that is returned
        # (resource, id) = self.parse_url(self.path)

        # if resource == "metals":
        #     if id is not None:
        #         response = get_single_metal(id)

        #         if response is not None:
        #             self._set_headers(200)

        #         else:
        #             self._set_headers(404)
        #             response = {"message": "That metal does not exist."}

        #     else:
        #         self._set_headers(200)
        #         response = get_all_metals()

        # elif resource == "orders":
        #     if id is not None:
        #         response = get_single_order(id)

        #         if response is not None:
        #             self._set_headers(200)

        #         else:
        #             self._set_headers(404)
        #             response = {"message": "That order was never placed, or was cancelled."}
        #     else:
        #         self._set_headers(200)
        #         response = get_all_orders()

        # elif resource == "styles":
        #     if id is not None:
        #         response = get_single_style(id)

        #         if response is not None:
        #             self._set_headers(200)

        #         else:
        #             self._set_headers(404)
        #             response = {"message": "That style does not exist."}

        #     else:
        #         self._set_headers(200)
        #         response = get_all_styles()

        # elif resource == "sizes":
        #     if id is not None:
        #         response = get_single_size(id)

        #         if response is not None:
        #             self._set_headers(200)

        #         else:
        #             self._set_headers(404)
        #             response = {"message": "That size does not exist."}
        #     else:
        #         self._set_headers(200)
        #         response = get_all_sizes()

        # else:
        #     self._set_headers(404)
        #     response = ""

        # self.wfile.write(json.dumps(response).encode())

    def do_POST(self):

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_data = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "orders":
            if "metalId" in post_body and "sizeId" in post_body and "styleId" in post_body:
                self._set_headers(201)
                new_data = create_order(post_body)
            else:
                self._set_headers(400)
                new_data = {
                    "message": f'{"metalId is required" if "metalId" not in post_body else ""} {"sizeId is required" if "sizeId" not in post_body else ""} {"styleId is required" if "styleId" not in post_body else ""}'
                }

        if resource == "metals":
            if "metal" in post_body and "price" in post_body:
                self._set_headers(201)
                new_data = create_metal(post_body)
            else:
                self._set_headers(400)
                new_data = {
                    "message": f'{"metal is required" if "metal" not in post_body else ""} {"price is required" if "price" not in post_body else ""}'
                }

        if resource == "sizes":
            if "carets" in post_body and "price" in post_body:
                self._set_headers(201)
                new_data = create_size(post_body)
            else:
                self._set_headers(400)
                new_data = {
                    "message": f'{"carets is required" if "carets" not in post_body else ""} {"price is required" if "price" not in post_body else ""}'
                }

        if resource == "styles":
            if "style" in post_body and "price" in post_body:
                self._set_headers(201)
                new_data = create_style(post_body)
            else:
                self._set_headers(400)
                new_data = {
                    "message": f'{"style is required" if "style" not in post_body else ""} {"price is required" if "price" not in post_body else ""}'
                }

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_data).encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "orders":
            update_order(id, post_body)
        # if resource == "customers":
        #     update_customer(id, post_body)
        # if resource == "employees":
        #     update_employee(id, post_body)
        # if resource == "locations":
        #     update_location(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "orders":
            delete_order(id)
        # if resource == "customers":
        #     delete_customer(id)
        # if resource == "employees":
        #     delete_employee(id)
        # if resource == "locations":
        #     delete_location(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
