from member1.pipeline import process_document

result = process_document("member1/sample.pdf")

print("\n===== MEMBER 1 PIPELINE =====")

print("\nSuccess:")
print(result["success"])

print("\n===== EXTRACTED FIELDS =====")
print(result["fields"])

print("\n===== CONSISTENCY ANALYSIS =====")
print(result["consistency"])