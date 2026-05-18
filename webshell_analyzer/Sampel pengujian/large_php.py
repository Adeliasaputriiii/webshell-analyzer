import os

def generate_large_php(filename, size_mb, mode="normal"):
    """
    Generate large PHP file

    Args:
        filename (str): nama file output
        size_mb (int): ukuran dalam MB
        mode (str): "normal" atau "webshell"
    """

    target_size = size_mb * 1024 * 1024

    # Payload
    if mode == "webshell":
        payload = "eval(base64_decode('ZWNobyAnaGVsbG8nOw=='));\n"
    else:
        payload = "echo 'This is normal PHP code';\n"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("<?php\n")

            written = f.tell()

            while written < target_size:
                f.write(payload)
                written = f.tell()

                # Progress (optional)
                if written % (1 * 1024 * 1024) < len(payload):
                    print(f"[INFO] {filename}: {written / (1024*1024):.2f} MB written")

        print(f"[SUCCESS] Generated {filename} ({size_mb} MB)")

    except Exception as e:
        print(f"[ERROR] Failed to generate file: {e}")


def batch_generate():
    """
    Generate multiple test files for experiment
    """

    test_cases = [
        ("file_5mb_normal.php", 5, "normal"),
        ("file_10mb_normal.php", 10, "normal"),
        ("file_12mb_normal.php", 12, "normal"),
        ("file_15mb_normal.php", 15, "normal"),

        ("file_5mb_webshell.php", 5, "webshell"),
        ("file_10mb_webshell.php", 10, "webshell"),
        ("file_12mb_webshell.php", 12, "webshell"),
        ("file_15mb_webshell.php", 15, "webshell"),
    ]

    for filename, size, mode in test_cases:
        print(f"\n[START] Generating {filename}")
        generate_large_php(filename, size, mode)


if __name__ == "__main__":
    print("=== PHP Large File Generator ===")
    print("1. Generate single file")
    print("2. Generate batch test files")

    choice = input("Choose option (1/2): ")

    if choice == "1":
        filename = input("Enter filename (e.g. large.php): ")
        size = int(input("Enter size in MB (e.g. 12): "))
        mode = input("Mode (normal/webshell): ").strip().lower()

        generate_large_php(filename, size, mode)

    elif choice == "2":
        batch_generate()

    else:
        print("Invalid choice")