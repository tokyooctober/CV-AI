# CVCustomizer Configuration System

This document explains the new configuration system that moves all hardcoded strings from the Python code to external configuration files.

## 📋 **Overview**

The CVCustomizer now uses a YAML-based configuration system that allows you to:
- **Customize all prompts and system messages** without modifying Python code
- **Modify API settings** (model, temperature, tokens, etc.)
- **Change document formatting** (margins, indentation, table styles)
- **Update error messages and UI text** for different languages
- **Configure output file naming** and formatting

## 🗂️ **Configuration Files**

### **Primary Configuration: `prompts_config.yaml`**
Contains all system messages, prompts, and application settings.

### **Test Configuration: `test_config.yaml`**
Contains test-specific parameters and scenarios.

## 📁 **Configuration Structure**

```yaml
# API Configuration
api:
  model: "gpt-4"
  temperature: 0.7
  max_tokens: 2000
  timeout: 30

# System Messages for LLM API calls
system_messages:
  summarize_experience: |
    You are an expert CV writer...
  customize_summary: |
    You are an expert CV writer...
  customize_achievements: |
    You are going to act as a professional resume writer...

# Prompts for LLM API calls
prompts:
  summarize_experience: |
    Job Description:
    {job_description}
    ...
  customize_summary: |
    Job Description:
    {job_description}
    ...
  customize_achievements: |
    Job Description:
    {job_description}
    ...

# Document formatting strings
document_strings:
  sections:
    summary: "Summary"
    professional_experience: "Professional Experience"
    certification: "Certification"
  
  table_headers:
    year: "Year"
    certification: "Certification"
  
  bullet_point: "• "
  contact_separator: " | "

# Error and warning messages
messages:
  warnings:
    no_api_key: "Warning: No API key provided..."
    no_api_key_available: "Warning: No API key available..."
    unexpected_api_response: "Warning: Unexpected API response format..."
    api_call_failed: "Warning: API call failed: {error}..."
  
  errors:
    file_not_found: "CV template file '{file}' not found."
    yaml_parse_error: "Error parsing YAML file: {error}"
    job_description_file_error: "Pls provide filename to the job description..."
  
  success:
    cv_saved: "Customized CV saved to: {output_file}"
    cv_customization_completed: "CV customization completed successfully!"
    output_file: "Output file: {output_file}"

# Step messages for progress tracking
step_messages:
  loading_template: "Step 1: Loading CV template..."
  customizing_achievements: "Step 2: Customizing achievements..."
  generating_summary: "Step 3: Generating summary from experience..."
  generating_document: "Step 4: Generating Word document..."

# Document formatting settings
document_settings:
  margins:
    top: 0.5
    bottom: 0.5
    left: 0.75
    right: 0.75
  
  indentation:
    title_indent: 0.2
    achievement_indent: 0.4
    achievement_spacing: 0.05
  
  tab_stops:
    right_aligned_tab: 6.0
  
  table_settings:
    style: "Light List"
    year_column_width: 1.0
    certification_column_width: 5.0

# Output file naming
output_settings:
  default_prefix: "customized_cv_"
  timestamp_format: "%Y%m%d_%H%M%S"
  file_extension: ".docx"
```

## 🔧 **How to Use the Configuration System**

### **1. Basic Usage (Default Configuration)**
```python
from cv_customizer import CVCustomizer

# Uses default prompts_config.yaml
customizer = CVCustomizer(api_key, api_endpoint)
```

### **2. Custom Configuration File**
```python
# Use your own configuration file
customizer = CVCustomizer(api_key, api_endpoint, "my_config.yaml")
```

### **3. Modifying Prompts and Messages**

#### **Change System Messages:**
```yaml
system_messages:
  summarize_experience: |
    You are a professional CV writer specializing in technology roles.
    Create compelling summaries that highlight technical expertise and leadership experience.
    Focus on quantifiable achievements and industry-specific terminology.
```

#### **Customize Prompts:**
```yaml
prompts:
  summarize_experience: |
    Job Requirements:
    {job_description}
    
    Candidate Experience:
    {experience_text}
    
    Please create a 2-paragraph professional summary that:
    1. Emphasizes technical skills relevant to the role
    2. Highlights leadership and team collaboration
    3. Uses industry-standard terminology
    4. Quantifies achievements with specific metrics
```

#### **Update Error Messages:**
```yaml
messages:
  warnings:
    no_api_key: "⚠️ API key not found. Please set LLM_API_KEY environment variable."
    api_call_failed: "❌ API request failed: {error}. Using fallback content."
  
  success:
    cv_saved: "✅ CV successfully saved to: {output_file}"
    cv_customization_completed: "🎉 CV customization completed successfully!"
```

### **4. API Configuration**
```yaml
api:
  model: "gpt-4-turbo"  # Use different model
  temperature: 0.3      # Lower temperature for more consistent results
  max_tokens: 3000     # Increase token limit
  timeout: 60          # Longer timeout for complex requests
```

### **5. Document Formatting**
```yaml
document_settings:
  margins:
    top: 0.75          # Larger top margin
    bottom: 0.75        # Larger bottom margin
    left: 1.0          # Larger left margin
    right: 1.0         # Larger right margin
  
  indentation:
    title_indent: 0.3   # Adjust title indentation
    achievement_indent: 0.5  # Adjust achievement indentation
    achievement_spacing: 0.1 # Adjust spacing between achievements
  
  table_settings:
    style: "Table Grid"  # Different table style
    year_column_width: 1.5
    certification_column_width: 4.5
```

### **6. Output File Naming**
```yaml
output_settings:
  default_prefix: "resume_"           # Change prefix
  timestamp_format: "%Y-%m-%d_%H-%M" # Different timestamp format
  file_extension: ".docx"             # Keep .docx extension
```

## 🌍 **Internationalization Support**

The configuration system supports multiple languages:

### **English Configuration:**
```yaml
document_strings:
  sections:
    summary: "Summary"
    professional_experience: "Professional Experience"
    certification: "Certification"
  
  table_headers:
    year: "Year"
    certification: "Certification"
```

### **Spanish Configuration:**
```yaml
document_strings:
  sections:
    summary: "Resumen"
    professional_experience: "Experiencia Profesional"
    certification: "Certificación"
  
  table_headers:
    year: "Año"
    certification: "Certificación"
```

### **French Configuration:**
```yaml
document_strings:
  sections:
    summary: "Résumé"
    professional_experience: "Expérience Professionnelle"
    certification: "Certification"
  
  table_headers:
    year: "Année"
    certification: "Certification"
```

## 🧪 **Testing with Configuration**

### **Run Tests with Custom Configuration:**
```bash
# Use custom configuration for tests
python test_cv_customizer_comprehensive.py init --config-file my_test_config.yaml

# Override specific parameters
python test_cv_customizer_comprehensive.py init --api-key "my-key" --test-job-description "Python developer role"
```

### **Test Configuration System:**
```bash
# Test the configuration system
python test_config_system.py
```

## 📝 **Configuration Best Practices**

### **1. Version Control**
- Keep configuration files in version control
- Use descriptive names for custom configurations
- Document changes in commit messages

### **2. Environment-Specific Configurations**
```yaml
# Development configuration
api:
  model: "gpt-3.5-turbo"  # Cheaper model for development
  temperature: 0.7
  max_tokens: 1000

# Production configuration  
api:
  model: "gpt-4"          # Best model for production
  temperature: 0.3
  max_tokens: 2000
```

### **3. Backup Default Configuration**
- Always keep a backup of the default `prompts_config.yaml`
- Test changes in a development environment first
- Validate YAML syntax before deployment

### **4. Configuration Validation**
```python
# Validate configuration on startup
def validate_config(config):
    required_sections = ['system_messages', 'prompts', 'messages', 'api']
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required section: {section}")
```

## 🔄 **Migration from Hardcoded Strings**

### **Before (Hardcoded):**
```python
system_message = """You are an expert CV writer. Create a compelling professional summary..."""
prompt = f"""Job Description: {job_description}..."""
print("Step 1: Loading CV template...")
```

### **After (Configuration-Based):**
```python
system_message = self.config['system_messages']['summarize_experience']
prompt = self.config['prompts']['summarize_experience'].format(job_description=job_description)
print(self.config['step_messages']['loading_template'])
```

## 🎯 **Benefits of the Configuration System**

1. **Maintainability**: No need to modify Python code for text changes
2. **Flexibility**: Easy to customize for different use cases
3. **Internationalization**: Support for multiple languages
4. **Testing**: Easy to test with different configurations
5. **Deployment**: Environment-specific configurations
6. **Collaboration**: Non-developers can modify text content
7. **Version Control**: Track changes to prompts and messages
8. **Reusability**: Share configurations across projects

## 🚀 **Quick Start**

1. **Copy the default configuration:**
   ```bash
   cp prompts_config.yaml my_config.yaml
   ```

2. **Modify your configuration:**
   ```yaml
   # Edit my_config.yaml with your custom settings
   system_messages:
     summarize_experience: "Your custom system message..."
   ```

3. **Use your configuration:**
   ```python
   customizer = CVCustomizer(api_key, api_endpoint, "my_config.yaml")
   ```

4. **Test your configuration:**
   ```bash
   python test_config_system.py
   ```

The configuration system makes the CVCustomizer much more flexible and maintainable while keeping all the hardcoded strings external to the Python code!
