#!/usr/bin/env python3
"""
OpenEnv Pre-Submission Validator
Checks all requirements for HF Spaces submission
"""

import os
import sys
import subprocess
import json
import tempfile
import shutil
from pathlib import Path

class Validator:
    def __init__(self):
        self.project_root = Path("/home/mohan/openenv-project")
        self.passed = []
        self.failed = []
        self.warnings = []
    
    def log_pass(self, test_name: str, message: str = ""):
        self.passed.append((test_name, message))
        print(f"✓ PASS: {test_name}")
        if message:
            print(f"  └─ {message}")
    
    def log_fail(self, test_name: str, message: str = ""):
        self.failed.append((test_name, message))
        print(f"✗ FAIL: {test_name}")
        if message:
            print(f"  └─ {message}")
    
    def log_warn(self, test_name: str, message: str = ""):
        self.warnings.append((test_name, message))
        print(f"⚠ WARN: {test_name}")
        if message:
            print(f"  └─ {message}")
    
    def check_inference_exists(self):
        """Check that inference.py exists in root directory"""
        inference_path = self.project_root / "inference.py"
        if inference_path.exists():
            self.log_pass("Inference Script Exists", f"Found at {inference_path}")
            return True
        else:
            self.log_fail("Inference Script Exists", f"inference.py not found in root")
            return False
    
    def check_environment_variables(self):
        """Check that environment variables are documented"""
        readme_path = self.project_root / "README.md"
        if not readme_path.exists():
            self.log_fail("Environment Variables Documented", "README.md not found")
            return False
        
        with open(readme_path) as f:
            readme = f.read()
        
        required_vars = ["API_BASE_URL", "MODEL_NAME", "HF_TOKEN"]
        found_vars = 0
        for var in required_vars:
            if var in readme:
                found_vars += 1
        
        if found_vars == len(required_vars):
            self.log_pass("Environment Variables Documented", 
                         f"All required variables ({', '.join(required_vars)}) documented")
            return True
        else:
            self.log_fail("Environment Variables Documented",
                         f"Missing {len(required_vars) - found_vars} required variables")
            return False
    
    def check_logging_format(self):
        """Check that inference.py contains [START], [STEP], [END] logging"""
        inference_path = self.project_root / "inference.py"
        if not inference_path.exists():
            self.log_fail("Structured Logging Format", "inference.py not found")
            return False
        
        with open(inference_path) as f:
            content = f.read()
        
        required_markers = ["[START]", "[STEP]", "[END]"]
        found_markers = 0
        for marker in required_markers:
            if marker in content:
                found_markers += 1
        
        if found_markers == len(required_markers):
            self.log_pass("Structured Logging Format",
                         f"Found all required markers: {', '.join(required_markers)}")
            return True
        else:
            self.log_fail("Structured Logging Format",
                         f"Missing {len(required_markers) - found_markers} required markers")
            return False
    
    def check_tasks_defined(self):
        """Check that 3+ tasks are defined"""
        env_path = self.project_root / "env" / "environment.py"
        if not env_path.exists():
            self.log_fail("3+ Tasks Defined", "environment.py not found")
            return False
        
        with open(env_path) as f:
            content = f.read()
        
        task_classes = ["EmailEnv", "CodeReviewEnv", "SupportEnv"]
        found_tasks = 0
        for task in task_classes:
            if f"class {task}" in content:
                found_tasks += 1
        
        if found_tasks >= 3:
            self.log_pass("3+ Tasks Defined", f"Found {found_tasks} task implementations")
            return True
        else:
            self.log_fail("3+ Tasks Defined", f"Found only {found_tasks} tasks (need 3+)")
            return False
    
    def check_graders_defined(self):
        """Check that graders are defined for all tasks"""
        grader_path = self.project_root / "env" / "grader.py"
        if not grader_path.exists():
            self.log_fail("Graders Defined", "grader.py not found")
            return False
        
        with open(grader_path) as f:
            content = f.read()
        
        graders = ["EmailClassificationGrader", "CodeReviewGrader", "SupportRoutingGrader"]
        found_graders = 0
        for grader in graders:
            if grader in content:
                found_graders += 1
        
        if found_graders >= 3:
            self.log_pass("Graders Defined", f"Found {found_graders} grader implementations")
            return True
        else:
            self.log_fail("Graders Defined", f"Found only {found_graders} graders (need 3+)")
            return False
    
    def check_openenv_yaml(self):
        """Check that openenv.yaml exists and is valid"""
        yaml_path = self.project_root / "openenv.yaml"
        if not yaml_path.exists():
            self.log_fail("openenv.yaml Exists", "openenv.yaml not found")
            return False
        
        with open(yaml_path) as f:
            content = f.read()
        
        # Check for required sections
        required_sections = ["tasks:", "observation_spaces:", "action_spaces:", "reward_structure:"]
        found_sections = 0
        for section in required_sections:
            if section in content:
                found_sections += 1
        
        if found_sections >= 3:
            self.log_pass("openenv.yaml Valid", f"Found required sections ({found_sections}/4)")
            return True
        else:
            self.log_fail("openenv.yaml Valid", f"Missing sections ({found_sections}/4)")
            return False
    
    def check_requirements_txt(self):
        """Check that requirements.txt has necessary packages"""
        req_path = self.project_root / "requirements.txt"
        if not req_path.exists():
            self.log_fail("requirements.txt Exists", "requirements.txt not found")
            return False
        
        with open(req_path) as f:
            content = f.read()
        
        required_packages = ["fastapi", "uvicorn", "pydantic", "openai"]
        found_packages = 0
        for pkg in required_packages:
            if pkg.lower() in content.lower():
                found_packages += 1
        
        if found_packages >= 3:
            self.log_pass("requirements.txt Complete",
                         f"Found {found_packages}/{len(required_packages)} required packages")
            return True
        else:
            self.log_fail("requirements.txt Complete",
                         f"Found only {found_packages}/{len(required_packages)} required packages")
            return False
    
    def check_dockerfile(self):
        """Check that Dockerfile exists and is valid"""
        docker_path = self.project_root / "Dockerfile"
        if not docker_path.exists():
            self.log_fail("Dockerfile Exists", "Dockerfile not found")
            return False
        
        with open(docker_path) as f:
            content = f.read()
        
        # Check for required lines
        required_elements = ["FROM", "EXPOSE 7860", "HEALTHCHECK", "ENTRYPOINT"]
        found_elements = []
        for elem in required_elements:
            if elem in content or (elem == "ENTRYPOINT" and "CMD" in content):
                found_elements.append(elem)
        
        if len(found_elements) >= 3:
            self.log_pass("Dockerfile Valid",
                         f"Found required elements: {', '.join(found_elements[:3])}")
            return True
        else:
            self.log_fail("Dockerfile Valid",
                         f"Found only {len(found_elements)} required elements")
            return False
    
    def check_docker_builds(self):
        """Check that Docker image builds successfully"""
        print("\n→ Building Docker image (this may take a minute)...")
        try:
            result = subprocess.run(
                ["docker", "build", "-t", "openenv-validator:latest", "."],
                cwd=self.project_root,
                capture_output=True,
                timeout=120
            )
            if result.returncode == 0:
                self.log_pass("Docker Builds", "Successfully built Docker image")
                return True
            else:
                self.log_fail("Docker Builds", f"Docker build failed: {result.stderr.decode()}")
                return False
        except subprocess.TimeoutExpired:
            self.log_fail("Docker Builds", "Docker build timed out")
            return False
        except Exception as e:
            self.log_fail("Docker Builds", f"Docker build error: {str(e)}")
            return False
    
    def check_inference_runs(self):
        """Check that inference.py runs without error"""
        print("\n→ Running inference script (using rule-based baseline)...")
        try:
            result = subprocess.run(
                ["python3", "inference.py"],
                cwd=self.project_root,
                capture_output=True,
                timeout=120,
                env={**os.environ, "NUM_EPISODES": "1"}
            )
            
            output = result.stdout.decode()
            
            # Check for required output markers
            if "[START]" in output and "[STEP]" in output and "[END]" in output:
                self.log_pass("Inference Runs",
                             "Script executed with all required log markers")
                
                # Check for JSON results
                if "[JSON_RESULTS]" in output:
                    self.log_pass("Inference Produces JSON",
                                 "Script produces structured JSON output")
                    return True
                else:
                    self.log_warn("Inference Produces JSON",
                                 "No [JSON_RESULTS] section found")
                    return True
            else:
                self.log_fail("Inference Runs",
                             f"Missing output markers. Got: {output[:200]}")
                return False
        except subprocess.TimeoutExpired:
            self.log_fail("Inference Runs", "Inference script timed out")
            return False
        except Exception as e:
            self.log_fail("Inference Runs", f"Script execution error: {str(e)}")
            return False
    
    def check_openai_client(self):
        """Check that inference.py uses OpenAI Client"""
        inference_path = self.project_root / "inference.py"
        if not inference_path.exists():
            self.log_fail("OpenAI Client Used", "inference.py not found")
            return False
        
        with open(inference_path) as f:
            content = f.read()
        
        if "from openai import OpenAI" in content or "OpenAI(" in content:
            self.log_pass("OpenAI Client Used",
                         "OpenAI Client properly imported and instantiated")
            return True
        else:
            self.log_fail("OpenAI Client Used",
                         "OpenAI Client not found in inference script")
            return False
    
    def run_all_checks(self):
        """Run all validation checks"""
        print("=" * 70)
        print("OpenEnv Pre-Submission Validation")
        print("=" * 70)
        print()
        
        # File structure checks
        print("[1] FILE STRUCTURE CHECKS")
        print("-" * 70)
        self.check_inference_exists()
        self.check_dockerfile()
        self.check_requirements_txt()
        self.check_openenv_yaml()
        
        print()
        print("[2] SPECIFICATION CHECKS")
        print("-" * 70)
        self.check_environment_variables()
        self.check_logging_format()
        self.check_openai_client()
        self.check_tasks_defined()
        self.check_graders_defined()
        
        print()
        print("[3] FUNCTIONALITY CHECKS")
        print("-" * 70)
        self.check_requirements_txt()
        self.check_docker_builds()
        self.check_inference_runs()
        
        # Summary
        print()
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print(f"✓ Passed: {len(self.passed)}")
        print(f"✗ Failed: {len(self.failed)}")
        print(f"⚠ Warnings: {len(self.warnings)}")
        print()
        
        if self.failed:
            print("FAILED TESTS:")
            for test, msg in self.failed:
                print(f"  ✗ {test}: {msg}")
            print()
        
        if self.warnings:
            print("WARNINGS:")
            for test, msg in self.warnings:
                print(f"  ⚠ {test}: {msg}")
            print()
        
        # Overall result
        if not self.failed:
            print("=" * 70)
            print("✓ ALL CHECKS PASSED - READY FOR SUBMISSION")
            print("=" * 70)
            return 0
        else:
            print("=" * 70)
            print("✗ SUBMISSION BLOCKED - PLEASE FIX FAILED TESTS")
            print("=" * 70)
            return 1

if __name__ == "__main__":
    validator = Validator()
    exit_code = validator.run_all_checks()
    sys.exit(exit_code)
