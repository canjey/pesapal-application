# PesaPal Problems Solutions
## Solutions to Problem 1 and Problem 3
### Setup
One must have python installed inorder to run the application

`
pip install -r requirements.text
`
### Problem 1
I created a HTTP web server application that would serve both static HTML and dynamically generated HTML using python, in the way Apache uses PHP. 
The server supports GET or POST requests 

More documentation is found in the code


To run the application

` python webserver.py ./sampleapp 8000
`      

### Problem 3
I created an application which asks the user for a url of the web page, which then downloads the text on it and counts the occurrences of each word.
The application works with wordnet dictionary that helps as find the non-english words on the page.
The user can compare words in two or more pages.

More documentation is found in the code

To run the application

`python dictionSol.py run
`
