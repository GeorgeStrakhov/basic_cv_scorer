from llm import answer, answer_json
from cv_scorer import CVScorer

def test_basic_response():
    print("Testing basic response:")
    response = answer("What is the capital of France?")
    print(f"Answer: {response}\n")

def test_json_response():
    print("Testing JSON response:")
    response = answer_json("Give me information about France's capital in JSON format with these fields: city, population, country")
    print("JSON Answer:")
    print(json.dumps(response, indent=2))

def process_cvs():
    print("\nProcessing CVs:")
    scorer = CVScorer()
    scorer.process_cvs()

if __name__ == "__main__":
    import json
    
    print("=== LLM Testing Script ===\n")
    
    try:
        test_basic_response()
        test_json_response()
    except Exception as e:
        print(f"An error occurred: {str(e)}")