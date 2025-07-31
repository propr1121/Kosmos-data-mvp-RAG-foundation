from etl.extractor import extract_project_data
from etl.transformer import transform_to_icms_format
from etl.loader import save_data
from etl.analyzer import analyze_structure

DATA_DIR = "data"
OUTPUT_TRANSFORMED = "output/transformed_data.json"
OUTPUT_ANALYSIS = "output/structure_report.json"

def main():
    print("🚀 Starting ETL process...")

    # 1. Extract
    print("\n📥 Extracting raw data...")
    raw_data = extract_project_data(DATA_DIR)

    if not raw_data:
        print("⚠️ No data found in input folder.")
        return

    # 2. Transform
    print("\n🔁 Transforming data to ICMS format...")
    transformed_data = transform_to_icms_format(raw_data)
    save_data(transformed_data, OUTPUT_TRANSFORMED)

    # 3. Analyze structure
    print("\n🔎 Analyzing structure...")
    structure_report = analyze_structure(raw_data)
    save_data(structure_report, OUTPUT_ANALYSIS)

    print(f"\n✅ ETL completed.")
    print(f"📄 Saved transformed data to {OUTPUT_TRANSFORMED}")
    print(f"📊 Saved structure analysis to {OUTPUT_ANALYSIS}")
    print("💬 You can now use the RAG-based chat interface for insights.")

if __name__ == "__main__":
    main()
