from utils.description_card import create_description_card

def create_api_fetching_description():
    description_text = (
        "This dataset was gathered using a GET request from the SpaceX REST API. "
        "Click the button to view the code snippet and explore how this data was fetched."
    )
    
    return create_description_card(
        "toggle-api-button-summary", 
        "Show/Hide Code Snippet", 
        description_text, 
        "", 
        "api-summary-content"
    )