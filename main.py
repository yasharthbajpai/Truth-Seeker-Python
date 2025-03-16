import os
import time
import json
import re
import openai
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init()

# Load environment variables
load_dotenv()

# Initialize Perplexity API client
openai.api_key = os.getenv("PERPLEXITY_API_KEY")
openai.api_base = "https://api.perplexity.ai"
model = os.getenv("PERPLEXITY_MODEL", "mistral-7b-instruct")

def print_colored(text, color=Fore.WHITE, bold=False):
    """Print colored text to terminal"""
    if bold:
        print(f"{color}{Style.BRIGHT}{text}{Style.RESET_ALL}")
    else:
        print(f"{color}{text}{Style.RESET_ALL}")

def clean_text(text):
    """Remove citations like [1][2]"""
    return re.sub(r'\[\d+\](?:\[\d+\])*', '', text).strip()

def parse_fact_check_response(text):
    """Parse the fact-checking response from Perplexity"""
    try:
        # Try to parse as JSON first
        try:
            json_response = json.loads(text)
            if json_response.get("verdict") and json_response.get("explanation") and json_response.get("corrections"):
                return {
                    "verdict": clean_text(json_response["verdict"]),
                    "explanation": clean_text(json_response["explanation"]),
                    "corrections": clean_text(json_response["corrections"])
                }
        except json.JSONDecodeError:
            # Not JSON, continue with regex parsing
            pass
        
        # Check if the response already has the expected format
        if "VERDICT:" in text and "EXPLANATION:" in text and "CORRECTIONS:" in text:
            verdict_match = re.search(r'VERDICT:(.*?)(?=EXPLANATION:|$)', text, re.DOTALL)
            explanation_match = re.search(r'EXPLANATION:(.*?)(?=CORRECTIONS:|$)', text, re.DOTALL)
            corrections_match = re.search(r'CORRECTIONS:(.*?)(?=$)', text, re.DOTALL)
            
            return {
                "verdict": clean_text(verdict_match.group(1).strip()) if verdict_match else "Undetermined",
                "explanation": clean_text(explanation_match.group(1).strip()) if explanation_match else clean_text(text),
                "corrections": clean_text(corrections_match.group(1).strip()) if corrections_match else "No corrections provided."
            }
        
        # If all else fails, use a simple heuristic approach
        if any(word in text.lower() for word in ["true", "accurate", "correct", "factual"]):
            paragraphs = text.split('\n\n')
            first_paragraph = paragraphs[0]
            last_paragraph = paragraphs[-1]
            
            return {
                "verdict": "Likely True",
                "explanation": clean_text(text[:text.rfind(last_paragraph)].strip()) if len(paragraphs) > 1 else clean_text(text),
                "corrections": "No corrections needed."
            }
        elif any(word in text.lower() for word in ["false", "inaccurate", "incorrect", "misleading"]):
            paragraphs = text.split('\n\n')
            first_paragraph = paragraphs[0]
            
            return {
                "verdict": "Likely False",
                "explanation": clean_text(first_paragraph),
                "corrections": clean_text(text[len(first_paragraph):].strip()) if len(paragraphs) > 1 else "No specific corrections provided."
            }
        else:
            return {
                "verdict": "Undetermined",
                "explanation": clean_text(text),
                "corrections": "Unable to determine specific corrections."
            }
    except Exception as error:
        print(f"Error parsing fact-check response: {error}")
        return {
            "verdict": "Error",
            "explanation": clean_text(text),
            "corrections": "Error parsing the fact-check response."
        }

def fact_check(content):
    """Send content to Perplexity for fact-checking"""
    print_colored("\nFact-checking in progress... 🔍", Fore.CYAN)
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": 'You are a fact-checking assistant. Your job is to verify the accuracy of the given information and provide a clear verdict. Structure your response in three parts:\n\n1. A clear verdict (True, Partially True, False, or Undetermined)\n2. A detailed explanation of your reasoning\n3. Any necessary corrections to the information\n\nFormat your response exactly as follows:\n\nVERDICT: [your verdict here]\n\nEXPLANATION: [your detailed explanation]\n\nCORRECTIONS: [any corrections to the information]'
                },
                {"role": "user", "content": f"Please fact-check the following information: {content}"}
            ],
            max_tokens=1024
        )

        raw_content = response.choices[0].message.content
        parsed_response = parse_fact_check_response(raw_content)
        
        return parsed_response
    except Exception as error:
        print_colored(f"Error: {error} ❌", Fore.RED)
        return {
            "verdict": "Error",
            "explanation": f"An error occurred: {str(error)}",
            "corrections": "Unable to complete fact-checking due to an error."
        }

def save_result(content, result, filename=None):
    """Save the fact-checking result to a file"""
    if not filename:
        # Create a sanitized filename from the content
        filename = re.sub(r'[^\w\s-]', '', content[:30])
        filename = re.sub(r'[-\s]+', '-', filename).strip('-')
        filename = f"fact-check-{filename}-{int(time.time())}.txt"
    
    # Create results directory if it doesn't exist
    results_dir = "fact_check_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    file_path = os.path.join(results_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"FACT CHECK RESULTS\n")
        f.write(f"=================\n\n")
        f.write(f"CLAIM: {content}\n\n")
        f.write(f"VERDICT: {result['verdict']}\n\n")
        f.write(f"EXPLANATION:\n{result['explanation']}\n\n")
        f.write(f"CORRECTIONS:\n{result['corrections']}\n\n")
        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    return file_path

def display_result(content, result):
    """Display the fact-checking result in the terminal"""
    print("\n" + "="*60)
    print_colored("FACT CHECK RESULTS ✅", Fore.CYAN, bold=True)
    print("="*60 + "\n")
    
    print_colored("CLAIM: 💬", Fore.YELLOW, bold=True)
    print(f"{content}\n")
    
    # Color-code the verdict
    verdict = result["verdict"]
    verdict_emoji = ""
    if "true" in verdict.lower():
        verdict_color = Fore.GREEN
        verdict_emoji = "✅ "
    elif "false" in verdict.lower():
        verdict_color = Fore.RED
        verdict_emoji = "❌ "
    elif "partially" in verdict.lower():
        verdict_color = Fore.YELLOW
        verdict_emoji = "⚠️ "
    else:
        verdict_color = Fore.WHITE
        verdict_emoji = "❓ "
    
    print_colored(f"VERDICT: {verdict_emoji}", Fore.CYAN, bold=True)
    print_colored(verdict, verdict_color, bold=True)
    print()
    
    print_colored("EXPLANATION: 🔍", Fore.CYAN, bold=True)
    print(f"{result['explanation']}\n")
    
    print_colored("CORRECTIONS: 📝", Fore.CYAN, bold=True)
    print(f"{result['corrections']}\n")

def main():
    """Main function to run the fact-checking program"""
    print_colored("\n=== FACT CHECKING ASSISTANT 🕵️‍♀️ ===", Fore.CYAN, bold=True)
    print_colored("This program will help you verify the accuracy of statements and claims.", Fore.WHITE)
    
    while True:
        print("\n" + "-"*60)
        print_colored("Enter the statement or claim you want to fact-check 🔍", Fore.YELLOW)
        print_colored("(or type 'exit' to quit):", Fore.YELLOW)
        
        content = input("\n> ")
        
        if content.lower() in ['exit', 'quit', 'q']:
            print_colored("\nThank you for using the Fact Checking Assistant. Goodbye! 👋", Fore.CYAN)
            break
        
        if not content.strip():
            print_colored("Please enter a statement or claim to fact-check. ⚠️", Fore.RED)
            continue
        
        # Perform fact-checking
        result = fact_check(content)
        
        # Display the result
        display_result(content, result)
        
        # Ask if user wants to save the result
        save_option = input("\nDo you want to save this fact-check result? (y/n): 💾 ").lower()
        if save_option in ['y', 'yes']:
            file_path = save_result(content, result)
            print_colored(f"\nResult saved to: {file_path} ✅", Fore.GREEN)
        
        # Ask if user wants to continue
        continue_option = input("\nDo you want to fact-check another statement? (y/n): 🔄 ").lower()
        if continue_option not in ['y', 'yes']:
            print_colored("\nThank you for using the Fact Checking Assistant. Goodbye! 👋", Fore.CYAN)
            break

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("PERPLEXITY_API_KEY"):
        print_colored("Error: PERPLEXITY_API_KEY not found in environment variables. ❌", Fore.RED)
        print("Please make sure you have a .env file with your API key. 🔑")
        exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\nProgram interrupted. Exiting... 👋", Fore.YELLOW)
    except Exception as e:
        print_colored(f"\nAn unexpected error occurred: {str(e)} ❌", Fore.RED)
        import traceback
        traceback.print_exc()
