#!/bin/bash

# Determine project root relative to this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Ensure PYTHONPATH includes the current directory
export PYTHONPATH="${PYTHONPATH}:${PROJECT_ROOT}"

# Create results directory
mkdir -p results

echo "========================================================"
echo "       Running Realistic Tasks Automation"
echo "========================================================"
echo "Project Root: $PROJECT_ROOT"
echo "Output Dir  : results/"
echo "--------------------------------------------------------"

# Function to run a task
run_task() {
    TASK_SCRIPT=$1
    OUTPUT_FILE=$2
    TASK_NAME=$3

    echo "▶ Running $TASK_NAME..."
    if [ -f "$TASK_SCRIPT" ]; then
        # Run python script and redirect both stdout and stderr to the output file
        python "$TASK_SCRIPT" > "$OUTPUT_FILE" 2>&1
        
        if [ $? -eq 0 ]; then
            echo "   ✅ Success! Output saved to $OUTPUT_FILE"
        else
            echo "   ❌ Failed! Check $OUTPUT_FILE for errors."
        fi
    else
        echo "   ❌ Error: Script $TASK_SCRIPT not found!"
    fi
    echo "--------------------------------------------------------"
}

# Run Task 1: Conference Preparation
run_task "tests/task_conference_preparation.py" "results/task_conference_preparation.txt" "Task 1: Conference Preparation"

# Run Task 2: Course Project Preparation
run_task "tests/task_course_project.py" "results/task_course_project.txt" "Task 2: Course Project Preparation"

# Run Task 3: Thesis Defense Preparation
run_task "tests/task_thesis_defense.py" "results/task_thesis_defense.txt" "Task 3: Thesis Defense Preparation"

echo "All tasks execution completed."
