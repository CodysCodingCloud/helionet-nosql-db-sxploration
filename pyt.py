import sys
from src.Neo4jInteraction import Neo4jInteraction

neo_interface = Neo4jInteraction()


def get_disease_info(disease_id, mode):
    """Placeholder for your Neo4j/Redis logic"""
    print(f"\n[Searching for {disease_id} in {mode} mode...]")
    # Your logic here:
    # if mode == "1": data = neo.get_disease(disease_id)
    # ...
    match mode:
        case '1':
            data = neo_interface.get_disease_by_id(disease_id)
            report = (
                f"DISEASE:\t{data['name']}\n"
                f"DRUGS:\t{', '.join(data['drugs'])}\n"
                f"LOCATIONS:\t{', '.join(data['locations'])}\n"
                f"GENES:\t{', '.join(data['genes'])}"
            )
            print(f"Results:\n{report}")
        case '2':
            compound_list = neo_interface.get_disease_drug_interactions_by_id(disease_id)
            if not compound_list:
                output_text = "Ups! No compounds on sight"
            else:
                output_text = "Here is the compunds list:\nname\t\tid\n" + "\n".join([f"{item['name']}\t({item['id']})" for item in compound_list])
            print(output_text)


def main():
    while True:
        print("\n" + "="*30)
        print("Helionet Disease research")
        print("="*30)
        print("1. get disease information")
        print("2. find unexplored treatments")
        print("q. Exit")

        choice = input("\nSelect an option (1, 2, or q): ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            sys.exit()

        if choice in ['1', '2']:
            disease_id = input("Enter Disease ID: ").strip()

            if not disease_id:
                print("Error: Disease ID cannot be empty.")
                continue

            get_disease_info(disease_id, choice)
        else:
            print(f"Invalid selection '{choice}'. Please try again. ")


if __name__ == "__main__":
    main()
