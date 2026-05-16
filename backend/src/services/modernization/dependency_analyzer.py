"""
Dependency analyzer for detecting outdated and vulnerable dependencies.
"""
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging

from .models import (
    DependencyAnalysis,
    OutdatedDependency,
    ModernizationPriority
)

logger = logging.getLogger(__name__)


class DependencyAnalyzer:
    """Analyzes project dependencies for modernization opportunities."""
    
    # Known deprecated packages and their alternatives
    DEPRECATED_PACKAGES = {
        'python': {
            'flask-cors': 'flask-cors (still maintained, but consider built-in CORS)',
            'pycrypto': 'pycryptodome',
            'python-dateutil': 'python-dateutil (still maintained)',
            'nose': 'pytest',
            'mock': 'unittest.mock (built-in)',
        },
        'javascript': {
            'request': 'axios or node-fetch',
            'gulp': 'webpack or vite',
            'bower': 'npm or yarn',
            'moment': 'date-fns or dayjs',
            'tslint': 'eslint with typescript-eslint',
        }
    }
    
    # Security vulnerability patterns (simplified)
    KNOWN_VULNERABILITIES = {
        'python': {
            'django': {'<2.2': 5, '<3.0': 3, '<3.2': 2},
            'flask': {'<1.0': 4, '<2.0': 2},
            'requests': {'<2.20': 3, '<2.25': 1},
            'pillow': {'<8.0': 4, '<9.0': 2},
            'pyyaml': {'<5.4': 3},
            'jinja2': {'<2.11': 3},
            'sqlalchemy': {'<1.3': 2},
        },
        'javascript': {
            'express': {'<4.17': 3},
            'lodash': {'<4.17.20': 4},
            'axios': {'<0.21': 2},
            'react': {'<16.14': 2, '<17.0': 1},
            'next': {'<10.0': 3},
        }
    }
    
    def __init__(self):
        """Initialize dependency analyzer."""
        self.dependency_files = {
            'python': ['requirements.txt', 'Pipfile', 'pyproject.toml', 'setup.py'],
            'javascript': ['package.json', 'yarn.lock', 'package-lock.json'],
            'java': ['pom.xml', 'build.gradle'],
            'ruby': ['Gemfile', 'Gemfile.lock'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.toml', 'Cargo.lock'],
        }
    
    def analyze(self, directory: str) -> DependencyAnalysis:
        """
        Analyze dependencies in the directory.
        
        Args:
            directory: Directory path to analyze
            
        Returns:
            DependencyAnalysis with findings
        """
        logger.info(f"Analyzing dependencies in {directory}")
        
        dir_path = Path(directory)
        all_dependencies = []
        
        # Detect and parse dependency files
        for lang, files in self.dependency_files.items():
            for dep_file in files:
                file_path = dir_path / dep_file
                if file_path.exists():
                    logger.info(f"Found {dep_file} for {lang}")
                    deps = self._parse_dependency_file(file_path, lang)
                    all_dependencies.extend(deps)
        
        # Analyze each dependency
        outdated_deps = []
        total_security_issues = 0
        critical_updates = 0
        deprecated = []
        alternatives = {}
        
        for dep in all_dependencies:
            analysis = self._analyze_dependency(dep)
            if analysis:
                outdated_deps.append(analysis)
                total_security_issues += analysis.security_vulnerabilities
                if analysis.update_priority == ModernizationPriority.CRITICAL:
                    critical_updates += 1
                
                # Check for deprecated packages
                lang = dep.get('language', 'python')
                if dep['name'] in self.DEPRECATED_PACKAGES.get(lang, {}):
                    deprecated.append(dep['name'])
                    alternatives[dep['name']] = self.DEPRECATED_PACKAGES[lang][dep['name']]
        
        # Calculate total effort
        total_effort = sum(dep.estimated_effort_hours for dep in outdated_deps)
        
        return DependencyAnalysis(
            total_dependencies=len(all_dependencies),
            outdated_dependencies=outdated_deps,
            critical_updates=critical_updates,
            security_issues=total_security_issues,
            deprecated_packages=deprecated,
            alternative_recommendations=alternatives,
            total_update_effort_hours=total_effort
        )
    
    def _parse_dependency_file(self, file_path: Path, language: str) -> List[Dict[str, Any]]:
        """Parse dependency file and extract dependencies."""
        dependencies = []
        
        try:
            if file_path.name == 'requirements.txt':
                dependencies = self._parse_requirements_txt(file_path)
            elif file_path.name == 'package.json':
                dependencies = self._parse_package_json(file_path)
            elif file_path.name == 'Pipfile':
                dependencies = self._parse_pipfile(file_path)
            elif file_path.name == 'pyproject.toml':
                dependencies = self._parse_pyproject_toml(file_path)
            
            # Add language info
            for dep in dependencies:
                dep['language'] = language
                
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
        
        return dependencies
    
    def _parse_requirements_txt(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse requirements.txt file."""
        dependencies = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse package==version or package>=version
                match = re.match(r'^([a-zA-Z0-9\-_]+)([>=<~!]+)(.+)$', line)
                if match:
                    name, operator, version = match.groups()
                    dependencies.append({
                        'name': name.lower(),
                        'version': version.strip(),
                        'operator': operator,
                        'file': str(file_path)
                    })
                else:
                    # Package without version
                    name = line.split('[')[0].strip()
                    if name:
                        dependencies.append({
                            'name': name.lower(),
                            'version': 'latest',
                            'operator': '',
                            'file': str(file_path)
                        })
        
        return dependencies
    
    def _parse_package_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse package.json file."""
        dependencies = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse dependencies and devDependencies
            for dep_type in ['dependencies', 'devDependencies']:
                if dep_type in data:
                    for name, version in data[dep_type].items():
                        # Remove ^ or ~ prefix
                        clean_version = version.lstrip('^~')
                        dependencies.append({
                            'name': name,
                            'version': clean_version,
                            'operator': '^' if version.startswith('^') else '~' if version.startswith('~') else '=',
                            'file': str(file_path),
                            'dev': dep_type == 'devDependencies'
                        })
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON in {file_path}: {e}")
        
        return dependencies
    
    def _parse_pipfile(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Pipfile."""
        dependencies = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple parsing (would use toml library in production)
            in_packages = False
            for line in content.split('\n'):
                line = line.strip()
                if line == '[packages]':
                    in_packages = True
                    continue
                elif line.startswith('['):
                    in_packages = False
                    continue
                
                if in_packages and '=' in line:
                    parts = line.split('=')
                    name = parts[0].strip()
                    version = parts[1].strip().strip('"\'')
                    dependencies.append({
                        'name': name.lower(),
                        'version': version,
                        'operator': '=',
                        'file': str(file_path)
                    })
        except Exception as e:
            logger.error(f"Error parsing Pipfile: {e}")
        
        return dependencies
    
    def _parse_pyproject_toml(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse pyproject.toml file."""
        dependencies = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple parsing for dependencies section
            in_dependencies = False
            for line in content.split('\n'):
                line = line.strip()
                if 'dependencies' in line and '=' in line:
                    in_dependencies = True
                    continue
                elif line.startswith('[') and in_dependencies:
                    in_dependencies = False
                    continue
                
                if in_dependencies and '=' in line:
                    match = re.match(r'"([^"]+)"', line)
                    if match:
                        dep_str = match.group(1)
                        # Parse package>=version format
                        dep_match = re.match(r'^([a-zA-Z0-9\-_]+)([>=<~!]+)(.+)$', dep_str)
                        if dep_match:
                            name, operator, version = dep_match.groups()
                            dependencies.append({
                                'name': name.lower(),
                                'version': version.strip(),
                                'operator': operator,
                                'file': str(file_path)
                            })
        except Exception as e:
            logger.error(f"Error parsing pyproject.toml: {e}")
        
        return dependencies
    
    def _analyze_dependency(self, dep: Dict[str, Any]) -> Optional[OutdatedDependency]:
        """Analyze a single dependency."""
        name = dep['name']
        current_version = dep['version']
        language = dep.get('language', 'python')
        
        # Simulate version checking (in production, would use package registries)
        latest_version, versions_behind = self._get_latest_version(name, current_version, language)
        
        if versions_behind == 0:
            return None  # Up to date
        
        # Check for security vulnerabilities
        security_vulns = self._check_security_vulnerabilities(name, current_version, language)
        
        # Determine priority
        priority = self._determine_update_priority(
            versions_behind, security_vulns, name, language
        )
        
        # Check for breaking changes
        breaking_changes = self._has_breaking_changes(name, current_version, latest_version)
        
        # Estimate effort
        effort = self._estimate_update_effort(
            versions_behind, breaking_changes, security_vulns
        )
        
        # Generate migration notes
        notes = self._generate_migration_notes(name, current_version, latest_version, language)
        
        return OutdatedDependency(
            name=name,
            current_version=current_version,
            latest_version=latest_version,
            versions_behind=versions_behind,
            security_vulnerabilities=security_vulns,
            breaking_changes=breaking_changes,
            update_priority=priority,
            migration_notes=notes,
            estimated_effort_hours=effort
        )
    
    def _get_latest_version(self, name: str, current: str, language: str) -> Tuple[str, int]:
        """Get latest version and calculate versions behind."""
        # Simplified version comparison
        # In production, would query PyPI, npm, etc.
        
        if current == 'latest':
            return 'latest', 0
        
        # Parse version numbers
        try:
            current_parts = [int(x) for x in current.split('.')[:3]]
        except (ValueError, AttributeError):
            return current, 0
        
        # Simulate latest version (increment minor version by 2-5)
        import random
        increment = random.randint(2, 5)
        latest_parts = current_parts.copy()
        latest_parts[1] += increment
        
        latest = '.'.join(map(str, latest_parts))
        versions_behind = increment
        
        return latest, versions_behind
    
    def _check_security_vulnerabilities(self, name: str, version: str, language: str) -> int:
        """Check for known security vulnerabilities."""
        vulns = self.KNOWN_VULNERABILITIES.get(language, {}).get(name, {})
        
        count = 0
        for version_pattern, vuln_count in vulns.items():
            if self._version_matches_pattern(version, version_pattern):
                count += vuln_count
        
        return count
    
    def _version_matches_pattern(self, version: str, pattern: str) -> bool:
        """Check if version matches vulnerability pattern."""
        if pattern.startswith('<'):
            try:
                threshold = pattern[1:]
                return self._compare_versions(version, threshold) < 0
            except:
                return False
        return False
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """Compare two version strings."""
        try:
            v1_parts = [int(x) for x in v1.split('.')[:3]]
            v2_parts = [int(x) for x in v2.split('.')[:3]]
            
            for i in range(3):
                if v1_parts[i] < v2_parts[i]:
                    return -1
                elif v1_parts[i] > v2_parts[i]:
                    return 1
            return 0
        except:
            return 0
    
    def _determine_update_priority(
        self, versions_behind: int, security_vulns: int, name: str, language: str
    ) -> ModernizationPriority:
        """Determine update priority."""
        if security_vulns >= 3:
            return ModernizationPriority.CRITICAL
        elif security_vulns >= 1 or versions_behind >= 10:
            return ModernizationPriority.HIGH
        elif versions_behind >= 5:
            return ModernizationPriority.MEDIUM
        else:
            return ModernizationPriority.LOW
    
    def _has_breaking_changes(self, name: str, current: str, latest: str) -> bool:
        """Check if update has breaking changes."""
        try:
            current_major = int(current.split('.')[0])
            latest_major = int(latest.split('.')[0])
            return latest_major > current_major
        except:
            return False
    
    def _estimate_update_effort(
        self, versions_behind: int, breaking_changes: bool, security_vulns: int
    ) -> float:
        """Estimate effort to update dependency."""
        base_effort = 0.5  # Base 30 minutes
        
        # Add effort based on versions behind
        base_effort += versions_behind * 0.25
        
        # Add effort for breaking changes
        if breaking_changes:
            base_effort += 4.0  # 4 hours for breaking changes
        
        # Add effort for security fixes
        base_effort += security_vulns * 0.5
        
        return round(base_effort, 1)
    
    def _generate_migration_notes(
        self, name: str, current: str, latest: str, language: str
    ) -> str:
        """Generate migration notes."""
        notes = []
        
        # Check for major version change
        try:
            current_major = int(current.split('.')[0])
            latest_major = int(latest.split('.')[0])
            
            if latest_major > current_major:
                notes.append(f"Major version upgrade from {current_major}.x to {latest_major}.x")
                notes.append("Review changelog for breaking changes")
                notes.append("Update code to use new APIs")
                notes.append("Run comprehensive tests after upgrade")
        except:
            pass
        
        # Add language-specific notes
        if language == 'python':
            notes.append("Update requirements.txt or pyproject.toml")
            notes.append("Test in virtual environment first")
        elif language == 'javascript':
            notes.append("Update package.json")
            notes.append("Run npm audit fix after update")
        
        return "; ".join(notes) if notes else "Standard update procedure"


# Made with Bob