This project is an AI powered chatbot that aims to make employment contract creation accessible to people who are not profecient in English and creating contracts that are easy to understand. 

Steps for setup:
1. In watsonx.py, initialise the following variables (line 37-40):
    1. project_id 
    2. api_key
    3. access_token
    4. ibm_cloud_iam_url
2. In the main directory, create a file titled .env and initialise the following variables in the file:
    1. API_KEY
    2. PROJECT_ID
    3. IAM_IBM_CLOUD_URL

Usage guide:
1. Train the AI model by dropping a pdf document into the docs folder. We have already included one CHATBOTFOOD.pdf in the docs folder so feel free to use that. If you want to add your own document, your document can either be named as CHATBOTFOOD.pdf or "CHATBOTFOOD.pdf" in the documents1 variable (line 22) in app.py can be replaced by the name of your document.     
2. Run all the .py scripts in the src folder
3. Browse to localhost:8501 in the browser of your choice. You should see a chatbot interface.
3. In the chatbox at the bottom of the screen, input a prompt for contract writing. It does not have to be in perfect English. For example: can help me write contract for my new part timer ah
4. It should ask for details of the employment. Respond accordingly. 

Contributors:
Emma Hope Ong,
Gurugubelli Rashini Das,
Gavin Ng Kar Swee

Limitations: we do not have access to a GPU and was unable to train the AI model with too large of a document. 
