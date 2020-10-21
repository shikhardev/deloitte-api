from flask import Flask, request, abort

app = Flask(__name__)


class Keywords:
    register = None

    def __init__(self):
        self.register = set()
        self.add_new_entry("Oracle")
        self.add_new_entry("Google")
        self.add_new_entry("Microsoft")
        self.add_new_entry("Amazon")
        self.add_new_entry("Deloitte")

    def add_new_entry(self, name: str):
        self.register.add(name.capitalize())
        return True

    def remove_entry(self, name: str):
        self.register.remove(name.capitalize())
        return True

    def get_list(self):
        return list(self.register)

    def __contains__(self, item):
        return item in self.register


keywords = Keywords()


def abort_if_keyword_does_not_exist(key: str):
    if key.capitalize() not in keywords:
        abort(409, {"error": "Keyword does not exist"})


def abort_if_keyword_already_exists(key: str):
    if key.capitalize() in keywords:
        abort(409, {"error": "Keyword already exists"})


@app.route("/", methods=["GET"])
def home():
    """
    :return:
    {
        "keyword": [List of current keywords]
     }
    """
    return {"keywords": keywords.get_list()}


@app.route("/keys/<string:key>", methods=["PUT", "POST", "DELETE"])
def key_functionalities(key: str):
    """
    PUT or POST request: adds a new keyword if it doesn't exist already
    NOTE: keys are Capitalized before adding to the list, to remain case insensitive during translation
            eg, test_string is stored as Test_string
    DELETE request: deletes a keyword if it exists
    Translations are performed only for entries present in the list of  keywords

    :param key: key to be added or deleted from consideration
    :return:
            if error occurred, responds with a 409 error code
            if add / delete transaction is success, returns the following dictionary
            {
                "success": True,
                "keywords": [List of current keywords]
            }
    """
    if request.method == "PUT" or request.method == "POST":
        abort_if_keyword_already_exists(key)
        keywords.add_new_entry(key)
    elif request.method == "DELETE":
        abort_if_keyword_does_not_exist(key)
        keywords.remove_entry(key)
    return {"success": True, "keywords": keywords.get_list()}


@app.route("/keys", methods=["GET", "DELETE"])
def keys_functionalities():
    """
    GET: Gets the list of all considered keywords
    DELETE: Resets the considered keywords list to the default consideration, removing all manually added keys
    :return:
        For Get:
            { "keywords": [List of current keywords] }

        For Reset:
            {
                "success": True,
                "keywords": [List of current keywords]
            }
    """
    global keywords
    if request.method == "GET":
        return {"keywords": keywords.get_list()}
    elif request.method == "DELETE":
        keywords = Keywords()
        return {"success": True, "keywords": keywords.get_list()}


@app.route("/translate/<string:input_string>", methods=["GET"])
def translate(input_string):
    """
    Assumes space separated words as input parameter.
    Translated response match case to the input string.
        EG, Google cloud is awesome is rendered as Google cloud&copy is awesome!"
            google cloud is awesome is rendered as google cloud&copy is awesome!"
    Assumes an entity name follows a Keyword. For example, "Cloud" follows "Google".
        The copyright symbol is added on the word after a keyword.
    """
    res = []
    add_copy = False
    input_string.strip()
    inp = input_string.split(" ")
    for i in inp:
        i.strip()
        res.append(i)
        if add_copy:
            add_copy = False
            res[-1] = res[-1] + "&copy"
        if i.capitalize() in keywords.register:
            add_copy = True
    return {"translated_message": " ".join(res).lstrip()}


if __name__ == '__main__':
    app.run(debug=True)
