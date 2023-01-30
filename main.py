import argparse

# NOTE: The file can be run with 'python main.py --verbose' for more output.

class RequestIdentifier:

    # A RequestIdentifier instance gets a URI-string as input
    def __init__(self, URI):
        self.URI = URI
        self.scheme = ''
        self.path = ''
        self.params = {} 
        self.valid = False # Whether the request is valid or not
    
    # Getter methods for returning the path and the parameters
    def get_path(self):
        return self.path
    
    def get_params(self):
        return self.params

    # Getter methods for prints in client class
    def get_valid(self):
        return self.valid
    
    def get_URI(self):
        return self.URI

    # 'Public' method to be called by the client class
    def parse_and_validate(self):
        self.__parse()
        self.__validate()

    # Parse the URI string with string splitting
    # self.URI = 'visma-identity://confirm?source=netvisor&paymentnumber=102226'
    def __parse(self):
        scheme, remaining = self.URI.split('://')
        path, params = remaining.split('?')

        # Store the scheme and path
        self.scheme = scheme
        self.path = path # The request is 'identidfied' here

        # Store the parameters in the self.params dictionnary:
        # self.params = {parameter_name --> parameter_value}
        for param in params.split('&'):
            name,val = param.split('=')
            self.params[name] = val
    
    # Validates a URI request, returns True if validation successful
    def __validate(self):
        # 1) Validate scheme
        if self.scheme != 'visma-identity':
            print('Validation failed: invalid scheme.')
            return False

        # 2) Validate path 
        if self.path not in ['login','confirm','sign']: 
            print('Validation failed: invalid path.')
            return False
        
        # 3) Validate source parameter (for any path)
        if type(self.params['source']) != str:
            print('Validation failed: invalid source.')
            return False

        # 4) Path specific parameter validations
        if self.path == 'confirm' and not self.params['paymentnumber'].isdigit():
            print('Validation failed: invalid payment number.')
            return False

        if self.path == 'sign' and type(self.params['documentid']) != str:
            print('Validation failed: invalid document ID.')
            return False

        # If none of the above conditions failed, the request is valid
        print('Validation successful.')
        self.valid = True
        return True
    
    # Override the print method to print the path and parameters
    # of the URI-request
    def __str__(self):
        res = 'RequestIdentifier:\n'
        res += '  Path of request:\n'
        res += f'    {self.path}'
        res += '\n  Parameters:\n'
        for name in self.params:
            res += f'    {name} : {self.params[name]}\n'
        return res

# The IdentityClient class can initialize and 'run' a RequestIdentifier instance,
# in other words feeds a URI string and calls the parsing and validation methods
# of the RequestIdentifier class. Finally, it stores the created RequestIdentifier instance.
class IdentityClient:

    # No parameteres given as input
    def __init__(self):
        self.RI = None

    # Similar getter methods for the client class
    def get_path(self):
        return self.RI.get_path()
    
    def get_params(self):
        return self.RI.get_params()

    def get_RI(self):
        return self.RI

    def get_valid(self):
        return self.RI.get_valid()

    # This method gets the URI string as input and passes it on to
    # an initializes RequestIdentifier instance. It then calls the
    # methods of this instance to identify the URI request. The method
    # returns whether the request was valid or not.
    def run(self,URI):

        RI = RequestIdentifier(URI)
        RI.parse_and_validate()
        self.RI = RI

        return RI.get_valid()
    
    # Override print method to print the URI string and the validity of the request.
    def __str__(self):
        res = '\nIdentityClient:\n'
        res += f'  URI: {self.RI.get_URI()}\n'
        res += '  Status: ' + 'valid\n' if self.RI.get_valid() else 'invalid\n'
        return res 

# The main function has several URI request examples and demonstrates the usage of
# the client class with some examples.
def main():

    # ------------------- Intended use case ---------------------
    # Initialize an IdentityClient instance
    client = IdentityClient()

    URI = 'visma-identity://login?source=severa'

    # Feed the URI request ot the client
    valid = client.run(URI)

    # If the request is valid and identified, get the path and parameters
    if valid:
        path = client.get_path()
        params = client.get_params()
    # ... and open automatically from the correct in-app
    #     location based the path and parameters ...

    if args.verbose:
        print(client)
        print(client.get_RI())
        print('-----------------------------------')
    # ------------------------------------------------------------

    # Running some examples
    URIs = ['visma-identity://confirm?source=netvisor&paymentnumber=102226',
            'visma-identity://sign?source=vismasign&documentid=105ab44',
            'Visma-Identity://login?source=severa',
            'visma-identity://logout?source=severa',
            'visma-identity://confirm?source=netvisor&paymentnumber=102226A']

    client = IdentityClient()
    for URI in URIs:
        client.run(URI)
        if args.verbose:
            print(client)
            print(client.get_RI())
            print('-----------------------------------')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    main()