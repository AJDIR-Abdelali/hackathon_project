# Fun Facts Pipeline

An automated pipeline that fetches random fun facts, processes them with AI to explain why they're interesting to humans, and saves the results.

## Features

- 🔄 **Data Ingestion**: Fetches random facts from external API
- 🤖 **AI Processing**: Uses Cohere's LLM to analyze facts (with simulation fallback)
- 📁 **Data Management**: Organizes raw data and processed results with timestamps
- 🛠️ **Flexible Pipeline**: Command-line interface with multiple options
- 🔒 **Secure**: Environment variables for API key management

## Project Structure

```
├── ingest.py          # Data fetching and saving
├── prompt_engine.py   # AI prompt processing
├── pipeline.py        # Main orchestration script
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (API keys)
├── .gitignore        # Git ignore file
└── data/
    ├── raw/          # Original facts data
    └── processed/    # AI-processed results
```

## Setup

1. **Clone and install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Get your API key:**
   - Go to [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)
   - Create an API key
   - Add it to your `.env` file (already created with your key)

3. **Ready to run!**

## Usage

### Basic Commands

**Full pipeline with real AI:**
```bash
py pipeline.py --real-model
```

**Quick test with simulation:**
```bash
py pipeline.py
```

### Command Options

| Flag | Description | Example |
|------|-------------|---------|
| `--real-model` | Use Cohere AI instead of simulation | `py pipeline.py --real-model` |
| `--skip-ingest` | Skip downloading new data, use existing | `py pipeline.py --skip-ingest` |
| `--mode` | Change prompt style | `py pipeline.py --mode summarize` |

### Common Combinations

```bash
# Use existing data with real AI
py pipeline.py --skip-ingest --real-model

# Summarize facts instead of explaining
py pipeline.py --real-model --mode summarize

# Custom prompt mode
py pipeline.py --real-model --mode "find the humor in"
```

### Individual Scripts

**Just fetch facts:**
```bash
py ingest.py
```

**Just process existing facts:**
```bash
py prompt_engine.py
```

## Pipeline Steps

1. **Ingest** → Fetches 10 random facts and saves to `data/raw/`
2. **Transform** → Processes each fact through AI with prompts like:
   - `"Explain why this fun fact is interesting to humans: {fact}"`
   - `"Summarize this fun fact in one sentence: {fact}"`
3. **Save** → Outputs results to `data/processed/` in JSON and text formats

## Example Output

```
Fact: Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible.

AI Insight: This fact fascinates humans because it challenges our understanding of food preservation and connects us to ancient civilizations. The idea that we could theoretically eat the same honey as ancient Egyptians creates a tangible link across millennia...
```

## File Formats

**Input** (from API):
- Raw facts with metadata saved as structured text files

**Output**:
- JSON files with structured data (facts, prompts, AI responses)
- Human-readable text files for easy review
- All files timestamped for organization

## Environment Variables

Create a `.env` file:
```bash
COHERE_API_KEY=your_api_key_here
```

## Error Handling

- **No API key?** → Automatically falls back to simulation
- **API error?** → Graceful fallback with error message  
- **No facts data?** → Clear error message with instructions
- **Network issues?** → Continues with available data

## Requirements

- Python 3.7+
- Internet connection for fact fetching and AI processing
- Cohere API key for real AI processing (optional, has simulation mode)

## API Usage

The pipeline uses:
- **Facts API**: `https://uselessfacts.jsph.pl/api/v2/facts/random`
- **Cohere AI**: `command-r-plus` model for text generation

## Contributing

1. Fork the repository
2. Make your changes
3. Ensure `.env` is in `.gitignore`
4. Test with both `--real-model` and simulation modes
5. Submit a pull request

## License

Open source - feel free to use and modify!

---

**Quick Start:** `py pipeline.py --real-model` 🚀