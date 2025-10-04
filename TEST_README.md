# CVCustomizer Parameterized Unit Testing Framework

This directory contains comprehensive unit tests for the CVCustomizer class. Each test is designed to be self-running and independent, with support for parameterized testing and configurable inputs.

## Test Files

- `test_cv_customizer_comprehensive.py` - Main test file containing all parameterized unit tests
- `run_tests.py` - Enhanced test runner script with configuration support
- `test_config.yaml` - Configuration file with default test parameters
- `demo_tests.py` - Demonstration script showing parameterized testing

## Running Tests

### Option 1: Run All Tests with Default Parameters
```bash
python test_cv_customizer_comprehensive.py
```

### Option 2: Run Specific Test Categories with Default Parameters
```bash
python test_cv_customizer_comprehensive.py init
python test_cv_customizer_comprehensive.py load_template
python test_cv_customizer_comprehensive.py call_llm_api
python test_cv_customizer_comprehensive.py summarize_experience
python test_cv_customizer_comprehensive.py customize_summary
python test_cv_customizer_comprehensive.py customize_achievements
python test_cv_customizer_comprehensive.py create_word_document
python test_cv_customizer_comprehensive.py customize_cv
```

### Option 3: Run Tests with Custom Parameters
```bash
# Run with custom API key and job description
python test_cv_customizer_comprehensive.py init --api-key "my-key" --test-job-description "Python developer role"

# Run with custom company and job title
python test_cv_customizer_comprehensive.py customize_achievements --test-company-name "Tech Corp" --test-job-title "Senior Developer"
```

### Option 4: Use the Enhanced Test Runner
```bash
# Run all tests with configuration file
python run_tests.py

# Run specific test category
python run_tests.py init
python run_tests.py load_template

# Run with custom configuration file
python run_tests.py --config my_config.yaml

# Run test scenarios
python run_tests.py --scenarios

# Override parameters via command line
python run_tests.py init --api-key "my-key" --job-description "Data scientist role"
```

### Option 5: Run Demo
```bash
python demo_tests.py
```

## Test Categories

### 1. TestCVCustomizerInit
Tests the `__init__` method:
- Initialization with API key and endpoint
- Initialization with None values (uses environment variables)
- Initialization with no API key (shows warning)

### 2. TestCVCustomizerLoadCVTemplate
Tests the `load_cv_template` method:
- Successful YAML file loading
- File not found error handling
- Invalid YAML error handling

### 3. TestCVCustomizerCallLLMAPI
Tests the `call_llm_api` method:
- API call with no API key
- Successful API calls
- API calls without system message
- Unexpected response format handling
- Request exception handling

### 4. TestCVCustomizerSummarizeExperience
Tests the `summarize_experience` method:
- Successful experience summarization
- Handling experience with no achievements

### 5. TestCVCustomizerCustomizeSummary
Tests the `customize_summary` method:
- Successful summary customization

### 6. TestCVCustomizerCustomizeAchievements
Tests the `customize_achievements` method:
- Empty achievements list handling
- Successful achievements customization
- Different bullet point formats
- Fallback to original achievements

### 7. TestCVCustomizerCreateWordDocument
Tests the `create_word_document` method:
- Successful Word document creation
- Document creation without qualifications
- Document creation with minimal contact info

### 8. TestCVCustomizerCustomizeCV
Tests the `customize_cv` method:
- Successful CV customization
- Customization without output file
- Template loading error handling

## Parameterized Testing Features

### Default Parameters
All tests use configurable default parameters that can be overridden:
- **API Configuration**: API key and endpoint
- **Test Data**: Job descriptions, company names, job titles
- **Personal Info**: Names, emails, phone numbers, LinkedIn profiles
- **File Paths**: YAML templates, output files

### Configuration Methods
1. **Command Line Arguments**: Override any parameter via command line
2. **Configuration File**: Use YAML configuration file for consistent settings
3. **Environment Variables**: Fallback to environment variables
4. **Default Values**: Sensible defaults for all parameters

### Test Scenarios
The framework supports multiple test scenarios:
- **Python Developer**: Tests with Python/Django focus
- **Data Scientist**: Tests with ML/data focus  
- **DevOps Engineer**: Tests with AWS/Docker focus

## Test Features

- **Parameterized**: All tests accept configurable parameters with defaults
- **Mocking**: Uses `unittest.mock` to mock external dependencies
- **Temporary Files**: Uses `tempfile` for safe file operations
- **Isolation**: Each test is independent and can be run alone
- **Comprehensive Coverage**: Tests both success and error scenarios
- **Self-Contained**: No external dependencies beyond the main module
- **Configuration-Driven**: Support for YAML configuration files
- **Scenario Testing**: Multiple test scenarios for different use cases

## Dependencies

The tests require the following packages (already in requirements.txt):
- `unittest` (built-in)
- `tempfile` (built-in)
- `os` (built-in)
- `yaml`
- `requests`
- `docx`
- `unittest.mock` (built-in)

## Example Usage

```bash
# Run all tests
python test_cv_customizer_comprehensive.py

# Run only initialization tests
python test_cv_customizer_comprehensive.py init

# Run only API call tests
python test_cv_customizer_comprehensive.py call_llm_api

# Use the test runner
python run_tests.py
python run_tests.py init
```

## Test Output

Each test run will show:
- Test method names being executed
- Success/failure status
- Error messages for failed tests
- Summary of results

Example output:
```
test_init_with_api_key_and_endpoint (__main__.TestCVCustomizerInit) ... ok
test_init_with_none_values (__main__.TestCVCustomizerInit) ... ok
test_init_with_no_api_key (__main__.TestCVCustomizerInit) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```
