# pipeline.py
import argparse
import json
import os
from datetime import datetime
from ingest import get_facts, save_facts_as_txt
from prompt_engine import call_model, load_facts

def save_output(results, mode="explain"):
    """Save the processed results to file."""
    os.makedirs("data/processed", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    
    # Save as JSON
    json_filename = f"data/processed/pipeline_results_{mode}_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Save as readable text
    txt_filename = f"data/processed/pipeline_results_{mode}_{timestamp}.txt"
    with open(txt_filename, 'w', encoding='utf-8') as f:
        for i, result in enumerate(results, 1):
            f.write(f"RESULT {i}:\n")
            f.write(f"Fact: {result['fact']}\n")
            f.write(f"Output: {result['output']}\n")
            f.write("=" * 60 + "\n")
    
    print(f"Results saved to {json_filename} and {txt_filename}")

# def transform_data(facts, mode="explain"):
def transform_data(facts, mode="explain", use_real_model=False):
    """Transform facts using prompt engine with specified mode."""
    results = []
    
    for fact in facts:
        # Customize prompt based on mode
        if mode == "explain":
            prompt = f"Explain why this fun fact is interesting to humans: {fact}"
        elif mode == "summarize":
            prompt = f"Summarize this fun fact in one sentence: {fact}"
        else:
            prompt = f"{mode} this fun fact: {fact}"
        
        # Get response from model
        # output = call_model(prompt)
        output = call_model(prompt, use_real_model=use_real_model)

        
        results.append({
            'fact': fact,
            'prompt': prompt,
            'output': output,
            'mode': mode
        })
    
    return results

# def run_pipeline(skip_ingest=False, mode="explain"):
def run_pipeline(skip_ingest=False, mode="explain", use_real_model=False):
    """Run the complete pipeline."""
    print(f"Starting pipeline with mode: {mode}")
    
    # Step 1: Ingest data (unless skipped)
    if not skip_ingest:
        print("Step 1: Ingesting new data...")
        facts_data = get_facts(10)
        save_facts_as_txt(facts_data)
        print("Data ingestion complete.")
    else:
        print("Step 1: Skipping data ingestion (using existing data)")
    
    # Step 2: Transform data using prompt engine
    print("Step 2: Loading facts and transforming with prompt engine...")
    facts = load_facts()
    
    if not facts:
        print("Error: No facts found. Please run without --skip-ingest first.")
        return
    
    # results = transform_data(facts, mode)
    results = transform_data(facts, mode=mode, use_real_model=use_real_model)
    print(f"Processed {len(results)} facts")
    
    # Step 3: Save the output
    print("Step 3: Saving output...")
    save_output(results, mode)
    
    print("Pipeline complete!")
    
    # Print sample results
    print("\nSample results:")
    for i, result in enumerate(results[:3]):  # Show first 3
        print(f"\nFact {i+1}: {result['fact'][:50]}...")
        print(f"Output: {result['output'][:80]}...")

def main():
    parser = argparse.ArgumentParser(description="Run the facts processing pipeline")
    
    parser.add_argument(
        "--skip-ingest", 
        action="store_true",
        help="Skip downloading new data, reuse the most recent raw file"
    )
    
    parser.add_argument(
        "--mode",
        type=str,
        default="explain",
        help='Customize the prompt mode (e.g., "explain", "summarize")'
    )

    parser.add_argument(
        "--real-model",
        action="store_true",
        help="Use the real Cohere model instead of simulation"
    )

    args = parser.parse_args()

    run_pipeline(skip_ingest=args.skip_ingest, mode=args.mode, use_real_model=args.real_model)


if __name__ == "__main__":
    main()