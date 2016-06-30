def format_string(string, formatter=None):
    class DefaultFormatter:
        def format(self, string):
            return str(string).title()
    if not formatter:
        formatter = DefaultFormatter()
    return formatter.format(string)

hello_string = "hello, world, how are you today?"
print(" input: " + hello_string)
print("output: " + format_string(hello_string))