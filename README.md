# Deloitte Cloud Engineer assignment API
Available at [URL](https://deloitte-api.ue.r.appspot.com/) 

    https://deloitte-api.ue.r.appspot.com/

The APIs have been built using Flask and deployed using Google App Engine. Python has been used, since it is one of the preferred languages in the cloud engineering team. Flask has been used, since it is extremely easy to directly get into the business logic and make API endpoints. Google App Engine has been used, since it allows to easily deploy scalable applications.

No authentication has been added, since server is live only on request. 


# Functionalities supported
## Translate
Translates the input string into the specified format with a copyright symbol.
    
    Sample Input:  Google Cloud is awesome!
    Sample Output: Google Cloud© is awesome!
    
    
    Sample Input:  Google
    Sample Output: Google
    
    
    Sample Input:  Amazon EKS is awesome!
    Sample Output: Amazon EKS© is awesome!
    
    
    Sample Input:  amazon EKS is awesome!
    Sample Output: amazon EKS© is awesome!


## Keywords
Allows users to add new or or delete existing keywords for which translation can be supported.
Functionality to Reset to default keywords also provided. 
Keywords are tied to a session and not written to any database for now.



# API endpoints
## Index 

```GET /```

Lists currently supported keywords for translation.


    Example
    Request: GET request to "https://deloitte-api.ue.r.appspot.com/"
    Response: 
    {
      "keywords": [
        "Microsoft", 
        "Amazon", 
        "Oracle", 
        "Google", 
        "Deloitte"
      ]
    }


----------
## Translate 

```GET /translate/<input_string>```

Translates input string. Insert input string after `/translate/`  without any angle brackets.

    Example
    Request: GET request to "https://deloitte-api.ue.r.appspot.com/translate/Google Cloud is amazing!"
    Response: 
    {
        "translated_message": "Google Cloud&copy is amazing!"
    }
        
----------
## Keys

 ```GET /keys```
 
Lists currently supported keywords for translation.

    Example
    Request: GET request to "https://deloitte-api.ue.r.appspot.com/keys"
    Response: 
    {
      "keywords": [
        "Microsoft", 
        "Amazon", 
        "Oracle", 
        "Google", 
        "Deloitte"
      ]
    }
        
     

```PUT or POST /keys/<keyword>```

Adds <keyword> to the list of supported translation keywords. The new keyword is to be added without angle brackets.

    Example
    Request: POST request to "https://deloitte-api.ue.r.appspot.com/keys/Shikhar"
    Response: 
    {
        "keywords": [
            "Microsoft",
            "Amazon",
            "Oracle",
            "Shikhar",
            "Google",
            "Deloitte"
        ],
        "success": true
    }


```DELETE /keys/<keyword>```

Deletes <keyword> from the list of supported translation. The keyword is to be added without angle brackets.

    Example
    Request: DELETE request to "https://deloitte-api.ue.r.appspot.com/keys/Shikhar"
    Response: 
    {
        "keywords": [
            "Microsoft",
            "Amazon",
            "Oracle",
            "Google",
            "Deloitte"
        ],
        "success": true
    }


    Example
    Request: DELETE request to "https://deloitte-api.ue.r.appspot.com/keys/Shikhar" where Shikhar has already been deleted. 
    Response: 
    {
        'error': 'keyword does not exist'
    }

```DELETE /keys```

Resets the list of supported keywords to the default list of [Oracle, Google, Microsoft, Amazon, Deloitte]

    Example
    Request: DELETE request to "https://deloitte-api.ue.r.appspot.com/keys"
    Response: 
    {
        "keywords": [
            "Microsoft",
            "Amazon",
            "Oracle",
            "Google",
            "Deloitte"
        ],
        "success": true
    }
----------



