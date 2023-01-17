import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import all, retrieve, update, create, delete, get_all_metals, get_single_metal, create_metal, delete_metal, update_metal, get_all_orders, get_single_order, create_order, delete_order, update_order, get_all_sizes, get_single_size, create_size, delete_size, update_size, get_all_styles, get_single_style, create_style, delete_style, update_style

method_mapper = {
    'single': retrieve, 'all': all
}


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def get_all_or_single(self, resource, id):
        """Determines whether the client is needing all items or a single item and then calls the correct function.
        """
        if id is not None:
            response = method_mapper["single"](resource, id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = method_mapper["all"](resource)

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

        if resource in ('styles', 'sizes', 'metals'):
            self._set_headers(405)

        elif resource == "orders":
            if "metalId" in post_body and "sizeId" in post_body and "styleId" in post_body:
                self._set_headers(201)
                new_data = create(resource, post_body)
            else:
                self._set_headers(400)
                new_data = {
                    "message": f'{"metalId is required" if "metalId" not in post_body else ""} {"sizeId is required" if "sizeId" not in post_body else ""} {"styleId is required" if "styleId" not in post_body else ""}'
                }

        self.wfile.write(json.dumps(new_data).encode())


        # if resource == "metals":
        #     if "metal" in post_body and "price" in post_body:
        #         self._set_headers(201)
        #         new_data = create_metal(post_body)
        #     else:
        #         self._set_headers(400)
        #         new_data = {
        #             "message": f'{"metal is required" if "metal" not in post_body else ""} {"price is required" if "price" not in post_body else ""}'
        #         }

        # if resource == "sizes":
        #     if "carets" in post_body and "price" in post_body:
        #         self._set_headers(201)
        #         new_data = create_size(post_body)
        #     else:
        #         self._set_headers(400)
        #         new_data = {
        #             "message": f'{"carets is required" if "carets" not in post_body else ""} {"price is required" if "price" not in post_body else ""}'
        #         }

        # if resource == "styles":
        #     if "style" in post_body and "price" in post_body:
        #         self._set_headers(201)
        #         new_data = create_style(post_body)
        #     else:
        #         self._set_headers(400)
        #         new_data = {
        #             "message": f'{"style is required" if "style" not in post_body else ""} {"price is required" if "price" not in post_body else ""}'
        #         }

    def do_PUT(self):
        """For PUT requests to a single resource"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource in ('orders', 'sizes', 'styles'):
            self._set_headers(405)

        if resource == "metals":
            self._set_headers(204)
            update(resource, id, post_body)
        
        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        self._set_headers(405)
        

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
