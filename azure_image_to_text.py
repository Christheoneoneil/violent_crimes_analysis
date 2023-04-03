from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
#from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import azure_keys as keys
import time
from pdf2image import convert_from_path



# Define key, endpoint, and client
subscription_key = keys.key1
endpoint = keys.endpoint
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))



def extract_text(the_pdf_path, the_txt_path):

    '''Given a pdf containing handwritten and/or typed text, this function 
    outputs the identified text to a .txt file'''

    # Convert PDF to image using pdf2image library
    pages = convert_from_path(the_pdf_path, 300)
    for i, page in enumerate(pages):
        # Save temporary image file
        img_path = f"temp_image_{i}.jpg"
        page.save(img_path)

    print("===== Read File - local =====")

    # Open the image
    read_image = open(img_path, "rb")

    # Call API with image and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(read_image, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        print ('Waiting for result...')
        time.sleep(10)

    # Print results, line by line and store it in a .txt file
    with open(the_txt_path, 'w') as f:
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    print(line.text)
                    print(line.bounding_box)
                    f.write(line.text + ' ')

    '''
    END - Read File - local
    '''
    print("End of Computer Vision quickstart.")



# example of function use
the_pdf_path = 'shooters_words_images/castillo_journal.pdf'
the_txt_path = 'shooters_words_text/castillo_journal.txt'
extract_text(the_pdf_path, the_txt_path)
