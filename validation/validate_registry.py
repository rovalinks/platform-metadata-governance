from registry_reader import RegistryReader
from schema_loader import SchemaLoader
from validator import RegistryValidator


def main():
    schema = SchemaLoader().load("application.schema.json")
    validator = RegistryValidator(schema)
    
    # Load all applications into a dictionary for cross-file validation
    # Assuming RegistryReader().load_all() returns an iterable of (filename, application)
    applications = {filename: app for filename, app in RegistryReader().load_all()}
    
    failed = False
    project_ids = {}

    # 1. Validate Schema and GCP project_id uniqueness
    for filename, application in applications.items():
        # Schema Validation
        errors = validator.validate(application)
        
        # Cross-file Project ID Validation
        if "bindings" in application:
            for binding in application["bindings"]:

                if binding["cloud"] != "gcp":
                    continue

                project_id = binding["projectId"]
                if project_id in project_ids:
                    print(
                        f"Duplicate projectId '{project_id}' found in "
                        f"{project_ids[project_id]} and {filename}"
                    )
                    failed = True

                project_ids[project_id] = filename

        # Reporting Schema errors
        if errors:
            failed = True
            print(f"\n{filename}")
            for error in errors:
                print(f"  - {error.message}")
        elif not failed:
            print(f"{filename} ✓")

    if failed:
        raise SystemExit(1)

    print("\nRegistry validation successful")


if __name__ == "__main__":
    main()