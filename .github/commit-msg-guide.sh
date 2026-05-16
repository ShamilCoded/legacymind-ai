#!/bin/bash

# Commit Message Guide for LegacyMind AI
# This script helps developers write proper commit messages

echo "======================================"
echo "LegacyMind AI - Commit Message Guide"
echo "======================================"
echo ""

# Function to display commit types
show_types() {
    echo "📝 COMMIT TYPES:"
    echo "  feat      - New feature"
    echo "  fix       - Bug fix"
    echo "  docs      - Documentation changes"
    echo "  style     - Code style changes (formatting)"
    echo "  refactor  - Code refactoring"
    echo "  perf      - Performance improvements"
    echo "  test      - Adding or updating tests"
    echo "  chore     - Maintenance tasks"
    echo "  ci        - CI/CD configuration changes"
    echo "  build     - Build system changes"
    echo ""
}

# Function to display scopes
show_scopes() {
    echo "🎯 COMMON SCOPES:"
    echo ""
    echo "  Frontend:"
    echo "    ui        - UI components"
    echo "    pages     - Page components"
    echo "    api-client- API client code"
    echo "    styles    - Styling changes"
    echo "    config    - Configuration files"
    echo ""
    echo "  Backend:"
    echo "    api       - API endpoints"
    echo "    services  - Service layer"
    echo "    models    - Data models"
    echo "    utils     - Utility functions"
    echo "    config    - Configuration files"
    echo "    db        - Database related"
    echo ""
    echo "  Shared:"
    echo "    deps      - Dependencies"
    echo "    docs      - Documentation"
    echo "    tests     - Testing"
    echo ""
}

# Function to display examples
show_examples() {
    echo "💡 EXAMPLES:"
    echo ""
    echo "  feat(ui): add risk analysis dashboard component"
    echo "  fix(api): correct timeout handling in architecture API"
    echo "  docs(readme): update installation instructions"
    echo "  refactor(services): extract common logic to utility functions"
    echo "  perf(ui): implement lazy loading for charts"
    echo "  chore(deps): update dependencies to latest versions"
    echo ""
}

# Function to display format
show_format() {
    echo "📋 FORMAT:"
    echo ""
    echo "  <type>(<scope>): <subject>"
    echo ""
    echo "  <body> (optional)"
    echo ""
    echo "  <footer> (optional)"
    echo ""
    echo "RULES:"
    echo "  - Use imperative mood (\"add\" not \"added\")"
    echo "  - Don't capitalize first letter"
    echo "  - No period at the end"
    echo "  - Max 72 characters for subject"
    echo "  - Separate body with blank line"
    echo "  - Reference issues: Closes #123"
    echo ""
}

# Main menu
while true; do
    echo "What would you like to see?"
    echo "  1) Commit Types"
    echo "  2) Scopes"
    echo "  3) Examples"
    echo "  4) Format & Rules"
    echo "  5) All"
    echo "  6) Exit"
    echo ""
    read -p "Enter choice [1-6]: " choice
    echo ""
    
    case $choice in
        1)
            show_types
            ;;
        2)
            show_scopes
            ;;
        3)
            show_examples
            ;;
        4)
            show_format
            ;;
        5)
            show_types
            show_scopes
            show_examples
            show_format
            ;;
        6)
            echo "Happy committing! 🚀"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter 1-6."
            echo ""
            ;;
    esac
done

# Made with Bob
