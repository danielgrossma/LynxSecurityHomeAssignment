from data_loader import IAMData
from sql_queries import security_risks

def display_menu(queries):
    """
    Displays the main menu of available risk analysis queries to the user.

    Args:
        queries (list): A list of dictionaries, where each dictionary
                        represents a security risk query with 'name' and 'description'.
    """
    print("\n--- Risk Analysis Menu ---")
    print("1. View Data Integrity Check Results")
    for i, query_info in enumerate(queries):
        print(f"{i + 2}. {query_info['name']}: {query_info['description']}")
    print("0. Exit")
    print("--------------------------")

def main():
    """
    Main function to run the CLI for risk analysis.
    Initializes IAMData, displays menu, and executes user-selected queries.
    """
    print("Loading IAM data and performing integrity checks...")
    # Initialize IAMData, which loads data and sets up the in-memory SQLite DB
    iam_data = IAMData()
    print("Data loading complete.")

    while True:
        display_menu(security_risks)
        try:
            choice = int(input("Enter your choice: "))

            if choice == 0:
                print("Exiting Risk Analyzer. Goodbye!")
                break
            elif choice == 1:
                # Display data integrity check results
                iam_data.print_check_results()
            elif 2 <= choice <= len(security_risks) + 1:
                # Get the selected query based on user's choice
                selected_query_info = security_risks[choice - 2]
                print(f"\n--- Running: {selected_query_info['name']} ---")
                print(f"Description: {selected_query_info['description']}")
                print("Executing SQL query...")

                try:
                    # Execute the SQL query using the sql method from IAMData
                    results = iam_data.sql(selected_query_info['sql'])
                    if not results.empty:
                        print("\n--- Results ---")
                        # Print the results in a nicely formatted table
                        print(results.to_string(index=False))
                    else:
                        print("No results found for this query.")
                except Exception as e:
                    print(f"An error occurred while executing the query: {e}")
            else:
                print("Invalid choice. Please enter a number from the menu.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
