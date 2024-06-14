import json
from utils import load_comments, analyze_sentiment, print_header

def test_load_comments():
    # Mock JSON data to test load_comments
    mock_json_data = [
        {
            "content": "I love the new update! Everything works perfectly.",
            "date": "13-06-2024"
        },
        {
            "content": "The app keeps crashing. Very frustrating!",
            "date": "13-06-2024"
        },
        {
            "content": "Not bad, but could be better.",
            "date": "13-06-2024"
        }
    ]
    
    # Write mock data to a temporary file
    with open('mock_google_play_reviews.json', 'w', encoding='utf-8') as f:
        for entry in mock_json_data:
            f.write(json.dumps(entry) + '\n')
    
    # Load comments using the function
    comments = load_comments('mock_google_play_reviews.json')
    
    # Check if the loaded comments match the mock data
    assert comments == [
        {
            "content": "I love the new update! Everything works perfectly.",
            "date": "13-06-2024"
        },
        {
            "content": "The app keeps crashing. Very frustrating!",
            "date": "13-06-2024"
        },
        {
            "content": "Not bad, but could be better.",
            "date": "13-06-2024"
        }
    ]

def test_analyze_sentiment():
    comments = [
        {
            "content": "I love the new update! Everything works perfectly.",
            "date": "13-06-2024"
        },
        {
            "content": "The app keeps crashing. Very frustrating!",
            "date": "13-06-2024"
        },
        {
            "content": "Not bad, but could be better.",
            "date": "13-06-2024"
        }
    ]
    analyze_sentiment(comments)

def test_print_header():
    print_header("Test Header")

if __name__ == "__main__":
    test_load_comments()
    test_analyze_sentiment()
    test_print_header()
