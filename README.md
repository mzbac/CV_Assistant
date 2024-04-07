# CV Assistant

The CV Assistant is a Python-based project that leverages the Anthropic API to refine and tailor a CV according to a specific job description. The result is a polished, job-specific CV.

## Project Structure

This project consists of the following files:

- `main.py`: The primary Python script that drives the functionality of the CV Assistant.
- `cv.md`: A Markdown file that contains the original CV.
- `job_description.md`: A Markdown file that contains the job description.

## Prerequisites

To use the CV Assistant, you need:

- Python 3.x installed on your machine.
- An Anthropic API key.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

To configure the CV Assistant, you need to update the Anthropic API key in the `main.py` file. Replace the placeholder text in the following line with your actual API key:

```python
ANTHROPIC_API_KEY = "YOUR KEY HERE"  # Replace with your Anthropic API key
```

## How to Use

1. Update the `cv.md` and `job_description.md` files with your CV and desired job description, respectively.
2. Run the following command in your terminal:

```
python main.py
```

This will generate a tailored CV based on the job description provided.
