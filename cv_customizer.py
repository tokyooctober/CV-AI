#!/usr/bin/env python3
"""
CV Customization System
Creates customized CVs based on job descriptions using LLM API for content adaptation.
"""

import yaml
import requests
import json
import argparse
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.shared import OxmlElement, qn
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml
import re


class CVCustomizer:
    def __init__(self, api_key=None, api_endpoint=None):
        """
        Initialize the CV Customizer with API credentials.

        Args:
            api_key (str): API key for the LLM service
            api_endpoint (str): API endpoint URL
        """
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.api_endpoint = api_endpoint or os.getenv(
            "LLM_API_ENDPOINT", "https://api.openai.com/v1/chat/completions"
        )

        if not self.api_key:
            print(
                "Warning: No API key provided. Set LLM_API_KEY environment variable or pass api_key parameter."
            )

    def load_cv_template(self, yaml_file):
        """
        Load CV template from YAML file.

        Args:
            yaml_file (str): Path to YAML template file

        Returns:
            dict: CV template data
        """
        try:
            with open(yaml_file, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"CV template file '{yaml_file}' not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

    def call_llm_api(self, prompt, system_message=None):
        """
        Make API call to LLM service for content customization.

        Args:
            prompt (str): The prompt to send to the LLM
            system_message (str): Optional system message

        Returns:
            str: LLM response
        """
        if not self.api_key:
            print("Warning: No API key available. Returning original content.")
            return prompt

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        data = {
            "model": "gpt-4",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
        }

        try:
            response = requests.post(
                self.api_endpoint, headers=headers, json=data, timeout=30
            )
            response.raise_for_status()

            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"].strip()
            else:
                print(
                    "Warning: Unexpected API response format. Returning original content."
                )
                return prompt

        except requests.exceptions.RequestException as e:
            print(f"Warning: API call failed: {e}. Returning original content.")
            return prompt

    def customize_summary(self, original_summary, job_description):
        """
        Customize CV summary based on job description.

        Args:
            original_summary (str): Original CV summary
            job_description (str): Job description to match

        Returns:
            str: Customized summary
        """
        system_message = """You are an expert CV writer. Rewrite the given CV summary to match the language, style, and key requirements found in the job description. 
        Maintain the same achievements and experience but adapt the language to align with the job posting's terminology and focus areas."""

        prompt = f"""
        Job Description:
        {job_description}
        
        Original CV Summary:
        {original_summary}
        
        Please rewrite the CV summary to match the language, style, and key requirements from the job description while maintaining the same achievements and experience.
        """

        return self.call_llm_api(prompt, system_message)

    def customize_achievements(
        self, achievements, job_description, company_name, job_title
    ):
        """
        Customize achievements for a specific role based on job description.

        Args:
            achievements (list): List of achievement strings
            job_description (str): Job description to match
            company_name (str): Company name for context
            job_title (str): Job title for context

        Returns:
            list: Customized achievements
        """
        if not achievements:
            return []

        system_message = """You are an expert CV writer. Rewrite the given achievements to match the language, style, and key requirements found in the job description. 
        Maintain the same accomplishments but adapt the language to align with the job posting's terminology and focus areas. Return only the rewritten achievements, one per line."""

        achievements_text = "\n".join(
            [f"- {achievement}" for achievement in achievements]
        )

        prompt = f"""
        Job Description:
        {job_description}
        
        Company: {company_name}
        Job Title: {job_title}
        
        Original Achievements:
        {achievements_text}
        
        Please rewrite these achievements to match the language, style, and key requirements from the job description while maintaining the same accomplishments.
        Return only the rewritten achievements, one per line starting with "- ".
        """

        response = self.call_llm_api(prompt, system_message)

        # Parse the response back into a list
        customized_achievements = []
        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("- "):
                customized_achievements.append(line[2:])
            elif line.startswith("• "):
                customized_achievements.append(line[2:])
            elif line and not line.startswith("#"):
                customized_achievements.append(line)

        return customized_achievements if customized_achievements else achievements

    def create_word_document(self, cv_data, output_file):
        """
        Create Word document with the customized CV.

        Args:
            cv_data (dict): CV data with customized content
            output_file (str): Output file path
        """
        doc = Document()

        # Set up document margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(0.5)
            section.bottom_margin = Inches(0.5)
            section.left_margin = Inches(0.75)
            section.right_margin = Inches(0.75)

        # Add name as title
        title = doc.add_heading(cv_data["name"], 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Add contact information
        contact = cv_data["contact"]
        contact_para = doc.add_paragraph()
        contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        contact_info = []
        if "phone" in contact:
            contact_info.append(contact["phone"])
        if "email" in contact:
            contact_info.append(contact["email"])
        if "linkedin" in contact:
            contact_info.append(contact["linkedin"])
        if "nationality" in contact:
            contact_info.append(contact["nationality"])

        contact_para.add_run(" | ".join(contact_info))

        # Add summary section
        doc.add_heading("Summary", level=1)
        summary_para = doc.add_paragraph()
        summary_para.add_run(cv_data["summary"])

        # Add professional experience section
        doc.add_heading("Professional Experience", level=1)

        for experience in cv_data["experience"]:
            # Company name and period (left and right justified)
            company_para = doc.add_paragraph()
            company_run = company_para.add_run(experience["company"])
            company_run.bold = True

            # Add tab for right alignment of period
            period_run = company_para.add_run("\t" + experience["period"])
            period_run.bold = True

            # Set tab stops for right alignment
            tab_stops = company_para.paragraph_format.tab_stops
            tab_stops.add_tab_stop(Inches(6.0), 2)  # Right-aligned tab

            # Job title
            title_para = doc.add_paragraph()
            title_para.add_run(experience["title"])
            title_para.paragraph_format.left_indent = Inches(0.2)

            # Achievements
            if experience["achievements"]:
                for achievement in experience["achievements"]:
                    achievement_para = doc.add_paragraph()
                    achievement_para.add_run("• " + achievement)
                    achievement_para.paragraph_format.left_indent = Inches(0.4)
                    achievement_para.paragraph_format.space_after = Inches(0.05)

            # Add space between experiences
            doc.add_paragraph()

        # Save the document
        doc.save(output_file)
        print(f"Customized CV saved to: {output_file}")

    def customize_cv(self, yaml_file, job_description, output_file=None):
        """
        Main method to customize CV based on job description.

        Args:
            yaml_file (str): Path to YAML template file
            job_description (str): Job description text
            output_file (str): Output file path (optional)

        Returns:
            str: Path to generated Word document
        """
        # Load CV template
        print("Step 1: Loading CV template...")
        cv_data = self.load_cv_template(yaml_file)

        # Customize summary
        print("Step 2: Customizing summary...")
        cv_data["summary"] = self.customize_summary(cv_data["summary"], job_description)

        # Customize achievements for each experience
        print("Step 3: Customizing achievements...")
        for experience in cv_data["experience"]:
            if experience["achievements"]:
                experience["achievements"] = self.customize_achievements(
                    experience["achievements"],
                    job_description,
                    experience["company"],
                    experience["title"],
                )

        # Generate output filename if not provided
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"customized_cv_{timestamp}.docx"

        # Create Word document
        print("Step 4: Generating Word document...")
        self.create_word_document(cv_data, output_file)

        return output_file


def main():
    """Main function to run the CV customizer."""
    parser = argparse.ArgumentParser(
        description="Customize CV based on job description"
    )
    parser.add_argument("yaml_file", help="Path to YAML CV template file")
    parser.add_argument("job_description", help="Job description text or path to file")
    parser.add_argument("-o", "--output", help="Output Word file path")
    parser.add_argument("--api-key", help="LLM API key")
    parser.add_argument("--api-endpoint", help="LLM API endpoint")

    args = parser.parse_args()

    # Read job description from file if it's a file path
    job_description = args.job_description
    if os.path.isfile(job_description):
        with open(job_description, "r", encoding="utf-8") as f:
            job_description = f.read()

    # Initialize customizer
    customizer = CVCustomizer(api_key=args.api_key, api_endpoint=args.api_endpoint)

    # Customize CV
    output_file = customizer.customize_cv(args.yaml_file, job_description, args.output)

    print(f"\nCV customization completed successfully!")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    main()
