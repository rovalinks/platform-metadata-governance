from registry_reader import RegistryReader
from schema_loader import SchemaLoader
from validator import RegistryValidator


def main():

    schema = SchemaLoader().load(
        "application.schema.json"
    )

    validator = RegistryValidator(schema)

    failed = False

    for filename, application in RegistryReader().load_all():

        errors = validator.validate(application)

        if errors:

            failed = True

            print(f"\n{filename}")

            for error in errors:

                print(f"  - {error.message}")

        else:

            print(f"{filename} ✓")

    if failed:

        raise SystemExit(1)

    print("\nRegistry validation successful")


if __name__ == "__main__":

    main()