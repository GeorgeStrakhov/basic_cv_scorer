import os
import pandas as pd
from pathlib import Path
from typing import Dict, List
import PyPDF2
import docx
from tqdm import tqdm
import json
from llm import answer_json
from prompts import CV_REVIEW_PROMPT
from scoring_config import ScoringConfig

class CVScorer:
    def __init__(self):
        # Create necessary directories
        self.submissions_dir = Path("submissions")
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        self.output_file = self.output_dir / "cv_scores.csv"
        
        # Initialize or load existing results
        self.processed_files = set()
        if self.output_file.exists():
            df = pd.read_csv(self.output_file)
            self.processed_files = set(df['filename'].tolist())

    def read_pdf(self, file_path: Path) -> str:
        """Extract text from a PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text

    def read_docx(self, file_path: Path) -> str:
        """Extract text from a DOCX file."""
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def read_cv(self, file_path: Path) -> str:
        """Read CV content based on file extension."""
        if file_path.suffix.lower() == '.pdf':
            return self.read_pdf(file_path)
        elif file_path.suffix.lower() == '.docx':
            return self.read_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

    def score_cv(self, cv_text: str) -> Dict:
        """Score a CV using the LLM."""
        try:
            result = answer_json(
                user_message=f"Review this CV:\n\n{cv_text}",
                system_prompt=CV_REVIEW_PROMPT,
                temperature=0.7
            )
            # Validate the scores against our criteria
            config = ScoringConfig()
            config.validate_scores(result)
            return result
        except Exception as e:
            print(f"Error scoring CV: {str(e)}")
            return None

    def process_cvs(self):
        """Process all CVs in the submissions directory."""
        # Get list of CV files and sort by name
        cv_files = []
        for ext in ['.pdf', '.docx']:
            cv_files.extend(self.submissions_dir.glob(f'*{ext}'))
        cv_files.sort()

        # Skip already processed files
        cv_files = [f for f in cv_files if f.name not in self.processed_files]

        if not cv_files:
            print("No new CVs to process.")
            return

        # Initialize results list and DataFrame
        results = []
        if self.output_file.exists():
            df = pd.read_csv(self.output_file)
        else:
            df = pd.DataFrame()

        # Process each CV
        for cv_path in tqdm(cv_files, desc="Processing CVs"):
            try:
                # Read CV content
                cv_text = self.read_cv(cv_path)
                
                # Score CV
                scores = self.score_cv(cv_text)
                if scores is None:
                    continue

                # Prepare result row
                result = {
                    'filename': cv_path.name,
                    **scores
                }
                
                # Append to results and update DataFrame
                results.append(result)
                new_df = pd.DataFrame([result])
                df = pd.concat([df, new_df], ignore_index=True)
                
                # Save after each CV
                df.to_csv(self.output_file, index=False)
                
            except Exception as e:
                print(f"Error processing {cv_path.name}: {str(e)}")

        print(f"\nProcessed {len(results)} new CVs")
        print(f"Results saved to {self.output_file}")

if __name__ == "__main__":
    scorer = CVScorer()
    scorer.process_cvs() 