# receipt-processor-challenge

This is a simple Receipt Processor API written in Python using Flask.


## Prerequisites

-Python 3

-Python Flask pip install Flask

-postman (for testing)

## Running the API locally

-Clone the repository:  
git clone https://github.com/arishaly/receipt-processor-challenge.git

-Navigate to the project directory:

-Run the Python script:

fetch.py

The Flask app will start running at http://127.0.0.1:5000/.



## Testing the API

-Open Postman

-Test Endpoint 1: Process Receipts (POST)

1.URL: http://127.0.0.1:5000/receipts/process

2.Method: POST (Note: you might need to add the following to Headers key:Content-type value: application/json)

3.Payload: The example below needs to be in the body
```python
{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}
```
4.Response: JSON containing an ID for the receipt
-Example Response:

{ "id": "b8ea8beb-9a1b-427b-89e3-bc92c6dce529" }

-Test Endpoint 2: Get Points (GET)

1.URL: http://127.0.0.1:5000/receipts/{id}/points (replace {id} with the ID obtained from Endpoint 1)

2.Method: GET

3.Response: JSON containing the number of points awarded

-Example Response:

{ "points": 22 }
