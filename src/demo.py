from .pipeline import extract_record


def main() -> None:
    text = "Claim number CLM-7788 from user@example.com. Patient asks for claim status. Call +91 8793147065."
    record = extract_record(text)
    print(record)


if __name__ == "__main__":
    main()
