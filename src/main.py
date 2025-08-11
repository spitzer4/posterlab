from poster_generator import generate_poster
import os
from datetime import datetime

if __name__ == "__main__":
    text = input("Enter your poster text: ")

    # Timestamp for output filename
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    output_path = os.path.join("outputs", f"poster-{timestamp}.png")

    generate_poster(text, output_path)
    print(f"Poster saved to {output_path}")fun nature fair on August 12, 2025 in the park
