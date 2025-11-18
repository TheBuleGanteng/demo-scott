# AI Opportunity Finder

A rapid prototype demonstrating the ability to quickly build AI-powered business solutions. This Streamlit application analyzes business process descriptions and generates concrete AI implementation opportunities with impact and complexity estimates.

## Purpose

This project showcases rapid prototyping skills for AI-based solutions. Given a brief problem statement describing a business workflow, the application leverages GPT-4o-mini to identify high-ROI AI use cases tailored to enterprise constraints.

## Features

- Analyzes business process descriptions
- Generates 3-5 concrete AI solution proposals
- Provides impact and complexity estimates for each solution
- Suggests MVPs achievable within 4-6 weeks
- Optimizes recommendations based on user-selected goals (cost savings, revenue uplift, risk reduction)

## Requirements

- Python 3.10+
- OpenAI API key

### Dependencies

```
streamlit
openai>=1.6.0
python-dotenv
```

## Setup

### Local Development

1. Clone the repository:
   ```bash
   git clone git@github.com:TheBuleGanteng/demo-scott.git
   cd demo-scott
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

5. Run the application:
   ```bash
   streamlit run app/app.py
   ```

### Docker Deployment

The application includes a Dockerfile for containerized deployment:

```bash
docker build -t scott-demo .
docker run -p 8501:8501 -v /path/to/.env:/app/.env scott-demo
```

## Usage

1. Open the application in your browser
2. Describe your current business process in the text area
3. Select your primary goal (cost savings, revenue uplift, or risk reduction)
4. Optionally specify your industry context
5. Click "Generate AI opportunities"
6. Review the generated AI solution proposals

## Example Input

```
Our customer support team handles ~2,000 emails per day. Agents manually read
each email, classify the issue, reply using templates, and escalate to Tier 2
when they're unsure...
```

## Live Demo

Available at: https://kebayorantechnologies.com/scott-demo

## License

See LICENSE file for details.
