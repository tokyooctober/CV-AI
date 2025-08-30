#!/usr/bin/env python3
"""
Test script for CV Customization System
Demonstrates functionality without requiring API key.
"""

import os
import sys
from cv_customizer import CVCustomizer


def test_cv_customization():
    """Test the CV customization functionality."""

    print("=== CV Customization System Test ===\n")

    # Check if YAML files exist
    yaml_files = ["cv2024.yaml", "cv2025.yaml"]
    available_files = [f for f in yaml_files if os.path.exists(f)]

    if not available_files:
        print("Error: No YAML CV template files found.")
        print(
            "Please ensure cv2024.yaml or cv2025.yaml exists in the current directory."
        )
        return False

    # Use the first available YAML file
    yaml_file = available_files[0]
    print(f"Using CV template: {yaml_file}")

    # Sample job description
    job_description = """
    Senior Cloud Solutions Architect
    
    We are seeking a dynamic and experienced Senior Cloud Solutions Architect to join our innovative technology team. 
    The ideal candidate will be responsible for designing and implementing cutting-edge cloud solutions that drive 
    business transformation and operational excellence.
    
    Key Responsibilities:
    • Lead the design and architecture of scalable cloud solutions across multiple platforms (AWS, Azure, GCP)
    • Collaborate with cross-functional teams to understand business requirements and translate them into technical solutions
    • Develop comprehensive solution proposals and technical documentation
    • Drive cloud adoption strategies and best practices implementation
    • Mentor junior architects and provide technical leadership
    • Engage with clients to understand their needs and present tailored solutions
    • Ensure solutions meet security, compliance, and performance requirements
    
    Required Skills:
    • Extensive experience with cloud platforms (AWS, Azure, GCP)
    • Strong background in solution architecture and enterprise design
    • Proven track record of delivering complex cloud projects
    • Excellent communication and presentation skills
    • Experience with DevOps practices and CI/CD pipelines
    • Knowledge of containerization technologies (Docker, Kubernetes)
    • Understanding of microservices architecture and API design
    """

    print(f"Job Description: Senior Cloud Solutions Architect")
    print(f"Job Description Length: {len(job_description)} characters\n")

    # Initialize customizer (without API key for testing)
    customizer = CVCustomizer()

    try:
        # Test loading CV template
        print("Step 1: Testing CV template loading...")
        cv_data = customizer.load_cv_template(yaml_file)
        print(f"✓ Successfully loaded CV template for: {cv_data['name']}")
        print(f"✓ Found {len(cv_data['experience'])} work experiences")

        # Test summary customization (will return original without API key)
        print("\nStep 2: Testing summary customization...")
        original_summary = cv_data["summary"]
        customized_summary = customizer.customize_summary(
            original_summary, job_description
        )
        print(f"✓ Summary customization completed")
        print(f"  Original length: {len(original_summary)} characters")
        print(f"  Customized length: {len(customized_summary)} characters")

        # Test achievement customization for first experience
        print("\nStep 3: Testing achievement customization...")
        if cv_data["experience"] and cv_data["experience"][0]["achievements"]:
            first_experience = cv_data["experience"][0]
            original_achievements = first_experience["achievements"]
            customized_achievements = customizer.customize_achievements(
                original_achievements,
                job_description,
                first_experience["company"],
                first_experience["title"],
            )
            print(
                f"✓ Achievement customization completed for {first_experience['company']}"
            )
            print(f"  Original achievements: {len(original_achievements)}")
            print(f"  Customized achievements: {len(customized_achievements)}")

        # Test Word document generation
        print("\nStep 4: Testing Word document generation...")
        output_file = "test_customized_cv.docx"

        # Update CV data with customized content
        cv_data["summary"] = customized_summary

        customizer.create_word_document(cv_data, output_file)
        print(f"✓ Word document generated: {output_file}")

        # Check if file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✓ File size: {file_size} bytes")
        else:
            print("✗ Error: Word document was not created")
            return False

        print("\n=== Test Completed Successfully! ===")
        print(f"Generated CV: {output_file}")
        print("\nNote: Without an API key, the content remains unchanged.")
        print("To see actual customization, provide an API key using:")
        print("  --api-key your_api_key_here")
        print("  or set the LLM_API_KEY environment variable")

        return True

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    success = test_cv_customization()
    sys.exit(0 if success else 1)
