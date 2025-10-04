# CV Customization System

A Python program that creates customized CVs based on job descriptions using LLM API for content adaptation. The system reads CV templates from YAML files, processes job descriptions, and generates professional Word documents with tailored content.

## Features

- **Template-based CV generation** from YAML files
- **LLM-powered content customization** using OpenAI GPT-4 or compatible APIs
- **Automatic language and style matching** to job descriptions
- **Professional Word document output** with proper formatting
- **Customizable employment history layout** with company names and dates
- **Bullet-point achievements** for each role

## Requirements

- Python 3.7 or higher
- LLM API key (OpenAI or compatible service)

## Installation

1. **Clone or download the project files**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   
   Option A: Set environment variable
   ```bash
   # Windows
   set LLM_API_KEY=your_api_key_here
   
   # Linux/Mac
   export LLM_API_KEY=your_api_key_here
   ```
   
   Option B: Pass as command line argument (see usage below)

## Usage

### Basic Usage

```bash
python cv_customizer.py cv2025.yaml "Job description text here"
```

### Using a Job Description File

```bash
python cv_customizer.py cv2025.yaml sample_job_description.txt
```

### Specifying Output File

```bash
python cv_customizer.py cv2025.yaml sample_job_description.txt -o my_customized_cv.docx
```

### With API Key

```bash
python cv_customizer.py cv2025.yaml sample_job_description.txt --api-key your_api_key_here
```

### Custom API Endpoint

```bash
python cv_customizer.py cv2025.yaml sample_job_description.txt --api-endpoint https://your-api-endpoint.com/v1/chat/completions
```

## Command Line Arguments

- `yaml_file`: Path to YAML CV template file (required)
- `job_description`: Job description text or path to file (required)
- `-o, --output`: Output Word file path (optional)
- `--api-key`: LLM API key (optional, can use environment variable)
- `--api-endpoint`: LLM API endpoint URL (optional, defaults to OpenAI)

## YAML Template Format

Your CV template should follow this structure:

```yaml
name: Your Name
contact:
  phone: (123) 456-7890
  email: your.email@example.com
  linkedin: linkedin.com/in/your-profile
  nationality: Your Nationality
summary: Your professional summary here...
experience:
- company: Company Name
  period: Jan 2020 – Present
  title: Job Title
  achievements:
  - Achievement 1
  - Achievement 2
  - Achievement 3
- company: Another Company
  period: Jan 2018 – Dec 2019
  title: Previous Job Title
  achievements:
  - Previous achievement 1
  - Previous achievement 2
```

## Output Format

The generated Word document includes:

1. **Name** (centered, large heading)
2. **Contact Information** (centered, separated by pipes)
3. **Summary** (customized to match job description)
4. **Professional Experience** with:
   - Company name (left-justified) and period (right-justified)
   - Job title (indented)
   - Bullet-point achievements (customized to match job description)

## How It Works

1. **Template Loading**: Reads CV data from YAML file
2. **Content Analysis**: Analyzes job description for key terms and style
3. **LLM Customization**: Uses AI to rewrite summary and achievements to match job requirements
4. **Document Generation**: Creates professionally formatted Word document
5. **Output**: Saves customized CV for further editing

## API Compatibility

The program is designed to work with OpenAI's GPT-4 API but can be adapted for other LLM services by modifying the API endpoint and request format in the `call_llm_api` method.

## Error Handling

- Graceful handling of missing API keys (returns original content)
- File not found errors with helpful messages
- YAML parsing errors with detailed feedback
- API call failures with fallback to original content

## Example Output

The program generates a Word document with the following structure:

```
                    Your Full ame
        (65) 9xxx | xxx@gmail.com | linkedin.com/in/XXX | Nationality

Summary
[Customized summary matching job description language and style]

Professional Experience

NCS                                                          Apr 2021 – Present
    Lead IT Architect, Cloud and Agile Solutions, Asia Pacific
    • [Customized achievement matching job requirements]
    • [Customized achievement matching job requirements]
    • [Customized achievement matching job requirements]

[Additional experiences with same formatting...]
```

## Troubleshooting

**API Key Issues:**
- Ensure your API key is valid and has sufficient credits
- Check that the API endpoint is correct
- Verify network connectivity

**YAML File Issues:**
- Ensure proper YAML syntax
- Check that all required fields are present
- Validate file encoding (should be UTF-8)

**Word Document Issues:**
- Ensure write permissions in output directory
- Check that python-docx is properly installed
- Verify sufficient disk space

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the system.

## License

This project is open source and available under the MIT License.
