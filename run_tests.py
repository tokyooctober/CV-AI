#!/usr/bin/env python3
"""
Enhanced test runner for CVCustomizer unit tests
Allows running individual test methods or all tests with parameters
"""

import sys
import subprocess
import os
import yaml
import argparse

def load_test_config(config_file="test_config.yaml"):
    """Load test configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: Configuration file {config_file} not found. Using defaults.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error loading configuration: {e}")
        return {}

def build_test_command(test_name=None, config=None, extra_args=None):
    """Build test command with parameters"""
    cmd = [sys.executable, "test_cv_customizer_comprehensive.py"]
    
    if test_name:
        cmd.append(test_name)
    
    # Add configuration parameters
    if config:
        if 'api_key' in config:
            cmd.extend(['--api-key', config['api_key']])
        if 'api_endpoint' in config:
            cmd.extend(['--api-endpoint', config['api_endpoint']])
        if 'test_yaml_file' in config:
            cmd.extend(['--test-yaml-file', config['test_yaml_file']])
        if 'test_output_file' in config:
            cmd.extend(['--test-output-file', config['test_output_file']])
        if 'test_job_description' in config:
            cmd.extend(['--test-job-description', config['test_job_description']])
        if 'test_company_name' in config:
            cmd.extend(['--test-company-name', config['test_company_name']])
        if 'test_job_title' in config:
            cmd.extend(['--test-job-title', config['test_job_title']])
        if 'test_name' in config:
            cmd.extend(['--test-name', config['test_name']])
        if 'test_email' in config:
            cmd.extend(['--test-email', config['test_email']])
        if 'test_phone' in config:
            cmd.extend(['--test-phone', config['test_phone']])
        if 'test_linkedin' in config:
            cmd.extend(['--test-linkedin', config['test_linkedin']])
        if 'test_nationality' in config:
            cmd.extend(['--test-nationality', config['test_nationality']])
    
    # Add extra arguments
    if extra_args:
        cmd.extend(extra_args)
    
    return cmd

def run_test(test_name=None, config_file="test_config.yaml", extra_args=None):
    """Run specific test or all tests with configuration"""
    config = load_test_config(config_file)
    cmd = build_test_command(test_name, config, extra_args)
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    return result.returncode == 0

def run_test_scenarios(config_file="test_config.yaml"):
    """Run tests with different scenarios"""
    config = load_test_config(config_file)
    
    if 'test_scenarios' in config:
        print("Running tests with different scenarios...")
        for scenario in config['test_scenarios']:
            print(f"\n🧪 Testing scenario: {scenario['name']}")
            print("-" * 40)
            
            # Create scenario-specific config
            scenario_config = config.copy()
            scenario_config.update({
                'test_job_description': scenario['job_description'],
                'test_company_name': scenario['company_name'],
                'test_job_title': scenario['job_title']
            })
            
            # Run a subset of tests with this scenario
            success = run_test("init", config_file, None)
            if not success:
                print(f"❌ Scenario {scenario['name']} failed!")
                return False
        
        print("\n✅ All scenarios completed!")
        return True
    else:
        print("No test scenarios found in configuration.")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='CVCustomizer Test Runner')
    parser.add_argument('test_name', nargs='?', help='Specific test category to run')
    parser.add_argument('--config', default='test_config.yaml', help='Configuration file path')
    parser.add_argument('--scenarios', action='store_true', help='Run test scenarios')
    parser.add_argument('--api-key', help='Override API key')
    parser.add_argument('--api-endpoint', help='Override API endpoint')
    parser.add_argument('--job-description', help='Override job description')
    parser.add_argument('--company-name', help='Override company name')
    parser.add_argument('--job-title', help='Override job title')
    
    args = parser.parse_args()
    
    # Build extra arguments from command line overrides
    extra_args = []
    if args.api_key:
        extra_args.extend(['--api-key', args.api_key])
    if args.api_endpoint:
        extra_args.extend(['--api-endpoint', args.api_endpoint])
    if args.job_description:
        extra_args.extend(['--test-job-description', args.job_description])
    if args.company_name:
        extra_args.extend(['--test-company-name', args.company_name])
    if args.job_title:
        extra_args.extend(['--test-job-title', args.job_title])
    
    if args.scenarios:
        success = run_test_scenarios(args.config)
    elif args.test_name:
        print(f"Running test: {args.test_name}")
        success = run_test(args.test_name, args.config, extra_args)
    else:
        print("Running all tests...")
        success = run_test(None, args.config, extra_args)
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
