# Helper functions for the Command Line Interface

from typing import List, Dict, Any, Optional
import textwrap

def display_menu(title: str, options: List[str]):
    """Displays a formatted menu."""
    print("\n" + "=" * (len(title) + 4))
    print(f"  {title}")
    print("=" * (len(title) + 4))
    for i, option in enumerate(options):
        print(f"  {i}. {option}")
    print("-" * (len(title) + 4))

def get_input(prompt: str, input_type: type = str, required: bool = True, allowed_values: Optional[List[str]] = None) -> Any:
    """Gets and validates user input."""
    while True:
        user_input = input(f"{prompt}: ").strip()
        if not user_input:
            if required:
                print("Input is required. Please try again.")
                continue
            else:
                return None # Allow empty input if not required

        if input_type == int:
            try:
                value = int(user_input)
                # Additional check if specific integer values are allowed (e.g., menu choices)
                if allowed_values is not None and str(value) not in allowed_values:
                     print(f"Invalid choice. Please enter a number between 0 and {len(allowed_values)-1}.")
                     continue
                return value
            except ValueError:
                print("Invalid input. Please enter a whole number.")
        elif input_type == float:
            try:
                return float(user_input)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif input_type == str:
             if allowed_values is not None and user_input not in allowed_values:
                 print(f"Invalid input. Allowed values are: {', '.join(allowed_values)}")
                 continue
             return user_input # Return the string directly
        else:
             # Fallback for other types or if validation logic needs expansion
             return user_input

def display_table(headers: List[str], data: List[Dict[str, Any]], empty_message="No data found.", max_col_width=30):
    """Displays data in a formatted table."""
    if not data:
        print(f"\n>> {empty_message}\n")
        return
    # Step 1: Calculate column widths (respecting max_col_width)
    col_widths = [min(max(len(str(h)), 
                     max((len(str(row.get(h, ''))) for row in data), default=0)), max_col_width)
                  for h in headers]

    # Step 2: Wrap each cell’s text
    wrapped_data = []
    for row in data:
        wrapped_row = []
        for i, h in enumerate(headers):
            cell = str(row.get(h, ''))
            wrapped_cell = textwrap.wrap(cell, width=col_widths[i]) or [""]
            wrapped_row.append(wrapped_cell)
        wrapped_data.append(wrapped_row)

    # Step 3: Compute max number of lines per row
    row_heights = [max(len(cell) for cell in row) for row in wrapped_data]

    # Step 4: Print header
    header_line = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    print("\n" + header_line)
    print(separator)

    # Step 5: Print wrapped rows
    for row, height in zip(wrapped_data, row_heights):
        for line_no in range(height):
            line = []
            for i, cell_lines in enumerate(row):
                cell_line = cell_lines[line_no] if line_no < len(cell_lines) else ""
                line.append(f"{cell_line:<{col_widths[i]}}")
            print(" | ".join(line))
    print()

    # # Calculate column widths
    # col_widths = [len(h) for h in headers]
    # for row in data:
    #     for i, key in enumerate(headers):
    #         col_widths[i] = max(col_widths[i], len(str(row.get(key, ""))))
        
    #     # for i, cell in enumerate(row):
    #     #     col_widths[i] = max(col_widths[i], len(str(cell)))

    # # Print header
    # header_line = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    # separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    # print("\n" + header_line)
    # print(separator)

    # # Print data rows
    # for row in data:
    #     row_line = " | ".join(f"{str(row.get(key, '')):<{col_widths[i]}}" for i, key in enumerate(headers))
    #     # row_line = " | ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row))
    #     print(row_line)
    # print()

def display_message(message: str, msg_type: str = "info"):
    """Displays a formatted message (info, success, error)."""
    if msg_type == "success":
        print(f"\n[SUCCESS] {message}")
    elif msg_type == "error":
        print(f"\n[ERROR] {message}")
    else:
        print(f"\n[INFO] {message}")

def confirm_action(prompt: str = "Are you sure you want to proceed?") -> bool:
    """Asks for user confirmation."""
    while True:
        choice = input(f"{prompt} (y/n): ").lower().strip()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def pause_screen():
    """Pauses execution until the user presses Enter."""
    input("\nPress Enter to continue...")