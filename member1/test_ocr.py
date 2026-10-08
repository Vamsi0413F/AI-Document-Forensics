from extraction import extract_image_text

result = extract_image_text("test_image.png")

print("\n===== OCR TEST =====")
print("Success:", result["success"])
print("Method:", result["method"])
print("Pages:", result["page_count"])

print("\n===== OCR TEXT =====")
print(result["text"])

print("\n===== ERROR =====")
print(result["error"])