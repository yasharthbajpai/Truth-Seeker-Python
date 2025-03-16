# Truth Seeker 🕵️‍♀️

A Python-based fact-checking tool that leverages the Perplexity API to verify claims and statements, providing clear verdicts, explanations, and corrections with a user-friendly colored terminal interface.

## Features

- **Real-time Fact Checking**: Verify the accuracy of statements and claims using Perplexity AI
- **Structured Results**: Get clear verdicts (True, Partially True, False, or Undetermined)
- **Detailed Explanations**: Understand the reasoning behind each verdict
- **Suggested Corrections**: Receive corrections for inaccurate information
- **Colorful Terminal Interface**: Easy-to-read color-coded results with emoji indicators
- **Save Results**: Option to save fact-check results to text files for future reference

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/truth-seeker.git
   cd truth-seeker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory with your Perplexity API key:
   ```
   PERPLEXITY_API_KEY=pplx-
   PERPLEXITY_MODEL=sonar-pro
   ```

## Usage

Run the program:
```
python fact_checker.py
```

Follow the interactive prompts:
1. Enter the statement you want to fact-check
2. Review the verdict, explanation, and corrections
3. Choose whether to save the results
4. Continue with another fact-check or exit

## Example

```
=== FACT CHECKING ASSISTANT 🕵️‍♀️ ===
This program will help you verify the accuracy of statements and claims.

------------------------------------------------------------
Enter the statement or claim you want to fact-check 🔍
(or type 'exit' to quit):

> The Earth is flat

Fact-checking in progress... 🔍

============================================================
FACT CHECK RESULTS ✅
============================================================

CLAIM: 💬
The Earth is flat

VERDICT: ❌ 
False

EXPLANATION: 🔍
The claim that "The Earth is flat" is false. There is overwhelming scientific evidence that the Earth is approximately spherical (technically an oblate spheroid). This has been confirmed through multiple lines of evidence including:

1. Photographs from space showing Earth's curvature
2. Circumnavigation of the Earth
3. The way ships disappear hull-first over the horizon
4. Time zone differences
5. The curved shadow of Earth during lunar eclipses
6. Gravitational measurements
7. GPS satellite operations that account for Earth's shape

CORRECTIONS: 📝
The Earth is not flat but is an oblate spheroid (a sphere slightly flattened at the poles and bulging at the equator). Its shape has been well-established by scientific observations and measurements for centuries.

Do you want to save this fact-check result? (y/n): 💾 y

Result saved to: fact_check_results/fact-check-The-Earth-is-flat-1710618360.txt ✅

Do you want to fact-check another statement? (y/n): 🔄 n

Thank you for using the Fact Checking Assistant. Goodbye! 👋
```

## How It Works

1. The program takes user input for claims to verify
2. It sends the claim to Perplexity AI with a specialized prompt for fact-checking
3. The AI response is parsed to extract the verdict, explanation, and corrections
4. Results are displayed with color-coding for easy interpretation
5. Users can save results to text files for future reference

## Requirements

```
openai==0.28
python-dotenv
colorama
```

## Video Demo

A video demonstration of Truth Seeker is available [here](https://drive.google.com/file/d/1C7lit2uCIwIQIRZBzzPH-iRRCcyMG7Al/view?usp=sharing).


## License

All rights reserved.

---

Made by Yasharth Bajpai  
© 2025

