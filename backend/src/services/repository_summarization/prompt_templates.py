"""
Prompt Templates for Repository Summarization

Optimized prompts for enterprise repository analysis.
"""

from typing import Dict, Any


class PromptTemplates:
    """
    Collection of optimized prompt templates for different aspects of repository analysis.
    Designed for enterprise-scale repositories with complex architectures.
    """
    
    @staticmethod
    def repository_overview(repo_data: Dict[str, Any]) -> str:
        """
        Generate prompt for repository overview analysis.
        
        Args:
            repo_data: Dictionary containing repository metadata and structure
            
        Returns:
            Formatted prompt string
        """
        return f"""Analyze this enterprise repository and provide a comprehensive overview.

Repository Metadata:
- Name: {repo_data.get('name', 'N/A')}
- Description: {repo_data.get('description', 'N/A')}
- Primary Language: {repo_data.get('primary_language', 'N/A')}
- Total Files: {repo_data.get('total_files', 0)}
- Total Lines of Code: {repo_data.get('total_loc', 0)}

File Structure:
{repo_data.get('file_structure', 'N/A')}

Top-Level Directories:
{repo_data.get('top_level_dirs', 'N/A')}

Provide a concise overview that includes:
1. **Purpose**: What is the primary purpose of this repository?
2. **Scope**: What problem domain does it address?
3. **Scale**: Assess the complexity and size (small/medium/large/enterprise)
4. **Organization**: How is the codebase organized?
5. **Key Characteristics**: Notable patterns or approaches used

Keep the overview professional, technical, and focused on actionable insights."""

    @staticmethod
    def architecture_analysis(repo_data: Dict[str, Any]) -> str:
        """
        Generate prompt for architecture analysis.
        
        Args:
            repo_data: Dictionary containing code structure and patterns
            
        Returns:
            Formatted prompt string
        """
        return f"""Analyze the software architecture of this enterprise repository.

Repository Structure:
{repo_data.get('directory_tree', 'N/A')}

Key Files and Modules:
{repo_data.get('key_files', 'N/A')}

Configuration Files:
{repo_data.get('config_files', 'N/A')}

Code Patterns Detected:
{repo_data.get('code_patterns', 'N/A')}

Provide a detailed architecture analysis covering:

1. **Architectural Pattern**: Identify the primary architecture (e.g., microservices, monolithic, layered, hexagonal, event-driven)

2. **Layer Structure**: Describe the application layers (presentation, business logic, data access, etc.)

3. **Module Organization**: How are modules/packages organized? What's the dependency flow?

4. **Design Patterns**: Identify key design patterns used (Factory, Repository, Strategy, etc.)

5. **Separation of Concerns**: How well are concerns separated? (UI, business logic, data)

6. **Scalability Considerations**: What architectural decisions support scalability?

7. **Integration Points**: How does the system integrate with external services?

8. **Configuration Management**: How is configuration handled across environments?

Focus on enterprise-level architectural decisions and their implications."""

    @staticmethod
    def services_identification(repo_data: Dict[str, Any]) -> str:
        """
        Generate prompt for identifying major services/components.
        
        Args:
            repo_data: Dictionary containing service-related code
            
        Returns:
            Formatted prompt string
        """
        return f"""Identify and analyze the major services and components in this enterprise repository.

Service Directories:
{repo_data.get('service_dirs', 'N/A')}

API Endpoints:
{repo_data.get('api_endpoints', 'N/A')}

Class Definitions:
{repo_data.get('class_definitions', 'N/A')}

Module Exports:
{repo_data.get('module_exports', 'N/A')}

For each major service/component, provide:

1. **Service Name**: Clear, descriptive name

2. **Purpose**: What does this service do?

3. **Responsibilities**: Core responsibilities and capabilities

4. **Dependencies**: What other services/components does it depend on?

5. **API Surface**: Key methods, endpoints, or interfaces exposed

6. **Data Flow**: How does data flow through this service?

7. **Integration**: How does it integrate with other services?

8. **Business Value**: What business capability does it enable?

Prioritize services by:
- Business criticality
- Complexity
- Integration points
- Usage frequency

Present findings in a structured format suitable for technical documentation."""

    @staticmethod
    def dependencies_analysis(repo_data: Dict[str, Any]) -> str:
        """
        Generate prompt for dependencies analysis.
        
        Args:
            repo_data: Dictionary containing dependency information
            
        Returns:
            Formatted prompt string
        """
        return f"""Analyze the dependencies and external integrations of this enterprise repository.

Package Dependencies:
{repo_data.get('package_dependencies', 'N/A')}

Internal Dependencies:
{repo_data.get('internal_dependencies', 'N/A')}

External APIs/Services:
{repo_data.get('external_apis', 'N/A')}

Database Connections:
{repo_data.get('database_connections', 'N/A')}

Provide a comprehensive dependency analysis:

1. **External Dependencies**:
   - List major third-party libraries/frameworks
   - Categorize by purpose (web framework, database, testing, etc.)
   - Identify version constraints and compatibility requirements
   - Flag any deprecated or outdated dependencies

2. **Internal Dependencies**:
   - Map module-to-module dependencies
   - Identify circular dependencies (if any)
   - Highlight tightly coupled components
   - Suggest areas for decoupling

3. **External Service Integrations**:
   - List external APIs and services
   - Describe integration patterns (REST, GraphQL, message queues, etc.)
   - Identify authentication/authorization mechanisms
   - Note any vendor lock-in concerns

4. **Database Dependencies**:
   - Identify database systems used
   - Describe data access patterns
   - Note any ORM or query builders used

5. **Risk Assessment**:
   - Security vulnerabilities in dependencies
   - Maintenance burden (unmaintained packages)
   - License compliance issues
   - Performance bottlenecks

6. **Recommendations**:
   - Dependency updates needed
   - Alternative libraries to consider
   - Opportunities for consolidation

Focus on enterprise concerns: security, maintainability, and long-term viability."""

    @staticmethod
    def business_logic_summary(repo_data: Dict[str, Any]) -> str:
        """
        Generate prompt for business logic analysis.
        
        Args:
            repo_data: Dictionary containing business logic code
            
        Returns:
            Formatted prompt string
        """
        return f"""Analyze and summarize the business logic implemented in this enterprise repository.

Core Business Modules:
{repo_data.get('business_modules', 'N/A')}

Domain Models:
{repo_data.get('domain_models', 'N/A')}

Business Rules:
{repo_data.get('business_rules', 'N/A')}

Workflow Implementations:
{repo_data.get('workflows', 'N/A')}

Validation Logic:
{repo_data.get('validation_logic', 'N/A')}

Provide a business logic summary covering:

1. **Core Business Domains**:
   - Identify primary business domains/bounded contexts
   - Describe the business capabilities each domain provides
   - Map domain relationships

2. **Business Entities**:
   - List key business entities/models
   - Describe their attributes and relationships
   - Identify entity lifecycle management

3. **Business Rules**:
   - Extract and document key business rules
   - Identify validation rules and constraints
   - Note any complex business logic algorithms

4. **Business Workflows**:
   - Describe major business processes/workflows
   - Identify state machines or process orchestration
   - Map workflow triggers and outcomes

5. **Business Logic Patterns**:
   - Identify patterns used (Domain-Driven Design, CQRS, etc.)
   - Note use of business logic frameworks
   - Assess separation of business logic from infrastructure

6. **Data Transformations**:
   - Key data transformation logic
   - Business calculations and computations
   - Aggregation and reporting logic

7. **Business Constraints**:
   - Authorization and access control rules
   - Data integrity constraints
   - Business-level validation

Present findings in business-friendly language while maintaining technical accuracy.
Focus on what the system does from a business perspective."""

    @staticmethod
    def tech_stack_analysis(repo_data: Dict[str, Any]) -> str:
        """
        Generate prompt for technology stack analysis.
        
        Args:
            repo_data: Dictionary containing technology information
            
        Returns:
            Formatted prompt string
        """
        return f"""Analyze the complete technology stack of this enterprise repository.

Programming Languages:
{repo_data.get('languages', 'N/A')}

Frameworks and Libraries:
{repo_data.get('frameworks', 'N/A')}

Build Tools:
{repo_data.get('build_tools', 'N/A')}

Testing Frameworks:
{repo_data.get('testing_frameworks', 'N/A')}

Infrastructure as Code:
{repo_data.get('infrastructure_code', 'N/A')}

CI/CD Configuration:
{repo_data.get('cicd_config', 'N/A')}

Provide a comprehensive tech stack analysis:

1. **Programming Languages**:
   - Primary and secondary languages used
   - Language versions and compatibility
   - Rationale for language choices

2. **Frontend Stack** (if applicable):
   - UI framework/library (React, Vue, Angular, etc.)
   - State management solution
   - Styling approach (CSS-in-JS, preprocessors, etc.)
   - Build tools and bundlers

3. **Backend Stack**:
   - Web framework
   - API design (REST, GraphQL, gRPC, etc.)
   - Authentication/authorization libraries
   - Background job processing

4. **Data Layer**:
   - Database systems (SQL, NoSQL, etc.)
   - ORM/ODM tools
   - Caching solutions
   - Data migration tools

5. **Testing Stack**:
   - Unit testing frameworks
   - Integration testing tools
   - E2E testing solutions
   - Code coverage tools
   - Mocking/stubbing libraries

6. **DevOps & Infrastructure**:
   - Containerization (Docker, etc.)
   - Orchestration (Kubernetes, etc.)
   - CI/CD platforms
   - Monitoring and logging tools
   - Infrastructure as Code tools

7. **Development Tools**:
   - Linters and formatters
   - Type checking tools
   - Documentation generators
   - Development environment setup

8. **Cloud Services** (if applicable):
   - Cloud provider (AWS, Azure, GCP, etc.)
   - Managed services used
   - Serverless components

9. **Security Tools**:
   - Security scanning tools
   - Dependency vulnerability checkers
   - Secret management

10. **Stack Assessment**:
    - Modern vs. legacy technologies
    - Consistency across the stack
    - Potential technical debt
    - Upgrade paths and migration needs
    - Team skill requirements

Provide enterprise-focused insights on maintainability, scalability, and long-term viability."""

    @staticmethod
    def comprehensive_summary(repo_data: Dict[str, Any]) -> str:
        """
        Generate prompt for a comprehensive repository summary combining all aspects.
        
        Args:
            repo_data: Dictionary containing all repository information
            
        Returns:
            Formatted prompt string
        """
        return f"""Generate a comprehensive executive summary of this enterprise repository.

Repository Information:
{repo_data.get('metadata', 'N/A')}

Structure Overview:
{repo_data.get('structure', 'N/A')}

Code Statistics:
{repo_data.get('statistics', 'N/A')}

Create an executive summary that synthesizes all aspects:

1. **Executive Overview** (2-3 paragraphs):
   - What is this system?
   - What business problem does it solve?
   - Who are the primary users/stakeholders?

2. **Technical Summary**:
   - Architecture pattern and design approach
   - Technology stack highlights
   - Key technical decisions and their rationale

3. **Major Components**:
   - List 5-7 most important services/modules
   - Brief description of each
   - How they work together

4. **Business Capabilities**:
   - Core business functions enabled
   - Key workflows supported
   - Value delivered to users

5. **Integration Landscape**:
   - External systems integrated
   - APIs exposed
   - Data flows

6. **Quality & Maturity**:
   - Code quality indicators
   - Testing coverage and approach
   - Documentation completeness
   - DevOps maturity

7. **Strengths**:
   - What is done well?
   - Notable best practices
   - Competitive advantages

8. **Areas for Improvement**:
   - Technical debt
   - Scalability concerns
   - Security considerations
   - Modernization opportunities

9. **Recommendations**:
   - Priority improvements
   - Strategic technology decisions
   - Risk mitigation strategies

Format for executive and technical audiences. Be concise but comprehensive.
Focus on strategic insights and actionable recommendations."""

    @staticmethod
    def get_all_prompts(repo_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate all prompt templates for comprehensive analysis.
        
        Args:
            repo_data: Dictionary containing all repository information
            
        Returns:
            Dictionary mapping analysis type to prompt
        """
        return {
            'overview': PromptTemplates.repository_overview(repo_data),
            'architecture': PromptTemplates.architecture_analysis(repo_data),
            'services': PromptTemplates.services_identification(repo_data),
            'dependencies': PromptTemplates.dependencies_analysis(repo_data),
            'business_logic': PromptTemplates.business_logic_summary(repo_data),
            'tech_stack': PromptTemplates.tech_stack_analysis(repo_data),
            'comprehensive': PromptTemplates.comprehensive_summary(repo_data)
        }

# Made with Bob
