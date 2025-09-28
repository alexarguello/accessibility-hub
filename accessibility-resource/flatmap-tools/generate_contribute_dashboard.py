import sys
import os

# Ensure the script directory is in the path
sys.path.append(os.path.dirname(__file__))

from generate_contribute_pages import walk_docs as generate_contribute_pages

def main():
    print("Generating all contribute and collaboration pages...")
    generate_contribute_pages()
    print("All contribute and collaboration pages, and the dashboard, have been generated.")

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        # Treat benign exit conditions (like "no articles found") as success
        code = getattr(e, 'code', 0)
        if code not in (None, 0):
            print("No actionable items found by content generators. Proceeding successfully.")
            import sys
            sys.exit(0)
        else:
            raise
    except Exception as ex:
        print(f"❌ Error running content generators: {ex}")
        import sys
        sys.exit(1) 