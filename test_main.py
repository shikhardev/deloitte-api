from unittest import TestCase, main
from main import app


class Test(TestCase):
    def test_home(self):
        tester = app.test_client(self)

        response = tester.put("/")
        self.assertEqual(response.status_code, 405)

        response = tester.post("/")
        self.assertEqual(response.status_code, 405)

        response = tester.delete("/")
        self.assertEqual(response.status_code, 405)

        response = tester.get("/test_string")
        self.assertEqual(response.status_code, 404)

        response = tester.get("/")
        self.assertEqual(response.status_code, 200)

        self.assertIn("keywords", response.json)
        self.assertEqual(5, len(response.json["keywords"]))

    def test_key_functionalities(self):
        tester = app.test_client(self)

        # Does not support get method
        response = tester.get("/keys/test_string")
        self.assertEqual(response.status_code, 405)

        # Verify functionality to add new keyword
        response = tester.put("/keys/test_string")
        self.assertEqual(response.status_code, 200)
        self.assertIn("keywords", response.json)
        self.assertEqual(6, len(response.json["keywords"]))
        self.assertIn("Test_string", response.json["keywords"])
        response = tester.get("/translate/test_string cloud is amazing!")
        self.assertEqual("test_string cloud&copy is amazing!",
                         response.json["translated_message"])

        # Keyword additions is case insensitive
        response = tester.get("/translate/Test_string cloud is amazing!")
        self.assertEqual("Test_string cloud&copy is amazing!",
                         response.json["translated_message"])

        # Should throw error if trying to add an existing keyword
        response = tester.put("/keys/test_string")
        self.assertEqual(response.status_code, 409)
        self.assertIsNone(response.json)

        # Verify functionality to delete an existing keyword
        response = tester.delete("/keys/test_string")
        self.assertEqual(response.status_code, 200)
        self.assertIn("keywords", response.json)
        self.assertEqual(5, len(response.json["keywords"]))
        self.assertNotIn("Test_string", response.json["keywords"])
        response = tester.get("/translate/test_string cloud is amazing!")
        self.assertEqual("test_string cloud is amazing!",
                         response.json["translated_message"])

        # Should throw error if trying to delete a non-existing keyword
        response = tester.delete("/keys/test_string")
        self.assertEqual(response.status_code, 409)
        self.assertIsNone(response.json)

        # Post should work the same as put
        response = tester.post("/keys/test_string")
        self.assertEqual(response.status_code, 200)
        self.assertIn("keywords", response.json)
        self.assertEqual(6, len(response.json["keywords"]))
        self.assertIn("Test_string", response.json["keywords"])

        # Resetting keyword list for future use
        tester.delete("/keys")

    def test_keys_functionalities(self):
        tester = app.test_client(self)

        # Does not support put method
        response = tester.put("/keys")
        self.assertEqual(response.status_code, 405)
        response = tester.get("/keys/test_string")
        self.assertEqual(response.status_code, 405)

        # Should return all the keywords
        response = tester.get("/keys")
        self.assertEqual(response.status_code, 200)
        self.assertIn("keywords", response.json)
        self.assertEqual(5, len(response.json["keywords"]))

        # Should return updated keywords if added new
        response = tester.post("/keys/test_string")
        self.assertEqual(6, len(response.json["keywords"]))
        self.assertIn("Test_string", response.json["keywords"])

        # Verify deleting functionality
        response = tester.delete("/keys")
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.json)
        self.assertTrue(response.json["success"])
        self.assertEqual(5, len(response.json["keywords"]))

        # Resetting keyword list for future use
        tester.delete("/keys")

    def test_translate(self):
        tester = app.test_client(self)

        # Does not support put request
        response = tester.put("/translate")
        self.assertEqual(response.status_code, 404)

        # Does not support post request
        response = tester.post("/translate")
        self.assertEqual(response.status_code, 404)

        # Does not support delete request
        response = tester.delete("/translate")
        self.assertEqual(response.status_code, 404)

        # Does not support get request without target string after a "/"
        response = tester.get("/translate")
        self.assertEqual(response.status_code, 404)

        # &copy is only added to string after keyword
        # If no string exists after keyword, return the entered string
        response = tester.get("/translate/Google")
        self.assertEqual(response.status_code, 200)
        self.assertIn("translated_message", response.json)
        self.assertEqual(response.json["translated_message"], "Google")

        # &copy is added in words following the keyword
        # Testing the default list of keyword
        response = tester.get("/translate/Google cloud is amazing")
        self.assertEqual(response.status_code, 200)
        self.assertIn("translated_message", response.json)
        self.assertEqual(response.json["translated_message"],
                         "Google cloud&copy is amazing")

        # Since "Testing" is not a keyword, &copy is not added in the response
        response = tester.get("/translate/Testing cloud is amazing")
        self.assertEqual(response.status_code, 200)
        self.assertIn("translated_message", response.json)
        self.assertEqual(response.json["translated_message"],
                         "Testing cloud is amazing")

        # Verify if translation works after ading a new keyword
        tester.put("/keys/testing")
        response = tester.get("/translate/Testing cloud is amazing")
        self.assertEqual(response.status_code, 200)
        self.assertIn("translated_message", response.json)
        self.assertEqual(response.json["translated_message"],
                         "Testing cloud&copy is amazing")

        # Adding new keys is case insensitive and returns translation as per input case
        response = tester.get("/translate/testing cloud is amazing")
        self.assertEqual(response.status_code, 200)
        self.assertIn("translated_message", response.json)
        self.assertEqual(response.json["translated_message"],
                         "testing cloud&copy is amazing")


if __name__ == '__main__':
    main()
