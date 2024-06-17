---
categories:
  - Code
tags:
  - linux
  - scripts
comment: 'https://github.com/whitead/paper-qa'
info: aberto.
date: '2024-06-16'
type: post
layout: post
published: true
slug: clipaper-qa
title: 'cliPaperQA'

---

# PaperQA CLI Script Documentation

This documentation provides a comprehensive guide on how to use the provided PaperQA CLI script. The script is designed to process PDF documents, generate embeddings, and answer questions using OpenAI's language models.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
    - [Command Line Arguments](#command-line-arguments)
    - [Examples](#examples)
5. [Detailed Explanation](#detailed-explanation)
    - [Loading Custom Prompts](#loading-custom-prompts)
    - [Creating Docs Object](#creating-docs-object)
    - [Loading Existing Embeddings](#loading-existing-embeddings)
    - [Adding PDF Documents](#adding-pdf-documents)
    - [Getting Questions](#getting-questions)
    - [Answering Questions](#answering-questions)
    - [Saving Data](#saving-data)
6. [Error Handling](#error-handling)
7. [Conclusion](#conclusion)

## Introduction

The PaperQA CLI script is a command-line tool that allows users to process PDF documents, generate embeddings, and answer questions using OpenAI's language models. It supports various configurations and options to customize the processing and querying of documents.

## Prerequisites

Before using the script, ensure you have the following:

- Python 3.7 or higher
- Required Python packages: `argparse`, `glob`, `json`, `pickle`, `sys`, `pathlib`, `typing`, `paperqa`

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages using pip:

```bash
pip3 install paperqa
```

Note: The other required packages (`argparse`, `glob`, `json`, `pickle`, `sys`, `pathlib`, `typing`) are part of the Python standard library and do not need to be installed separately.

## Usage

### Command Line Arguments

The script accepts several command-line arguments to customize its behavior. Below is a list of available arguments:

- `--pdf_dir`: Directory containing PDF files
- `--question`: Question to ask (use quotes for multi-word questions)
- `--questions_file`: Path to a text file containing a list of questions, one per line
- `--save_embeddings`: Path to save the Docs object with embeddings (default: `paperqa_embeddings.pkl`)
- `--load_embeddings`: Path to load a pre-saved Docs object with embeddings
- `--save_answers`: Path to save the answers to a text file (default: `answers.txt`)
- `--save_data`: Path to save all data (answers, Docs object) to a pickle file (default: `paperqa_data.pkl`)
- `--save_embeddings_txt`: Path to save embeddings in a text file (for debugging/analysis)
- `--llm`: OpenAI LLM model name (default: `gpt-4o`)
- `--embedding`: OpenAI embedding model name (default: `text-embedding-3-large`)
- `--summary_llm`: OpenAI LLM model name for summarization (defaults to same as `--llm`)
- `--k`: Number of top-k results to retrieve for each query (default: 50)
- `--max_sources`: Maximum number of sources to use in the final answer (default: 50)
- `--chunk_chars`: Number of characters per chunk when splitting documents (default: 3200)
- `--overlap`: Number of overlapping characters between chunks (default: 1600)
- `--json_summary`: Use JSON format for summarization (requires GPT-3.5-turbo or later)
- `--detailed_citations`: Include full citations in the context
- `--disable_vector_search`: Disable vector search and use all text chunks
- `--key_filter`: Filter evidence by document keys based on question similarity
- `--custom_prompt_file`: Path to a JSON file containing custom prompts
- `--batch_size`: Batch size for processing documents (default: 10)
- `--max_concurrent`: Maximum number of concurrent requests (default: 4)
- `--strip_citations`: Strip citations from the generated answers
- `--jit_texts_index`: Enable just-in-time text indexing
- `--answer_length`: Specify the desired length of the answer

### Examples

1. Ask a single question:

```bash
python script.py --pdf_dir /path/to/pdfs --question "What is the impact of climate change on agriculture?"
```

2. Ask multiple questions from a file:

```bash
python script.py --pdf_dir /path/to/pdfs --questions_file questions.txt
```

3. Load existing embeddings and ask a question:

```bash
python script.py --load_embeddings embeddings.pkl --question "What are the latest advancements in AI?"
```

## Detailed Explanation

### Loading Custom Prompts

If a custom prompt file is provided using `--custom_prompt_file`, the script loads the prompts from the specified JSON file. This allows users to customize the prompts used for querying the documents.

### Creating Docs Object

The script creates a `Docs` object with the specified configurations, including the LLM model, embedding model, and other parameters. This object is used to manage the documents and perform queries.

### Loading Existing Embeddings

If a pre-saved Docs object with embeddings is provided using `--load_embeddings`, the script loads the object from the specified file. This allows users to reuse previously generated embeddings.

### Adding PDF Documents

The script adds PDF documents from the specified directory to the `Docs` object. It ensures that only new documents are added to avoid duplication.

### Getting Questions

The script retrieves questions from the command line, a file, or standard input. It supports multiple sources for questions to provide flexibility in querying the documents.

### Answering Questions

The script processes each question using the `Docs` object and generates answers. It supports various configurations for querying, including the number of top-k results, maximum sources, and answer length.

### Saving Data

The script saves the generated embeddings, answers, and other data to the specified files. This allows users to persist the results and reuse them later.

## Error Handling

The script includes error handling for various scenarios, such as file not found errors and JSON decoding errors. It prints appropriate error messages and exits gracefully in case of errors.

# Script

```
from paperqa import Answer, Docs, PromptCollection, OpenAILLMModel, OpenAIEmbeddingModel
import argparse
import sys
import pickle
import json
import glob
from pathlib import Path
from typing import List, Dict

def main():
    parser = argparse.ArgumentParser(description="PaperQA CLI")
    parser.add_argument(
        "--pdf_dir",
        type=str,
        default="/home/mario/gpt-researcher/BIBTEX",
        help="Directory containing PDF files",
    )
    parser.add_argument(
        "--question", type=str, help="Question to ask (use quotes for multi-word questions)"
    )
    parser.add_argument(
        "--questions_file",
        type=str,
        help="Path to a text file containing a list of questions, one per line",
    )
    parser.add_argument(
        "--save_embeddings",
        type=str,
        default="paperqa_embeddings.pkl",
        help="Path to save the Docs object with embeddings",
    )
    parser.add_argument(
        "--load_embeddings",
        type=str,
        help="Path to load a pre-saved Docs object with embeddings",
    )
    parser.add_argument(
        "--save_answers",
        type=str,
        default="answers.txt",
        help="Path to save the answers to a text file",
    )
    parser.add_argument(
        "--save_data",
        type=str,
        default="paperqa_data.pkl",
        help="Path to save all data (answers, Docs object) to a pickle file",
    )
    parser.add_argument(
        "--save_embeddings_txt",
        type=str,
        help="Path to save embeddings in a text file (for debugging/analysis)",
    )
    parser.add_argument(
        "--llm",
        type=str,
        default="gpt-4o",
        help="OpenAI LLM model name (e.g., 'gpt-4o', 'gpt-4o')",
    )
    parser.add_argument(
        "--embedding",
        type=str,
        default="text-embedding-3-large",
        help="OpenAI embedding model name (e.g., 'text-embedding-3-large')",
    )
    parser.add_argument(
        "--summary_llm",
        type=str,
        help="OpenAI LLM model name for summarization (defaults to same as --llm)",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=50,
        help="Number of top-k results to retrieve for each query",
    )
    parser.add_argument(
        "--max_sources",
        type=int,
        default=50,
        help="Maximum number of sources to use in the final answer",
    )
    parser.add_argument(
        "--chunk_chars",
        type=int,
        default=3200,
        help="Number of characters per chunk when splitting documents",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=1600,
        help="Number of overlapping characters between chunks",
    )
    parser.add_argument(
        "--json_summary",
        action="store_true",
        help="Use JSON format for summarization (requires GPT-3.5-turbo or later)",
    )
    parser.add_argument(
        "--detailed_citations",
        action="store_true",
        help="Include full citations in the context",
    )
    parser.add_argument(
        "--disable_vector_search",
        action="store_true",
        help="Disable vector search and use all text chunks",
    )
    parser.add_argument(
        "--key_filter",
        action="store_true",
        help="Filter evidence by document keys based on question similarity",
    )
    parser.add_argument(
        "--custom_prompt_file",
        type=str,
        help="Path to a JSON file containing custom prompts",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=10,  # Increased batch size for efficiency
        help="Batch size for processing documents (adjust for performance)",
    )
    parser.add_argument(
        "--max_concurrent",
        type=int,
        default=4,
        help="Maximum number of concurrent requests (adjust for performance)",
    )
    parser.add_argument(
        "--strip_citations",
        action="store_true",
        help="Strip citations from the generated answers",
    )
    parser.add_argument(
        "--jit_texts_index",
        action="store_true",
        help="Enable just-in-time text indexing",
    )
    parser.add_argument(
        "--answer_length",
        type=str,
        default="about 100 words",
        help="Specify the desired length of the answer (e.g., 'about 200 words')",
    )
    args = parser.parse_args()

    # Load custom prompts from JSON file if provided
    custom_prompts: Dict[str, str] = {}
    if args.custom_prompt_file:
        try:
            with open(args.custom_prompt_file, "r", encoding="utf-8") as f:
                custom_prompts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading custom prompts: {e}", file=sys.stderr)
            sys.exit(1)
    # Initialize PromptCollection without arguments
    prompts = PromptCollection()

    # If custom prompts are needed, set them directly
    if custom_prompts:
        for key, value in custom_prompts.items():
            setattr(prompts, key, value)

    llm_model = OpenAILLMModel(config={"model": args.llm, "temperature": 0.1})
    embedding_model = OpenAIEmbeddingModel(config={"model": args.embedding})
    summary_llm_model = (
        OpenAILLMModel(config={"model": args.summary_llm, "temperature": 0.1})
        if args.summary_llm
        else llm_model
    )

    # Create Docs object with supported parameters
    docs = Docs(
        llm=args.llm,  # Pass the model name as a string
        embedding=args.embedding,  # Pass the model name as a string
        summary_llm=args.summary_llm if args.summary_llm else args.llm,  # Pass the model name as a string
        prompts=prompts,  # Use the initialized and updated PromptCollection
        max_concurrent=args.max_concurrent,
        jit_texts_index=args.jit_texts_index,
    )

    # Load existing embeddings if provided
    if args.load_embeddings:
        try:
            with open(args.load_embeddings, "rb") as f:
                docs = pickle.load(f)
            docs.set_client()  # Required after loading from pickle
        except FileNotFoundError as e:
            print(f"Error loading embeddings: {e}", file=sys.stderr)
            sys.exit(1)

    # Add PDF documents
    pdf_dir = Path(args.pdf_dir)
    pdf_files = glob.glob(str(pdf_dir / "*.pdf"))
    for pdf_file in pdf_files:
        if pdf_file not in [doc.dockey for doc in docs.docs.values()]:
            docs.add(pdf_file)

    # Get questions from command line, file, or standard input
    questions: List[str] = []
    if args.question:
        questions.append(args.question)
    if args.questions_file:
        try:
            with open(args.questions_file, "r", encoding="utf-8") as f:
                questions.extend([line.strip() for line in f])
        except FileNotFoundError as e:
            print(f"Error reading questions file: {e}", file=sys.stderr)
            sys.exit(1)
    if not questions:
        questions = [line.strip() for line in sys.stdin]

    # Get answers for each question
    answers = []
    for question in questions:
        answer = docs.query(question, k=args.k, max_sources=args.max_sources)
        print(f"Answer object: {answer}")  # Debug print to inspect the Answer object
        answers.append(str(answer))  # Use str(answer) to store the entire Answer object

    # Save answers to file
    with open(args.save_answers, "w", encoding="utf-8") as f:
        for answer in answers:
            f.write(answer + "\n")

    # Save embeddings to file
    if args.save_embeddings:
        with open(args.save_embeddings, "wb") as f:
            pickle.dump(docs, f)

    # Save all data to file
    if args.save_data:
        with open(args.save_data, "wb") as f:
            pickle.dump({"docs": docs, "answers": answers}, f)

    # Save embeddings to text file (for debugging/analysis)
    if args.save_embeddings_txt:
        with open(args.save_embeddings_txt, "w", encoding="utf-8") as f:
            for doc in docs.docs.values():
                f.write(f"{doc.dockey}\t{doc.embedding.tolist()}\n")

if __name__ == "__main__":
    main()
```
